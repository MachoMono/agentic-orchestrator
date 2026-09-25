# Merge report: `ontology.json`

- Agent output: 831 entity mentions, 1911 relationship mentions
- After merge: **680 entities**, **1339 relationships**
- Ticket coverage: **100%** of 1012 tickets cited as evidence
- Schema violations flagged: **32** (2% of relationships)
- Confidence: high 1034, medium 273, low 32

## Entities by type

| Type | Count |
|---|---|
| System | 10 |
| Component | 363 |
| Interface | 151 |
| Initiative | 84 |
| Release | 15 |
| External Dependency | 19 |
| Failure Mode | 15 |
| Business Impact | 8 |
| Role | 7 |
| Process | 8 |

## Relationships by predicate

| Predicate | Count |
|---|---|
| PART_OF | 368 |
| DEPENDS_ON | 31 |
| EXPOSES | 139 |
| EXHIBITS | 488 |
| TRIGGERED_BY | 26 |
| CAUSES | 47 |
| CHANGES | 117 |
| SUPERSEDES | 2 |
| DELIVERED_IN | 23 |
| MITIGATED_BY | 11 |
| CONCERNED_WITH | 9 |
| PERFORMS | 8 |
| GOVERNED_BY | 70 |

## Problems found

### relationship violates schema (flagged for critic) (32)

- interface:sync-topic-configs-enabled -TRIGGERED_BY-> component:mirrorsourceconnector: domain/range: Interface -TRIGGERED_BY-> Component
- component:kafkametadataquorum-cli -PART_OF-> system:tooling: dangling reference
- component:kafkametadataquorum-cli -EXHIBITS-> failure:api-usability-gap: dangling reference
- dependency:jetty-server -EXHIBITS-> failure:security-vulnerability: domain/range: External Dependency -EXHIBITS-> Failure Mode
- dependency:jose4j -EXHIBITS-> failure:security-vulnerability: domain/range: External Dependency -EXHIBITS-> Failure Mode
- dependency:scala-collection-compat -EXHIBITS-> failure:security-vulnerability: domain/range: External Dependency -EXHIBITS-> Failure Mode
- component:kafkametadataquorum-cli -EXHIBITS-> failure:flaky-test: dangling reference
- system:connect -EXPOSES-> interface:sourceconnector-alteroffsets: domain/range: System -EXPOSES-> Interface
- system:controller -EXHIBITS-> failure:missing-observability: domain/range: System -EXHIBITS-> Failure Mode
- system:clients -EXPOSES-> interface:appinfo-metrics: domain/range: System -EXPOSES-> Interface
- system:connect -EXPOSES-> interface:versioned-interface: domain/range: System -EXPOSES-> Interface
- system:mirrormaker -EXHIBITS-> failure:flaky-test: domain/range: System -EXHIBITS-> Failure Mode
- system:broker -EXPOSES-> interface:deleterecords-api: domain/range: System -EXPOSES-> Interface
- system:mirrormaker -EXHIBITS-> failure:config-not-honored: domain/range: System -EXHIBITS-> Failure Mode
- initiative:zk-to-kraft-migration -MITIGATED_BY-> process:release-backport: domain/range: Initiative -MITIGATED_BY-> Process
- system:connect -EXPOSES-> interface:connect-tasks-config-endpoint: domain/range: System -EXPOSES-> Interface
- system:streams -EXHIBITS-> failure:build-ci-failure: domain/range: System -EXHIBITS-> Failure Mode
- system:controller -EXHIBITS-> failure:incorrect-behavior: domain/range: System -EXHIBITS-> Failure Mode
- system:connect -EXPOSES-> interface:connector-plugins-endpoint: domain/range: System -EXPOSES-> Interface
- system:build-ci -EXHIBITS-> failure:performance-degradation: domain/range: System -EXHIBITS-> Failure Mode
- system:build-ci -EXHIBITS-> failure:flaky-test: domain/range: System -EXHIBITS-> Failure Mode
- system:streams -DELIVERED_IN-> release:3-6-0: domain/range: System -DELIVERED_IN-> Release
- dependency:zookeeper -EXHIBITS-> failure:security-vulnerability: domain/range: External Dependency -EXHIBITS-> Failure Mode
- system:connect -EXHIBITS-> failure:api-usability-gap: domain/range: System -EXHIBITS-> Failure Mode
- system:controller -EXHIBITS-> failure:performance-degradation: domain/range: System -EXHIBITS-> Failure Mode
- …and 7 more

