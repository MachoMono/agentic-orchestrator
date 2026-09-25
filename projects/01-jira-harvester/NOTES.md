# Notes: Project 01 Jira Harvester

## 2026-09-25
**Did:** harvested 1,012 KAFKA issues (2021Q1–2026Q3, 44/quarter, seed 42) → `data/raw/kafka_issues.jsonl`. Validation hit a spot-check failure (the search API drops milliseconds from `created`); fixed the comparison and all 7 checks pass. Built the trimmed digest `data/tickets.md` (≈199K tokens).

**State:** done.

**Re-run:**
```
python3 projects/01-jira-harvester/harvest.py      # --project SPARK etc.
python3 projects/01-jira-harvester/validate.py --target 1012
python3 projects/01-jira-harvester/make_digest.py
```

**Next step:** Project 02 (Ontology Forge), prompt 1: sample 40 tickets from `data/tickets.md` and propose `ontology/schema.md`, then stop for review.
