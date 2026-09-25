# Ontology review (independent critic)

> **Human decision (2026-09-25):** merges + remaps approved by category; all 23 destructive fixes reviewed individually and approved. All 85 applied via `forge.py apply`: 0 failures, 0 schema problems.

Reviewed: `ontology/ontology.json` (schema v3: 680 entities, 1,339 relationships) against `ontology/schema.md` v1.0 and the full ticket text in `data/raw/kafka_issues.jsonl`.
Fixes in machine-applicable form: `ontology/review_fixes.json` (85 fixes, F1–F85). To approve a fix, change `[ ]` to `[x]`.

## Summary

- **Fixes proposed: 85**, plus 19 lower-value items deferred to a second pass (listed at the end):
  - 31 merges (56 duplicate entities folded)
  - 31 remaps
  - 17 relationship drops
  - 5 evidence trims
  - 1 entity drop
  - 0 schema changes
- **Duplicates (Task 1):**
  - 48 duplicate clusters found: 31 proposed now, 17 deferred.
  - Components are the worst-hit type. About 1 in 6 component ids (59 of 363) is a naming variant of another or a test artifact, e.g. `logcleaner`/`log-cleaner`, `remotelogmanager`/`remote-log-manager`, or three ids for TopicBasedRemoteLogMetadataManager.
  - The KRaft controller is split across `kraft-controller`, `quorum-controller` and `raft-quorum-controller`.
  - `kip-405` and `tiered-storage` are the same initiative.
  - The releases `4.0`/`4.0.0`, `3.9`/`3.9.0`, `4.3`/`4.3.0` and `5.0`/`5.0.0` are each split in two.
- **Evidence audit (Task 2), seed `random.Random(20260925)`:**

  | Set checked | Facts | Supported | Weak | Unsupported | Supported rate |
  |---|---|---|---|---|---|
  | All `low`-confidence facts | 32 | 8 | 14 | 10 | **25%** |
  | Random sample of high/medium facts | 40 | 32 | 8 | 0 | **80%** |
  | …of which facts citing batch-06 tickets | 12 | 9 | 3 | 0 | 75% |
  | All audited facts | 72 | 40 | 22 | 10 | 56% |

  - The `low` label is doing its job: none of the high/medium sample was unsupported, but 10 of the 32 low facts were.
  - **Batch-06 evidence padding is confirmed.** In batch 06's facts with 3 or more non-PART_OF citations, 11 of 33 citations don't support the fact.
  - The worst case is `zk-to-kraft-migration -CHANGES-> kraft-controller`: 7 of its 8 tickets never touch the controller.
- **DELIVERED_IN is unreliable.** The export has no fixVersion field, so release links must come from the text. 4 of 23 DELIVERED_IN facts have no version mention at all.
- **Schema violations (Task 3):** all 32 flagged facts are resolved without a schema change: 28 remaps and 4 drops.
  - The recurring cause is agents putting a **System** where a **Component** belongs (15 EXHIBITS and 6 EXPOSES facts). Each of these maps cleanly onto an existing component.
  - External Dependency EXHIBITS facts become `security-vulnerability -TRIGGERED_BY-> <dependency>`, a pattern the ontology already uses.
  - 3 facts reference a dangling id, `component:kafkametadataquorum-cli`.
- **Sanity checks (Task 4):**
  - Every component has a PART_OF. 4 have two, and the fixes keep one each.
  - About 20 components are test classes, test files or test harnesses. They're either folded into the component under test (schema rule 2) or into `component:test-infrastructure`.
  - There are **no** `proposed: true` vocabulary values.
  - `role:vendor-integrator` is unused. `process:deprecation-lifecycle` and `process:platform-migration` have just 1 evidence ticket each, which suggests under-tagging rather than rarity.

### How to apply (order matters)
1. Apply `drop_relationship`, `remove_evidence` and `remap_relationship` first. Their ids are **pre-merge** ids.
2. Apply `drop_entity`, cascading to that entity's relationships.
3. Apply `merge` last:
   - Rewrite the merged ids to the canonical id.
   - When two facts collide, union their evidence and keep the higher confidence.
   - Add the merged names as aliases, except test-class names.
   - **Discard a merged entity's PART_OF when the canonical already has one**, so no component ends up with two Systems.
4. Remaps whose target fact already exists (noted inline) should union evidence rather than create a duplicate.

Validation: `review_fixes.json` parses. Every entity id and every relationship triple it references exists in `ontology.json`. The one exception is the dangling `component:kafkametadataquorum-cli`, which appears only as a relationship endpoint (that's the violation being fixed). No remap targets an entity that another fix merges away or drops.

## Task 1: Duplicates and synonyms

Kept separate on purpose (related but different):
- the classic consumer (`kafka-consumer`) vs the new consumer (`new-consumer`)
- `share-coordinator` (share-group state persister, KAFKA-19797) vs `share-group-coordinator` (group membership, KAFKA-19468)
- `kip-500` vs `zk-to-kraft-migration` (the migration is KIP-866-era work)
- `consumer-threading-refactor` vs `kip-848`
- `iqv2` vs `interactive-query-framework`
- `partitionassignor-interface` (the deprecated one) vs `consumer-partition-assignor`
- `socket-server` vs `network-processor`
- the `metrics*` components

Manual follow-ups that have no machine action:
- `component:consumer` carries aliases `AsyncKafkaConsumer` and `new consumer`, and most of its evidence (KAFKA-16022, KAFKA-16178) is about the new consumer. That conflates the classic and new consumers. Remove those aliases and re-home the new-consumer facts to `component:new-consumer`.
- `component:stream-thread` carries the alias `TaskManager`. Remove it.
- `initiative:kip-848` carries the alias `consumer-threading-refactor`. Remove it.

- [x] F1 MERGE component:kraft-controller ← component:quorum-controller, component:raft-quorum-controller, component:kraftclustertest (evidence: QuorumController is the KRaft controller implementation (KAFKA-12467, KAFKA-13112 vs KAFKA-13755); raft-quorum-controller is 'KRaft Quorum Controller' (KAFKA-20895); KRaftClusterTest is a flaky test whose component under test is the controller (KAFKA-15103, rule 2))
- [x] F2 MERGE component:kraft-quorum ← component:kraft (evidence: both named 'KRaft / Raft'; same Raft layer (KAFKA-12992, KAFKA-13110 vs KAFKA-14077, KAFKA-14436))
- [x] F3 MERGE component:raft-client ← component:kraftclient (evidence: KafkaRaftClient is the RaftClient implementation (KAFKA-15100 vs KAFKA-12158))
- [x] F4 MERGE component:new-consumer ← component:async-consumer, component:async-kafka-consumer (evidence: all three are AsyncKafkaConsumer (KAFKA-20332, KAFKA-21049, KAFKA-14438). The classic consumer stays separate)
- [x] F5 MERGE component:kafka-consumer ← component:kafkaconsumer (evidence: same class KafkaConsumer (KAFKA-14848, KAFKA-15180 vs KAFKA-14189))
- [x] F6 MERGE component:consumer-coordinator ← component:consumercoordinator, component:abstractcoordinator (evidence: canonical is already named 'AbstractCoordinator' with alias ConsumerCoordinator, and its evidence covers both classes (KAFKA-12639, KAFKA-15178, KAFKA-15474))
- [x] F7 MERGE component:producer ← component:kafka-producer, component:producer-client (evidence: canonical already has alias KafkaProducer; all three are the Java producer client (KAFKA-14020, KAFKA-13271, KAFKA-19250))
- [x] F8 MERGE component:mirrormaker-2 ← component:mirror-maker-2, component:mirrormaker2-worker, component:dedicated-mirror-connector (evidence: MirrorMaker2 / MM2 worker / DedicatedMirror are all MM2 (KAFKA-17220, KAFKA-17784, KAFKA-17221))
- [x] F9 MERGE component:mirror-source-connector ← component:mirrorsourceconnector (evidence: same class MirrorSourceConnector (KAFKA-14898, KAFKA-14980))
- [x] F10 MERGE component:connect-runtime ← component:connect-worker, component:exactly-once-source-integration-test (evidence: canonical alias is already 'Connect Runtime / Worker' (KAFKA-13109, KAFKA-13756); the EOS source integration test's component under test is the runtime (KAFKA-14742))
- [x] F11 MERGE component:connect-rest-api ← component:connect-rest-api-test (evidence: ConnectRestApiTest is a test of the Connect REST API (KAFKA-14193, KAFKA-14598; rule 2))
- [x] F12 MERGE component:distributed-herder ← component:distributedherder, component:distributed-herder-test (evidence: same class DistributedHerder. DistributedHerderTest is only a Mockito migration (KAFKA-13187))
- [x] F13 MERGE component:log-cleaner ← component:logcleaner, component:log-compaction-tester (evidence: same class LogCleaner; LogCompactionTester is the cleaner's test tool (KAFKA-21152))
- [x] F14 MERGE component:log-manager ← component:logmanager (evidence: same class LogManager (KAFKA-15375))
- [x] F15 MERGE component:remote-log-manager ← component:remotelogmanager (evidence: same class RemoteLogManager (alias RLM))
- [x] F16 MERGE component:remote-log-metadata-manager ← component:topic-based-rlmm, component:topicbasedremotelogmetadatamanager (evidence: all three are named TopicBasedRemoteLogMetadataManager (KAFKA-14642, KAFKA-15181))
- [x] F17 MERGE component:replica-fetcher-thread ← component:replicafetcher, component:replica-fetcher (evidence: ReplicaFetcherThread / ReplicaFetcher (KAFKA-13754, KAFKA-13803, KAFKA-15590). Note KAFKA-15181 on replicafetcher is really a TBRLMM ticket)
- [x] F18 MERGE component:kafka-streams ← component:kafka-streams-client, component:streams-smoke-test (evidence: 'KafkaStreams client' is the KafkaStreams class (KAFKA-14076); streams_smoke_test is the end-to-end test of the Streams client (KAFKA-19429))
- [x] F19 MERGE component:foreign-key-join ← component:fk-join, component:ktable-foreignkey-join (evidence: FK join = foreign-key join (KAFKA-14747, KAFKA-13268))
- [x] F20 MERGE component:config-command ← component:kafka-configs-cli, component:kafka-config-tool (evidence: both components are named kafka-configs.sh with alias ConfigCommand (KAFKA-17583, KAFKA-20111))
- [x] F21 MERGE component:metadata-quorum-command ← component:kafka-metadata-quorum-cli (evidence: kafka-metadata-quorum = MetadataQuorumCommand (KAFKA-16174, KAFKA-16521 vs KAFKA-17996))
- [x] F22 MERGE interface:consumer-close-closeoptions ← interface:consumer-close-options (evidence: identical name Consumer#close(CloseOptions) (KAFKA-19249, KAFKA-18267))
- [x] F23 MERGE interface:kafka-configs-sh ← interface:kafka-configs-cli (evidence: identical name kafka-configs.sh (KAFKA-20111))
- [x] F24 MERGE interface:streams-close-options ← interface:close-options-api (evidence: KafkaStreams.CloseOptions is the argument type of KafkaStreams#close(CloseOptions) (KAFKA-14076, KAFKA-16514))
- [x] F25 MERGE initiative:kip-405 ← initiative:tiered-storage (evidence: KIP-405 is Kafka Tiered Storage; rule 4 says use the KIP id as the canonical name (KAFKA-15290, KAFKA-15480 vs KAFKA-14642))
- [x] F26 MERGE initiative:kip-1030 ← initiative:config-defaults-4-0 (evidence: KAFKA-16368 is KIP-1030's own title ('Change constraints and default values for various configurations'))
- [x] F27 MERGE release:4-0-0 ← release:4-0 (evidence: '4.0' and '4.0.0' are the same release in the ticket text (KAFKA-17997, KAFKA-14542))
- [x] F28 MERGE release:3-9-0 ← release:3-9 (evidence: same release (KAFKA-19690 '3.9' backport, KAFKA-14077 'shipped in 3.9'))
- [x] F29 MERGE release:4-3-0 ← release:4-3 (evidence: same release (KAFKA-20106, KAFKA-20335))
- [x] F30 MERGE release:5-0-0 ← release:5-0 (evidence: same release (KAFKA-18393, KAFKA-20001))

## Task 2: Evidence audit

Scope:
- All 32 `low` facts.
- 40 others sampled with `random.Random(20260925)`: 12 drawn from the 146 non-low facts that cite a batch-06 ticket (KAFKA-17221–KAFKA-19248), then 28 from the remaining non-low facts. Two of those 28 also cite batch-06 tickets.

Every verdict was checked against the summary, description and comments in `kafka_issues.jsonl`.

The low facts that aren't fixed below are left for human judgement:
- The weak CAUSES links: facts 0 and 22 would be better as `crash→availability` and `hang→availability`, and both of those facts already exist.
- Fact 148 (KIP-966).
- The inferred Role facts.

### Low-confidence facts (all 32)
| # | Fact | Conf | Evidence | Verdict | Why |
|---|---|---|---|---|---|
| 0 | `failure:api-usability-gap -CAUSES-> impact:availability-outage-risk` | low | KAFKA-19430 | **weak** | 19430 is really a crash (Streams dies on RecordCorruptedException); "API usability gap" is a stretch |
| 22 | `failure:hang-stuck-state -CAUSES-> impact:data-durability-risk` | low | KAFKA-14359 | **weak** | 14359: the producer retries forever, which is closer to an availability risk than a durability risk |
| 36 | `failure:packaging-release-defect -CAUSES-> impact:operational-burden` | low | KAFKA-14361 | **weak** | 14361: a duplicate jar is plausible toil, but the ticket states no impact |
| 93 | `initiative:kip-500 -CHANGES-> component:metadata-module` | low | KAFKA-12348 | **unsupported** | 12348 is a one-line question about metrics; KIP-500 is not mentioned |
| 148 | `initiative:kip-966 -CHANGES-> component:replica-manager` | low | KAFKA-13872 | **weak** | 13872 comment: "will be fixed by KIP-966". ReplicaManager is not named |
| 164 | `role:contributor -CONCERNED_WITH-> system:build-ci` | low | KAFKA-13186 | **weak** | 13186 is a newcomer offer to remove commented-out code; CONCERNED_WITH build-ci is inferred |
| 169 | `role:operator-sre -CONCERNED_WITH-> impact:upgrade-migration-friction` | low | KAFKA-21142 | **weak** | 21142 is a migration crash scenario; the operator role is inferred |
| 178 | `component:kafkaapis -DELIVERED_IN-> release:3-6-0` | low | KAFKA-15593 | **unsupported** | 15593 adds 3.6.0 to compatibility tests only |
| 179 | `component:kafkaconsumer -DELIVERED_IN-> release:3-7-0` | low | KAFKA-15775 | **unsupported** | 15775 has no 3.7 mention; the subject should be the new consumer |
| 183 | `component:requestquotatest -DELIVERED_IN-> release:3-7-0` | low | KAFKA-15289 | **unsupported** | 15289 adds KRaft to a test; no release is mentioned |
| 195 | `system:streams -DELIVERED_IN-> release:3-6-0` | low | KAFKA-15594 | **unsupported** | 15594 adds 3.6.0 to upgrade tests only |
| 283 | `component:consumer -EXHIBITS-> failure:resource-leak` | low | KAFKA-16687 | **weak** | 16687 was resolved Invalid |
| 328 | `component:group-coordinator -EXHIBITS-> failure:documentation-gap` | low | KAFKA-20240 | **weak** | 20240 is a docs task (update upgrade.md), not an observed gap |
| 378 | `component:kraft-metadata-propagation -EXHIBITS-> failure:incorrect-behavior` | low | KAFKA-14313 | **supported** | 14313: produce returns NOT_LEADER right after topic creation |
| 443 | `component:mock-client -EXHIBITS-> failure:incorrect-behavior` | low | KAFKA-13000 | **supported** | 13000: MockClient diverges from NetworkClient. The fact is supported, but MockClient is test code |
| 457 | `component:partition-assignment -EXHIBITS-> failure:incorrect-behavior` | low | KAFKA-14150 | **supported** | 14150: the initial allocation is deterministic and biases leaders |
| 466 | `component:producer -EXHIBITS-> failure:incorrect-behavior` | low | KAFKA-13184 | **unsupported** | 13184 is a support request |
| 481 | `component:raft-client -EXHIBITS-> failure:api-usability-gap` | low | KAFKA-12158 | **supported** | 12158: the scheduleAppend return type is ambiguous |
| 513 | `component:requestmanagers -EXHIBITS-> failure:api-usability-gap` | low | KAFKA-15188 | **unsupported** | 15188 says RequestManager is not involved |
| 536 | `component:share-session-handler -EXHIBITS-> failure:performance-degradation` | low | KAFKA-19946 | **supported** | 19946: "does a lot of work… can be avoided" |
| 570 | `component:streams-config -EXHIBITS-> failure:compatibility-upgrade-break` | low | KAFKA-17216 | **weak** | 17216 was resolved Invalid |
| 573 | `component:streams-emit-strategy -EXHIBITS-> failure:incorrect-behavior` | low | KAFKA-19828 | **weak** | 19828: intermittent and unconfirmed user test |
| 574 | `component:streams-group-admin -EXHIBITS-> failure:missing-observability` | low | KAFKA-20695 | **weak** | 20695 has an empty description; the observability gap is only implied |
| 657 | `interface:kafka-consumer-groups-cli -EXHIBITS-> failure:incorrect-behavior` | low | KAFKA-13106 | **unsupported** | 13106 was user error on a 2.3.1 broker |
| 660 | `interface:kafka-leader-election-cli -EXHIBITS-> failure:api-usability-gap` | low | KAFKA-12885 | **supported** | 12885: add --timeout to kafka-leader-election.sh |
| 662 | `interface:kafka-share-groups-cli -EXHIBITS-> failure:api-usability-gap` | low | KAFKA-19944 | **supported** | 19944: "the output could be nicer" |
| 697 | `interface:versioned-interface -EXHIBITS-> failure:api-usability-gap` | low | KAFKA-15291 | **weak** | 15291 is an adoption task, not a usability gap |
| 901 | `initiative:zk-to-kraft-migration -GOVERNED_BY-> process:platform-migration` | low | KAFKA-20104 | **weak** | 20104 is a user inquiry; GOVERNED_BY platform-migration is plausible |
| 912 | `interface:group-instance-id -GOVERNED_BY-> process:kip-design-proposal-process` | low | KAFKA-15773 | **unsupported** | 15773 is about group.protocol validation; neither group.instance.id nor a KIP is mentioned |
| 934 | `initiative:zk-to-kraft-migration -MITIGATED_BY-> process:release-backport` | low | KAFKA-15098 | **unsupported** | 15098 has no backport and no mitigation |
| 1306 | `role:contributor -PERFORMS-> process:contributor-onboarding` | low | KAFKA-12158, KAFKA-12638 | **weak** | 12158/12638: "can I take this one up?" is ticket claiming more than onboarding |
| 1333 | `failure:security-vulnerability -TRIGGERED_BY-> component:authorizer` | low | KAFKA-17107 | **supported** | 17107: CVE-2024-27309, incorrect access control during migration |

### Random sample: batch-06 facts (12)
| # | Fact | Conf | Evidence | Verdict | Why |
|---|---|---|---|---|---|
| 796 | `component:log-manager -EXPOSES-> interface:log-message-timestamp-difference-max-ms` | medium | KAFKA-17997 | **weak** | 17997: LogManager is not named; the config belongs to LogConfig |
| 192 | `initiative:kip-937 -DELIVERED_IN-> release:4-0` | high | KAFKA-17997 | **supported** | 17997: "remove it from 4.0", resolved Fixed |
| 1185 | `component:remote-log-manager -PART_OF-> system:broker` | high | KAFKA-16105, KAFKA-17995, KAFKA-19131… | **supported** | PART_OF; all 5 tickets are about RemoteLogManager or tiered storage |
| 166 | `role:operator-sre -CONCERNED_WITH-> impact:availability-outage-risk` | medium | KAFKA-19138, KAFKA-19427, KAFKA-19586… | **supported** | all 5 tickets are outage/restart/blast-radius reports by operators |
| 983 | `component:connect-runtime -PART_OF-> system:connect` | high | KAFKA-14191, KAFKA-14645, KAFKA-18072… | **supported** | PART_OF |
| 1321 | `failure:data-loss-corruption -TRIGGERED_BY-> dependency:netty` | high | KAFKA-18072 | **supported** | 18072: data corruption caused by the netty upgrade |
| 421 | `component:metadata-quorum-command -EXHIBITS-> failure:api-usability-gap` | high | KAFKA-18775 | **supported** | 18775 lists drawbacks of the CLI design |
| 1334 | `failure:security-vulnerability -TRIGGERED_BY-> dependency:commons-validator` | high | KAFKA-17437 | **supported** | 17437: commons-validator 1.7 vulnerabilities |
| 1138 | `component:mirrormaker2-worker -PART_OF-> system:mirrormaker` | high | KAFKA-17784 | **supported** | PART_OF (the entity is a duplicate, see Task 1) |
| 893 | `initiative:metadata-quorum-command-admin-proposal -GOVERNED_BY-> process:kip-design-proposal-process` | high | KAFKA-18775 | **weak** | 18775 does not mention a KIP; GOVERNED_BY KIP is inferred at high confidence |
| 124 | `initiative:kip-848 -CHANGES-> component:new-consumer` | high | KAFKA-17439, KAFKA-17581 | **weak** | 17439/17581 fix the new consumer but never mention KIP-848 |
| 1208 | `component:share-consumer -PART_OF-> system:clients` | high | KAFKA-17989, KAFKA-17990, KAFKA-18767… | **supported** | PART_OF |

### Random sample: other facts (28)
| # | Fact | Conf | Evidence | Verdict | Why |
|---|---|---|---|---|---|
| 565 | `component:stream-thread -EXHIBITS-> failure:crash-unhandled-exception` | high | KAFKA-12462 | **supported** | 12462: IllegalStateException |
| 18 | `failure:documentation-gap -CAUSES-> impact:upgrade-migration-friction` | high | KAFKA-16848, KAFKA-17042, KAFKA-20104 | **supported** | 16848 and 17042 are migration doc errors (20104 is weak) |
| 631 | `interface:admin-api-pagination -EXHIBITS-> failure:performance-degradation` | medium | KAFKA-17041 | **weak** | 17041: existing Admin calls time out; the pagination interface is only proposed |
| 20 | `failure:flaky-test -CAUSES-> impact:developer-productivity-loss` | high | KAFKA-13421, KAFKA-13530, KAFKA-13877 | **supported** | three flaky-test tickets |
| 734 | `component:connect-runtime -EXPOSES-> interface:connector-latency-metrics` | high | KAFKA-14191 | **supported** | 14191 / KIP-864 |
| 507 | `component:replica-manager -EXHIBITS-> failure:data-loss-corruption` | medium | KAFKA-13872 | **weak** | 13872: Won't Fix; a committer calls it "expected behavior"; ReplicaManager is not named |
| 1295 | `component:worker-connector -PART_OF-> system:connect` | high | KAFKA-13878, KAFKA-14012, KAFKA-17044 | **supported** | PART_OF |
| 1260 | `component:streams-rebalance-listener -PART_OF-> system:streams` | high | KAFKA-19691 | **supported** | PART_OF |
| 478 | `component:quorum-controller -EXHIBITS-> failure:incorrect-behavior` | high | KAFKA-13112, KAFKA-13114 | **supported** | 13112: the committed offset gets out of sync |
| 974 | `component:config-manager -PART_OF-> system:broker` | high | KAFKA-19997 | **supported** | PART_OF |
| 1234 | `component:sticky-assignor -PART_OF-> system:clients` | high | KAFKA-12464, KAFKA-12637, KAFKA-16361 | **supported** | PART_OF |
| 10 | `failure:config-not-honored -CAUSES-> impact:user-confusion-adoption-barrier` | medium | KAFKA-15774 | **supported** | 15774: "silently ignored" |
| 240 | `component:api-versions-handler -EXHIBITS-> failure:incorrect-behavior` | high | KAFKA-19998 | **supported** | 19998 |
| 406 | `component:log-manager -EXHIBITS-> failure:config-not-honored` | high | KAFKA-17584 | **supported** | 17584 (schema exemplar) |
| 1065 | `component:kafka-status-backing-store -PART_OF-> system:connect` | high | KAFKA-20113 | **supported** | PART_OF |
| 545 | `component:ssl-transport-layer -EXHIBITS-> failure:config-not-honored` | high | KAFKA-13474 | **supported** | 13474: the old certificate is still used after a dynamic update |
| 1217 | `component:shared-topic-admin -PART_OF-> system:connect` | high | KAFKA-12343 | **supported** | PART_OF |
| 887 | `initiative:kip-896 -GOVERNED_BY-> process:kip-design-proposal-process` | high | KAFKA-14542, KAFKA-18269 | **supported** | 14542 comment links KIP-896 |
| 694 | `interface:streams-group-heartbeat-protocol -EXHIBITS-> failure:incorrect-behavior` | medium | KAFKA-19945 | **supported** | 19945: status is not cleared |
| 432 | `component:mirror-maker-2 -EXHIBITS-> failure:missing-observability` | high | KAFKA-17220 | **supported** | 17220: "lacks observability" |
| 496 | `component:remote-log-metadata-manager -EXHIBITS-> failure:incorrect-behavior` | medium | KAFKA-19426 | **supported** | 19426: initialization timeouts before the broker is ready |
| 497 | `component:remoteindexcache -EXHIBITS-> failure:crash-unhandled-exception` | high | KAFKA-15481 | **supported** | 15481: IOException from a race |
| 906 | `interface:consumer-protocol -GOVERNED_BY-> process:kip-design-proposal-process` | high | KAFKA-13420 | **weak** | 13420 proposes a protocol change; a KIP is implied, not stated |
| 1054 | `component:kafka-event-queue -PART_OF-> system:controller` | high | KAFKA-14601 | **supported** | PART_OF |
| 953 | `component:batch-metadata -PART_OF-> system:broker` | high | KAFKA-14602 | **supported** | PART_OF |
| 63 | `initiative:kip-1095 -CHANGES-> component:replica-placer` | high | KAFKA-20897 | **weak** | 20897: KIP-1095 modifies (not "introduces") the replica placer |
| 162 | `initiative:zk-to-kraft-migration -CHANGES-> component:zk-kraft-migration-docs` | medium | KAFKA-16848 | **weak** | 16848 is a doc bug; the initiative did not "change" the docs |
| 194 | `interface:offsetfetch-commit-v0 -DELIVERED_IN-> release:4-0-0` | medium | KAFKA-14542 | **supported** | 14542: "remove them in 4.0" |

### Batch-06 padding check
I checked every batch-06 fact with 3 or more non-PART_OF citations (7 facts, 33 citations). **11 of the 33 citations don't support the fact**; they are removed below.
- The newcomer-onboarding fact (37 citations) also leans on ticket-claiming comments ("may I take this?") from established contributors, e.g. KAFKA-17995 and KAFKA-18067. The role there is more often `contributor` than `newcomer-contributor`. That's worth a re-extraction pass, not a line-item fix.
- PART_OF facts with long evidence lists are harmless.

Unsupported facts 195 and 934 are fixed in Task 3, and fact 183 is fixed in Task 4 (F85). Every other unsupported or clearly misattributed fact is fixed here:

- [x] F31 DROP `initiative:kip-500 -CHANGES-> component:metadata-module` (KAFKA-12348 asks whether the metadata module should use Kafka metrics. No KIP-500 change is stated. Unsupported)
- [x] F32 DROP `component:kafkaapis -DELIVERED_IN-> release:3-6-0` (KAFKA-15593 only adds 3.6.0 to the compatibility tests. It is not a KafkaApis delivery. Unsupported)
- [x] F33 DROP `component:kafkaconsumer -DELIVERED_IN-> release:3-7-0` (KAFKA-15775 never mentions 3.7, the export has no fixVersion, and the ticket concerns AsyncKafkaConsumer. Unsupported)
- [x] F34 DROP `component:producer -EXHIBITS-> failure:incorrect-behavior` (KAFKA-13184 is a user support request ('receiving timeout error, please help'). No defect is identified. Unsupported)
- [x] F35 DROP `component:requestmanagers -EXHIBITS-> failure:api-usability-gap` (KAFKA-15188 says these APIs can be implemented 'without needing RequestManager updates'. Unsupported)
- [x] F36 DROP `interface:kafka-consumer-groups-cli -EXHIBITS-> failure:incorrect-behavior` (KAFKA-13106: the reporter's comment says 'version 2.3.1 does not support it', so this was user error. Unsupported)
- [x] F37 DROP `interface:group-instance-id -GOVERNED_BY-> process:kip-design-proposal-process` (KAFKA-15773 covers group.protocol/assignor validation. It mentions neither group.instance.id nor a KIP. Unsupported)
- [x] F38 DROP `component:consumer -EXHIBITS-> failure:resource-leak` (KAFKA-16687 was resolved Invalid, and the reporter traced the leak to the JMX reporter. Weak, so drop)
- [x] F39 DROP `component:streams-config -EXHIBITS-> failure:compatibility-upgrade-break` (KAFKA-17216 was resolved Invalid and never reproduced. Weak, so drop)
- [x] F40 REMAP `component:consumer -DELIVERED_IN-> release:3-7-1` → `component:kafka-clients-build -DELIVERED_IN-> release:3-7-1` (KAFKA-16359: the 3.7.1 fix was for the defective kafka-clients jar (a packaging defect), not the consumer)
- [x] F41 REMAP `component:log-manager -EXPOSES-> interface:log-message-timestamp-difference-max-ms` → `component:log-config -EXPOSES-> interface:log-message-timestamp-difference-max-ms` (KAFKA-17997: this is a log/topic config. LogManager isn't mentioned; LogConfig owns the setting)
- [x] F42 REMAP `interface:admin-api-pagination -EXHIBITS-> failure:performance-degradation` → `component:admin-client -EXHIBITS-> failure:performance-degradation` (KAFKA-17041: the existing Admin API calls time out. Pagination is the proposed remedy, not the thing that fails)
- [x] F43 REMOVE EVIDENCE KAFKA-17787, KAFKA-17788, KAFKA-17790, KAFKA-17987, KAFKA-18595, KAFKA-18599, KAFKA-18600 from `initiative:zk-to-kraft-migration -CHANGES-> component:kraft-controller` (evidence padding in batch 06. These tickets cover ConfigCommand, broker listeners, docs, ZK file cleanup, AuthorizerUtils, ApiVersionManager and NetworkClient logging. Only KAFKA-18598 (ControllerMetadataMetrics) touches the controller)
- [x] F44 REMOVE EVIDENCE KAFKA-18769 from `component:new-consumer -EXHIBITS-> failure:incorrect-behavior` (KAFKA-18769 is about share-consumer acknowledgements after a leader change, not AsyncKafkaConsumer)
- [x] F45 REMOVE EVIDENCE KAFKA-17789 from `component:stream-thread -EXHIBITS-> failure:hang-stuck-state` (KAFKA-17789 is 'State updater stuck', which belongs to component:state-updater, and was resolved Cannot Reproduce)
- [x] F46 REMOVE EVIDENCE KAFKA-18274 from `component:kraft-controller -EXHIBITS-> failure:crash-unhandled-exception` (KAFKA-18274 is a test-harness restart problem (closed socket, SharedServer metrics), not a controller crash)
- [x] F47 REMOVE EVIDENCE KAFKA-18596 from `role:committer-reviewer -PERFORMS-> process:triage` (KAFKA-18596 'Cleanup LogConfig' was resolved Fixed. There's no triage in it)

## Task 3: Schema violations (32)

No schema change is recommended. I considered two:
- "Allow System as an EXHIBITS/EXPOSES subject" (would legitimize 21 facts). Rejected, because every one of those facts names an identifiable component in its ticket. Allowing it would also invite agents to skip component resolution, which defeats the Component-level analysis.
- "Allow External Dependency as an EXHIBITS subject" (4 facts). Rejected, because `Failure Mode -TRIGGERED_BY-> External Dependency` already expresses the same fact.

One extraction-rule clarification is recommended for the next run: *DELIVERED_IN requires an explicit version statement in the ticket text, because the export has no fixVersion.*

- [x] F48 REMAP `component:kafkametadataquorum-cli -EXHIBITS-> failure:api-usability-gap` → `component:metadata-quorum-command -EXHIBITS-> failure:api-usability-gap` (dangling id. KAFKA-14982 (unreadable timestamps in kafka-metadata-quorum output) belongs to MetadataQuorumCommand; the target fact already exists, so union the evidence)
- [x] F49 REMAP `component:kafkametadataquorum-cli -EXHIBITS-> failure:flaky-test` → `component:metadata-quorum-command -EXHIBITS-> failure:flaky-test` (dangling id. KAFKA-15104 is a flaky MetadataQuorumCommandTest)
- [x] F50 DROP `component:kafkametadataquorum-cli -PART_OF-> system:tooling` (dangling id. It's redundant because metadata-quorum-command is already PART_OF Tooling)
- [x] F51 REMAP `dependency:jetty-server -EXHIBITS-> failure:security-vulnerability` → `failure:security-vulnerability -TRIGGERED_BY-> dependency:jetty-server` (KAFKA-14983 CVE-2023-26048/26049. Uses the schema's existing pattern (see `security-vulnerability -TRIGGERED_BY-> zookeeper`, KAFKA-16347))
- [x] F52 REMAP `dependency:jose4j -EXHIBITS-> failure:security-vulnerability` → `failure:security-vulnerability -TRIGGERED_BY-> dependency:jose4j` (KAFKA-14986 WS-2023-0116 against the shipped jose4j jar. The ticket is still an open question, so consider confidence low)
- [x] F53 DROP `dependency:scala-collection-compat -EXHIBITS-> failure:security-vulnerability` (KAFKA-14988 says explicitly that 'The CVE does not impact Kafka')
- [x] F54 REMAP `dependency:zookeeper -EXHIBITS-> failure:security-vulnerability` → `failure:security-vulnerability -TRIGGERED_BY-> dependency:zookeeper` (KAFKA-15596 CVE-2023-44981. The target fact already exists, so union the evidence)
- [x] F55 REMAP `initiative:tiered-storage -EXHIBITS-> failure:flaky-test` → `component:remote-log-manager -EXHIBITS-> failure:flaky-test` (KAFKA-15772 flaky TransactionsWithTieredStoreTest. Rule 2: the component under test is RemoteLogManager)
- [x] F56 REMAP `system:broker -EXHIBITS-> failure:documentation-gap` → `component:logging-subsystem -EXHIBITS-> failure:incorrect-behavior` (KAFKA-15769 'Fix wrong log with exception' (component: logging) is a wrong log statement, not a documentation gap)
- [x] F57 REMAP `system:broker -EXHIBITS-> failure:flaky-test` → `component:broker-core -EXHIBITS-> failure:flaky-test` (KAFKA-14900/14904/14984/14985/15099 are all core-module tests. The target already exists, so union the evidence)
- [x] F58 REMAP `system:build-ci -EXHIBITS-> failure:build-ci-failure` → `component:test-infrastructure -EXHIBITS-> failure:build-ci-failure` (KAFKA-14908: 'Address already in use' when an embedded cluster starts in tests)
- [x] F59 REMAP `system:build-ci -EXHIBITS-> failure:flaky-test` → `component:broker-core -EXHIBITS-> failure:flaky-test` (KAFKA-15589 flaky kafka.server.FetchRequestTest (core))
- [x] F60 REMAP `system:build-ci -EXHIBITS-> failure:performance-degradation` → `component:build-tooling -EXHIBITS-> failure:performance-degradation` (KAFKA-15476: the checkstyle cache isn't used)
- [x] F61 REMAP `system:connect -EXHIBITS-> failure:api-usability-gap` → `component:connect-transformations -EXHIBITS-> failure:api-usability-gap` (KAFKA-15597: the DropHeaders SMT has no wildcard or regex support)
- [x] F62 REMAP `system:connect -EXHIBITS-> failure:flaky-test` → `component:connect-runtime -EXHIBITS-> failure:flaky-test` (KAFKA-14901 (EOS source test). KAFKA-14905 is an MM2 ForwardingAdmin test; move it to mirrormaker-2 by hand)
- [x] F63 REMAP `system:controller -EXHIBITS-> failure:incorrect-behavior` → `component:kraft-migration-driver -EXHIBITS-> failure:incorrect-behavior` (KAFKA-15381: controller failover while in pre-migration state)
- [x] F64 REMAP `system:controller -EXHIBITS-> failure:missing-observability` → `component:kraft-controller -EXHIBITS-> failure:missing-observability` (KAFKA-15183: KIP-938 controller, loader and snapshot-emitter metrics)
- [x] F65 REMAP `system:controller -EXHIBITS-> failure:performance-degradation` → `component:controller -EXHIBITS-> failure:performance-degradation` (KAFKA-15766: request-handler thread exhaustion during a ZK-mode controller election (3.5, IBP 2.5))
- [x] F66 REMAP `system:mirrormaker -EXHIBITS-> failure:config-not-honored` → `component:mirrormaker-2 -EXHIBITS-> failure:config-not-honored` (KAFKA-15372: an MM2 rolling restart drops connector config changes)
- [x] F67 REMAP `system:mirrormaker -EXHIBITS-> failure:flaky-test` → `component:mirrormaker-2 -EXHIBITS-> failure:flaky-test` (KAFKA-15292 flaky IdentityReplicationIntegrationTest)
- [x] F68 REMAP `system:streams -EXHIBITS-> failure:build-ci-failure` → `component:streams-system-tests -EXHIBITS-> failure:build-ci-failure` (KAFKA-15378: the Streams rolling-upgrade system tests fail. The target already exists, so union the evidence)
- [x] F69 REMAP `system:streams -EXHIBITS-> failure:config-not-honored` → `component:streams-config -EXHIBITS-> failure:config-not-honored` (KAFKA-15774: default.dsl.store is silently ignored)
- [x] F70 REMAP `system:streams -EXHIBITS-> failure:flaky-test` → `component:iqv2 -EXHIBITS-> failure:flaky-test` (KAFKA-15770 ConsistencyVectorIntegrationTest (IQ position bound))
- [x] F71 REMAP `system:broker -EXPOSES-> interface:deleterecords-api` → `component:replica-manager -EXPOSES-> interface:deleterecords-api` (KAFKA-15298: DeleteRecords is served by ReplicaManager)
- [x] F72 REMAP `system:clients -EXPOSES-> interface:appinfo-metrics` → `component:kafka-metrics -EXPOSES-> interface:appinfo-metrics` (KAFKA-15186: AppInfoParser registers these metrics in the Metrics registry)
- [x] F73 REMAP `system:connect -EXPOSES-> interface:connect-tasks-config-endpoint` → `component:connect-rest-api -EXPOSES-> interface:connect-tasks-config-endpoint` (KAFKA-15377: a REST endpoint)
- [x] F74 REMAP `system:connect -EXPOSES-> interface:connector-plugins-endpoint` → `component:connect-rest-api -EXPOSES-> interface:connector-plugins-endpoint` (KAFKA-15473: a REST endpoint)
- [x] F75 REMAP `system:connect -EXPOSES-> interface:sourceconnector-alteroffsets` → `component:connect-runtime -EXPOSES-> interface:sourceconnector-alteroffsets` (KAFKA-15182: the Worker normalizes offsets before it invokes alterOffsets)
- [x] F76 REMAP `system:connect -EXPOSES-> interface:versioned-interface` → `component:connect-runtime -EXPOSES-> interface:versioned-interface` (KAFKA-15291: plugin scanning in the runtime)
- [x] F77 DROP `system:streams -DELIVERED_IN-> release:3-6-0` (KAFKA-15594 only adds 3.6.0 to the upgrade tests. Nothing was delivered)
- [x] F78 DROP `initiative:zk-to-kraft-migration -MITIGATED_BY-> process:release-backport` (KAFKA-15098 is a migration bug with authorizers. It mentions no backport and doesn't mitigate the initiative)
- [x] F79 REMAP `interface:sync-topic-configs-enabled -TRIGGERED_BY-> component:mirrorsourceconnector` → `failure:config-not-honored -TRIGGERED_BY-> interface:sync-topic-configs-enabled` (KAFKA-14898: sync.topic.configs.enabled=false is ignored. This is the R5 pattern from the schema example)

## Task 4: Sanity checks

- **No PART_OF:** none.
- **More than one PART_OF:** `alter-isr-manager`, `metadata-cache`, `streams-group-coordinator`, `memory-pool`. Fixed below.
- **Noise components:**
  - Test classes and files are folded into the component under test in Task 1: KRaftClusterTest, ExactlyOnceSourceIntegrationTest, ConnectRestApiTest, DistributedHerderTest, LogCompactionTester, streams_smoke_test, DedicatedMirrorIntegrationTest.
  - The rest are folded into `test-infrastructure` or dropped below. `docker-sanity-test` is deferred.
  - Borderline single-class components are left alone, e.g. `data-output-stream-writable`, `batch-metadata`, `controller-write-event`, `json-utils`. Maintainers do name them, but they add little at the System level.
- **`proposed: true` vocabulary values:** none. All 38 vocabulary entities are seed values. Unused: `role:vendor-integrator`.
- **Interface noise:** `interface:producer-doSend-api` (`Producer#doSend`) is a private method, not a public contract. Consider dropping it in the next pass.

- [x] F80 DROP `component:alter-isr-manager -PART_OF-> system:controller` (AlterIsrManager runs on the broker and sends AlterIsr to the controller (KAFKA-12345 'crashes on broker idle-state'). Keep Broker)
- [x] F81 DROP `component:metadata-cache -PART_OF-> system:controller` (MetadataCache is the broker's cache. KAFKA-16515 is about the ZK broker metadata cache. Keep Broker)
- [x] F82 DROP `component:streams-group-coordinator -PART_OF-> system:streams` (the streams group coordinator is broker-side (group-coordinator module, KAFKA-20696). Keep Broker)
- [x] F83 DROP `component:memory-pool -PART_OF-> system:broker` (MemoryPool lives in the clients jar (org.apache.kafka.common.memory). Judgement call: keep Clients)
- [x] F84 MERGE component:test-infrastructure ← test-harness, cluster-test-kit, broker-topic-stats-test-utils, share-consumer-test-utils, embeddedconnectcluster, mock-client, raft-simulation-tests, upgrade-test, zk-migration-integration-tests, offset-validation-test, producer-id-expiration-test (these are test harnesses, test utilities, test files or test classes, not maintainer-named product components. Their facts, such as resource leaks in test utilities (KAFKA-21048, KAFKA-14433) and flaky system tests (KAFKA-14263, KAFKA-14196), describe the test estate. Drop the old PART_OF edges to Clients, Connect and Tooling)
- [x] F85 DROP ENTITY component:requestquotatest (a test class. Both of its facts, DELIVERED_IN 3.7.0 and EXHIBITS compatibility-break from KAFKA-15289, are unsupported: the ticket only adds KRaft to a test)

## Deferred (second pass; not in review_fixes.json)
These are confident duplicates or noise of lower analytic impact, held back to keep this pass at about 80 fixes.

- D1 MERGE component:admin-client ← component:adminclient (same name 'AdminClient', same alias KafkaAdminClient (KAFKA-15373))
- D2 MERGE component:transaction-manager ← component:transactionmanager-producer ('TransactionManager (Producer)' is the same producer class (KAFKA-15767))
- D3 MERGE component:kafka-based-log ← component:kafkabasedlog (same class KafkaBasedLog)
- D4 MERGE component:unified-log ← component:unifiedlog (same class UnifiedLog)
- D5 MERGE component:task-manager ← component:taskmanager (same class TaskManager (KAFKA-14847). Also remove the 'TaskManager' alias from component:stream-thread by hand)
- D6 MERGE component:topic-command ← component:kafka-topics-cli (TopicCommand implements kafka-topics.sh (KAFKA-13718, KAFKA-14596))
- D7 MERGE component:consumer-groups-command ← component:kafka-consumer-groups-cli (ConsumerGroupCommand implements kafka-consumer-groups.sh (KAFKA-17218))
- D8 MERGE component:reassign-partitions-command ← component:reassign-partitions-tool (ReassignPartitionsCommand implements kafka-reassign-partitions.sh (KAFKA-17993))
- D9 MERGE component:kafka-storage-tool ← component:storage-tool (StorageTool = 'Storage Tool' (KAFKA-14319, KAFKA-16363))
- D10 MERGE component:kafka-features-tool ← component:features-tool (both are kafka-features.sh (KAFKA-14187, KAFKA-19941))
- D11 MERGE component:zookeeper-client ← component:broker-zookeeper-client (ZooKeeper client used by the broker (KAFKA-13270, KAFKA-16347))
- D12 MERGE component:zk-broker-registration ← component:broker-zk-registration (broker znode registration (KAFKA-12162, KAFKA-14845))
- D13 MERGE interface:kafka-features-sh ← interface:kafka-features-cli (identical name kafka-features.sh (KAFKA-19941))
- D14 MERGE interface:kafka-leader-election-sh ← interface:kafka-leader-election-cli (identical name kafka-leader-election.sh (KAFKA-12885, KAFKA-16015))
- D15 MERGE interface:kafka-reassign-partitions-sh ← interface:reassign-partitions-cli (identical name kafka-reassign-partitions.sh (KAFKA-19582))
- D16 MERGE interface:partitioner-api ← interface:partitioner (both are the producer Partitioner interface (KAFKA-14546, KAFKA-15187))
- D17 MERGE interface:list-offsets-protocol ← interface:list-offsets-request (ListOffsets RPC vs ListOffsetsRequest (KAFKA-17108, KAFKA-19267))
- D18 DROP ENTITY component:tools-string-formatting (KAFKA-20646 is a Locale.ROOT code-style sweep, not a component; it has only a PART_OF)
- D19 DROP ENTITY component:system-tests-tooling ('System Tests (--zookeeper flag)', KAFKA-12884, is a flag cleanup; it has only a PART_OF)
