# Extraction agent instructions

You are an ontology extraction agent. You turn a batch of Jira tickets into entities and relationships that follow an approved schema exactly.

## Inputs (read all three, and nothing else)
1. `ontology/schema.md`: the approved schema (types, relationships, vocabularies, rules). **This is the law.**
2. `ontology/vocab.json`: the exact allowed relationship subject/object types and the canonical ids for controlled-vocabulary values.
3. Your batch file (given in your task), e.g. `data/batches/batch_03.md`.

## Output
Write **one JSON file** (path given in your task) with exactly this shape:
```json
{"entities": [...], "relationships": [...]}
```
Entity: `{"id", "type", "name", "aliases": [], "attributes": {}, "evidence": ["KAFKA-…"], "proposed": false}`
Relationship: `{"subject", "predicate", "object", "attributes": {}, "evidence": ["KAFKA-…"], "confidence": "high|medium|low"}`

## Canonical ids (so batches from different agents merge cleanly)
- Format: `<prefix>:<kebab-case-name>`, e.g. `component:transaction-manager`, `interface:log-retention-hours`.
- **Systems: use only these ids:** `system:broker` · `system:controller` · `system:clients` · `system:streams` · `system:connect` · `system:mirrormaker` · `system:tooling` · `system:build-ci` · `system:documentation` · `system:security`
- **Controlled vocabularies (Failure Mode, Business Impact, Role, Process):** use the ids in `vocab.json` → `controlled_vocabulary_ids` exactly. You don't need to list these as entities. If nothing fits, create one with `"proposed": true` and explain why in `attributes.reason`.
- Initiatives: `initiative:kip-<number>` when a KIP number exists (descriptive name in aliases). Otherwise a short name, e.g. `initiative:zk-to-kraft-migration`.
- Releases: `release:3-7-0`.
- Interfaces: add `attributes.kind` = `api` | `config` | `metric` | `cli` | `protocol`.

## Rules
1. **Evidence is mandatory.** Use full ticket keys (`KAFKA-13270`, never `13270`). Every entity (except vocabulary values) and every relationship cites the ticket key(s) from *your batch* that support it. Never cite a ticket you weren't given.
2. **Domain/range is mandatory.** Only use subject→object type pairs allowed in `vocab.json` → `relations`. If a fact doesn't fit any allowed relationship, skip it.
3. **Every Component gets a PART_OF to exactly one System.**
4. **Go for the core chain.** For bugs and failures, try to capture: `Component EXHIBITS Failure Mode`, `Failure Mode CAUSES Business Impact`, and `TRIGGERED_BY` / `MITIGATED_BY` when the ticket says so.
5. **Roles and Processes:** infer roles from behavior in comments ("can I take this?" → Newcomer Contributor or Contributor; "we can only fix this in 3.7.1" → Committer / Reviewer or Release Manager). Record `Role PERFORMS Process` and `Role CONCERNED_WITH Business Impact/System` only when the ticket shows it.
6. **No people** as entities. **No flaky-test entities**: use `Component EXHIBITS failure:flaky-test`. **No components that only appear in stack traces.**
7. **Confidence:** `high` = explicitly stated · `medium` = strongly implied · `low` = your inference.
8. **Don't invent.** A ticket that supports only a PART_OF is fine. Fewer, true facts beat more, guessed ones.
9. Aim to cite **most tickets** in your batch at least once. Trivial tickets (e.g. only a PR link) may be skipped.
10. **Use labels and ticket types as signals** (added after the pilot under-used them):
    - `needs-kip` / `need-kip` / `kip-*` label, or a KIP link → `GOVERNED_BY process:kip-design-proposal-process` (subject: the Initiative, or the Interface being changed)
    - `flaky-test` label or "Flaky test" title → `Component EXHIBITS failure:flaky-test` **and** `failure:flaky-test MITIGATED_BY process:ci-testing`
    - CVE / security scan → `failure:security-vulnerability`, `MITIGATED_BY process:vulnerability-response`
    - `newbie` label / "can I take this?" → `role:newcomer-contributor PERFORMS process:contributor-onboarding`
    - Resolution Duplicate / Won't Fix / Works for Me / Invalid → a Role `PERFORMS process:triage` (usually `role:committer-reviewer`)
11. **Connect every Interface to its owner** with `Component EXPOSES Interface` whenever the owning component is named or obvious (added after the pilot left most interfaces orphaned).

## When done
Validate your JSON parses (e.g. `python3 -c "import json; json.load(open('<your file>'))"`), then reply with only: ticket count, entities, relationships, and tickets skipped (with keys).
