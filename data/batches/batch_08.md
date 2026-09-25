## KAFKA-20113: Add Configurable Retry Parameters for Status Backing Store
New Feature · Open · Major · components: connect · labels: configuration, connect, improvement, reliability · created 2026-02-02

Implement configurable retry parameters for the +KafkaStatusBackingStore+ to address the TODO comment "retry more gracefully and not forever" and provide operators with control over retry behavior during transient failures.
h3. Problem Statement
KafkaStatusBackingStore currently retries status updates indefinitely when encountering retriable exceptions. This behavior is problematic because:
 # *Infinite retry loops* can cause the worker to become unresponsive during extended Kafka broker outa…

- **Mickael Maison:** Moving to the next release as we're now in code freeze for 4.3.0.
- **Omnia Ibrahim:** Moving to 4.5 as we are now in 4.4.0 code freeze

## KAFKA-20114: Fix race between requestInFlight and backoffDeadlineMs in RPCProducerIdManager causing premature retries
Bug · Resolved (Fixed) · Minor · labels: producer, transaction · created 2026-02-02 · resolved 2026-05-09

RPCProducerIdManager uses two independent atomics, requestInFlight and backoffDeadlineMs. There is a remaining race that can cause premature retries when maybeRequestNextBlock reads an outdated backoffDeadlineMs and then a concurrent in-flight failure applies a new backoff and clears requestInFlight.
If the interleaving happens such that:
 * maybeRequestNextBlock reads backoffDeadlineMs before the failure handler updates it, and
 * the failure handler clears requestInFlight before maybeReques…

- **sanghyeok An:** {quote}Pack {{backoffDeadlineMs}} and {{requestInFlight}} into the same atomic, by creating a record class to hold them.
 {quote}
 Hi, [~squah-confluent]! 
 I'll go with that option and create a PR!
- **Sean Quah:** Thanks, looking forward to your PR!

## KAFKA-20144: Authority for LIST_CONFIG_RESOURCES should be dependent upon resource type
Improvement · Open · Major · labels: need-kip · created 2026-02-06

KIP-1142 introduced the LIST_CONFIG_RESOURCES RPC as a way of listing Kafka resources for which configuration properties can be described. It built upon KIP-1000 which was specifically concerned with client-metrics resources.
Unfortunately, this RPC requires DESCRIBE_CONFIGS permission on the cluster resource for all resource types. This has the side-effect that you need different permission to list groups (DESCRIBE on CLUSTER) than to list which groups have configs (DESCRIBE_CONFIGS on CLUSTER…

- **Chia-Ping Tsai:** [~brandboat] and I will address this
- **Aditya Kousik:** Hi, drive-by comment here. I see two duplicate KIPs. KIP-1296 is shared by https://issues.apache.org/jira/browse/KAFKA-20144 and https://issues.apache.org/jira/browse/KAFKA-20216
 Looking at confluence history, https://issues.apache.org/jira/browse/KAFKA-20216 was the first one to the finish line.
- **Kuan Po Tseng:** Thanks for the heads-up, [~adikou]. I haven’t filed the discussion thread for the KIP yet, as I’m still discussing this issue with [~chia7712]. And I’ve updated my KIP number to 1298.
- **Mickael Maison:** Moving to the next release as we're now in code freeze for 4.3.0.
- **Omnia Ibrahim:** Moving to 4.5 as we are now in 4.4.0 code freeze

## KAFKA-20145: Improve consumer HB ack on unchanged target assignment
Task · Resolved (Fixed) · Minor · components: clients, consumer · created 2026-02-06 · resolved 2026-06-04

The new consumer (async, KIP-848) sends ack back to the broker whenever it completes a reconciliation. But it also sends acks when receiving the same target assignment (to cover the case where a member may get the same assignment after being fenced)
To achieve this last bit, there is logic in the client state machine reconciliation, to ack on every reconciliation attempt, even if no change/progress. That would be ok when the reconciliation was only triggered when a HB with a new assignment was…

- **Lianet Magrans:** Hey [~nileshk03] , since you were asking, I think this is a small nice one on the consumer (good to get into the client state machine & Consumer protocol). Feel free to take it if you are interested (ping your questions/reviews when needed). Thanks!
- **Nilesh Kumar:** Thanks [~lianetm]  for pointing me at KAFKA-20145. I’m assigning the ticket to myself and will start from the {{AbstractMembershipManager}} partial-reconcile / ACK path you linked. I’ll ping you when I have something to review or if I hit questions.

## KAFKA-20146: Add CI job to detect dependency conflicts in setup.py
Improvement · Resolved (Fixed) · Minor · created 2026-02-07 · resolved 2026-02-22

from: [https://github.com/apache/kafka/pull/21415]


## KAFKA-20147: Add CI job to detect dependency conflicts in setup.py
Improvement · Resolved (Duplicate) · Minor · created 2026-02-07 · resolved 2026-02-07

from: [https://github.com/apache/kafka/pull/21415]


## KAFKA-20148: Data Loss Risk When Disabling Remote Storage Due to Race Condition
Bug · Patch Available · Major · components: core · created 2026-02-07

# Summary
  When disabling remote log storage (`remote.storage.enable=true` → `false`) with
  `remote.log.delete.on.disable=true`, there is a race condition between
  `RLMExpirationTask` and `ConfigHandler` that can lead to premature deletion of
  local log segments, resulting in **data loss**.
 # Affected Versions
  Kafka 3.0+ (all versions with tiered storage support)
  # Severity
  Critical - Data Loss
  # Root Cause Analysis
  ## Simplified Flow
  Cancel Tasks → Reset Offset → [RA…

- **Kamal Chandraprakash:** [~dyingjiecai]
 Could you add more details on the data loss that you're observing?  If you want to preserve the remote data while disabling remote storag, then use {{remote.storage.enable=true,remote.log.copy.disable=true}} setting.
- **chomingi:** Hi [~dyingjiecai] 
 I looked into this issue. Based on your logs, I think the mechanism may differ from the race condition described.
 Your logs show
  - 15:14:37.184: \{{ReplicaFetcherThread-1-1}} increments logStartOffset to 3123750 ("leader offset increment")
  - 15:16:37.068: TS disabled, follow…
- **Yunseop Eom:** PR opened: https://github.com/apache/kafka/pull/23025
 Fixed remote-log cleanup cancellation ordering so an in-flight expiration task cannot publish a stale log-start-offset update after remote storage is disabled. Cancellation now interrupts and waits for task completion before partition cleanup.…
- **Yunseop Eom:** Update on PR #23025: https://github.com/apache/kafka/pull/23025
 The PR serializes remote-log task execution with cancellation cleanup, waits for in-flight work before stopPartitions continues, and prevents stale expiration updates after cancellation.
 The regression and RemoteLogManagerTest pass, a…
- **Yunseop Eom:** PR #23025 is open and ready for maintainer review: https://github.com/apache/kafka/pull/23025

## KAFKA-20149: C4 Architecture Diagram for Apache Kafka Ecosystem
Improvement · Open · Major · created 2026-02-07

Provide C4 architecture diagram for the Entire Apache kafka ecosystem . This would bring the architecture documentation of Apache Kafka to Industry standards and also codify the software architecture of Apache Kafka and provide better Archiecture Understanding, governance and evolution.
Version-controlled, architecture-as-code diagrams to improve contributor onboarding and Entire Apache kafka ecosystem understanding.


## KAFKA-20150: Spike and explore usage of C4 diagram too like structurizr
Sub-task · Patch Available · Major · components: documentation · labels: architecture, documentation · created 2026-02-07

- **Sujay Hegde:** Pull request  - [https://github.com/apache/kafka/pull/21428.]
 Please review

## KAFKA-20151: Provide and execution Strategy for adding C4 diagram architecture
Sub-task · Open · Major · created 2026-02-07


## KAFKA-20152: Remove unused CoordinatorMetrics#registry
Improvement · Resolved (Fixed) · Trivial · created 2026-02-07 · resolved 2026-02-18

Removing the API from the interface as it is irrelevant to `ShareCoordinatorMetrics` and currently unused
[https://github.com/apache/kafka/blob/trunk/coordinator-common/src/main/java/org/apache/kafka/coordinator/common/runtime/CoordinatorMetrics.java#L58]
[code/log omitted]


## KAFKA-20153: Upgrade ducktape from 0.12 to 0.13
Improvement · Resolved (Fixed) · Minor · created 2026-02-07 · resolved 2026-02-26

from https://github.com/apache/kafka/pull/21415#discussion_r2777079381


## KAFKA-20154: Migrate Kakfa - client and non-client modules to Java 21(JDK 21)
Improvement · Open · Major · components: clients · labels: architecture · created 2026-02-08

Migrate Kakfa - client and non-client modules to Java 21(JDK 21)

- **Chia-Ping Tsai:** Java 21 is cool, but it's more of a *long-term goal* for us. :)

## KAFKA-20233: Add Broker + Controller Registrations to SamplingRequestLogFilter ADMIN_APIS
Task · Open · Major · created 2026-02-26


## KAFKA-20234: Replace System.out.println with proper logger for missing property file warning
Improvement · Open · Trivial · created 2026-02-28

Currently, when a property file is not specified, the message "Did not load any properties since the property file is not specified" is printed using           
  System.out.println. This is inconsistent with the rest of the codebase, which uses SLF4J logging.
  Replace System.out.println with log.warn to ensure consistent logging behavior and allow proper log level filtering and output control.

- **Aman Ahmad:** Hi [~high.lee] ,
 I would like to work on this if you are not working on this yourself.
 Thanks!
- **Harikrishnan:** [~high.lee] , [~aman82500] I would like to work on this if any one you are not working on this yourself. 
 Thanks!

## KAFKA-20235: Expose EffectiveMinIsr as a Partition metric
Improvement · Open · Minor · labels: need-kip · created 2026-02-28

from: [https://github.com/apache/kafka/pull/14594#discussion_r2606393474]
Since the EffectiveMinIsr calculation was updated in 3.7.0 (dynamically bouned by the actual replica count), it would be highly beneficial to expose this value as a metric. Exposing `EffectiveMinIsr` allows operators to track the exact real-time threshold protecting `acks=all` produce requests, which is crucial for troubleshooting and monitoring reassignment transition


## KAFKA-20236: Allow kafka-configs.sh to delete all dynamic configs for a group
New Feature · Open · Minor · labels: need-kip · created 2026-03-01

Currently, deleting a group does not automatically remove its associated dynamic configurations, leaving orphaned configs in the cluster. This not only consumes space, but may also cause unexpected behavior if a new group is created with the same name.

- **Jhen-Yung Hsu:** I'm working on this, thanks :)
- **David Jacot:** Hey. This was done intentionally as per KIP-848: [https://cwiki.apache.org/confluence/display/KAFKA/KIP-848%3A+The+Next+Generation+of+the+Consumer+Rebalance+Protocol#KIP848:TheNextGenerationoftheConsumerRebalanceProtocol-DynamicGroupConfiguration]
- **Chia-Ping Tsai:** [~dajac] Thanks for sharing. My intention with this proposal isn't to change that default broker behavior. Instead, I'm looking at this from an operational perspective. The goal here is simply to enhance the kafka-configs.sh CLI tool to allow users to explicitly delete these configs.
 Do you think t…
- **Andrew Schofield:** My view is that it is worth tidying up a little here.
  * I have two consumer groups with no configs defined:
 andrew@Andrews-MacBook-Pro kafka % bin/kafka-configs.sh --bootstrap-server localhost:9092 --entity-type groups --describe
 Dynamic configs for group console-consumer-43887 are:
 Dynamic con…
- **Chia-Ping Tsai:** [~schofielaj] Thanks for sharing this great example. Yes, addressing this can definitely be included in this KIP.
 The reason the group still exists in the output is that we currently don't have a removal operation in `GroupConfigManager`. We could modify the CLI tool to filter out such groups (thos…
- _…4 more comments_

## KAFKA-20237:  TransactionManager stuck in `INITIALIZING` state after initial SSL handshake failure
Bug · Open · Major · components: clients, producer  · created 2026-03-02

I encountered a scenario where the `KafkaProducer` fails to recover if the initial SSL handshake with the broker fails, even after the underlying SSL configuration is corrected.
*Steps to Reproduce:*
1. Configure a `KafkaProducer` with SSL enabled, but use an incorrect/untrusted certificate on the server side to trigger an `SSLHandshakeException`.
2. Start the Producer and attempt to send a message.
3. The Producer logs show recurring SSL handshake errors. At this point, `TransactionManager`…

- **sanghyeok An:** Transaction Coordinator likely needs further investigation, 
 but this seems primarily a Kafka Producer issue and appears to affect both TV1 and TV2.
 For example, an AuthenticationException occurs in the Producer’s sender thread before a message is sent. 
 Since the initProducerId request that was…
- **Yin Lei:** Thanks for the quick investigation! Your analysis about the initProducerId being dequeued without re-enqueuing perfectly explains the "deadlock" state I observed.
 Regarding the recovery behavior, I understand that SSL failures are typically long-lasting. However, in containerized or cloud-native en…
- **sanghyeok An:** [~finalecho] 
 Ah, sorry for the confusion.
 The comment I left was simply as a contributor: I read through the issue, analyzed it, and shared my thoughts on the pros and cons. Since I’m also just a contributor like you, it’s difficult for me to define or decide the final solution for this issue. Th…
- **Yin Lei:** Hi [~chickenchickenlove] 
 Thank you for clarifying! I really appreciate the feedback from a fellow contributor, and the links to the KIP process are very helpful.
 You've raised a crucial point regarding the Public Contract. From my perspective, the current behavior — where the Producer remains per…

## KAFKA-20238: Kafka 4.0+ monitoring documentation still includes some controller metrics only supported in ZK mode
Improvement · Patch Available · Minor · components: docs · created 2026-03-02

Kafka 4.0+ removed support for ZK mode, but the [monitoring.md documentation|https://kafka.apache.org/42/operations/monitoring/#security-considerations-for-remote-monitoring-using-jmx] for 4.0+ still includes some controller metrics that are only supported in ZK mode:
 * RequestRateAndQueueTimeMs
 * EventQueueSize
 * LeaderElectionRateAndTimeMs
 * ReplicasIneligibleToDeleteCount
 * ReplicasToDeleteCount
 * TopicsIneligibleToDeleteCount
 * TopicsToDeleteCount
These metrics should either b…

- **Karl Sorensen:** https://github.com/apache/kafka-site/pull/828

## KAFKA-20239: Document Kafka ACLs required for Connect workers
Improvement · Resolved (Fixed) · Minor · components: connect, docs, documentation · created 2026-03-02 · resolved 2026-03-04

Kafka Connect documentation does not currently specify what Kafka ACLs are required by the Connect worker itself. There is a [table in the Connect User Guide|https://kafka.apache.org/42/kafka-connect/user-guide/#acl-requirements] for enabling Exactly-Once Support that lists required permissions and the reasons they're needed (but only for the additional ACLs needed to enable EOS).
We should add a similar section for Kafka Connect in general, documenting the minimum ACLs required by the Connect…


## KAFKA-20240: Update upgrade.md to mention new batching and background thread pool configs
Sub-task · Resolved (Fixed) · Blocker · components: group-coordinator · created 2026-03-02 · resolved 2026-04-07


## KAFKA-20241: Jackson core vulnerability GHSA-72hv-8253-57qq
Bug · Resolved (Fixed) · Major · created 2026-03-02 · resolved 2026-03-04

Jackson core vulnerability [https://www.miggo.io/vulnerability-database/cve/GHSA-72hv-8253-57qq] that affects most versions of Apache Kafka, including the recently released 4.2.
I will back with PR later today

- **Aleksei Veremeev:** Failed tests:
 +Streams integration test:+ 
  # IQv2StoreIntegrationTest. initializationError
  # KafkaStreamsTelemetryIntegrationTest. "shouldPushGlobalThreadMetricsToBroker(String, String).recordingLevel=TRACE, groupProtocol=streams"
 +Tools build:+
  # JmxToolTest. initializationError
 +Core buil…
- **Mickael Maison:** Thanks for submitting this issue.
 Some of these are known to be flaky tests. I suggest you open a PR so we can run the CI and start reviewing the changes.
- **Aleksei Veremeev:** Done. [PR# 21621|https://github.com/apache/kafka/pull/21621]
- **Aleksei Veremeev:** New [PR# 21622|https://github.com/apache/kafka/pull/21622] which includes changed LICENSE-binary ([~chia7712] suggestion)
- **Aleksei Veremeev:** [PR# 21622|https://github.com/apache/kafka/pull/21622] losed as duplicate
 LICENSE-binary is added to [PR# 21621|https://github.com/apache/kafka/pull/21621]

## KAFKA-20242: Release notes links are broken in documentation
Bug · Resolved (Fixed) · Minor · components: documentation · labels: documentation, newbie, site · created 2026-03-02 · resolved 2026-03-02

Trying to find the release notes for 3.9.1, I first navigated the [release announcement page|https://kafka.apache.org/blog/2025/05/20/apache-kafka-3.9.1-release-announcement/] and followed the [release notes link|https://downloads.apache.org/kafka/3.9.1/RELEASE_NOTES.html] from there. This results in a 404 Not Found response.
I checked _some_ other versions (not all) but found no other release notes missing.

- **Karl Sorensen:** i'm happy to pick this up
- **Karl Sorensen:** PR [https://github.com/apache/kafka-site/pull/820] raised
- **Karl Sorensen:** https://github.com/apache/kafka-site/pull/820
- **ASF GitHub Bot:** mjsax merged PR #820: URL: https://github.com/apache/kafka-site/pull/820

## KAFKA-20243: TCP connection count per client.id
Improvement · Open · Minor · components: core, metrics · created 2026-03-02

The main idea is to introduce a metric that tracks TCP connection counts per ClientID. This can improve visibility into resource utilization of specific producers and consumers, per IP address is to coarse plus many clients can be on the same address in scenarios I deal with.
Add an opt-in ClientID connection count gauge to each broker's network processor.
When a TCP connection is established, it starts in an "unknown" bucket. On the first request, the broker extracts the ClientID from the req…

- **Mahesh Sambaram:** [~nebojsasimic] , can i work on this as a new comer? Can i know what should be done and get familier with code base?

## KAFKA-20326: WindowStoreMaterializerTests needs to get updated
Sub-task · Resolved (Fixed) · Blocker · components: streams · created 2026-03-17 · resolved 2026-03-20

`shouldCreateHeadersStoreWithOnWindowCloseAndCachingEnabled` is incorrect – we removed a check to make it pass for now, but need to add back the correct assertion after the root cause was fixed.
ref: [https://github.com/apache/kafka/pull/21580/changes#r2921529513]


## KAFKA-20327: Add SessionStore overrides to Abstract decorators
Sub-task · Resolved (Fixed) · Major · components: streams · created 2026-03-17 · resolved 2026-03-17

- **Bill Bejeck:** Resolved by https://github.com/apache/kafka/pull/21791

## KAFKA-20328: Audit and extend test coverage for all headers-aware APIs
Sub-task · Patch Available · Minor · components: streams · created 2026-03-17

Audit and improve unit/integration test coverage for header-aware state stores and their decorator/forwarding layers so that regressions like missing method overrides (e.g., {{{}backwardFetch(){}}}, {{{}backwardFindSessions(){}}}) are caught by tests rather than by manual testing.
h3. Goal
Define and implement stronger test coverage and test patterns around:
 * Headers-aware KV, window, and session stores.
 * Their decorator/forwarding classes (e.g., {{AbstractReadWriteDecorator}} / {{Abstra…

- **Muralidhar Basani:** There are a few missing test classes. Picking it up.
- **Muralidhar Basani:** [~alisa23] closed the previous PR and opened a new one, based on the missing overrides like backwardFetch(), and also considering the pr 21830 work (which deletes 3 classes).

## KAFKA-20329: Test `headers` dsl.store.format further
Sub-task · Resolved (Fixed) · Major · components: streams · created 2026-03-18 · resolved 2026-07-10


## KAFKA-20330: Share partition leader restart without leadership change gives wrong exception
Bug · Resolved (Fixed) · Major · created 2026-03-18 · resolved 2026-03-30

If I have a single-broker cluster and a share consumer with implicit acknowledgement, it is possible to get a share session error when records are fetched before the broker restarts but acknowledged afterwards. The handling of the exception looks good, but it's not the intended exception in this situation. The code handles leadership change correctly, but it can be confused by a leadership non-change in spite of a restart.


## KAFKA-20331: Update upgrade.md to mention new assignment offload configs
Sub-task · Resolved (Fixed) · Major · created 2026-03-18 · resolved 2026-04-07


## KAFKA-20332: Ensure app thread not collecting records for partitions being revoked
Bug · Resolved (Fixed) · Blocker · components: clients, consumer · created 2026-03-18 · resolved 2026-04-08

With the changes to not fully wait on a PollEvent on the asyncConsumer app thread (4.2), there could be a race if records are buffered for a partition and the partition gets revoked, with the app thread potentially collecting records from the buffer while the partition is being revoked (ending with records being returned to the app after commit/revocation)
This sequence: hb received revoking partitions, reconciliation identified but not triggered in background needing commit, app thread sends A…

- **Lianet Magrans:** Merged and cherry-picked to:
 4.3 - [https://github.com/apache/kafka/commit/6b05369445b00c96f854b798753e45542faceeb8]
 4.2 - [https://github.com/apache/kafka/commit/23aaf8129175bf42fceb98e80a0be565ead42f9a]
- **Lianet Magrans:** Reopened for minor gap with wakeup. Small PR in review
- **Lianet Magrans:** Second PR merged and cherry picked:
 4.3 -> [https://github.com/apache/kafka/commit/5d6248c4486f48471849caf09861b02db5009cbd] 
 4.2 -> https://github.com/apache/kafka/commit/6a50244a80de5c3042144a22e6bb65beff372a8d

## KAFKA-20333: Flaky runCloseClassicConsumerMultiConsumerSessionTimeoutTest
Test · Resolved (Fixed) · Major · components: clients, consumer · created 2026-03-18 · resolved 2026-03-30

Flaky in trunk lately.
[https://develocity.apache.org/scans/tests?search.relativeStartTime=P28D&search.rootProjectNames=kafka&search.tags=trunk&search.timeZoneId=America%2FToronto&tests.container=org.apache.kafka.clients.consumer.PlaintextConsumerPollTest&tests.sortField=FLAKY&tests.test=runCloseClassicConsumerMultiConsumerSessionTimeoutTest()%5B1%5D]
Logs show :
[2026-03-16 13:28:44,969] WARN [Consumer clientId=consumer-test-group-65, groupId=test-group] consumer poll timeout has expired. Th…


## KAFKA-20334: Consider to update KStream-KStream join to use plain-value-header-window stores
Improvement · In Progress · Major · components: streams · labels: needs-kip · created 2026-03-18

When we did KIP-1271 we decided to _not_ add a plain-value-header-window store to keep the number of stores limited, and to not end up with a zoo of too many store types.
However, while working on KIP-1285 we realized that the DSL would actually benefit from such a store. However, we compromised and use the existing value-ts-header-window store now, "wasting" 8 bytes per record on the ts field we don't need. This happens for KStream-KStream-joins.
We should consider to fix this.

- **PoAn Yang:** [~mjsax] Currently, in both [WindowSegmentWithHeaders|https://github.com/apache/kafka/blob/eb111f6695ef30889e7367bbad759f7e772d65ea/streams/src/main/java/org/apache/kafka/streams/state/internals/WindowSegmentWithHeaders.java#L39] and [RocksDBMigratingWindowStoreWithHeaders|https://github.com/apache/…
- **Matthias J. Sax:** The goal of this ticket is to change the format to `[headersSize(varint)][headersBytes][value]` – We don't need the `[timestamp(8)]` field, and it's currently wasting 8-bytes per row. – Apparently, the JavaDocs you mention describe the "intended format" instead of the currently implemented one, so i…
- **PoAn Yang:** Thanks for the clarification. I create a PR to update the JavaDocs. [https://github.com/apache/kafka/pull/21917]

## KAFKA-20335: Update docs
Sub-task · Resolved (Fixed) · Blocker · components: documentation, streams · created 2026-03-19 · resolved 2026-05-27

- **Nilesh Kumar:** I will work on this.
- **Mickael Maison:** Temporarily removed 4.3.0 as fix version to run 4.3.0-rc0
- **Mickael Maison:** Temporarily removed 4.3.0 as fix version to run 4.3.0-rc1
- **ASF GitHub Bot:** nileshkumar3 opened a new pull request, #870: URL: https://github.com/apache/kafka-site/pull/870    ## Summary
    Sync the KIP-1271 (header-aware state stores) documentation from
    apache/kafka `4.3` branch into `content/en/43/`, following the merge of
    apache/kafka#21840.
    apache/kafka#218…
- **ASF GitHub Bot:** mjsax merged PR #870: URL: https://github.com/apache/kafka-site/pull/870
- _…2 more comments_

## KAFKA-20336: Update docs
Sub-task · Resolved (Fixed) · Blocker · components: documentation, streams · labels: patch-available · created 2026-03-19 · resolved 2026-06-02

- **Shekhar Prasad Rajak:** https://github.com/apache/kafka/pull/21905
- **Mickael Maison:** Temporarily removed 4.3.0 as fix version to run 4.3.0-rc0
- **Mickael Maison:** Temporarily removed 4.3.0 as fix version to run 4.3.0-rc1

## KAFKA-20450: SafeObjectInputStream uses denylist based approach
Bug · Resolved (Fixed) · Major · created 2026-04-14 · resolved 2026-04-28

File : connect/runtime/src/main/java/org/apache/kafka/connect/util/SafeObjectInputStream.java 
The current SafeObjectInputStream uses a denylist based approach - having a fixed denylist to be validated against for deserialization. This is a bad security practise and has also been mentioned in the original PR.
We need to use allowlisting as a better security practise.


## KAFKA-20451: Move RequestChannel Responses to server module
Task · Resolved (Fixed) · Major · created 2026-04-14 · resolved 2026-07-10


## KAFKA-20452: Avoid creating unnecessary empty batches in LogCleaner below the High Watermark
Improvement · Resolved (Fixed) · Minor · created 2026-04-14 · resolved 2026-05-08

see https://github.com/apache/kafka/pull/17193#discussion_r1826381383

- **Kartikay Dubey:** Picking this up
- **Chia-Ping Tsai:** [~dubeykartikay] thanks for picking this up. However, we actually have a draft PR in progress for this issue. Would you be interested in reviewing it for us instead?
- **Kartikay Dubey:** Apologize for jumping the gun *😅 .* 
 Yes, ill be happy to review the PR : )

## KAFKA-20453: Metrics of group "kafka.network.SocketServer" should have tags unique to each SocketServer
Bug · Open · Major · components: metrics, unit tests · created 2026-04-15

kafka.network.SocketServer scala creates metrics which have no tags to distinguish them from those of another SocketServer 
e.g. for MemoryPool
{color:#871094}metricsGroup{color}.newGauge({color:#067d17}"MemoryPoolAvailable"{color}, () => {color:#871094}memoryPool{color}.availableMemory)
This is a problem found in ClusterTests - which run in a single JVM and have a singleton KafkaYammerRegistry. So there is a single gauge even though there are multiple MemoryPools.
The test created for https…

- **Edoardo Comar:** see also https://issues.apache.org/jira/browse/KAFKA-19606 and implemented PRs

## KAFKA-20454: Verify that `bin/kafka-consumer-groups.sh --reset-offsets` fails for "streams" group
Test · Open · Minor · components: streams, unit tests · created 2026-04-15

With KIP-848/1071 we now have three types of groups, "classic", "consumer", and "streams". (And with KIP-932, actually also "share" groups, but they are orthogonal to this ticket).
When users reset group offset, they can use `bin/kafka-consumer-groups.sh` tool, which always uses group-type "classic".
For a "consumer" group, this is not a problem, because mixed groups are supported.
However, for a "streams" group, mixed mode (with "classic") is not supported atm. We should add a test that veri…


## KAFKA-20455: Wait for all producers to send startup_complete before executing system test
Improvement · Patch Available · Major · components: clients, producer , system tests · created 2026-04-15

Tests that use the {{verifiable_producer}} will sporadically fail because the test initialization does not wait for all the producers to fully start up before running the test. The {{verifiable_producer}} should use a similar mechanism to the {{verifiable_consumer}} to wait for all of the producers to send the {{startup_complete}} event.

- **Lianet Magrans:** No bandwidth on our side for this at the moment, delaying to 4.5 (If anyone interested to take over please go ahead :) ), happy to help with reviews.
- **Sree Varshini S:** I would like to take this over if it's still up for grabs! I can address the comments left on the open PR, please confirm once [~lianetm]
- **Lianet Magrans:** Sure, go ahead, happy to help with reviews. Thanks!
- **Sree Varshini S:** opened a fresh PR where changes already done + addressing of comments on the previous stale PR has been done: [https://github.com/apache/kafka/pull/23236]
 cc: [~lianetm] - please review, thanks!

## KAFKA-20456: Task not found in StateUpdater throwing an exception and causing unnecessary restoration
Bug · Resolved (Fixed) · Blocker · components: streams · created 2026-04-15 · resolved 2026-04-27

2026-04-14 06:58:52.742 Caused by: java.lang.IllegalStateException: Task 1_12 was not found in the state updater. This indicates a bug. Please report at [https://issues.apache.org/jira/projects/KAFKA/issues] or to the dev-mailing list ([https://kafka.apache.org/contact]). 2026-04-14 06:58:52.742 at org.apache.kafka.streams.processor.internals.TaskManager.waitForFuture(TaskManager.java:710) ~[kafka-streams-4.3.0-SNAPSHOT.jar:?] 2026-04-14 06:58:52.742 at org.apache.kafka.streams.processor.interna…


## KAFKA-20457: Consider to exclude repartition topics from auto.offset.reset
Improvement · Open · Minor · components: streams · created 2026-04-16

In Kafka Streams, repartition topics serve a very special purpose to shuffle intermediate data, that is not fully processed yet. To avoid any data-loss, these topics are configured with infinite retention time and use explicit "delete record" requests.
However, repartition topic still apply auto.offset.reset strategy. While it is expected that auto.offset.rest would only fire a single time at startup, when the repartition topic is still empty (and thus "latest" vs "earliest" does not matter), t…

- **Daeho Kwon:** I'd like to work on this. May I pick this up?
- **Matthias J. Sax:** Sure. Just a note: we are currently overwhelmed with review request. So you need to be patient.
- **Daeho Kwon:** Hi [~mjsax] ,                                                                                                                                                                                                 
 I've been looking into this. Setting auto.offset.reset=none for repartition topics in Optimi…
- **Matthias J. Sax:** For committing offsets, we need to consider the "classic" and "streams" protocol.
 For "classic" we create repartition topics during a rebalance on the group leader clients side, so we need to add a second admin call to commit offsets – the problem is, like always, how to handle errors? We cannot ju…
- **Lucas Brutschy:** That sounds incredibly complex to me. Especially triggering this in KIP-1071 from within the broker. 
 Could we just do the same thing at startup of the streams application, for all protocols? Seems like this would also simplify the error handling, because we do it before joining the group, so we do…
- _…1 more comments_

## KAFKA-20458: AcknowledgeType.RENEW re-delivers records to application via poll() in explicit acknowledgement mode, undocumented and inconsistent with broker-side contract
Bug · Open · Major · created 2026-04-16

AcknowledgeType.RENEW is documented as a way to extend the acquisition lock on a record that is still being processed, without changing the record's state on the broker. However, the client-side implementation silently re-delivers the same records back to the application on the next poll() call. This behavior is nowhere documented, violates the explicit acknowledgement mode invariant, and diverges from the broker-side contract.
RENEW simultaneously satisfies two contradictory contracts:
Contex…

- **Andrew Schofield:** The javadoc for `KafkaShareConsumer` explains the behaviour for renew acknowledgements. It's Option B above.
- **Shekhar Prasad Rajak:** Thanks [~schofielaj] for checking, but is not if we extending the lock means we are processing the record and do not want to get the same record back ? Otherwise we will end up duplicate processing ? 
 I believe it is better to extend the lock, until consumer alive or till the next poll or till the…
- **Andrew Schofield:** The idea is that the poll following a RENEW returns the records which the consumer currently has acquired. So, the renewed ones will be returned repeatedly as long as the renewal occurs. If an application is using RENEW, it should maintain a separate map of the records it is actively processing, and…

## KAFKA-20459: JDK 25 # UnsupportedOperationException: getSubject is not supported
Bug · Resolved (Not A Problem) · Trivial · components: kraft, security · created 2026-04-16 · resolved 2026-04-17

Environment details already provided in environment section.
The same config working with kafka 3.9.1.
Using SASL_SAL protocal and SCRAM-SHA-512 mechanism.
Kafka broker/server keystore and truststore at client are validated using keytool.
*OPTION:* -Djava.security.manager=allow not accepted in our environment.
For more details, please refer the copilot link below.
Prompt [Tried this facing the same error | Try in Copilot Chat|https://m365.cloud.microsoft/chat/entity1-d870f6cd-4aa5-4d42-962…

- **Hareesh Billa:** As per JDK 25 getSubject() method will not work. 
 What is the solution to this? Why this LegacyStrategy is invoked?
 !image-2026-04-16-15-43-54-212.png!
 !image-2026-04-16-15-45-31-128.png!
- **Hareesh Billa:** Sorry for logging this issue at earliest.
 Fallback mechanism worked fine.
 Identied another issue and corrected my client config.
 Closing this issue.
 Thanks.
- **Hareesh Billa:** I could not close this. Can anyone close this.
 Thanks.

## KAFKA-20460: Potential delivery slow-down for record-limit share consumers when draining record backlog
Improvement · In Progress · Major · components: clients, core · created 2026-04-16

When draining a backlog of records using share consumers with record-limit acquisition mode for a multi-partition topic with uneven record distribution, it has been observed that sometimes there is a slow down in the consumption rate of records. This is because a share consumer consumes from one broker at a time in record-limit mode, and if one broker has records to fetch and another has no records to fetch, the share consumer waits for record arrival on the empty broker before fetching records…


## KAFKA-20496: Interactive Query isolation level configuration and framework
Sub-task · Resolved (Fixed) · Major · components: streams · created 2026-04-20 · resolved 2026-05-15

To support customizing the isolation level of Interactive Queries, we need to add a new config {{{}default.interactive.query.isolation.level{}}}, and add the {{readOnly}} method to the {{ReadOnly*Store}} interfaces.
We will also need to update the IQv2 API with the machinery to specify a custom {{IsolationLevel}} in queries, and add all the necessary wrapper implementations.

- **Nicholas Telford:** https://github.com/apache/kafka/pull/22143

## KAFKA-20497: ReadOnlyView implementations for wrapping stores
Sub-task · Resolved (Fixed) · Major · components: streams · created 2026-04-20 · resolved 2026-06-16

Each of the {{Caching*Store and}} {{Metered*Store}}  implementations need to provide a custom {{ReadOnlyView}} store implementation that implements their domain logic (caching/metering) on a read-only version of their {{wrapped()}} store (via: {{wrapped().readOnly(isolationLevel).}}
{{{}ChangeLogging*Store{}}}s can simply delegate to {{{}wrapped().readOnly(isolationLevel){}}}, because read-only stores do not log any changes.


## KAFKA-20498: RocksDBStore readOnly implementation
Sub-task · Resolved (Fixed) · Major · components: streams · created 2026-04-20 · resolved 2026-06-25

This will return a custom store implementation ({{{}RocksDBStore#ReadOnlyView{}}}), that routes its reads ({{{}get{}}}, {{{}all{}}}, {{{}range{}}}, {{{}prefixScan{}}}, etc.) through a {{DBAccessor}} determined by the {{IsolationLevel}} specified to {{{}RocksDBStore#readOnly(IsolationLevel){}}}:
 * When {{{}READ_UNCOMMITTED{}}}, uses a {{DirectDBAccessor}}
 * When {{{}READ_COMMITTED{}}}, uses a {{TransactionalDBAccessor}}


## KAFKA-20499: InMemoryStores readOnly implementations
Sub-task · Resolved (Fixed) · Major · components: streams · created 2026-04-20 · resolved 2026-06-30

Each of {{{}InMemoryKeyValueStore{}}}, {{{}InMemorySessionStore{}}}, and {{InMemoryWindowStore}} need to provide an implementation of {{readOnly}} that produces a read-only view.
Reads are either served by the {{{}TransactionBuffer{}}}, or directly by the store's committed map, dependent on the requested {{{}IsolationLevel{}}}.


## KAFKA-20500: Transactional support for VersionedStores
Sub-task · Resolved (Fixed) · Major · components: streams · created 2026-04-20 · resolved 2026-06-30

Versioned state stores also need transactionality. Under the hood, they simply use {{{}RocksDBStore{}}}, so make use of the {{{}RocksDBTransctionBuffer{}}}. However, we need to wire up the various pieces of {{{}VersionedStateStore{}}}s to make it work:
 * {{LogicalKeyValueSegment}}
 * {{VersionedBytesStore}}
 * {{VersionedKeyValueStore}}
 * {{Versioned(Metered|Caching|ChangeLogging)Stores}}


## KAFKA-20501: Integration tests for IQv1 transaction isolation
Sub-task · Resolved (Fixed) · Major · components: streams · created 2026-04-20 · resolved 2026-08-04

We need to verify that, under IQv1, writes are properly isolated from IQv1 threads when transactions are enabled and the requested isolation level is {{{}READ_COMMITTED{}}}.


## KAFKA-20502: Integration tests for IQv2 transaction isolation
Sub-task · Resolved (Fixed) · Major · components: streams · created 2026-04-20 · resolved 2026-08-11

We need to verify that uncommitted writes are correctly isolated from IQv2 queries when transactions are enabled and the {{READ_COMMITTED}} isolation level has been specified.


## KAFKA-20503: Integration tests for transaction buffering
Sub-task · Resolved (Fixed) · Major · components: streams · created 2026-04-20 · resolved 2026-08-04

We need to verify that, when transactions are enabled and {{processing.guarantee}} is EOS, records are buffered and committed to stores as expected.
We should probably make use of the existing {{EOSIntegrationTest}} for this, as it already handles verifying EOS invariants.


## KAFKA-20504: Update state wipe tests
Sub-task · Resolved (Fixed) · Major · components: streams · created 2026-04-20 · resolved 2026-08-04

Existing tests that verify correct state wipe behaviour need to be updated to only apply when transactional stores are disabled.
We should also add new tests to verify that, when transactional stores are enabled and the processing guarantee is EOS, we do _not_ wipe stores on error.


## KAFKA-20505: Deadlock in KIP-932 share path: `SharePartition.rollbackOrProcessStateUpdates` completes future inside write lock, reenters `DelayedOperation` lock held by request handler
Bug · Resolved (Fixed) · Blocker · components: core · created 2026-04-20 · resolved 2026-04-24

I had Claude dig in over night to figure out why my tests against a local 3 node cluster were hanging, after ruling out problems within my own test. The following is the full analysis it came up with:
—
The JVM's own deadlock detector (\{{kill -3}} SIGQUIT thread dump) reports a cross-thread deadlock between two locks in the share-fetch + share-acknowledge path on a single-broker KRaft 4.2.0 cluster. Once it fires, every \{{ShareFetch}} and \{{ShareAcknowledge}} against the affected broker han…


## KAFKA-20506: kafka-configs.sh can't delete the config from a offline broker when using bootstrap controller
Bug · Resolved (Fixed) · Major · created 2026-04-20 · resolved 2026-04-23

see https://github.com/apache/kafka/pull/22070#issuecomment-4282766703

- **Mickael Maison:** In the issue I reported, the config actually exists. I've dynamically set cordoned.log.dirs while the broker was online, but then I'm not able to delete or amend it using bootstrap-controller if the broker is offline. While this works if you use the Admin API directly.
- **Chia-Ping Tsai:** Sorry for the confusing phrasing. The existence of the config doesn't actually impact this.
- **Mickael Maison:** Unfortunately 4.3 still has the Scala ConfigCommand. If it's not too much work I think there would be value in having this in 4.3 for the decommissioning log dir process.
- **Chia-Ping Tsai:** {quote}
 Unfortunately 4.3 still has the Scala ConfigCommand. If it's not too much work I think there would be value in having this in 4.3 for the decommissioning log dir process.
 {quote}
 Agreed. Once the trunk PR is merged, we will file another PR specifically targeted for 4.3 to handle the diffe…

## KAFKA-20639: Move EnvelopeUtils to server module
Sub-task · Resolved (Fixed) · Minor · created 2026-05-29 · resolved 2026-06-01


## KAFKA-20640: Consumer group accepts new classic members when migration policy is disabled
Bug · Resolved (Fixed) · Major · created 2026-05-29 · resolved 2026-06-12

When group.consumer.migration.policy=disabled, a new classic-protocol member is still admitted into an existing consumer group. Because the policy permits neither an online upgrade nor an online downgrade, the group can never converge back to a single protocol — it stays permanently mixed.
This is inconsistent with the other direction. With disabled, a new consumer-protocol member joining a classic group is refused, because the upgrade it would require is turned off. A new classic member joinin…


## KAFKA-20641: ConsumerGroup should clean up the state when a static member temporarily leaves
Improvement · Open · Minor · created 2026-05-29

When a static ConsumerGroup member temporarily leaves with LEAVE_GROUP_STATIC_MEMBER_EPOCH (-2), consumerGroupStaticMemberGroupLeave clears pending revocations but leaves UNREVOKED_PARTITIONS state unchanged. ConsumerGroup should match StreamsGroup semantics by treating unrevoked partitions as revoked and transitioning the member back to STABLE.
More details are available here
https://github.com/apache/kafka/pull/22245#discussion_r3323708342


## KAFKA-20642: Support character ranges in Kafka shell globs
Improvement · In Progress · Minor · components: tools · created 2026-05-29

Kafka shell glob matching currently supports `*`, `?`, and `\{a,b}` groups in GlobComponent, but character classes/ranges are not implemented.
GlobComponent.java contains a TODO for this:
  // TODO: handle character ranges
As a result, glob patterns such as:
  topic-[0-9]
  topic-[abc]
  topic-[!abc]
are not interpreted as character classes/ranges.
Expected behavior:
  topic-[0-9] should match topic-0, topic-1, ..., topic-9
  topic-[0-9] should not match topic-a or topic-10
  topic-[a…


## KAFKA-20643: Share common implementation for downstream offset translation boundary in MirrorMaker offset syncs
Improvement · Open · Minor · components: connect, mirrormaker · created 2026-05-30

OffsetSyncWriter.PartitionState currently determines whether the translated downstream offset is too stale using:
downstreamOffset - (lastSyncDownstreamOffset + 1) >= maxOffsetLag
The +1 is required because OffsetSyncStore.translateDownstream translates consumer group offsets beyond the latest sync to at most one downstream offset past the sync.
This relationship is currently enforced only by a comment/TODO in OffsetSyncWriter. If the translation logic in OffsetSyncStore changes without a mat…


## KAFKA-20644: Connect’s RestServer assumes admin.listeners differ from listeners, silently orphaning admin resources when they match
Bug · Patch Available · Minor · components: connect · created 2026-05-30

The Kafka Connect REST server lets operators expose admin endpoints on a separate listener via admin.listeners. RestServer handles three intended cases:
 # admin.listeners unset (null) → admin resources are served on the main listeners.
 # admin.listeners set to an empty list → admin resources are disabled.
 # admin.listeners set to values distinct from listeners → admin resources are served on a separate Jetty connector.
It does not handle a fourth case: when admin.listeners overlaps listen…

- **Pavel Zeger:** I would like to create PR for it

## KAFKA-20645: Move LogLoaderTest to storage module
Sub-task · Resolved (Fixed) · Major · created 2026-05-30 · resolved 2026-06-25


## KAFKA-20646: Use Locale.ROOT in String.format() calls in tools/ and server-common/ modules
Improvement · Open · Minor · components: tools · labels: cleanup, locale, new-bie · created 2026-05-31

String.format() without a Locale parameter can produce locale-dependent output (e.g., different decimal separators for numbers, locale-specific formatting). This is inconsistent
  with the project's existing checkstyle rule that enforces Locale.ROOT for toLowerCase() and toUpperCase() calls.
  The tools/ and server-common/ modules contain ~75 occurrences of String.format( without an explicit Locale. These should be changed to String.format(Locale.ROOT, ...) for
  consistent, locale-independen…

- **Basivi Vanga:** https://github.com/apache/kafka/pull/22428

## KAFKA-20647: Add example for Queues for Kafka
Task · Open · Minor · created 2026-05-31

Queues for Kafka is now production-ready, but the examples module does not include a basic example demonstrating its usage.
Add an example to help users understand the basic usage of Queues for Kafka / share groups.

- **majialong:** Hi [~schofielaj] ,
 I noticed that the examples module does not include an example for Share Groups yet. I’d like to add a simple example to help users understand the basic usage of Queues for Kafka / Share Groups.
 Before starting the work, I’d like to check with you whether this JIRA makes sense.
- **Chia-Ping Tsai:** +1 to add samples. They can be the ground truth to AI :)
- **Federico Valeri:** +1, I also though about adding one but didn't have time so far. Feel free to ping me for review if you want a contributor opinion. Thanks.

## KAFKA-20648: Move Processor to server module
Sub-task · Open · Major · created 2026-06-01


## KAFKA-20649: KIP-1352: Ranges and Range Aggregations in the Kafka Streams DSL
New Feature · Open · Major · components: streams · labels: kip · created 2026-06-01

This ticket tracks the implementation for {*}KIP-1352: Ranges and Range Aggregations in the Kafka Streams DSL{*}.
*KIP Document:* [https://cwiki.apache.org/confluence/display/KAFKA/KIP-1352%3A+Ranges+and+Range+Aggregations+in+the+Kafka+Streams+DSL]
*Summary:* The Kafka Streams DSL currently excels at temporal grouping through fixed, sliding, and hopping windows, but lacks a native mechanism for event-centric, non-incremental aggregations (similar to SQL's {{OVER}} clause with {{{}ROWS/RANGE BE…


## KAFKA-20695: Extend "describe group" to return "task offset" metadata
Sub-task · Resolved (Fixed) · Major · components: admin, streams · created 2026-06-15 · resolved 2026-07-22


## KAFKA-20696: Periodic plugin.deleteTopology cleanup for naturally-expired streams groups
Sub-task · Resolved (Fixed) · Major · created 2026-06-15 · resolved 2026-06-24

Periodic topology description cleanup task: when a plugin is configured, the broker runs a cleanup cycle every offsets.retention.check.interval.ms to release plugin-side state for naturally-expired streams groups before the offset-expiration sweep tombstones them.
Cycle: fan out a read-only eligibility query across the broker's hosted __consumer_offsets partitions (isEmpty && allOffsetsExpired && StoredDescriptionTopologyEpoch != -1), then for each eligible group call plugin.deleteTopology and,…


## KAFKA-20697: Add cross-version system tests
Sub-task · Resolved (Fixed) · Blocker · components: streams, system tests · created 2026-06-15 · resolved 2026-09-25

With AK 4.4 release, we bump the HB request/response RPCs to `1`, and start to send certain fields if both client and server are on version 4.4+.
To ensure that nothing breaks, we need to test older clients against 4.4+ brokers, to ensure that no warmup tasks are assigned (an 4.2/4.3 client won't report lag information and should never get warmup task assigned) even if configured for the group. – We should also think about other compatibility scenarios to cover?
Similarly, we should run a 4.4+…

- **Muralidhar Basani:** Hi [~mjsax] , I'd like to pick this up if it's still open.
 I can add ducktape coverage for the mentioned 42/43/44 scenarios.
- **Matthias J. Sax:** The feature is not completed yet, so there is nothing to be tested at this point. I filed it to we don't forget about it, but it's not actionable right now.
- **Muralidhar Basani:** Is it ok if I wait for it to be picked up?
- **Omnia Ibrahim:** I'll move this to 4.5 as it past the code freeze for 4.4

## KAFKA-20698: Remove deprecated ConsumerRecords(Map) constructor
Task · Open · Blocker · components: clients, consumer · created 2026-06-16

This ticket tracks the removal of the deprecated ConsumerRecords(Map) constructor in version 5.0. See https://issues.apache.org/jira/browse/KAFKA-20660 for more info


## KAFKA-20699: TopologyTestDriver.getStateStore corrupts the task's record context
Bug · Resolved (Fixed) · Major · components: streams-test-utils · created 2026-06-16 · resolved 2026-06-25

h2. Summary
{{TopologyTestDriver.getStateStore}} mutates the task's live record context as a side effect, wiping the in-flight record's metadata.
h2. Affects
Since KAFKA-19638 ([#20403|https://github.com/apache/kafka/pull/20403]).
h2. Description
Before KAFKA-19638, the dummy record context was set once at task construction and {{getStateStore}} was read-only.
Since that change, {{getStateStore}} unconditionally calls {{setRecordContext}} with a dummy context (null topic, -1 offset/partiti…

- **Matthias J. Sax:** [~m1a2st] – why did you add 4.3.2 as fixed version? The fix was shipped with AK 4.3.1 and "fixed version" already contains this version. So adding 4.3.2 is redundant and there was not even an 4.3.2 release.
- **Ken Huang:** Apologies, that was my mistake. I'll revert the change.

## KAFKA-20700: AllowedPaths should resolve symlinks before validating paths against allowed.paths
Bug · Resolved (Fixed) · Major · created 2026-06-16 · resolved 2026-06-24

h2. Problem
`AllowedPaths.parseUntrustedPath()` validates user-supplied paths using lexical `Path.normalize()` only. It does not resolve symbolic links before checking whether a path is under a configured `allowed.paths` base directory.
As a result, if a symlink exists inside an allowed directory (e.g. `/opt/kafka/secrets/link -> /some/other/path`), validation passes because the lexical path appears under the allowed base, but `FileConfigProvider` and `DirectoryConfigProvider` later read the s…


## KAFKA-20701: KIP drafting, publication, discussion, vote 
Sub-task · Resolved (Fixed) · Major · components: streams · created 2026-06-16 · resolved 2026-06-26

- **Jess Jin:** https://cwiki.apache.org/confluence/display/KAFKA/KIP-1356%3A+Introduce+IQv2+for+headers-aware+state+stores

## KAFKA-20702: PoC PR of query type 1 (TimestampedKeyQueryWithHeaders)
Sub-task · Resolved (Fixed) · Major · components: streams · created 2026-06-16 · resolved 2026-06-25

- **Jess Jin:** https://github.com/apache/kafka/pull/22583

## KAFKA-20703: Implement query type 1 (TimestampedKeyWithHeadersQuery)
Sub-task · Resolved (Fixed) · Major · components: streams · created 2026-06-16 · resolved 2026-07-08


## KAFKA-20704: Implement query type 2 (TimestampedRangeWithHeadersQuery)
Sub-task · Resolved (Fixed) · Major · components: streams · created 2026-06-16 · resolved 2026-07-14


## KAFKA-20705: Implement query type 3 (TimestampedWindowKeyWithHeadersQuery)
Sub-task · Resolved (Fixed) · Major · components: streams · created 2026-06-16 · resolved 2026-07-16


## KAFKA-20791: Bump log4j to 2.25.5
Bug · Resolved (Fixed) · Major · created 2026-07-09 · resolved 2026-07-09

https://github.com/apache/logging-log4j2/releases#release-rel/2.25.5


## KAFKA-20792: Kafka Streams FK LeftJoin - IllegalArgumentException: Invalid partition: -1
Bug · Patch Available · Major · components: streams · created 2026-07-09

Reproduced with https://github.com/pkleindl/kafka-streams-fk-exception/
The topology has a foreign-key left join where the left-side state store has a Punctuator attached to perform regular cleanups of old records.
After the punctuator deletes a record from the log, the stream crashes with "java.lang.IllegalArgumentException: Invalid partition: -1. Partition number should always be non-negative or null."
The exception only happens if StreamsConfig.CACHE_MAX_BYTES_BUFFERING_CONFIG is not 0.
T…

- **Siddhartha Devineni:** [~pkleindl], 
 Thank you for the reproducer repo; it made this straightforward to narrow down. The punctuator plus caching combination was the key detail;
 The mechanism: StreamTask#punctuate sets a dummy ProcessorRecordContext with partition -1, the cache captures it at delete time and replays it a…

## KAFKA-20793: Mark share.version=2 stable
Sub-task · Resolved (Fixed) · Major · created 2026-07-10 · resolved 2026-07-23


## KAFKA-20794: Add documentation and tests for the RPC deprecatedVersions field
Improvement · Open · Minor · created 2026-07-10

It seems to have been introduced by https://cwiki.apache.org/confluence/x/K5sODg, but I can't find any tests or documentation for it ...


## KAFKA-20795: RequestConvertToJson#request and RequestConvertToJson#response could be implemented by generator
Improvement · Open · Minor · created 2026-07-10

These methods are currently hardcoded to convert requests/responses to JSON. This is a perfect use case for the generator module, so we should delegate the implementation to it.

- **dino2895:** {{Hi, I will take this up.}}

## KAFKA-20796: num-open-iterators metric under-counts iterators from MeteredTimestampedKeyValueStore
Bug · Open · Major · components: streams · created 2026-07-10

MeteredTimestampedKeyValueStoreIterator(streams/src/main/java/org/apache/kafka/streams/state/internals/MeteredTimestampedKeyValueStore.java:301) registers itself in {{openIterators}} but never calls {{{}numOpenIterators.increment () / decrement(){}}}.
As a result, iterators opened against a plain (non-headers) timestamped key-value store are invisible to the '{{{}num-open-iterators{}}}' metric while still visible to '{{{}oldest-iterator-open-since-ms{}}}' - the two gauges disagree about how man…


## KAFKA-20797: KIP-1365: Transform Observability and Skipped Record Handling for Kafka Connect
Improvement · Open · Major · components: connect, kip · created 2026-07-11

Kafka Connect's Single Message Transform (SMT) framework allows users to build chains of transformations that process records between the connector and Kafka. Transforms can modify records, route them to different topics, or *drop them entirely* by returning {{null}} (a filter operation). When combined with the error tolerance framework ({{{}errors.tolerance=all{}}}), records can also be diverted to a Dead Letter Queue (DLQ) before reaching the connector.
Today, the transform layer has two sign…


## KAFKA-20798: Add readOnly(IsolationLevel) to TimestampedWindowStoreWithHeaders and SessionStoreWithHeaders
Bug · Resolved (Fixed) · Major · components: streams · created 2026-07-12 · resolved 2026-07-14

Similar to KAFKA-20497, MeteredTimestampedWindowStoreWithHeaders and MeteredSessionStoreWithHeaders never override readOnly(IsolationLevel). KAFKA-20497 added this override to `MeteredKeyValueStore`, `MeteredWindowStore`, and `MeteredSessionStore` (PRs [#22316|https://github.com/apache/kafka/pull/22316]/[#22318|https://github.com/apache/kafka/pull/22318]/[#22317|https://github.com/apache/kafka/pull/22317]), but never extended it to their WithHeaders subclasses, which were added separately.
Sinc…


## KAFKA-20799: Introduce new error for consumer/share group name collision
Improvement · Open · Major · created 2026-07-13

When shared group and classic consumer group has name collision, the error is not clear to users.
Scenarios:
*1. Existing classic consumer group: "test_group"*
1.1. When creating a new shared group named "test_group", the clients will get this exception:
[code/log omitted]
1.2. When altering the offset for a classic consumer group named "test_group", the clients will get this exception:
[code/log omitted]
*2. Existing share group: "test_share_group"*
2.1. When creating a new classic cons…

- **majialong:** Hi [~showuon] , if you're not working on this, may I take it? Thanks.
- **Luke Chen:** Assigned to you [~majialong] . Thanks. It needs a KIP if we want to create a new error. FYI.
- **Andrew Schofield:** [https://cwiki.apache.org/confluence/spaces/KAFKA/pages/430409229/KIP-1359+Improve+usability+of+resetting+group+offsets] is related.

## KAFKA-20800:  Adjust Kafka security logging with more context
Improvement · Open · Minor · created 2026-07-13

Currently, there is a problem that Kafka broker don't write any context to logs, while some SASL authentication problem happens.
It makes assessment hard for the cases when external client (for which we don't have an access to the actual configuration) fails to be authenticated in our Kafka cluster 
Need to adjust logging somehow to log at least username which was currently tried by the client.


## KAFKA-20801: KIP-1366: Configurable Segment Interval for Window and Session Stores
Improvement · Open · Major · components: streams · labels: kip · created 2026-07-13

implementation of [https://cwiki.apache.org/confluence/spaces/KAFKA/pages/440304328/KIP-1366+Configurable+Segment+Interval+for+Window+and+Session+Stores]
This adds a public API to set segmentSize explicitly for segmented Window and Session Stores


## KAFKA-20893: KafkaStreams incorrectly reports task-offsets (ie state) for non-existing (previously owned) in-memory stores to the task assignor
Bug · Resolved (Fixed) · Critical · components: streams · created 2026-08-05 · resolved 2026-08-05

KIP-1035 replaced the local state directory .checkpoint files with persistent state store internal offset tracking, plus an in-memory offsets cache inside StateDirectory. However, the cache is incorrectly populated with in-memory store offsets, while it should only contain persistent store offsets (cf [https://github.com/apache/kafka/commit/5740a26525a27df9eacd847a6d4ed6eb23fda0dc] which replaces `ProcessorStateManger#checkpoint()` which contains a check `storeMetadata.stateStore.persistent()` w…


## KAFKA-20894: StreamsGroupDescription.toString throws NullPointerException when authorized operations are omitted
Bug · Resolved (Fixed) · Minor · components: clients, streams · created 2026-08-05 · resolved 2026-08-12

h2. Problem
`DescribeStreamsGroupsOptions.includeAuthorizedOperations()` defaults to `false`. In this normal request path, the broker omits authorized operations and `AdminUtils.validAclOperations()` converts the omitted value to `null`. `StreamsGroupDescription` and its Javadoc explicitly allow that nullable state.
However, `StreamsGroupDescription.toString()` unconditionally calls `authorizedOperations.stream()`. As a result, merely logging or rendering a successfully returned description ca…

- **Matthias J. Sax:** Thanks for the ticket – I am just wondering how we could hit this, ie, when is `toString()` actually used?
- **GiminKim:** Thanks for asking. I could not find a Kafka-internal runtime path that
 directly invokes StreamsGroupDescription.toString(); for example,
 StreamsGroupCommand accesses the individual fields instead.
 The failure is reachable by Admin API consumers, though. The convenience
 describeStreamsGroups(Coll…
- **Matthias J. Sax:** Thanks for the details!

## KAFKA-20895: Different controller election behavior depending on node count
Improvement · Open · Major · created 2026-08-05

On a clean shutdown, the leader computes a preferred successors list. This list is order by log end offsets and by node.id for followers with the same log end offsets.
With a 3 node quorum, when the leader enters the resigned state, each follower will wait a specific time based on its position in the successors list before initiating a vote. As the first entry waits the least amount of time, it starts a vote first. It will receive its own vote as well as the vote from the resigned leader. This…

- **Suman Pal:** Hi [~mimaison] , I'm looking into this. If nobody else is working on it, I'll assign it to myself and investigate further.
- **Suman Pal:** Hi [~mimaison] , added a \{{hasLeaderResigned}} flag on \{{FollowerState}}, whose purpose is to tell a follower that its leader has stepped down. It is set from the EndQuorumEpoch the leader sends on a clean shutdown, and \{{canGrantVote()}} then grants a pre-vote once it is set, since granting is n…

## KAFKA-20896: Avoid epoch bump when adding a new config to the assignor
Improvement · Open · Major · created 2026-08-05

num.standby.replicas is still written unconditionally, so the "omit default-valued configs"fix only covers the new config and the next one added hits the upgrade epoch bump again.


## KAFKA-20897: KIP-1095: Kafka Canary Isolation
New Feature · Open · Major · components: clients, core · created 2026-08-05

A bad broker deployment can affect any partition hosted on the brokers being
upgraded. Operators have no way to bound that set in advance: a new broker
build takes whatever partitions the replica placer assigns it, so the blast
radius of a regression is discovered after the fact rather than chosen
beforehand.
This issue adds an optional broker attribute, "pod", which groups brokers
into named subsets, and a replica placer that can confine a configurable
fraction of partitions to a single…


## KAFKA-20898: PushTelemetry sets terminating flag on validation failure, permanently locking out client instance
Bug · Resolved (Fixed) · Major · created 2026-08-06 · resolved 2026-09-24

[https://github.com/apache/kafka/blob/89ccd6a1260130e1a5ea83a0aa98a7d397482ace/server/src/main/java/org/apache/kafka/server/ClientMetricsManager.java#L209]
[https://cwiki.apache.org/confluence/spaces/KAFKA/pages/173085915/KIP-714+Client+metrics+and+observability]
{quote}*Client termination*
When a client with an active metrics subscription is being shut down, it should send its final metrics without waiting for the PushIntervalMs time.
To avoid the receiving broker’s metrics rate-limiter dis…


## KAFKA-20899: StickyTaskAssignor not sticky for standby tasks ("streams" protocol)
Bug · Resolved (Fixed) · Major · components: group-coordinator, streams · created 2026-08-06 · resolved 2026-08-10

The problem is in `StickyTaskAssignor#findPrevMemberWithLeastLoad` which does not cycle all members correctly as candidates:
It select `member.get(0)` unconditionally as first candidate, even if this member might also host the active task, and is not a candidate.
It pins the `candidateProcessState` to the first "seed" candidate and never updates it, comparing incorrect process states later.
Thus, load of other members is always compared to the load of the "seed" member, and this happens even…


## KAFKA-20900: docker_sanity_test.py should not ignore "Error" count
Bug · Resolved (Fixed) · Minor · created 2026-08-06 · resolved 2026-08-15

The `failure_count` does not account for environment or execution errors. This leads to a misleading console output stating "all tests passed successfully", even when no tests were actually executed
[code/log omitted]

- **Gaurav Narula:** Thanks for reporting this Chia! I had found the same last week but had covered it under a minor PR at https://github.com/apache/kafka/pull/22987
 I've edited its title now and given it this issue number
- **Chia-Ping Tsai:** Yes, you are right. I will take a look at your PR

## KAFKA-20901: [KRaft] cordoned.log.dirs is accepted but not enforced when log.dirs uses a relative path
Bug · Open · Major · components: core · created 2026-08-06

h2. Description
When {{log.dirs}} is configured with a relative path, setting {{cordoned.log.dirs}} has inconsistent behavior:
 # Setting {{cordoned.log.dirs}} to the absolute path returned by {{DescribeLogDirs}} is rejected because it does not exactly match the relative value in {{{}log.dirs{}}}.
 # Setting {{cordoned.log.dirs}} to the relative path succeeds and the dynamic configuration is persisted.
 # However, the directory is not actually treated as cordoned, and replicas for newly crea…

- **majialong:** Thanks for reporting this. I reproduced the issue locally on the current trunk. I’d like to work on it, so I’ll assign it to myself and investigate a fix.
- **majialong:** Hi [~mimaison] , I’ve opened PR  [https://github.com/apache/kafka/pull/23241] to address this issue. Could you please review it when you have a chance? Thanks!

## KAFKA-20902: Streams metered stores: oldest-iterator-open-since-ms can be wrong when two iterators open in the same millisecond
Bug · Open · Minor · components: streams · created 2026-08-06

{{openIterators}} is a {{ConcurrentSkipListSet}} keyed only by {{startTimestamp()}} (ms resolution). Two iterators opened in the same millisecond compare equal, so the second {{add()}} is a silent no-op and a {{remove()}} on close can evict the still-open one — the {{oldest-iterator-open-since-ms}} gauge then under-reports (may skip a still-open iterator or return 0). {{num-open-iterators}} is unaffected (separate {{LongAdder}}); iterators still close correctly, so it's a metric-accuracy issue,…

- **Suman Pal:** Hi [~jess], I’ve locally reproduced this issue using UT and am working on a fix (total comparator with a per-iterator sequence id, as suggested in the ticket). Assigning this to myself, will open a PR soon for review.

## KAFKA-20903: Revert public API changes from KIP-1238
Task · Resolved (Fixed) · Blocker · components: streams · created 2026-08-07 · resolved 2026-08-11

We started to implement KIP-1238 and public API changes for TDD landed, however, the feature is not completed.
Thus, we should revert the public API changes (only in `4.4` branch) before 4.4.0 is released, to avoid unnecessary API deprecation noise for users.
[https://github.com/apache/kafka/pull/22892]
[https://github.com/apache/kafka/pull/22673]
[https://github.com/apache/kafka/pull/22612]


## KAFKA-21047: Make Kafka Connect KIP-909 ready
Improvement · Open · Major · components: connect · created 2026-09-07

KIP-909 ships improved error handling behavior for Kafka clients with regard to DNS changes, and broker re-discovery. However, it also introduces behavior changes and new exceptions when enabled. For this reason, it's locked down in Kafka Connect at the moment and cannot be enable.
This ticket is about updating KC code base do become KIP-909 ready: we need to change the code to allow to handle the new exceptions correctly.
Open question: KIP-909 is disabled on the clients because it requires c…


## KAFKA-21048: DumpLogSegmentsTest leaks BrokerTopicStats and causes JmxToolTest to fail
Improvement · Open · Minor · created 2026-09-07

DumpLogSegmentsTest creates a BrokerTopicStats instance but does not close it.
When JmxToolTest runs afterward, it fails because the same MBean is still registered:
javax.management.InstanceAlreadyExistsException:
kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec
Reproduce with:
./gradlew :tools:unitTest \
  --tests org.apache.kafka.tools.DumpLogSegmentsTest \
  --tests org.apache.kafka.tools.JmxToolTest \
  -PmaxParallelForks=1 --max-workers=1 --rerun
Reproduced on Kafka 4.4.0…

- **Lianet Magrans:** Hey folks, I just removed the 4.4 fix version since this is minor and we're past code freeze. Feel free to add 4.5 if there is PR coming. Thanks!
- **Jheng-Sing Chen:** Thanks! I’ll prepare a PR targeting 4.5.

## KAFKA-21049: Async consumer can busy-loop while waiting for fetch progress when retry.backoff.ms is zero
Bug · Open · Minor · created 2026-09-08

When retry.backoff.ms is configured to 0, the async consumer can use 0 as
the application-thread fetch wait.
FetchRequestManager.maximumTimeToWait() returns retryBackoffMs when there
is no fetch request in flight, and AsyncKafkaConsumer.pollForFetches()
also uses it while waiting for assignment, fetch positions, or fetch
progress. This can cause FetchBuffer.awaitWakeup() to return immediately
and the outer poll loop to repeat without progress.
Use a minimum positive value when retryBackof…


## KAFKA-21050: Flaky test ConsumerBounceTest#testClassicClose[1]
Bug · Open · Major · components: clients · created 2026-09-08

Flaky during build of [https://github.com/apache/kafka/pull/23234], but was already appearing as a flaky test in other builds.


## KAFKA-21051: testShareConsumerAfterCoordinatorMovement can halt the test JVM
Test · Open · Minor · created 2026-09-09

[code/log omitted]
The consumer could end too early due to a rough condition:`records.count()` does not mean there is no more data. Hence, the following assertion fails.
[code/log omitted]
The failure ends the test without closing the thread which is shutting down the broker.
[code/log omitted]
As a result, the cleanup of {{ClusterInstance}} skips the broker, but the broker stays alive until the next test.. However, the folder has already been removed, and hence the broker started by the pr…


## KAFKA-21052: Deprecate TokenInformation#fromRecord and TokenInformation#setExpiryTimestamp
Improvement · Open · Minor · labels: need-kip · created 2026-09-09

TokenInformation#fromRecord is only used by the server, so it should be moved out of the public API. Also, TokenInformation#setExpiryTimestamp is already dead code.


## KAFKA-21053: Rewrite shouldThrowIllegalStateExceptionOnOffsetIfNoRecordContext
Test · Resolved (Fixed) · Minor · created 2026-09-09 · resolved 2026-09-11

It stays on the very old logic. We should rewrite it to match the current implementation.


## KAFKA-21054: Use assertThrows in InternalTopicManagerTest timeout tests
Test · Open · Minor · components: streams, unit tests · created 2026-09-09

[code/log omitted]
[code/log omitted]
It should leverage assertThrows to ensure it does throw exception.


## KAFKA-21055: upgrade from jackson 2.x to jackson 3.x
Improvement · Open · Major · created 2026-09-09

kafka currently uses jackson 2.x, see [{{dependencies.gradle}}|https://github.com/apache/kafka/blob/81e8ebc9f1648d7dfdfd0e8051a6dd39431f068a/gradle/dependencies.gradle#L65]
jackson 3.x has now been out for a while and and the clock is counting down for jackson 2.x (2.21.x is an LTS with ~2 years of support acc. to their documents).
more information can be found in their [migration guide|https://github.com/FasterXML/jackson/blob/main/jackson3/MIGRATING_TO_JACKSON_3.md]
there are several reason…


## KAFKA-21056: migrate to gradle version catalog
Improvement · Open · Minor · created 2026-09-09

the kafka project currently has its own custom [{{dependencies.gradle}}|https://github.com/apache/kafka/blob/trunk/gradle/dependencies.gradle] mechanism to manage dependency versions.
gradle nowadays has a standard way of dealing with this, the [version catalog|https://docs.gradle.org/current/userguide/version_catalogs.html], which is also clearly listed as part of their [best practices|https://docs.gradle.org/current/userguide/best_practices_dependencies.html#use_version_catalogs].
i'd sugges…


## KAFKA-21057: Extract share-group DLQ record and validation logic into reusable helpers
Bug · Resolved (Fixed) · Major · created 2026-09-09 · resolved 2026-09-09

Minor refactor to extract share-group DLQ record and validation logic into reusable helpers


## KAFKA-21142: KRaftMigrationZkWriter may fail to create TopicPartitionStateZnode during a crash fault
Bug · Open · Major · components: kraft, migration, zkclient · created 2026-09-22

Kafka quorum controller leader may fail to correctly update state in ZK when it crashes in the following scenario
*Setup*
Consider a 3 controller quorum in dual-write mode, i.e. the quorum leader is acting as the coordinator and owning writes to ZK via KRaftMigrationDriver. Also consider the brokers to not be bounced in KRaft mode.
*Failure Scenario*
1. Let's say a client sends a request to increase the topic-partition count of topic {{T1}} from {{2}} to {{3}}
2. After the request is proces…


## KAFKA-21143: Server-only OAUTHBEARER listener with private JWKS CA triggers token login and fails broker startup
Bug · Open · Critical · components: security · created 2026-09-22

h2. Problem
A broker configured with an external _SASL_SSL/OAUTHBEARER_ listener can fail during startup when the broker is intended to act only as an OAuth token validator and the JWKS endpoint requires a private CA.
h3. Topology
[code/log omitted]
The JWKS endpoint uses HTTPS with a private CA, so trust configuration is supplied for the OAUTHBEARER listener:
[code/log omitted]
h2. Actual behavior
During broker startup, initialization of the external SASL listener reaches {{OAuthBearerLo…

- **Muralidhar Basani:** > Is there an intended supported configuration that allows JWKS TLS trust options to be supplied while retaining the tokenless server-side behavior
 [~akshatha] can you try adding _unsecuredLoginStringClaim_sub_ workaround (not a fix)?
 I tried the below jaas config and was able to start the server…
- **akshatha ramesh:** Hi [~muralibasani],
 Thanks for your quick response.
 According to the Kafka documentation, this configuration is intended solely for development or testing and is not recommended for production, which makes me hesitant to adopt it. However, unsecuredLoginStringClaim_sub was already tested before ra…
- **Muralidhar Basani:** [~akshatha] I have a fix, you might want to try as. well if it works.
 https://github.com/apache/kafka/pull/23557

## KAFKA-21144: Producer auth errors may become stale but still be thrown later on cold/new topics
Bug · Open · Major · components: clients, producer  · created 2026-09-22

Whenever the producer encounters an auth failure, it's recorded as a fatal error in the producer's metadata, and it's thrown only when the producer has to wait for metadata for a topic (this would be when using a new topic or "idle" topics, with no produce for longer than the metadata.max.idle).
These errors are only cleared when thrown, which means that it could remain in the internal cache for a long time if the producer lets some topics go idle. So a producer that keeps producing to its hot…


## KAFKA-21145: Reenable tests once compression is supported 
Sub-task · Open · Minor · created 2026-09-22

See the comment: https://github.com/apache/kafka/pull/23135#discussion_r3769371194


## KAFKA-21146: Test classes leak BrokerTopicStats metrics into the shared Yammer registry
Test · Open · Minor · created 2026-09-23

[code/log omitted]
I ran into the above issue while testing 4.4.0 RC. It appears some tests don't close the `BrokerTopicStats` correctly. We need to fix `DumpLogSegmentsTest` obviously, but it would be good to take a look at the following tests
 * {{SchedulerTest}}
 * {{BrokerCompressionTest}}
 * {{LogCleanerManagerTest}}
 * {{LogCleanerTest}}
 * {{LogConcurrencyTest}}
 * {{LogManagerTest}}
 * {{LogTestUtils}}
 * {{ShareFetchUtilsTest}}


## KAFKA-21147: Expose explicit config deletions to AlterConfigPolicy
Improvement · Open · Minor · labels: need-kip · created 2026-09-23

see https://github.com/apache/kafka/pull/23310#discussion_r4062992415


## KAFKA-21148: speed up JoinStoreIntegrationTest
Improvement · Open · Minor · created 2026-09-23

similar to KAFKA-21133


## KAFKA-21149: Speed up JoinGracePeriodDurabilityIntegrationTest
Improvement · Open · Minor · created 2026-09-23

It can leverage the LEAVE_GROUP to speed up the bounce in {{{}shouldRecoverBufferAfterShutdown{}}}, since the restart with the same application id waits for the previous member's session timeout otherwise.
[code/log omitted]

- **Chia-Ping Tsai:** KStreamRepartitionIntegrationTest.shouldGoThroughRebalancingCorrectly and KafkaStreamsTelemetryIntegrationTest.shouldPassMetrics have similar issue

## KAFKA-21150: Refactor AbstractKafkaConfig#processRoles
Improvement · Open · Minor · created 2026-09-23

[code/log omitted]
We could add a helper method to {{ProcessRole}} that converts a string to a {{{}ProcessRole{}}}, and then rewrite {{processRoles()}} in a fluent style.


## KAFKA-21151: Extract streams group topology description orchestration into a shared runtime abstraction
Improvement · Open · Major · created 2026-09-23

The streams-group topology-description plugin's orchestration (push validation, the UNCERTAIN barrier write, plugin invocation and epoch bookkeeping, the periodic cleanup cycle, and the DeleteGroups pre-delete flow) is implemented directly inside GroupCoordinatorService, with its logic tightly coupled to `CoordinatorRuntime<GroupCoordinatorShard, CoordinatorRecord>`
This split leaves related logic scattered between the two classes and keeps `GroupCoordinatorService` doing state-machine-level wo…


## KAFKA-21152: LogCompactionTester should read until the end offsets instead of stopping at an empty poll
Bug · Open · Minor · components: system tests, tools · labels: flaky-test · created 2026-09-24

h3. What happened
{{LogCompactionTest.test_log_compaction}} is flaky. In the 4.4.0-rc1 system test run (zstd level 10, ISOLATED_KRAFT), the tester read only 7498 of about 191k rows and the validation failed. The same case passed 5 out of 5 times on rerun. The trimmed logs are attached.
The cause is in the tester, not in the broker or the consumer. {{LogCompactionTester.consumeMessages()}} ({{tools/src/main/java/org/apache/kafka/tools/LogCompactionTester.java}}) stops at the first empty {{poll(…

- **Eric Chang:** This issue is not caused by 4.4.0 rc, so I marked it as minor priority.
