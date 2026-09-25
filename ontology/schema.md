# Ontology Schema v1.0 (APPROVED 2026-09-25)

**Domain:** Apache Kafka, as seen through its Jira tickets
**Derived from:** 40 tickets sampled evenly across 2021–2026 (1 per 1/40th slice of `data/tickets.md`, seed 40)
**Purpose:** a business model of the product: *what exists, what goes wrong, why it matters, who cares, and how the organization responds.*

> **Status:** reviewed and approved by the human owner. See *Decisions* at the bottom. Extraction agents must follow this file exactly.

---

## Design principles
1. **Tickets are evidence, not entities.** A ticket is a source document. Every entity and relationship must cite the ticket keys that support it.
2. **Few types, rich attributes.** For example, one `Interface` type with a `kind` attribute (api / config / metric / cli / protocol), not five separate types. That keeps extraction consistent.
3. **Controlled vocabularies for the analytic types.** `Failure Mode`, `Business Impact`, `Role` and `Process` use a fixed seed list, so we can count and compare them. New values are allowed only if flagged `proposed: true` for review.
4. **Roles, not people.** Individuals stay in the structured ticket data (assignee, commenters) for Project 7's bus-factor analysis. The ontology models *functions*.
5. **Every fact has a time.** `first_seen` / `last_seen` come from evidence ticket dates. That's what powers the time-lapse in Project 3.

---

## Entity types

| # | Type | Definition | Examples from the sample |
|---|---|---|---|
| 1 | **System** | A top-level product area. It's what a customer or team would call "a part of Kafka." | Broker (core) · Controller · Clients · Streams · Connect · MirrorMaker · Tooling · Build & CI · Documentation · Security |
| 2 | **Component** | A named module, subsystem or major class inside a System. It must be named by maintainers, not just appear once in a stack trace. | TransactionManager ([KAFKA-20237]) · LogCleaner ([KAFKA-20452]) · AlterIsrManager ([KAFKA-12345]) · MirrorSourceTask ([KAFKA-14266]) · ByteArrayConverter ([KAFKA-16844]) · KRaft / Raft ([KAFKA-14436]) · Share Consumer ([KAFKA-18969]) |
| 3 | **Interface** | A public contract that users depend on. `kind`: `api` · `config` · `metric` · `cli` · `protocol` | `log.retention.hours` config ([KAFKA-17584]) · `cordoned.log.dirs` config ([KAFKA-20901]) · `Consumer#close(CloseOptions)` api ([KAFKA-19249]) · `ActiveBrokerCount` metric ([KAFKA-12882]) · `kafka-broker-api-versions.sh` cli ([KAFKA-19663]) · DescribeLogDirs protocol ([KAFKA-13527]) |
| 4 | **Initiative** | A deliberate, named change effort: a KIP, migration or epic. It has an identifier and a lifecycle. | KIP-500 (ZooKeeper removal, [KAFKA-12345]) · KIP-848 (new consumer protocol, [KAFKA-15184]) · ZK→KRaft migration ([KAFKA-14436]) · KIP-1092 ([KAFKA-19249]) · KIP-1365 ([KAFKA-20797]) |
| 5 | **Release** | A shipped or planned version. | 3.7.0 (defective artifact) · 3.7.1 (fix) ([KAFKA-16359]) · 4.0 ([KAFKA-17215]) · 5.0.0 ([KAFKA-20001]) |
| 6 | **External Dependency** | Third-party software that Kafka relies on. | jackson-databind ([KAFKA-13805]) · ZooKeeper ([KAFKA-12892]) · RocksDB ([KAFKA-20500]) · Gradle shadow plugin ([KAFKA-16359]) · JDK |
| 7 | **Failure Mode** | *How* something goes wrong. Controlled vocabulary, see below. | Config Not Honored ([KAFKA-17584], [KAFKA-20901]) · Hang / Stuck State ([KAFKA-20237], [KAFKA-14266]) · Flaky Test ([KAFKA-12567], [KAFKA-14014]) |
| 8 | **Business Impact** | *Why it matters* to users or the organization. Controlled vocabulary, see below. | Data Durability Risk ([KAFKA-17584]) · Security & Compliance Exposure ([KAFKA-13805]) · Developer Productivity Loss ([KAFKA-12892]) |
| 9 | **Role** | A function a participant plays. Inferred from behavior, never from a person's name. Controlled vocabulary. | Committer/Reviewer ("we cannot re-publish a 3.7.0 artifact", [KAFKA-16359]) · Newcomer Contributor ("new to the Kafka project… beginner-level task", [KAFKA-19249]) · Operator/SRE ("we are monitoring records-age…", [KAFKA-14266]) |
| 10 | **Process** | A repeatable way the organization gets work done. Controlled vocabulary. | KIP Process ("needs-kip", [KAFKA-19663]) · Release & Backport ("cherry-pick to 3.7 branch", [KAFKA-17584]) · Vulnerability Response ([KAFKA-13805]) |

### Controlled vocabularies (seed lists)

**Failure Mode**
| Value | Meaning |
|---|---|
| Crash / Unhandled Exception | A process or thread dies |
| Hang / Stuck State | Stops making progress without dying |
| Data Loss / Corruption | Records lost, altered or unreadable |
| Incorrect Behavior | Runs but produces the wrong result (e.g. round-robin skips partitions, [KAFKA-13359]) |
| Config Not Honored | A setting is accepted but ignored, reset or misapplied |
| Performance Degradation | Slow, or excessive CPU/memory ([KAFKA-17444]) |
| Resource Leak | Handles, memory or files not released ([KAFKA-19466]) |
| Security Vulnerability | A CVE or access-control weakness |
| Flaky Test | A test passes or fails nondeterministically |
| Build / CI Failure | The pipeline breaks for reasons other than flaky tests |
| Packaging / Release Defect | The shipped artifact is wrong ([KAFKA-16359]) |
| Compatibility / Upgrade Break | Fails across versions or during migration ([KAFKA-14319], [KAFKA-12157]) |
| Documentation Gap | Docs wrong, missing or confusing ([KAFKA-18766], [KAFKA-18070]) |
| API Usability Gap | Awkward, inconsistent or limiting public interface ([KAFKA-17215], [KAFKA-13870]) |
| Missing Observability | Can't see or measure what's happening ([KAFKA-14740], [KAFKA-12882]) |

**Business Impact**
| Value | Meaning |
|---|---|
| Data Durability Risk | Customers could lose data |
| Availability / Outage Risk | The service or pipeline stops serving |
| Security & Compliance Exposure | Vulnerability, audit or access risk |
| Upgrade / Migration Friction | Makes adopting new versions harder or riskier |
| Operational Burden | More toil to run, monitor or troubleshoot |
| Developer Productivity Loss | Slows the people building the product (CI, flaky tests) |
| User Confusion / Adoption Barrier | Users misunderstand or struggle to adopt |
| Performance / Cost | Wastes compute, memory or money |

**Role**
End User / App Developer · Operator / SRE · Contributor · Newcomer Contributor · Committer / Reviewer · Release Manager · Security Reporter · Vendor / Integrator

**Process**
KIP (Design Proposal) Process · Release & Backport · CI / Testing · Deprecation Lifecycle · Vulnerability Response · Contributor Onboarding · Triage (duplicate / won't-fix / works-for-me) · Platform Migration

---

## Relationship types

| # | Relationship | From → To | Meaning | Example (evidence) |
|---|---|---|---|---|
| R1 | **PART_OF** | Component → System | Structural containment | TransactionManager → Clients ([KAFKA-20237]) |
| R2 | **DEPENDS_ON** | Component/System → Component/System/External Dependency | Relies on it to function | Versioned State Stores → RocksDB ([KAFKA-20500]) |
| R3 | **EXPOSES** | Component → Interface | Owns this public contract | LogManager → `cordoned.log.dirs` ([KAFKA-20901]) |
| R4 | **EXHIBITS** | Component/Interface/Release → Failure Mode | Has shown this failure | TransactionManager → Hang / Stuck State ([KAFKA-20237]) |
| R5 | **TRIGGERED_BY** | Failure Mode → Interface/Component/External Dependency | What sets the failure off | Config Not Honored → `message.max.bytes` dynamic update ([KAFKA-17584]) |
| R6 | **CAUSES** | Failure Mode → Business Impact | Why the failure matters | Config Not Honored → Data Durability Risk ([KAFKA-17584]) |
| R7 | **CHANGES** | Initiative → Component/Interface. Attribute `action`: introduces / deprecates / removes / modifies | What an initiative does to the product | KIP-1092 → `Consumer#close(Duration)` *deprecates* ([KAFKA-19249]) |
| R8 | **SUPERSEDES** | Component/Interface → Component/Interface | The new thing replaces the old | KRaft Controller → ZooKeeper-based Controller ([KAFKA-14436]) |
| R9 | **DELIVERED_IN** | Initiative/fix → Release | When it shipped | Packaging fix → 3.7.1 ([KAFKA-16359]) |
| R10 | **MITIGATED_BY** | Failure Mode → Process/Initiative/Interface | What reduces or detects the failure | Hang / Stuck State (MirrorSource) → `select-rate` metric alerting ([KAFKA-14266]) |
| R11 | **CONCERNED_WITH** | Role → Business Impact/System | What a role cares about (feeds the Project 5 personas) | Operator/SRE → Operational Burden ([KAFKA-14266]) |
| R12 | **PERFORMS** | Role → Process | Who does what | Committer/Reviewer → Release & Backport ([KAFKA-17584]) |
| R13 | **GOVERNED_BY** | Initiative/Interface change → Process | Which process controls the change | Interface change to `kafka-broker-api-versions` → KIP Process ([KAFKA-19663]) |

---

## Output format (what the extraction agents will produce)

```json
{
  "entities": [
    {"id": "component:transaction-manager", "type": "Component", "name": "TransactionManager",
     "aliases": ["TxnManager"], "attributes": {},
     "evidence": ["KAFKA-20237"], "first_seen": "2026-03-02", "last_seen": "2026-03-02"}
  ],
  "relationships": [
    {"subject": "component:transaction-manager", "predicate": "EXHIBITS",
     "object": "failure:hang-stuck-state", "attributes": {"trigger": "initial SSL handshake failure"},
     "evidence": ["KAFKA-20237"], "confidence": "high"}
  ]
}
```
- **id** = `type:kebab-case-name`, which is stable, so batches merge cleanly.
- **confidence**: `high` = stated explicitly in the ticket · `medium` = strongly implied · `low` = inferred. Low-confidence facts get extra scrutiny from the critic.

## Extraction rules
1. Don't extract **people** as entities. Record roles only.
2. Don't make each **flaky test** an entity. Record `Component --EXHIBITS--> Flaky Test` for the component under test.
3. Don't extract a component that only appears in a stack trace (those are removed from the digest anyway).
4. Initiatives use their official identifier as the canonical name (`KIP-848`), with the descriptive name as an alias.
5. If a ticket supports no relationship beyond `PART_OF`, that's fine. Don't invent impacts.

---

## How this maps to your company's Jira
The same 10 types transfer directly to a business Jira:

| Kafka | Typical company Jira |
|---|---|
| System / Component | Product line / feature area / service |
| Interface | Customer-facing API, report, setting, integration |
| Initiative (KIP) | Epic, program, change request |
| Release | Release, sprint, launch |
| External Dependency | Vendor, SaaS tool, partner system |
| Failure Mode / Business Impact | Incident type / customer, revenue or compliance impact |
| Role / Process | Department or function / SOP, approval flow |

---

## Decisions (human checkpoint, approved 2026-09-25)
1. **Types:** keep all 10 entity types.
2. **People:** roles only. No individuals in the ontology.
3. **Controlled vocabularies:** fixed seed lists for Failure Mode, Business Impact, Role and Process. New values only as `proposed: true`.
4. **Business Impact list:** approved as written.
5. **Scope:** pilot on the 40 schema-sample tickets, check quality, then run all 1,012.

[KAFKA-12345]: https://issues.apache.org/jira/browse/KAFKA-12345
[KAFKA-12157]: https://issues.apache.org/jira/browse/KAFKA-12157
[KAFKA-12567]: https://issues.apache.org/jira/browse/KAFKA-12567
[KAFKA-12882]: https://issues.apache.org/jira/browse/KAFKA-12882
[KAFKA-12892]: https://issues.apache.org/jira/browse/KAFKA-12892
[KAFKA-13359]: https://issues.apache.org/jira/browse/KAFKA-13359
[KAFKA-13527]: https://issues.apache.org/jira/browse/KAFKA-13527
[KAFKA-13805]: https://issues.apache.org/jira/browse/KAFKA-13805
[KAFKA-13870]: https://issues.apache.org/jira/browse/KAFKA-13870
[KAFKA-14014]: https://issues.apache.org/jira/browse/KAFKA-14014
[KAFKA-14266]: https://issues.apache.org/jira/browse/KAFKA-14266
[KAFKA-14319]: https://issues.apache.org/jira/browse/KAFKA-14319
[KAFKA-14436]: https://issues.apache.org/jira/browse/KAFKA-14436
[KAFKA-14740]: https://issues.apache.org/jira/browse/KAFKA-14740
[KAFKA-15184]: https://issues.apache.org/jira/browse/KAFKA-15184
[KAFKA-16359]: https://issues.apache.org/jira/browse/KAFKA-16359
[KAFKA-16844]: https://issues.apache.org/jira/browse/KAFKA-16844
[KAFKA-17215]: https://issues.apache.org/jira/browse/KAFKA-17215
[KAFKA-17444]: https://issues.apache.org/jira/browse/KAFKA-17444
[KAFKA-17584]: https://issues.apache.org/jira/browse/KAFKA-17584
[KAFKA-18070]: https://issues.apache.org/jira/browse/KAFKA-18070
[KAFKA-18766]: https://issues.apache.org/jira/browse/KAFKA-18766
[KAFKA-18969]: https://issues.apache.org/jira/browse/KAFKA-18969
[KAFKA-19249]: https://issues.apache.org/jira/browse/KAFKA-19249
[KAFKA-19466]: https://issues.apache.org/jira/browse/KAFKA-19466
[KAFKA-19663]: https://issues.apache.org/jira/browse/KAFKA-19663
[KAFKA-20001]: https://issues.apache.org/jira/browse/KAFKA-20001
[KAFKA-20237]: https://issues.apache.org/jira/browse/KAFKA-20237
[KAFKA-20452]: https://issues.apache.org/jira/browse/KAFKA-20452
[KAFKA-20500]: https://issues.apache.org/jira/browse/KAFKA-20500
[KAFKA-20797]: https://issues.apache.org/jira/browse/KAFKA-20797
[KAFKA-20901]: https://issues.apache.org/jira/browse/KAFKA-20901
