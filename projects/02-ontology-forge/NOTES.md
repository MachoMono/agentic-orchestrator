# Notes: Project 02 Ontology Forge

## 2026-09-25
**Did:**
- Schema v1.0 approved: all 10 types, roles only, controlled vocabularies, pilot first.
- Pilot (40 tickets): fixed 1 checker bug and added 2 instruction rules.
- Fan-out: 8 Sonnet agents.
- Investigated alarms: a bare-number format slip plus 2 checker bugs.
- Gap-fill agent: coverage reached 100%.
- Opus critic: 85 fixes. The human approved by category (merges/remaps) and reviewed all 23 destructive fixes. Applied with 0 failures.

**State:** done. Final: `ontology/ontology.json`, 620 entities, 1,235 relationships, 99% coverage, 0 schema problems.

**Pipeline (re-runnable):**
```
python3 projects/02-ontology-forge/forge.py split     # tickets.md -> data/batches/
python3 projects/02-ontology-forge/forge.py vocab     # -> ontology/vocab.json
# run extraction agents per ontology/EXTRACTION_PROMPT.md -> ontology/batches/*.json
python3 projects/02-ontology-forge/forge.py merge     # -> ontology.merged.json + merge_report.md
# critic agent per ontology/CRITIC_PROMPT.md -> review.md + review_fixes.json; human approves
python3 projects/02-ontology-forge/forge.py apply     # -> ontology.json
```

**Known gaps / backlog:**
- 19 lower-value critic fixes deferred (end of review.md)
- Release links are weak: add `fixVersions` to the P1 harvester and re-derive DELIVERED_IN
- `process:deprecation-lifecycle` / `platform-migration` are under-tagged; `role:vendor-integrator` is unused

**Next step:** Project 03 (Organizational Archaeology): a time-lapse knowledge graph in `docs/archaeology/` from `ontology/ontology.json` (entities carry first_seen/last_seen).
