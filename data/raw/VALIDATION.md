# Validation: `kafka_issues.jsonl`

Generated 2026-09-25T17:31:20 by `projects/01-jira-harvester/validate.py`

**Overall: ✅ ALL CHECKS PASS**

| Check | Result | Detail |
|---|---|---|
| Total count | ✅ PASS | 1012 issues (target ≈1012, ±5%) |
| Duplicate keys | ✅ PASS | 0 duplicates |
| Even spread across quarters | ✅ PASS | 23 quarters, 44–44 issues each |
| Required fields present | ✅ PASS | key: 0 missing, summary: 0 missing, type: 0 missing, status: 0 missing, created: 0 missing |
| Comments not truncated | ✅ PASS | 0 truncated; 2117 comments total |
| Changelog not truncated | ✅ PASS | 0 truncated; 2558 status/assignee/resolution changes kept |
| Spot-check re-fetch | ✅ PASS | KAFKA-14431: match; KAFKA-20793: match; KAFKA-13464: match |

## Issues per quarter

| Quarter | Issues |
|---|---|
| 2021Q1 | 44 |
| 2021Q2 | 44 |
| 2021Q3 | 44 |
| 2021Q4 | 44 |
| 2022Q1 | 44 |
| 2022Q2 | 44 |
| 2022Q3 | 44 |
| 2022Q4 | 44 |
| 2023Q1 | 44 |
| 2023Q2 | 44 |
| 2023Q3 | 44 |
| 2023Q4 | 44 |
| 2024Q1 | 44 |
| 2024Q2 | 44 |
| 2024Q3 | 44 |
| 2024Q4 | 44 |
| 2025Q1 | 44 |
| 2025Q2 | 44 |
| 2025Q3 | 44 |
| 2025Q4 | 44 |
| 2026Q1 | 44 |
| 2026Q2 | 44 |
| 2026Q3 | 44 |

## Optional fields: missing rate

Missing values here are normal (e.g. open tickets have no resolved date).

| Field | Missing |
|---|---|
| description | 10% |
| priority | 0% |
| assignee | 25% |
| resolved | 34% |
| resolution | 34% |
| components | 43% |
| labels | 80% |

## Issue types

| Type | Count |
|---|---|
| Bug | 414 |
| Improvement | 259 |
| Sub-task | 209 |
| Task | 52 |
| Test | 41 |
| New Feature | 28 |
| Wish | 9 |
