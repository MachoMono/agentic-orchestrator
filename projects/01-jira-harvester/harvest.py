#!/usr/bin/env python3
"""Harvest a stratified sample of issues from a public Jira (default: Apache KAFKA).

Sampling: every calendar quarter in [start_year, end_year] gets the same number of
issues, taken as several small chunks spread across the quarter at seeded-random
offsets, so no period (or week within a quarter) dominates. Same seed -> same sample.

Output: <out>/<project>_issues.jsonl (one normalized issue per line).
Resumable: each finished quarter is checkpointed in <out>/.checkpoint/.
"""
import argparse
import datetime as dt
import json
import math
import random
import sys
import time
from pathlib import Path

import requests

BASE = "https://issues.apache.org/jira/rest/api/2"
USER_AGENT = "agentic-orchestrator-portfolio (github.com/MachoMono/agentic-orchestrator)"
FIELDS = ("summary,description,issuetype,status,priority,components,labels,"
          "assignee,reporter,created,resolutiondate,resolution,comment")
CHANGELOG_FIELDS = {"status", "assignee", "resolution"}
MIN_INTERVAL = 1.0  # seconds between requests: be polite to Apache
CHUNKS_PER_QUARTER = 4

session = requests.Session()
session.headers["User-Agent"] = USER_AGENT
_last_request = 0.0


def get(url, params=None, max_tries=6):
    """GET with rate limiting and exponential backoff on 429/5xx/network errors."""
    global _last_request
    for attempt in range(1, max_tries + 1):
        wait = MIN_INTERVAL - (time.monotonic() - _last_request)
        if wait > 0:
            time.sleep(wait)
        _last_request = time.monotonic()
        try:
            r = session.get(url, params=params, timeout=60)
        except requests.RequestException as e:
            delay = 2 ** attempt
            print(f"  ! network error ({e.__class__.__name__}), retry {attempt} in {delay}s", flush=True)
            time.sleep(delay)
            continue
        if r.status_code == 200:
            return r.json()
        if r.status_code == 429 or r.status_code >= 500:
            delay = int(r.headers.get("Retry-After", 0)) or 2 ** attempt
            print(f"  ! HTTP {r.status_code}, retry {attempt} in {delay}s", flush=True)
            time.sleep(delay)
            continue
        raise RuntimeError(f"HTTP {r.status_code} for {r.url}: {r.text[:300]}")
    raise RuntimeError(f"gave up after {max_tries} tries: {url}")


def quarters(start_year, end_year, today):
    for y in range(start_year, end_year + 1):
        for q in range(4):
            start = dt.date(y, 3 * q + 1, 1)
            end = dt.date(y + (q == 3), (3 * q + 3) % 12 + 1, 1)
            if start > today:
                return
            yield f"{y}Q{q + 1}", start, min(end, today + dt.timedelta(days=1))


def name(obj, key="name"):
    return obj.get(key) if obj else None


def normalize(issue):
    f = issue["fields"]
    comment = f.get("comment") or {}
    changelog = issue.get("changelog") or {}
    changes = [
        {"author": name(h.get("author"), "displayName"), "created": h["created"],
         "field": it["field"], "from": it.get("fromString"), "to": it.get("toString")}
        for h in changelog.get("histories", [])
        for it in h.get("items", [])
        if it.get("field") in CHANGELOG_FIELDS
    ]
    return {
        "key": issue["key"],
        "summary": f.get("summary"),
        "description": f.get("description"),
        "type": name(f.get("issuetype")),
        "status": name(f.get("status")),
        "priority": name(f.get("priority")),
        "components": [c["name"] for c in f.get("components") or []],
        "labels": f.get("labels") or [],
        "assignee": name(f.get("assignee"), "displayName"),
        "reporter": name(f.get("reporter"), "displayName"),
        "created": f.get("created"),
        "resolved": f.get("resolutiondate"),
        "resolution": name(f.get("resolution")),
        "comments": [
            {"author": name(c.get("author"), "displayName"), "created": c.get("created"), "body": c.get("body")}
            for c in comment.get("comments", [])
        ],
        "changelog": changes,
        # Completeness bookkeeping, checked by validate.py
        "_comment_total": comment.get("total", len(comment.get("comments", []))),
        "_comment_returned": len(comment.get("comments", [])),
        "_history_total": changelog.get("total", len(changelog.get("histories", []))),
        "_history_returned": len(changelog.get("histories", [])),
    }


def fetch_full_comments(key):
    """Fallback when the search response truncated an issue's comments."""
    out, start = [], 0
    while True:
        d = get(f"{BASE}/issue/{key}/comment", {"startAt": start, "maxResults": 100})
        out.extend(d["comments"])
        start += len(d["comments"])
        if start >= d["total"] or not d["comments"]:
            return out, d["total"]


def search(jql, start_at, max_results):
    return get(f"{BASE}/search", {"jql": jql, "startAt": start_at, "maxResults": max_results,
                                  "fields": FIELDS, "expand": "changelog"})


def harvest_quarter(project, label, start, end, n, rng):
    jql = (f'project = {project} AND created >= "{start}" AND created < "{end}" '
           f"ORDER BY created ASC")
    total = get(f"{BASE}/search", {"jql": jql, "maxResults": 0})["total"]
    if total <= n:
        spans = [(0, total)]
    else:
        # Split the quarter into equal segments; take one chunk at a random offset in each.
        k = CHUNKS_PER_QUARTER
        sizes = [n // k + (i < n % k) for i in range(k)]
        seg = total / k
        spans = []
        for i, size in enumerate(sizes):
            lo, hi = int(i * seg), int((i + 1) * seg) - size
            spans.append((rng.randint(lo, max(lo, hi)), size))
    issues = []
    for start_at, size in spans:
        got = 0
        while got < size:
            page = search(jql, start_at + got, size - got)
            if not page["issues"]:
                break
            issues.extend(page["issues"])
            got += len(page["issues"])
    rows = []
    for raw in issues:
        row = normalize(raw)
        if row["_comment_returned"] < row["_comment_total"]:
            full, total_c = fetch_full_comments(row["key"])
            row["comments"] = [{"author": name(c.get("author"), "displayName"), "created": c.get("created"),
                                "body": c.get("body")} for c in full]
            row["_comment_total"], row["_comment_returned"] = total_c, len(full)
        rows.append(row)
    print(f"{label}: {total:>5} issues in quarter -> sampled {len(rows)}", flush=True)
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", default="KAFKA")
    ap.add_argument("--start-year", type=int, default=2021)
    ap.add_argument("--end-year", type=int, default=dt.date.today().year)
    ap.add_argument("--target", type=int, default=1000, help="approximate total issues")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="data/raw")
    args = ap.parse_args()

    today = dt.date.today()
    qs = list(quarters(args.start_year, args.end_year, today))
    per_q = math.ceil(args.target / len(qs))
    out = Path(args.out)
    ckpt = out / ".checkpoint"
    ckpt.mkdir(parents=True, exist_ok=True)
    print(f"{args.project}: {len(qs)} quarters x {per_q} = up to {len(qs) * per_q} issues (seed {args.seed})")

    for label, start, end in qs:
        path = ckpt / f"{label}.jsonl"
        if path.exists():
            print(f"{label}: checkpoint found, skipping", flush=True)
            continue
        # Per-quarter RNG so resuming mid-run reproduces the exact same sample.
        rng = random.Random(f"{args.seed}-{args.project}-{label}")
        rows = harvest_quarter(args.project, label, start, end, per_q, rng)
        tmp = path.with_suffix(".tmp")
        tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        tmp.rename(path)

    final = out / f"{args.project.lower()}_issues.jsonl"
    with final.open("w") as fh:
        for label, _, _ in qs:
            fh.write((ckpt / f"{label}.jsonl").read_text())
    n = sum(1 for _ in final.open())
    print(f"done: {n} issues -> {final}")


if __name__ == "__main__":
    sys.exit(main())
