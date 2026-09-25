#!/usr/bin/env python3
"""Turn harvested JSONL into a compact, readable markdown digest for LLM reading.

Trimming (the token-saving step): code/log blocks and stack traces are removed,
descriptions are capped, and only the first few comments are kept, each capped.
"""
import argparse
import json
import re
from pathlib import Path

BLOCK = re.compile(r"\{(code|noformat)[^}]*\}.*?\{\1\}", re.S)
STACK = re.compile(r"^\s*(at [\w.$<>]+\(.*\)|\.\.\. \d+ more|Caused by: .*)\s*$", re.M)
SPACE = re.compile(r"\n\s*\n+")


def clean(text, limit):
    if not text:
        return ""
    text = BLOCK.sub("[code/log omitted]", text)
    text = STACK.sub("", text)
    text = SPACE.sub("\n", text).strip()
    return text if len(text) <= limit else text[:limit].rstrip() + "…"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="data/raw/kafka_issues.jsonl")
    ap.add_argument("--out", default="data/tickets.md")
    ap.add_argument("--desc-chars", type=int, default=500)
    ap.add_argument("--max-comments", type=int, default=5)
    ap.add_argument("--comment-chars", type=int, default=300)
    args = ap.parse_args()

    rows = [json.loads(line) for line in open(args.file)]
    raw_chars = sum(len(r["description"] or "") + sum(len(c["body"] or "") for c in r["comments"]) for r in rows)
    out = [f"# KAFKA ticket digest ({len(rows)} issues)", "",
           f"Trimmed for reading: descriptions ≤{args.desc_chars} chars, first {args.max_comments} comments "
           f"≤{args.comment_chars} chars each, code blocks and stack traces removed. "
           f"Full data: `{args.file}`.", ""]
    for r in sorted(rows, key=lambda r: r["created"]):
        meta = " · ".join(filter(None, [
            r["type"], r["status"] + (f" ({r['resolution']})" if r["resolution"] else ""),
            r["priority"], "components: " + ", ".join(r["components"]) if r["components"] else None,
            "labels: " + ", ".join(r["labels"]) if r["labels"] else None,
            f"created {r['created'][:10]}", f"resolved {r['resolved'][:10]}" if r["resolved"] else None]))
        out += [f"## {r['key']}: {r['summary']}", meta, ""]
        desc = clean(r["description"], args.desc_chars)
        if desc:
            out += [desc, ""]
        for c in r["comments"][:args.max_comments]:
            body = clean(c["body"], args.comment_chars).replace("\n", " ")
            if body:
                out.append(f"- **{c['author']}:** {body}")
        extra = len(r["comments"]) - args.max_comments
        if extra > 0:
            out.append(f"- _…{extra} more comments_")
        out.append("")
    text = "\n".join(out)
    Path(args.out).write_text(text)
    print(f"wrote {args.out}: {len(text):,} chars (≈{len(text)//4:,} tokens); "
          f"raw description+comment text was {raw_chars:,} chars (≈{raw_chars//4:,} tokens)")


if __name__ == "__main__":
    main()
