#!/usr/bin/env python3
"""Validate a harvested Jira JSONL file and write VALIDATION.md next to it.

Exits non-zero if any check fails, so it can gate automation later.
"""
import argparse
import collections
import datetime as dt
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import harvest  # noqa: E402

REQUIRED = ["key", "summary", "type", "status", "created"]
OPTIONAL = ["description", "priority", "assignee", "resolved", "resolution", "components", "labels"]
COMPARE = ["summary", "description", "type", "priority", "components", "labels", "created",
           "comments", "changelog"]  # status/assignee/resolved may legitimately change after harvest


def quarter_of(ts):
    d = dt.date.fromisoformat(ts[:10])
    return f"{d.year}Q{(d.month - 1) // 3 + 1}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="data/raw/kafka_issues.jsonl")
    ap.add_argument("--target", type=int, default=1000)
    ap.add_argument("--spot-checks", type=int, default=3)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()

    path = Path(args.file)
    rows = [json.loads(line) for line in path.open()]
    checks = []  # (name, passed, detail)

    # 1. Count
    n = len(rows)
    checks.append(("Total count", abs(n - args.target) <= args.target * 0.05,
                   f"{n} issues (target ≈{args.target}, ±5%)"))

    # 2. Duplicates
    dupes = [k for k, c in collections.Counter(r["key"] for r in rows).items() if c > 1]
    checks.append(("Duplicate keys", not dupes, f"{len(dupes)} duplicates" + (f": {dupes[:5]}" if dupes else "")))

    # 3. Spread across quarters
    per_q = collections.Counter(quarter_of(r["created"]) for r in rows)
    lo, hi = min(per_q.values()), max(per_q.values())
    checks.append(("Even spread across quarters", hi - lo <= 1,
                   f"{len(per_q)} quarters, {lo}–{hi} issues each"))

    # 4. Required fields
    missing = {f: sum(1 for r in rows if not r.get(f)) for f in REQUIRED}
    checks.append(("Required fields present", not any(missing.values()),
                   ", ".join(f"{f}: {m} missing" for f, m in missing.items())))

    # 5/6. Truncation
    trunc_c = [r["key"] for r in rows if r["_comment_returned"] < r["_comment_total"]]
    checks.append(("Comments not truncated", not trunc_c,
                   f"{len(trunc_c)} truncated; {sum(r['_comment_total'] for r in rows)} comments total"))
    trunc_h = [r["key"] for r in rows if r["_history_returned"] < r["_history_total"]]
    checks.append(("Changelog not truncated", not trunc_h,
                   f"{len(trunc_h)} truncated; {sum(len(r['changelog']) for r in rows)} status/assignee/resolution changes kept"))

    # 7. Spot-check: re-fetch individually and compare
    rng = random.Random(args.seed)
    sample = rng.sample(rows, args.spot_checks)
    spot_detail, spot_ok = [], True
    for r in sample:
        fresh = harvest.normalize(harvest.get(f"{harvest.BASE}/issue/{r['key']}",
                                              {"fields": harvest.FIELDS, "expand": "changelog"}))
        if fresh["_comment_returned"] < fresh["_comment_total"]:
            full, _ = harvest.fetch_full_comments(r["key"])
            fresh["comments"] = [{"author": harvest.name(c.get("author"), "displayName"),
                                  "created": c.get("created"), "body": c.get("body")} for c in full]
        # The search endpoint drops milliseconds from `created` (…18.000 vs …18.105), so compare to the second.
        fresh["created"], stored = fresh["created"][:19], dict(r, created=r["created"][:19])
        diffs = [f for f in COMPARE if fresh[f] != stored[f]]
        # New activity after harvest is fine as long as what we stored is a prefix of the fresh data.
        grew = [f for f in diffs if f in ("comments", "changelog") and fresh[f][:len(stored[f])] == stored[f]]
        bad = [f for f in diffs if f not in grew]
        spot_ok &= not bad
        spot_detail.append(f"{r['key']}: " + ("match" if not diffs else
                           f"new activity since harvest in {grew}" if not bad else f"MISMATCH in {bad}"))
    checks.append(("Spot-check re-fetch", spot_ok, "; ".join(spot_detail)))

    # Report
    all_ok = all(ok for _, ok, _ in checks)
    lines = [f"# Validation: `{path.name}`", "",
             f"Generated {dt.datetime.now().isoformat(timespec='seconds')} by `projects/01-jira-harvester/validate.py`", "",
             f"**Overall: {'✅ ALL CHECKS PASS' if all_ok else '❌ FAILURES'}**", "",
             "| Check | Result | Detail |", "|---|---|---|"]
    lines += [f"| {c} | {'✅ PASS' if ok else '❌ FAIL'} | {d} |" for c, ok, d in checks]
    lines += ["", "## Issues per quarter", "", "| Quarter | Issues |", "|---|---|"]
    lines += [f"| {q} | {per_q[q]} |" for q in sorted(per_q)]
    lines += ["", "## Optional fields: missing rate", "",
              "Missing values here are normal (e.g. open tickets have no resolved date).", "",
              "| Field | Missing |", "|---|---|"]
    lines += [f"| {f} | {sum(1 for r in rows if not r.get(f)) / n:.0%} |" for f in OPTIONAL]
    types = collections.Counter(r["type"] for r in rows)
    lines += ["", "## Issue types", "", "| Type | Count |", "|---|---|"]
    lines += [f"| {t} | {c} |" for t, c in types.most_common()]
    (path.parent / "VALIDATION.md").write_text("\n".join(lines) + "\n")

    for c, ok, d in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {c}: {d}")
    print("OVERALL:", "ALL CHECKS PASS" if all_ok else "FAILURES")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
