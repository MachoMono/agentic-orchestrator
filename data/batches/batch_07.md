## KAFKA-19249: Replace Consumer#close(Duration) with Consumer#close(CloseOptions)
Improvement · Resolved (Fixed) · Major · created 2025-05-07 · resolved 2025-11-25

We have introduced Consumer#close(CloseOptions) in KIP-1092.
We should also replace the deprecated method with the new method.

- **Vinod Baba:** [~frankvicky] I am new to the Kafka project and looking to start with a beginner-level task. Can I take this up ? Thanks
- **Chang-Yu Huang:** [~vinodbaba] are you still looking for this issue? I will take it if you don't have time.

## KAFKA-19250: abortTransactions should not return abortable exception
Sub-task · Resolved (Fixed) · Major · created 2025-05-07 · resolved 2025-06-04


## KAFKA-19251: Resolve the flaky test ShareConsumerTest.testMultipleConsumersInGroupConcurrentConsumption
Sub-task · Resolved (Fixed) · Major · created 2025-05-07 · resolved 2025-05-30

All the flaky runs had this common error log.
[code/log omitted]

- **Shivsundar R:** After this PR went in to AK - [https://github.com/apache/kafka/pull/19781,] we stopped seeing the error logs related to state epoch, and the test has had clean runs for the past 7 days.
 Develocity link - [https://develocity.apache.org/scans/tests?search.tags=trunk&search.timeZoneId=Asia%2FCalcutta&…

## KAFKA-19252: Support broker and controller restarts in testkit
Improvement · Open · Major · components: unit tests · created 2025-05-07

We should support broker and controller restarts in ClusterTest (and testkit). Since these components are not designed to be reused, we will need to create them on-demand when a node is restarted.
Not having this feature makes it difficult for many tests to be converted from IntegrationTestHarness. Some tests have done so, but by reaching down into the broker implementation classes like [https://github.com/apache/kafka/commit/c527530e806c7d9f79348656d801b1b78e8f2bec#diff-9003994ba58aae31e74ea55…

- **PoAn Yang:** It looks like we have a similar ticket https://issues.apache.org/jira/browse/KAFKA-17259. I will keep working on it. Thanks.

## KAFKA-19253: Improve metadata handling for share version using feature listeners
Sub-task · Resolved (Fixed) · Major · created 2025-05-07 · resolved 2025-05-15

Reference comment - [https://github.com/apache/kafka/pull/19542/files#r2064029087]


## KAFKA-19254: Add generic feature level metric
New Feature · Resolved (Fixed) · Major · created 2025-05-07 · resolved 2025-07-14

KIP link: https://cwiki.apache.org/confluence/display/KAFKA/KIP-1180%3A+Add+a+generic+feature+level+metric

- **Mickael Maison:** Moving to the next release as we're now in code freeze for 4.1.0.

## KAFKA-19255: KRaft request manager should support one in-flight request per request type
Improvement · Resolved (Won't Fix) · Major · created 2025-05-08 · resolved 2025-10-23

- **Mickael Maison:** Moving to the next release as we're now in code freeze for 4.1.0.

## KAFKA-19256: Only send IQ information on assignment changes
Sub-task · Resolved (Fixed) · Major · components: streams · created 2025-05-08 · resolved 2025-06-03


## KAFKA-19264: Remove fallback for thread pool sizes in RemoteLogManagerConfig
Task · Resolved (Fixed) · Minor · components: Tiered-Storage · created 2025-05-11 · resolved 2025-05-11

The fallback mechanism was first introduced in [KIP-950|https://cwiki.apache.org/confluence/x/joqzDw]. According to the proposal, if no thread values are set for {{remote.log.manager.copier.thread.pool.size}} and {{{}remote.log.manager.expiration.thread.pool.size{}}}, these two configs would default to using the value of {{{}remote.log.manager.thread.pool.size{}}}.
As quoted from the KIP:
{quote}If no thread values are set for the two new configurations presented later on in the document we wi…


## KAFKA-19265: Use snapshotting of remote log metedata topic that is used when a broker is restarted.
Improvement · Open · Major · components: core · created 2025-05-11

This is an incremental approach to the remote log metadata snapshot mechanism already covered in KIP-405.

- **Mickael Maison:** Moving to the next release as we're now in code freeze for 4.1.0.
- **Christo Lolov:** Moving to 4.3 since we are past the code freeze for 4.2! Let me know if I have misunderstood something!
- **Mickael Maison:** Moving to the next release as we're now in code freeze for 4.3.0.
- **Omnia Ibrahim:** Moving to 4.5 as we are now in 4.4.0 code freeze

## KAFKA-19266: Eliminate flakiness in test SharePartitionTest.testAcquisitionLockTimeoutForBatchesPostStartOffsetMovement
Sub-task · Resolved (Not A Problem) · Major · created 2025-05-11 · resolved 2025-05-27

There seems to be flakiness in test SharePartitionTest.testAcquisitionLockTimeoutForBatchesPostStartOffsetMovement  [https://develocity.apache.org/scans/tests?search.rootProjectNames=kafka&search.timeZoneId=Asia%2FCalcutta&tests.container=kafka.server.share.SharePartitionTest&tests.test=testAcquisitionLockTimeoutForBatchesPostStartOffsetMovement()] which is unrelated to acquisition lock timeout, but more related to initialization of share partition

- **Abhinav Dixit:** The develocity link posted in description does not include the tag 'trunk'. I think the test {{testAcquisitionLockTimeoutForBatchesPostStartOffsetMovement}} got fixed when I had pushed the fix for https://issues.apache.org/jira/browse/KAFKA-19216 on 6th May. Now, I am querying [develocity|https://de…

## KAFKA-19267: the min version used by ListOffsetsRequest should be 1 rather than 0
Improvement · Resolved (Fixed) · Minor · created 2025-05-11 · resolved 2025-05-16

in the protocol, `ListOffsetsRequest` v0 is unsupported - but in the code base we still set the  oldestAllowedVersion to 0.

- **Chia-Ping Tsai:** related code:
 https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/common/requests/ListOffsetsRequest.java#L69
 https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/common/requests/ListOffsetsRequest.java#L84
- **Ismael Juma:** We should replace the hardcoded value with `ApiKeys.LIST_OFFSETS.oldestVersion()`.
- **Chia-Ping Tsai:** {quote}
 We should replace the hardcoded value with `ApiKeys.LIST_OFFSETS.oldestVersion()`.
 {quote}
 good idea!

## KAFKA-19268: Missing mocks for SharePartitionManagerTest tests
Sub-task · Resolved (Fixed) · Major · created 2025-05-12 · resolved 2025-05-26

A few tests in SharePartitionManagerTest throw silent exceptions but the tests pass. This is mainly due to missing mocks in those tests. The following tests need to be analyzed and fixed - 
testAcknowledgeCompletesDelayedShareFetchRequest
testMultipleConcurrentShareFetches
testCachedTopicPartitionsForValidShareSessions
testReleaseSessionCompletesDelayedShareFetchRequest
testReleaseSessionSuccess

- **jiseung:** May I take this one?
- **Abhinav Dixit:** Feel free to work on this issue, I am assigning it to you
- **Andrew Schofield:** [~jasonryu] I am not able to assign the ticket to you. Maybe there's a problem with account permissions.
- **jiseung:** Since I am new to here, I have no ideas to get permission. I just sent mail to request permission to [jira@kafka.apache.org|mailto:to%C2%A0jira@kafka.apache.org] (not sure this is right).
- **Apoorv Mittal:** [~jasonryu] You should send the request at dev@kafka.apache.org.
- _…5 more comments_

## KAFKA-19269: "Unexpected error .." should not happen when the delete.topic.enable is false
Improvement · Resolved (Fixed) · Minor · created 2025-05-12 · resolved 2025-05-15

Because ControllerAPIs directly throw an exception when delete.topic.enable is false, the "Unexpected error .." message is unexpectedly appended to the log.

- **kangning.li:** [~chia7712]   Cloud you assign it to me ?

## KAFKA-19270: Remove optional from ClusterInstance#controllerListenerName
Improvement · Resolved (Fixed) · Minor · created 2025-05-12 · resolved 2025-05-15

in kraft mode, the listener name should be always exist.


## KAFKA-19271: Private interface for injecting test wrappers for KIP-1071 enabled consumers
Sub-task · Resolved (Fixed) · Major · components: streams · created 2025-05-12 · resolved 2025-06-03

The new rebalance protocol cannot be supported by the existing KafkaClientSupplier and KIP-1088 is on hold.
For now, to support current internal testing cases that use KafkaClientSupplier for injecting test behavior, we need a private interface that can fulfil this functionality for KIP-1071.


## KAFKA-19272: Handling different scenarios for initPid(keepPrepared=true)
Sub-task · In Progress · Major · created 2025-05-12

When initPid(keepPrepared = true) is called when a client crashes, there are quite a few situations that we should consider. 
When there is an ongoing txn, we can transition it to the newly added PREPARED_TRANSACTION state, but what if there's no ongoing transaction?
Another scenario could be:
 # Issued a commit, to commit prepared
 # The commit succeeded on the TC, but the client crashed
 # Client restarted with keepPreparedTxn=true (because it doesn't know if the commit succeeded or not a…


## KAFKA-19273: Ensure the delete policy is configured when the tiered storage is enabled
Improvement · Resolved (Fixed) · Minor · created 2025-05-13 · resolved 2025-05-14

tiered storage will move the segments to remote storage, so it does not make sense to disable delete policy.

- **Chia-Ping Tsai:** see https://lists.apache.org/thread/5mrbmz461djcwn8b8cblv3s2pxpmvolf for discussion
- **Chia-Ping Tsai:** code: https://github.com/apache/kafka/blob/6eafe407bd859f147d7a5ecfe261f6e20698fb4a/storage/src/main/java/org/apache/kafka/storage/internals/log/LogConfig.java#L564

## KAFKA-19274: Group Coordinator Shards are not unloaded when __consumer_offsets topic is deleted
Bug · Resolved (Fixed) · Major · created 2025-05-13 · resolved 2025-05-15

Group Coordinator Shards are not unloaded when __consumer_offsets topic is deleted. The unloading is scheduled but it is ignored because the epoch is equal to the current epoch:
[code/log omitted]
The issue seems to be in this code:
[code/log omitted]
We use `None` when a partition is deleted and the actual leader epoch when the topic is deleted. The issue is that the leader epoch is not incremented when the topic is deleted so the unloading logic does not accept the resignation. We should u…


## KAFKA-19424: FindCoordinator inconsistent across brokers when __consumer_offsets partition count is increased
Bug · Open · Major · components: group-coordinator · created 2025-06-20

{{GroupCoordinatorService}} captures the number of partitions of {{\_\_consumer_offsets}} at startup. This is used to map group ids to {{\_\_consumer_offsets}} partitions in {{GroupCoordinatorService.partitionFor}}.
When adding partitions to {{\_\_consumer_offsets}}, {{GroupCoordinatorService}} doesn't update its cached partition count. This means that newly started brokers will map group ids to partitions differently to existing brokers and FindCoordinator requests can return different results…

- **sanghyeok An:** Hi, [~squah-confluent] .
 If you are not working in this task, May I take a look?
- **Sean Quah:** Hi, [~chickenchickenlove]. Sure, please feel free to reassign the task to yourself. I'm not currently working on it.
- **sanghyeok An:** [~squah-confluent] Thanks a lot! 
 Self assigned!
- **sanghyeok An:** Hi [~squah-confluent] !
 During my investigation of both __consumer_offsets and  {{__transaction_state}} alongside this work, 
 I realized that this issue extends to all internal topics. 
 Also, the documentation explicitly discourages modifying the partition count for internal topics post-deploymen…

## KAFKA-19425: local segment on disk never deleted forever when remote storage initial failed
Bug · Resolved (Fixed) · Critical · components: Tiered-Storage · created 2025-06-21 · resolved 2025-07-28

remote storage initial failed is silence so that the disk keep increasing forever.
[stop the server when fail to initialize to avoid local segment never got deleted. by jiafu1115 · Pull Request #20007 · apache/kafka|https://github.com/apache/kafka/pull/20007]

- **fujian:** [~yangpoan] hi. can you help to take I look? thanks!  
 I see you are the only person which is active on this module:)
- **PoAn Yang:** [~fujian1115] I will take a look today. Thanks.

## KAFKA-19426: TopicBasedRemoteLogMetadataManager's initial should happen after the broker ready
Bug · Resolved (Fixed) · Major · components: Tiered-Storage · created 2025-06-21 · resolved 2025-11-02

currently. the default value don't make sure the retry can always happen with successful
For example: There are possible two timeout (2 * 60s) happen at TopicBasedRemoteLogMetadataManager#initializeResources
[2025-06-03 21:57:21,151] INFO Topic __remote_log_metadata does not exist. Error: Timed out waiting for a node assignment. Call: listNodes at
[2025-06-03 21:58:21,153] ERROR Encountered error while creating __remote_log_metadata topic. java.util.concurrent.ExecutionException: org.apache.k…


## KAFKA-19427: The __consumer_offsets topic applies the broker configuration message.max.bytes, which may cause the coordinator broker to allocate too much memory and cause OOM
Bug · Resolved (Fixed) · Critical · components: consumer, group-coordinator · created 2025-06-23 · resolved 2025-07-16

h3. Kafka cluster configuration
1.Kafka version：4.0
2.The cluster specifications are: 3 brokers and 3 controllers
3.JVM startup parameters:
!image-2025-06-23-14-16-00-554.png!
4.JDK version：
!image-2025-06-23-14-17-34-767.png!
h3. Steps to reproduce the problem
1.In this new cluster, create a test topic: {*}test{*}，and this cluster will eventually have *only this one topic* tested by external users.
topic config : NewTopic newTopic = new NewTopic("test", 3, (short) 1);
2.Start the prod…

- **RivenSun:** [~guozhang] [~dajac] 
 Could you please help me look into this issue? 
 Thank you very much!
- **Sean Quah:** [~RivenSun] to help diagnose the issue, could you attach the broker logs and the output of {{{}kafka-topics --describe --topic __consumer_offsets{}}}?
- **RivenSun:** The above document has posted the client log and coordinator broker log when the problem occurs.
 The coordinator broker log is posted here in text form. We can see that two OOM exceptions occurred:
 [code/log omitted]
 Today I used rivenTest6 to start the consumer again and found that this group ca…
- **RivenSun:** Add additional information. When the consumer is not started, the broker's log is normal.
 There are only two topics in the cluster, details of the test topic.
 !image-2025-06-24-10-50-17-396.png!
- **David Jacot:** [~RivenSun] Thanks for the Jira. Could you please share a heap dump of the broker when the issue happens? It would help to diagnose what consumes a lot of memory. For the context, the byte buffers that you highlighted in the description are indeed kept by the group coordinator. It has one per __cons…
- _…29 more comments_

## KAFKA-19428: IOException during writing max timestamp should not be ignored
Bug · Resolved (Not A Problem) · Minor · created 2025-06-23 · resolved 2025-06-25

this is similar to KAFKA-19221. The IOException caused by writing max timestamp is currently ignored.
[code/log omitted]
That could be an issue since we assume the last entry is the max timestamp after restarting. If the write fails, the loading log should re-build the index to ensure it catches the "correct" max timestamp.

- **Gaurav Narula:** -Mind if I take this one as well [~chia7712] ?:)-
 Edit: nvm, I see Lan is already working on it. Happy to help with the review.
- **Chia-Ping Tsai:** [~gnarula] I think [~isding_l] is working on that already :)
- **Lan Ding:** It seems like an IOException might not be thrown here. Only the `maxTimestampSoFar()` and `shallowOffsetOfMaxTimestampSoFar()` methods could potentially throw an IOException. However, the code within these methods that throws the exception will only execute if `maxTimestampAndOffsetSoFar == Timestam…
- **Chia-Ping Tsai:** [~isding_l] thanks for your response. you are right that checked IOException is thrown only if the time index is not initialized, and the segment having new timestamp data should initialize the time index already. Please feel free to close this jira

## KAFKA-19429: Deflake streams_smoke_test
Bug · Resolved (Fixed) · Major · components: streams, system tests · created 2025-06-23 · resolved 2025-06-24

It looks like we are checking for properties that are not guaranteed under at_least_once, for example, exact counting (not allowing for overcounting).


## KAFKA-19430: Don't fail on RecordCorruptedException
Improvement · In Progress · Major · components: streams · created 2025-06-23

From [https://github.com/confluentinc/kafka-streams-examples/issues/524]
Currently, the existing `DeserializationExceptionHandler` is applied when de-serializing the record key/value byte[] inside Kafka Streams. This implies that a `RecordCorruptedException` is not handled.
We should explore to not let Kafka Streams crash, but maybe retry this error automatically (as `RecordCorruptedException extends RetriableException`), and find a way to pump the error into the existing exception handler.
I…

- **Uladzislau Blok:** [~mjsax] Hey. I could handle this, if there is no objections
- **Matthias J. Sax:** Thanks. No objections at all. I just don't know how complex it will be, to resolve this (just as FYI).
- **Uladzislau Blok:** [~mjsax] Hey Matthias. Sorry for the delay. I took a look into issue. Problem here is that exception is threw by Kafka client not streams, so it's even before we're trying to de-serialize the message. I don't think it's good to handle it inside 'DeserializationExceptionHandler' because it's not abou…
- **Matthias J. Sax:** Well, that's all up for discussion I guess :) – And there is multiple issue we need to consider.
  # The idea to maybe reuse `DeserializationExceptionHandler` was, to avoid having too many callback interfaces, and to keep the API surface area small. Even if this error is not really about deserializa…
- **Uladzislau Blok:** I'm not fully sure for now what would be the best way to handle the error.
 About CONTINUE case: exception is threw by Kafka consumer when we're trying read butch of messages, not sure how we can skip only one message, if we don't know which one from the butch is corrupted.
 From my perspective, we…
- _…11 more comments_

## KAFKA-19431: Stronger assignment consistency with subscription for consumer groups 
Improvement · Resolved (Fixed) · Major · components: group-coordinator · created 2025-06-24 · resolved 2025-10-06

Currently, consumer group assignments are eventually consistent with subscriptions: when a member has unrevoked partitions, it is not allowed to reconcile with the latest target assignment. If a member with unrevoked partitions shrinks its subscription, it may observe assignments from the broker containing topics it is no longer subscribed to.
If we wanted to, we could tighten this up at the cost of extra CPU time. Note that it's not feasible to close the gap for regex subscriptions, since ther…


## KAFKA-19432: Add an ERROR log message if broker.heartbeat.interval.ms is too large
Improvement · Resolved (Fixed) · Minor · created 2025-06-24 · resolved 2025-09-03

We should add an ERROR log message if broker.heartbeat.interval.ms is too large. Specifically, it should not be long enough that two missed heartbeats are longer than broker.session.timeout.ms.


## KAFKA-19433: Unify broker heartbeat RPC timeout and periodic resend timeout
Improvement · Open · Minor · created 2025-06-24

We should unify the broker heartbeat RPC timeout and the periodic resend timeout so that RPC timeouts don't result in us sending broker heartbeats less frequently than usual.

- **Jimmy Wang:** Hi [~cmccabe] ,
 I think I could help with this issue :)
- **Jimmy Wang:** Hi [~cmccabe] , sorry for the late response. I'm a bit confused because currently, for the broker, both the periodic resend timeout and the RPC timeout are set to {{{}broker.heartbeat.interval.ms{}}}. I wonder if I've missed something or if I didn't understand your point correctly. Could you help to…

## KAFKA-19434: Move logic for state store initiation to StreamThread handover
Task · Resolved (Fixed) · Blocker · components: streams · created 2025-06-24 · resolved 2026-02-20

When starting a Kafka Streams instance, if it has pre-existing state, the state stores are initialized on the main thread. Part of this
initialization registers the stateful metrics with the JMX thread-id tag of {{{}main{}}}. This breaks the KIP-1076 implementation where need to
register metrics with thread-id tags of {{{}xxxStreamThread-N{}}}. This is necessary due to the fact that the {{StreamsMetric}} is a singleton shared
by all {{StreamThread}} instances, so we need to make sure only add…

- **Eduwer Camacaro:** Hi,
 I opened this PR that proposes an alternative solution to this issue [https://github.com/apache/kafka/pull/20749]. Let me know what you think about this approach that basically proposes some changes in the StateStores lifecycle, but this will require modifications in KIP-1035.
- **Matthias J. Sax:** This one is not a blocker for 4.2 any longer – we reverted the code introduced with KIP-1035 which causes the issue in the 4.2 branch.
- **Bill Bejeck:** Merged into trunk

## KAFKA-19466: LogConcurrencyTest should close the log when the test completes
Improvement · Resolved (Fixed) · Major · created 2025-07-02 · resolved 2025-07-09

In 
testUncommittedDataNotConsumedFrequentSegmentRolls() and testUncommittedDataNotConsumed(), we call createLog(), but never close the log when the tests complete.

- **Jhen-Yung Hsu:** I’d like to work on this. Thank you :)
- **Chia-Ping Tsai:** [~yung] thanks for taking over it. This test class is also ready to be migrated. Could you please rewrite the test by Java code and then move it to storage module?
- **Jhen-Yung Hsu:** Sure. I’m happy to do that.
- **Jhen-Yung Hsu:** Here is the fix along with the migration: [https://github.com/apache/kafka/pull/20110]. Thank you

## KAFKA-19467: Add a metric for controller thread idleness
New Feature · Resolved (Fixed) · Major · labels: need-kip · created 2025-07-03 · resolved 2025-10-02

KIP-1190: [https://cwiki.apache.org/confluence/display/KAFKA/KIP-1190%3A+Add+a+metric+for+controller+thread+idleness]

- **TengYao Chi:** [~mahsaseifikar] I think this ticket may require a KIP.
- **Mahsa Seifikar:** [~frankvicky] I'm preparing a KIP right now for this

## KAFKA-19468: Share group epoch increments on every heartbeat if subscribed topics removed
Sub-task · Resolved (Fixed) · Major · created 2025-07-03 · resolved 2025-07-04

If topics are removed from the set of subscribed topics for a share group, subsequent heartbeats will erroneously increment the group epoch thinking that outstanding state initialisations are present. The condition for incrementing the epoch is too strict.


## KAFKA-19469: Dead-letter queues for share groups
New Feature · Resolved (Fixed) · Major · labels: queues-for-kafka · created 2025-07-04 · resolved 2026-07-27

This Jira tracks the development of KIP-1191: https://cwiki.apache.org/confluence/display/KAFKA/KIP-1191%3A+Dead-letter+queues+for+share+groups

- **Lan Ding:** Hi [~schofielaj],  [~apoorvmittal10], Do you think it would be feasible to introduce Dead Letter queue in Share Group?
- **Andrew Schofield:** Yes, my thinking too. I have a KIP almost ready to publish. Watch this space.
- **Lan Ding:** Great work! Looking forward to your KIP being published.
- **Andrew Schofield:** [https://cwiki.apache.org/confluence/display/KAFKA/KIP-1191%3A+Dead-letter+queues+for+share+groups]
 [~isding_l] I was thinking of using this Jira for the KIP, as opposed to creating a new one. wdyt?
- **Lan Ding:** Sounds good, please go ahead.
- _…5 more comments_

## KAFKA-19470: Avoid creating loggers repeatedly to affect the performance of request processing
Improvement · Patch Available · Major · components: core · created 2025-07-04

We see that the broker has a performance bottleneck when processing requests in kafka 2.8.2 version + jdk 11 environment. The CPU profiler is as follows:
!image-2025-07-04-19-05-51-900.png|width=1065,height=489!
After research, we found that this is a problem with jdk11 but without resolution [https://bugs.openjdk.org/browse/JDK-8266964]  StackWalker has a performance degradation for jdk11.
When creating every logger, log4j2 will invoke StackWalker, the following is the performance data obser…

- **Yunseop Eom:** PR opened: https://github.com/apache/kafka/pull/23044 for KAFKA-19470. Added a thread-safe logger-name cache so immutable Scala logger wrappers are reused across Logging instances while preserving loggerName overrides. Added a regression test; core LoggingTest, Spotless, Checkstyle, and SpotBugs pas…
- **Yunseop Eom:** PR #23044 is open and ready for maintainer review: https://github.com/apache/kafka/pull/23044

## KAFKA-19471: Enable acknowledgement for a record which could not be deserialized
Sub-task · Resolved (Fixed) · Major · created 2025-07-04 · resolved 2025-07-27

If a record fetched by a share consumer fails to be deserialized, the KIP states that it is automatically released and that the application cannot override this behavior. Actually, experience with KafkaShareConsumer shows that it would be helpful to be able to override this to REJECT such records instead.
We can add an override `KafkaShareConsumer.acknowledge(String topic, int partition, long offset, AcknowledgeType type)` for this purpose where the user does not have a `ConsumerRecord` instanc…

- **Lan Ding:** Hi [~schofielaj], if you're not working on this, may I take it? Thanks.
- **Andrew Schofield:** Sure. Go ahead.
- **Lan Ding:** During the process of fixing this issue, I seem to have discovered another issue. When parseRecord fails and throws a {{{}SerializationException{}}}, the following code executes:
 [code/log omitted]
 In the outer code, the exception is not caught and is directly thrown:
 [code/log omitted]
 This ult…
- **Andrew Schofield:** [~isding_l] If you are aware of any remaining issues with exception handling, please open another issue.

## KAFKA-19472: A BufferOverflowException is thrown by RemoteLogManager when FetchApiVersion <= 2
Bug · Patch Available · Major · components: log · created 2025-07-04

RemoteLogReader throws a BufferOverflowException when FetchApi version <= 2 and firstBatchSize exceeds max.partition.fetch.bytes
Exception Message
[code/log omitted]
firstBatch.writeTo(buffer) will throw BufferOverflowException when firstBatch size is larger than  the size of buffer passed to the method.
The fix below appears to resolve this issue, however, the potential side effects remain unknown.
 !screenshot-1.png!

- **dyingjiecai:** https://github.com/apache/kafka/pull/20117

## KAFKA-19473: The client does not throw RecordTooLargeException when the Record size exceeds max.partition.fetch.bytes
Bug · Open · Major · components: core · created 2025-07-04

When the Record size is greater than max.partition.fetch.bytes, the client does not fail with RecordTooLargeException, and then gets stuck consuming this message indefinitely.
!image-2025-07-05-00-54-23-657.png!
The fix below appears to resolve this issue, however, the potential side effects remain unknown.
 !screenshot-2.png!


## KAFKA-19474: Wrong placement of WARN log for truncation below HWM
Bug · Resolved (Fixed) · Major · components: core · created 2025-07-04 · resolved 2025-07-09

{{ReplicaFetcherThread#truncate}} has a useful [WARN log|https://github.com/apache/kafka/blob/da4fbba2793528e283458e080a690ad141857b0b/core/src/main/scala/kafka/server/ReplicaFetcherThread.scala#L171] when a follower is truncating its log segment below its HWM.
This is of particular help when debugging data loss scenarios like those described in the motivation for [KIP-966|https://cwiki.apache.org/confluence/display/KAFKA/KIP-966%3A+Eligible+Leader+Replicas].
Unfortunately, a refactoring in [P…

- **Rajani Karuturi:** created a PR https://github.com/apache/kafka/pull/20125 for the fix 
 Also added a test to test a scenario where HWM is changed

## KAFKA-19475: updateQuotaMetricConfigs could iterate through all metrics under a write lock
Improvement · Resolved (Invalid) · Major · created 2025-07-06 · resolved 2025-09-07

see the comment: https://github.com/apache/kafka/pull/19807#discussion_r2185848328

- **Chia-Ping Tsai:** we need the writelock to update both `overriddenQuotas` and `quota` together

## KAFKA-19476: Improve state transition handling in SharePartition
Sub-task · Resolved (Fixed) · Major · created 2025-07-06 · resolved 2025-08-02


## KAFKA-19579: Add missing metrics for document tiered storage
Task · Resolved (Fixed) · Minor · components: documentation · created 2025-08-04 · resolved 2025-08-05

Add missing metrics for document tiered storage
 * 
kafka.log.remote:type=RemoteLogManager,name=RemoteLogReaderFetchRateAndTimeMs：Introduced in [KIP-1018|https://cwiki.apache.org/confluence/display/KAFKA/KIP-1018%3A+Introduce+max+remote+fetch+timeout+config+for+DelayedRemoteFetch+requests]
 * 
kafka.server:type=DelayedRemoteListOffsetsMetrics,name=ExpiresPerSec,topic=([-.\w]+),partition=([0-9]+)：Introduced in [KIP-1075|https://cwiki.apache.org/confluence/display/KAFKA/KIP-1075%3A+Introduce+d…


## KAFKA-19580: Upgrade spotbug to 4.9.4
Improvement · Resolved (Fixed) · Minor · created 2025-08-05 · resolved 2025-08-10

see discussion https://github.com/apache/kafka/pull/20295#issuecomment-3146551515

- **xuanzhang gong:** hello,I will fix it
- **Stig Rohde Døssing:** I've raised https://github.com/apache/kafka/pull/20333 to fix this.
 [~gongxuanzhang] Sorry, I didn't notice your comment until now, I didn't mean to steal this issue, it just kind of happened since I did the previous spotbugs-related work too. Feel free to let me know if you have a better fix than…

## KAFKA-19581: Issues running Streams system tests on release candidates
Task · Open · Major · components: streams, system tests · created 2025-08-05

During release we now merge the RC tag into the release branch. This means the release branch has a real release number instead of <VERSION>-SNAPSHOT.
The Streams upgrade system tests expect <VERSION>-SNAPSHOT and thus fail to run.
We should either only merge RC tags once the vote pass or change the tests to use <VERSION> instead of <VERSION>-SNAPSHOT.
See:
- https://lists.apache.org/thread/v6873zlvp5bl9qf5zsr3g904nxdynr74
- https://lists.apache.org/thread/y3rh1nnxqz6tc4brnyfbpbrx2gy655y6


## KAFKA-19582: the current assignments shown by ReassignPartitionsCommand should include the log directories
Bug · Resolved (Fixed) · Major · created 2025-08-06 · resolved 2025-08-22

https://github.com/apache/kafka/blob/trunk/tools/src/main/java/org/apache/kafka/tools/reassign/ReassignPartitionsCommand.java#L572
https://github.com/apache/kafka/blob/trunk/tools/src/main/java/org/apache/kafka/tools/reassign/ReassignPartitionsCommand.java#L931
Since we always pass `Map.of`, the log directories are always treated as "any"


## KAFKA-19583: Native docker image fails to start when using SASL OAUTHBEARER mechanism
Sub-task · Resolved (Fixed) · Minor · components: docker · labels: native-image · created 2025-08-06 · resolved 2026-09-11

Running the native image with `KAFKA_SASL_ENABLED_MECHANISMS=OAUTHBEARER` results in an exception that prevents it starting:
[code/log omitted]
Here is a reproducer bash script:
[code/log omitted]
I guess some config is needed to avoid pruning out the reflectively instantiated class.
`./run-oauthbearer.sh kafka-native:4.0.0` and `./run-oauthbearer.sh kafka-native:4.1.0-rc2` fail with exception.
Running the same script with the main image works:
`./run-oauthbearer.sh kafka:4.0.0` or `./run…


## KAFKA-19584: Native docker image authentication fails with SASL PLAIN
Sub-task · Resolved (Fixed) · Minor · components: docker · labels: native-image · created 2025-08-06 · resolved 2026-07-21

I'm trying to use the native docker image for SASL PLAIN authentication.
The server starts okay but when I connect a client it emits an exception:
[code/log omitted]
Reproducer bash script:
[code/log omitted]
then to connect I use the producer script to try and send messages:
[code/log omitted]
For `./run-plain.sh kafka-native:4.0.0` and `./run-plain.sh kafka-native:4.1.0-rc2` the producer spins, trying repeatedly to reconnect
For the main image `./run-plain.sh kafka:4.0.0` and `./run-pl…

- **Stanislav Kozlovski:** [~gnarula] are you planning to work on this, or should we keep it unassigned?
 I'm hitting this same issue fwiw
- **Gaurav Narula:** Hi [~stanislavkozlovski]! I'm picking this up now. I suspect the issue is because some classes are missing from native image reachability metadata. Will update this ticket as I dig more

## KAFKA-19585: Avoid noisy NPE logs when closing consumer after constructor failures
Bug · Resolved (Fixed) · Minor · components: clients, consumer · created 2025-08-07 · resolved 2025-09-08

If there's a failure in the kafka consumer constructor, we attempt to close it https://github.com/lianetm/kafka/blob/2329def2ff9ca4f7b9426af159b6fa19a839dc4d/clients/src/main/java/org/apache/kafka/clients/consumer/internals/AsyncKafkaConsumer.java#L540
In that case, it could be the case that some components may have not been created, so we should consider some null checks to avoid noisy logs about NPE. 
This noisy logs have been reported with the console share consumer in a similar scenario, s…

- **Francis Godinho:** Hi [~lianetm], I'm new to contributing to Kafka and would be happy to take a stab at this. Can I assign this ticket to myself?
- **Lianet Magrans:** Hi [~francisgodinho]! Thanks for your interest! There is already someone from the team working on this :S 
 But stay on the lookout for new issue that we create, and also maybe check what's already out with minor/trivial complexity (ex. [this filter|https://issues.apache.org/jira/browse/KAFKA-15642?…

## KAFKA-19586: Kafka broker freezes and gets fenced during rolling restart with KRaft mode
Bug · Open · Blocker · components: core · created 2025-08-07

After upgrading our Kafka clusters to *Kafka 3.9.0* with *KRaft mode enabled* in production, we started observing strange behavior during rolling restarts of broker nodes — behavior we had never seen before.
When a broker is {*}gracefully shut down by the KRaft controller{*}, it immediately restarts. Shortly afterward, while it is busy {*}replicating missing data{*}, the broker suddenly {*}freezes for approximately 20–50 seconds{*}. During this time, it produces {*}no logs, no metrics{*}, and *…

- **Tal Asulin:** Sharing a 5m Flame graph profiling snapshot that was taken after a broker restart that experienced this exact issue - [^flame3.html].
 The Kafka cluster spec during the simulation was:
  * 12 Broker nodes
  * Using 8 vCPUs, 32G of RAM & 3.7TB local volume (im4gn.2xlarge AWS instances)
  * Disk utili…

## KAFKA-19587: Unify kraft shutdown logic in poll methods
Task · Open · Major · created 2025-08-07

Currently, different KRaft replica states handle polling during graceful shutdown differently. This Jira aims to unify their logic.


## KAFKA-19588: Reduce waiting for event completion in AsyncKafkaConsumer.poll()
Improvement · Resolved (Won't Do) · Major · components: clients, consumer · labels: async-kafka-consumer-performance, consumer-threading-refactor, performance · created 2025-08-08 · resolved 2025-09-17

We create—and wait on—{{{}PollEvent{}}} in {{Consumer.poll()}} to ensure we wait for reconciliation and/or auto-commit. However, reconciliation is relatively rare, and auto-commit only happens every _N_ seconds, so the remainder of the time, we should try to avoid sending poll events.


## KAFKA-19589: Check for ability to skip position validation in application thread when collecting buffered data
Improvement · Resolved (Fixed) · Major · components: clients, consumer · labels: async-kafka-consumer-performance, consumer-threading-refactor, performance · created 2025-08-08 · resolved 2025-11-27

We create—and wait on—validating positions in the background thread even though, in a stable system, 99.9%+ of the time there are no updates to perform.

- **Lianet Magrans:** Cherry-picked to 4.2 https://github.com/apache/kafka/commit/9ced615194aae5998a65a9626afdff04dc3760b9

## KAFKA-19658: Tweak org.apache.kafka.clients.consumer.OffsetAndMetadata
Improvement · Resolved (Fixed) · Minor · created 2025-08-31 · resolved 2025-09-04

1. Using `leaderEpoch=" + leaderEpoch` feels a bit odd, since not every value of `leaderEpoch` is invalid
2. `leaderEpoch=null` should be treated as same as `leaderEpoch=-1`, but `OffsetAndMetadata#equals` does not respect it.
3. `OffsetAndMetadata#metadata` currently has neither integration nor unit tests


## KAFKA-19659: Wrong generic type for UnregisterBrokerOptions
Bug · Resolved (Fixed) · Major · created 2025-09-01 · resolved 2025-09-05

This UnregisterBrokerOptions extends from the UpdateFeaturesOptions, which is obviously wrong.
[https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/clients/admin/UnregisterBrokerOptions.java#L23]
And that's why in KafkaAdminClientTest.java, we set timeout via `options.timeoutMs = 10;`. We should set it via timeoutMs(int) method gracefully like other tests.

- **Kuan Po Tseng:** [~showuon], can I take over this?
- **Luke Chen:** Thank you, [~brandboat] !
- **Chia-Ping Tsai:** great find

## KAFKA-19660: JoinWithIncompleteMetadataIntegrationTest fails in isolated run of one parameter
Sub-task · Resolved (Fixed) · Major · components: streams, unit tests · created 2025-09-01 · resolved 2025-09-10

When I run JoinWithIncompleteMetadataIntegrationTest, with only the new protocol enabled, it fails (since it does not run long enough for the exception to be triggered by the timer).
When the test is run for both protocols, the second run passes because it uses an existing group ID and that is why it why streams is shutting down.


## KAFKA-19661: Streams groups sometimes describe as NOT_READY when STABLE
Sub-task · Resolved (Fixed) · Major · created 2025-09-01 · resolved 2025-10-14

Streams groups sometimes describe as NOT_READY when STABLE. That is, the group is configured and all topics exist, but when you use LIST_GROUP and STREAMS_GROUP_DESCRIBE, the group will show up as not ready.
The root cause seems to be that [https://github.com/apache/kafka/pull/19802] moved the creation of the soft state configured topology from the replay path to the heartbeat. This way, LIST_GROUP and STREAMS_GROUP_DESCRIBE, which show the snapshot of the last committed offset, may not show th…

- **Jimmy Wang:** Hi [~lucasbru] , if you haven't start to handle this issue yet, maybe I could help. :)

## KAFKA-19662: Support resetting offsets in kafka-share-groups.sh for topics which are not currently subscribed
Sub-task · Resolved (Fixed) · Major · components: tools · created 2025-09-01 · resolved 2025-10-23

The kafka-share-groups.sh tool can be used to reset the start offset for consumption if the share group is empty. One use for this is to initialise the start offset before starting to use the share group. Currently, the tool only lets the user reset the start offset for a topic which already has offsets in the share group. Instead, it should permit setting the SPSO for any topic, subject to auth checking.
This brings the tool's behaviour in line with kafka-consumer-groups.sh.


## KAFKA-19663: kafka-broker-api tool should support to get controller api version
New Feature · Resolved (Fixed) · Major · labels: need-kip · created 2025-09-02 · resolved 2026-07-16

like tool kafka-broker-api-versions.sh, we can get all RPC version from broker.
It should also support for controller.
KIP: [https://cwiki.apache.org/confluence/display/KAFKA/KIP-1220%3A+kafka-broker-api-versions+tool+support+bootstrap+controllers]

- **Andrew Schofield:** I've been meaning to do this for a while. Please fix this. When adding new APIs and testing the upgrades, this would be a really useful tool.
- **TaiJuWu:** I will prepare KIP ASAP.
- **Chia-Ping Tsai:** If all we want is to list the RPC versions of the "voters", this can be done with `DescribeQuorumRequest`. That means we don't need a KIP to support `bootstrap.controller`. By contrast, we would need a KIP if we wanted to list all the RPCs of "observers"
 [~taijuwu] [~schofielaj] WDYT?
- **TaiJuWu:** If we don't need all controllers including observers, that is good enough.
 But there is another benefit if we have KIP is we can align the tool usage like [https://cwiki.apache.org/confluence/display/KAFKA/KIP-1147%3A+Improve+consistency+of+command-line+arguments]
- **Andrew Schofield:** I *think* this needs a KIP really. When I played around with this before using a cluster with separate controllers and brokers, I was not able to use `kafka-broker-api-versions` with the controller because the tool uses APIs which the controller does not support (or that was my guess anyway).{*}{*}
- _…3 more comments_

## KAFKA-19664: Support building with Java 25 (LTS release)
Improvement · Resolved (Fixed) · Major · components: build · labels: CI, CI/CD, Gradle, Java, Java25, Scala, build, github-actions, gradle, java, scala, update, upgrade · created 2025-09-02 · resolved 2025-10-08

*Depends upon/blocked by:*
 * Kafka ticket: KAFKA-19174 Gradle version upgrade 8 -->> 9 (review is under way)
 * Spotbugs next version:
 ** [https://github.com/spotbugs/spotbugs/issues/3564]
 ** [https://github.com/spotbugs/spotbugs/issues/3569]
 ** https://issues.apache.org/jira/browse/BCEL-377 
 ** [https://github.com/spotbugs/spotbugs/pull/3712]
 ** [https://github.com/spotbugs/spotbugs/discussions/3380] 
*Related links:*
 * JDK 25 release date: September 16th 2025:
 ** [https://mai…

- **Dejan Stojadinović:** Update: *Mockito* version needs to be upgraded to resolve build issues (see the output of *_./gradlew test_* below).
 *Related links:*
  * https://issues.apache.org/jira/browse/SOLR-17718
  * [https://github.com/mockito/mockito/issues/3647]
  * [https://github.com/mockito/mockito/releases/tag/v5.20.…
- **Dejan Stojadinović:** *Small update:*
  * Gradle version upgrade (8.14.3 -->> 9.1.0) will hopefully end up in trunk in the next few days
  * It seems that Apache *{{commons-bcel}}* will release Java 25 compatible version soon enough - this is important for us because SpotBugs Java 25 compatible versions will follow immed…
- **Dejan Stojadinović:** *Update:*
 * A few of the tests are failing with Java 25 (x)
 * ticket is created here: KAFKA-19769 (i)
- **Dejan Stojadinović:** Solution has been merged into a trunk: [https://github.com/apache/kafka/commit/ede6c90dfb5fa5faa7472541dde3bcc90cbd68d3] :D
 Follow-up ticket is created here: KAFKA-19771

## KAFKA-19665: Remove waiting for event completion in AsyncKafkaConsumer.pollForRecords()
Improvement · Resolved (Won't Fix) · Major · components: clients, consumer · labels: async-kafka-consumer-performance, consumer-threading-refactor, performance · created 2025-09-02 · resolved 2026-02-24

We create—and wait on—{{{}CreateFetchRequestEvent{}}}s in {{{}AsyncKafkaConsumer.pollForRecords(){}}}. The inter-thread communication involved in sending the event, notifying the event future, and blocking on the event future results in high CPU usage. Investigate if it is possible to reduce/eliminate the need for the event future.


## KAFKA-19666: Clean up integration tests related to state-updater
Sub-task · Resolved (Resolved) · Blocker · components: streams, unit tests · created 2025-09-02 · resolved 2025-09-12

This is the first step in the parent task: To clean up all the integration tests related to state-updater flag
See [https://github.com/apache/kafka/pull/20392#issuecomment-3240659815] for more details


## KAFKA-19667: Close ShareConsumer in ShareConsumerPerformance only after metrics displayed
Sub-task · Resolved (Fixed) · Major · created 2025-09-03 · resolved 2025-09-04

This is a peer of https://issues.apache.org/jira/browse/KAFKA-19564.
Essentially, it's not reliable to access the metrics from the share consumer once it has been closed, and this tool does precisely that. As a result, it prints a truncated list of metrics.


## KAFKA-19668: processValues() must be declared as value-changing operation
Bug · Resolved (Fixed) · Blocker · components: streams · created 2025-09-03 · resolved 2025-09-08

When adding `KStreams#processValues()` we missed to declare the operation as "value changing". This can lead to an "incorrectly" built topology.
The main problem is, that `processValues()` is the replacement of `transformValues()` which we removed with AK 4.0.0 release. Thus, if users rewrite existing programs from `transformValues()` to the new `processValues()` (what will be required when upgrading to 4.x release), they might observe this change as a regression.
The impact of the changed top…

- **Matthias J. Sax:** Do not break backward compatibility, we decided to not enable this fix by default in AK 4.0.1 and 4.1.1 releases, and will do some follow up work for AK 4.2.0 for allow us to enable the fix by default there.
- **ASF GitHub Bot:** mjsax opened a new pull request, #721: URL: https://github.com/apache/kafka-site/pull/721    (no comment)
- **ASF GitHub Bot:** mjsax commented on code in PR #721: URL: https://github.com/apache/kafka-site/pull/721#discussion_r2331305729 ########## 33/streams/developer-guide/dsl-api.html: ########## @@ -3496,6 +3496,9 @@ <h5><a class="toc-backref" href="#id34">KTable-KTable Foreign-Key                      </tr>…
- **ASF GitHub Bot:** mjsax merged PR #721: URL: https://github.com/apache/kafka-site/pull/721
- **Matthias J. Sax:** While we mark this ticket as resolved for AK 4.2.0 release, we also need a follow up for a cleaner fix. Filed https://issues.apache.org/jira/browse/KAFKA-19688 for AK 4.2.0 follow up work.

## KAFKA-19683: Clean up TaskManagerTest
Sub-task · Resolved (Resolved) · Blocker · components: streams, unit tests · created 2025-09-07 · resolved 2025-12-02

See https://github.com/apache/kafka/pull/20392#issuecomment-3241457533

- **Shashank:** Hi [~lucasbru], since the tests in the cleanup of this file are many, I would like to propose to make incremental changes to this cleanup.
 - Removal of dead tests and address these 3 comments - [#1|https://github.com/apache/kafka/pull/19275#discussion_r2107811068], [#2|https://github.com/apache/kaf…
- **sanghyeok An:** I think, after this tickets are resolved, https://issues.apache.org/jira/browse/KAFKA-12569 can be resolved as well.
- **Shashank:** You're right! Thank you [~chickenchickenlove]

## KAFKA-19684: Move Gauge#value to MetricValueProvider
Improvement · Resolved (Fixed) · Minor · labels: need-kip · created 2025-09-07 · resolved 2025-10-04

from: https://github.com/apache/kafka/pull/3705#discussion_r140830112

- **Chia-Ping Tsai:** the main benefit is to remove the type check from `KafkaMetric`
 [code/log omitted]
 [code/log omitted]
 Also, the following code could be removed
 [code/log omitted]
- **Chia-Ping Tsai:** we may need to keep the method in `Guave` to avoid possible compatibility issue (see KAFKA-6174)

## KAFKA-19685: Revoked partitions are included in currentOffsets passed to preCommit on task stop
Bug · Open · Minor · components: connect · created 2025-09-08

When a task stops, [{{WorkerSinkTask#closeAllPartitions()}}|https://github.com/apache/kafka/blob/84caaa6e9da06435411510a81fa321d4f99c351f/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSinkTask.java#L664] runs and the [task’s {{preCommit}} is invoked|https://github.com/apache/kafka/blob/3c7f99ad31397a6a7a4975d058891f236f37d02d/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSinkTask.java#L444]. At that time, the {{currentOffsets}} argument may include {…

- **Guang Zhao:** Added clarification in https://github.com/apache/kafka/pull/20756.

## KAFKA-19686: Trigger Docker image builds in release script
Task · Resolved (Fixed) · Major · components: build · created 2025-09-08 · resolved 2026-07-27

In the release process, you release manager has to manually trigger the Docker Build Test Workflow for both the jvm and native images ([https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=34840886#ReleaseProcess-CreateJVMApacheKafkaDockerArtifacts(Forversions>=3.7.0)|https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=34840886#ReleaseProcess-CreateJVMApacheKafkaDockerArtifacts(Forversions>=3.7.0)]).
The release script could trigger these jobs automatically using the Gi…

- **Muralidhar Basani:** [~mimaison] can someone help me in reviewing this ? Perhaps [~davidarthur]  ?

## KAFKA-19687: MetaDataShell log error message for SNAPSHOT_HEADER and SNAPSHOT_FOOTER
Improvement · Open · Minor · created 2025-09-08

```
./bin/kafka-metadata-shell.sh -s /tmp/kafka-meta/bootstrap.checkpoint
17:31:43 Loading...
[2025-09-08 17:32:19,271] ERROR Ignoring control record with type SNAPSHOT_HEADER at offset 0 (org.apache.kafka.metadata.util.SnapshotFileReader)
[2025-09-08 17:32:19,274] ERROR Ignoring control record with type SNAPSHOT_FOOTER at offset 5 (org.apache.kafka.metadata.util.SnapshotFileReader) Starting...
```


## KAFKA-19688: Provide clean upgrade path from transformValues to processValues
Improvement · Open · Critical · components: streams · labels: needs-kip · created 2025-09-08

This ticket is a follow up to https://issues.apache.org/jira/browse/KAFKA-19668
With K19668, we introduced some "hot fix", that is actually disabled by default for backward compatibility reasons. A cleaner fix (which required a KIP, and thus cannot go into a bug-fix release), would be to add a new overload of `processValues()` which has the fix enabled, and deprecate the existing `processValues()` methods.

- **Mickael Maison:** Moving to the next release as we're now in code freeze for 4.3.0.
- **TengYao Chi:** as offline discussion, I will take over this one.
- **Omnia Ibrahim:** Moving to 4.5 as we're now in code freeze for 4.4.0

## KAFKA-19689: TopologyTestDriver spends most of its time forcing changes to disk with persistent state stores
Improvement · Resolved (Invalid) · Minor · components: streams-test-utils · created 2025-09-08 · resolved 2025-09-08

We are using TopologyTestDriver 
It looks like the test driver is syncing the entire state directory to disk for every record processed:
!image-2025-09-08-14-07-05-768.png!

- **Steven Schlansker:** I apologize, this was actually a correlated change on our end, not a regression in Kafka Streams.

## KAFKA-19690: Unexpected Fatal error InvalidTxnStateException on Kafka Streams (KIP-890)
Bug · Resolved (Fixed) · Major · components: core, streams · created 2025-09-08 · resolved 2025-10-06

We are seeing cases where a Kafka Streams (KS) thread stalls for ~20 seconds, resulting in a visible gap in the logs. During this stall, the broker correctly aborts the open transaction (triggered by the 10-second transaction timeout). So far, this is expected behavior. However, when the KS thread resumes, instead of receiving the expected InvalidProducerEpochException (which we already handle gracefully as part of transaction abort), the client is instead hit with an InvalidTxnStateException. K…

- **Chia-Ping Tsai:** 3.9: https://github.com/apache/kafka/commit/4dd35126656e2af2ff3cd67705d1dd495f68c0ec
 trunk: https://github.com/apache/kafka/commit/0a483618b9cc169a0f923478812141630baf2a4c
- **Chia-Ping Tsai:** 4.1: https://github.com/apache/kafka/commit/a10c1f3ea1454dbd644ea65a885c965529e1d37d
- **Chia-Ping Tsai:** 4.0: https://github.com/apache/kafka/commit/4b0ba424837a76c94b2432f6e2ac4237f92e1ff7

## KAFKA-19691: Add metrics corresponding to consumer rebalance listener metrics
Improvement · Resolved (Fixed) · Major · components: streams · labels: kip · created 2025-09-09 · resolved 2025-10-22

The consumer provides metrics for execution of the consumer rebalance listener:
 * Consumer PartitionsLost Latency
 * Consumer PartitionsAssigned Latency
 * Consumer PartitionsRevoked Latency
It would be useful for the StreamsRebalanceListener to replicate semilar metrics for TasksLost, TasksAssigned and TasksRevoked.


## KAFKA-19692: improve the docs of "clusterId" for AddRaftVoterOptions and RemoveRaftVoterOptions
Improvement · Resolved (Fixed) · Minor · created 2025-09-09 · resolved 2025-09-30

1. The cluster id is optional, but users are not aware of its purpose
2. the RPC documentation is also missing
3. there are no integration tests


## KAFKA-19693: Introduce PersisterBatch in SharePartition
Sub-task · Resolved (Fixed) · Major · created 2025-09-09 · resolved 2025-09-10


## KAFKA-19794: MirrorCheckpointTask causes consumers on target cluster to rewind offsets or skip messages due to erroneous offset commits
Bug · Open · Major · components: mirrormaker · created 2025-10-15

h2. *Description*
The MirrorCheckpointTask in Mirror Maker 2 commits offsets for active consumer groups on the target cluster, causing consumers to rewind their offsets or skip messages. Typically brokers prevent committing offsets for consumer groups that are not in `EMPTY` state by throwing {{{}UnknownMemberIdException{}}}. In addition, {{MirrorCheckpointTask}} has logic in place to prevent committing offsets older than target for {{EMPTY}} consumer groups. However, due to a bug in {{MirrorCh…


## KAFKA-19795: Mark the minOneMessage as false when delayedRemoteFetch is present in the first partition
Task · Resolved (Fixed) · Major · created 2025-10-16 · resolved 2025-10-16


## KAFKA-19796: Introduce computations for inFlightTerminalRecords
Sub-task · Resolved (Fixed) · Minor · created 2025-10-16 · resolved 2025-10-29


## KAFKA-19797: Implement deliveryCompleteCount in writeShareGroupStateRPC
Sub-task · Resolved (Fixed) · Minor · created 2025-10-16 · resolved 2025-11-03


## KAFKA-19798: Persist deliveryCompleteCount in ShareSnapshot and ShareUpdate records
Sub-task · Resolved (Fixed) · Minor · created 2025-10-16 · resolved 2025-11-03


## KAFKA-19799: Introduce deliveryCompleteCount in ReadShareGroupStateSummary
Sub-task · Resolved (Fixed) · Minor · created 2025-10-16 · resolved 2025-11-04


## KAFKA-19800: Compute share partition lag in GroupCoordinatorService
Sub-task · Resolved (Fixed) · Minor · created 2025-10-16 · resolved 2025-11-17


## KAFKA-19801: Introduce deliveryCompleteCount in DescribeShareGroupStateOffsets
Sub-task · Resolved (Fixed) · Minor · created 2025-10-16 · resolved 2025-11-17


## KAFKA-19802: Update ShareGroupCommand to use share partition lag information
Sub-task · Resolved (Fixed) · Minor · created 2025-10-16 · resolved 2025-11-04


## KAFKA-19803: Relax state directory file system restrictions
Improvement · Resolved (Fixed) · Minor · components: streams · labels: kip · created 2025-10-16 · resolved 2025-10-25

The implementation of permission restriction by https://issues.apache.org/jira/browse/KAFKA-10705 is very restrictive on groups. Existing group write permissions should be kept.
We could also make this configurable, which would require a KIP.
KIP-1230 [https://cwiki.apache.org/confluence/display/KAFKA/KIP-1230%3A+Add+config+for+file+system+permissions]


## KAFKA-19804: Improve heartbeat request manager initial HB interval 
Task · Open · Major · components: clients, consumer · created 2025-10-16

With KIP-848, consumer HB interval config moved to the broker, so currently, the consumer HB request manager starts with a 0ms interval (mainly to send a first HB right away after the consumer subscribe + poll). Once a response is received, the consumer takes the interval from the response and starts using it. 
That 0ms initial interval makes that the HB mgr poll continuously executes logic on a tight loop that may not really be needed. It mostly has to wait for a response (or a failure).
Prob…

- **Kuan Po Tseng:** [~lianetm], are you planning to work on this issue? If not, I’d be happy to take it over. Thanks!
- **Lianet Magrans:** Sure, feel free to take it and I can help with reviews. Thanks for your help!
- **Arpit Goyal:** [~brandboat]  It seems you are already working on other issues .Can i take this up ? .It would be my first hand on the new consumer group protocol.
- **Kuan Po Tseng:** [~goyarpit] Thanks for checking! I’ve already started exploring this one. If you are interested, you can help review once I have a PR ready.
- **Kuan Po Tseng:** Hi [~lianetm],
 I took a closer look at this issue and wanted to share a few thoughts.
 {quote}That 0 ms initial interval causes the HB manager poll to run continuously in a tight loop, executing logic that may not really be needed—it mostly just waits for a response or failure.
 {quote}
 This actua…
- _…5 more comments_

## KAFKA-19821: Duplicated batches should be logged
Improvement · Resolved (Fixed) · Major · created 2025-10-22 · resolved 2025-10-22

When writing records with idempotent producer, the broker can help de-duplicate records. But when records being de-duplicated, there is no log in the broker side. This will confuse the producer because the records sent going to nowhere. Sometimes it's caused by the buggy producer that keeps using the wrong sequence number to cause the duplicated records. We should at least log the duplicated records info instead of pretending nothing happened.


## KAFKA-19822: Remove all static classes in Field except TaggedFieldsSection
Improvement · Resolved (Fixed) · Major · components: clients · created 2025-10-22 · resolved 2025-11-05

All static classes in Field except TaggedFieldsSection are not really being used. We should remove them.


## KAFKA-19823: PartitionMaxBytesStrategy bug when request bytes is lesser than acquired topic partitions
Sub-task · Resolved (Fixed) · Major · created 2025-10-22 · resolved 2025-10-27

There is a bug in the broker logic of splitting bytes in {{PartitionMaxBytesStrategy.java}} due to which we are setting {{partitionMaxBytes}} as 0 in case requestMaxBytes is lesser than 
acquiredPartitionsSize


## KAFKA-19824: New ConnectorClientConfigOverridePolicy with allowlist of configurations
New Feature · Resolved (Fixed) · Major · created 2025-10-22 · resolved 2025-10-28

Jira for KIP-1188: https://cwiki.apache.org/confluence/x/2IkvFg


## KAFKA-19825: KIP-1224: Add batch-linger-time and batch-flush-time metrics
Sub-task · Resolved (Fixed) · Minor · components: group-coordinator · created 2025-10-22 · resolved 2025-11-14


## KAFKA-19826: KIP-1224: Implement adaptive append.linger.ms for the group coordinator and share coordinator
Sub-task · Resolved (Fixed) · Minor · components: group-coordinator · created 2025-10-22 · resolved 2025-11-14

Add a new allowed value for group.coordinator.append.linger.ms and share.coordinator.append.linger.ms of -1.
When append.linger.ms is set to -1, use the flush strategy outlined in the KIP.


## KAFKA-19827: Call acknowledgement commit callback at end of waiting calls
Sub-task · Resolved (Fixed) · Major · components: clients · created 2025-10-22 · resolved 2025-10-24

The acknowledgement commit callback in the share consumer gets called on the application thread at the start of the poll, commitSync and commitAsync methods. Specifically in the peculiar case of using the callback together with commitSync, the acknowledgement callback for the committed records is called at the start of the next eligible call, even though the information is already known at the end of the commitSync's execution. The results are correct already, but the timing could be improved in…


## KAFKA-19828: Intermittent test failures when using chained emit strategy on window close
Bug · Open · Major · components: streams · created 2025-10-23

Hi,
I have a test case that contains a topology with 2 time windows and chained emitStrategy calls. The standalone reproduction use case is attached to this issue
The problem is that about 25% of the time the test fails. About 75% of the time the test succeeds. I followed the conclusions of 
!https://issues.apache.org/jira/secure/viewavatar?size=xsmall&avatarId=21133&avatarType=issuetype|width=16,height=16! KAFKA-19810
to make sure that I am sending events at the correct times (at least I th…

- **Greg F:** Most of the time I run the test, I see this:
 [INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.880 s – in com.k8sflowprocessor.ChainedEmitStrategyTopologyTest3
 [INFO] 
 [INFO] Results:
 [INFO] 
 [INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
 [INFO] 
 However, like…
- **Greg F:** the goal, of course, is to have unit test that is reliable, i.e. doesn't fail intermittently. I need to understand whether the issue is in my test code (attached) or elsewhere in kafka test framework.
- **Greg F:** I run the test in a loop in a shell script like this:
 #!/bin/bash
 set -e
 for i in \{1..100}; do
   echo ========================================================
   echo ======================== $i ============================
   echo ========================================================
   mvn…
- **Greg F:** @[~mjsax] ^^^^
- **Matthias J. Sax:** I am not sure – did spend some time but don't understand yet what's happening. It could be a bug in Kafka Streams. Needs more investigation.
- _…5 more comments_

## KAFKA-19829: Implement group-level initial rebalance delay
Improvement · Resolved (Fixed) · Major · components: streams · created 2025-10-23 · resolved 2025-11-18

During testing, an artifact of the new rebalance protocol showed up. In some cases, the first joining member gets all active tasks assigned, and is slow to revoke the tasks after more member has joined the group. This affects in particular cases where the first member is slow (possibly overloaded in the case of cloudlimits benchmarks) and there are a lot of tasks to be assigned.
To help with this situation, we want to introduce a new group-specific configuration to delay the initial rebalance.


## KAFKA-19830: Refactor KafkaRaftClient to use event scheduler framework
Improvement · Open · Major · created 2025-10-23


## KAFKA-19831: Failures in the StateUpdater thread may lead to inability to shut down a stream thread
Bug · Resolved (Fixed) · Major · components: streams · created 2025-10-23 · resolved 2025-11-21

If during rebalance a failure occurs in the StateUpdater thread, and this failure leads to the thread shutdown, the Stream thread may get into an infinite wait state during it's shutdown.
See the attached test that reproduces the issue.

- **Arpit Goyal:** Hi [~nikita-shupletsov]  if you have not started ,can i pick this up ?
- **Nikita Shupletsov:** Hi [~goyarpit] 
 I am already working on it.
 I will let you know if I need help. thanks!

## KAFKA-19936: ReplicaManager counts duplicated records to BytesInPerSec and MessagesInPerSec metric
Bug · In Progress · Major · created 2025-11-28

For an idempotent producer, duplicated records are not written to disk; however, they still contribute to the {{BytesInPerSec}} and {{MessagesInPerSec}} metrics.
1. If the records are duplicated, UnifiedLog skips these messages.
[https://github.com/apache/kafka/blob/d27d90ccb3b2b98e02de42afd50910fbbbc162d0/storage/src/main/java/org/apache/kafka/storage/internals/log/UnifiedLog.java#L1221-L1234]
2. ReplicaManager counts result from Partition#appendRecordsToLeader to metrics.
[https://github.c…

- **PoAn Yang:** This test case cannot pass in trunk branch, because ReplicaManager counts duplicated records to metrics.
 [code/log omitted]
- **Luke Chen:** Question: Does the MessagesInPerSec and BytesInPerSec count for the corrupted records?
- **PoAn Yang:** For corrupted records, do you mean records which cannot pass validator and throw CorruptRecordException? These records doesn't contribute to metrics and will get into this catch.
 [https://github.com/apache/kafka/blob/d27d90ccb3b2b98e02de42afd50910fbbbc162d0/core/src/main/scala/kafka/server/ReplicaM…
- **Luke Chen:** OK, thanks. I just want to confirm the definition of these 2 metrics. Does it mean "the data enter the broker" or "the data enter the disk"? It looks like we only count it when data enter the disk. So this issue is valid. Thank you.

## KAFKA-19937: Use the same reaper thread in Persister as well as NetworkPartitionMetadataClient
Sub-task · Resolved (Fixed) · Major · created 2025-11-28 · resolved 2026-04-28

- **Rion Williams:** I'm happy to take this task if available. 
 I'd imagine we'd want to simply create a new sharable, standalone `ReaperThread` class that could easily be shared between both of these components. We could also allow the existing `SystemTimerReaper` class to accept and optionally own/manage the thread i…
- **Andrew Schofield:** [~rionmonster] Are you still interested in taking this task?
- **Rion Williams:** [~schofielaj]
 Sure! I think I have a branch stashed away somewhere where I was experimenting with one of the approaches above. Feel free to assign it to me and I’ll revisit it.
- **Andrew Schofield:** Thank you.
- **Rion Williams:** [~schofielaj] 
 I've gone ahead and [put together a PR|https://github.com/apache/kafka/pull/21842] that takes the approach detailed earlier in the thread (e.g. extracted previously nested ReaperThread into its own class and extended an instance to be passed into SystemTimerReaper to support sharing)…

## KAFKA-19938: KafkaClusterTestKit not formatting all log directories on combined noes
Bug · Resolved (Fixed) · Major · created 2025-11-28 · resolved 2025-12-03

If I create a cluster via KafkaClusterTestKit with combined nodes and multiple log directories, the log directories that does not host the metadata log are not formatted.
For example:
[code/log omitted]
I get the following:
[code/log omitted]
we can see the combined_0_1 directory has not been formatted, we don't have a meta.properties file.
If I run
[code/log omitted]
With log.dirs=/tmp/kraft-controller-logs,/tmp/kraft-controller-logs in controller.properties, the 2 log directories are c…


## KAFKA-19939: ProductionExceptionHandler not supported on global thread
Improvement · Resolved (Fixed) · Major · components: streams · created 2025-11-28 · resolved 2026-03-08

Follow up to https://issues.apache.org/jira/browse/KAFKA-19930
We should look into making the ProcessingExceptionHandler, and DLQ work for the global thread, too (DLQ tracked via https://issues.apache.org/jira/browse/KAFKA-20280)
Depending on how we do this, this might require a KIP, as we might need to add a new producer to the global thread to support DLQ. An alternative could be, to explicitly exclude DLQ.
For this work, we also need to make sure the restore path works, which would read fr…

- **Arpit Goyal:** [~mjsax]  Can i pick this up
- **Arpit Goyal:** https://github.com/apache/kafka/pull/21535
- **Arpit Goyal:** We will implement support for DLQ in a separate ticket.
- **Matthias J. Sax:** I just filed https://issues.apache.org/jira/browse/KAFKA-20280 for DLQ support, so we can close this one.

## KAFKA-19940: Reduce the log4j2 cpu usage in PersisterStateManager
Bug · Resolved (Fixed) · Blocker · created 2025-11-29 · resolved 2025-12-17

see https://github.com/apache/kafka/pull/20175/files#r2572693459

- **Chia-Ping Tsai:** trunk: https://github.com/apache/kafka/commit/a2eae88a2293ad18e902dcc0abb3bb30b16272b9
 4.2: https://github.com/apache/kafka/commit/7ae882623a0b006c99e58c756f7cddbc5a89ff49

## KAFKA-19941: Tidy up the output of `kafka-features.sh`
Improvement · Resolved (Fixed) · Minor · created 2025-11-29 · resolved 2025-12-08

Feature: eligible.leader.replicas.version	SupportedMinVersion: 0	SupportedMaxVersion: 1	FinalizedVersionLevel: 0	Epoch: 408
Feature: group.version	SupportedMinVersion: 0	SupportedMaxVersion: 1	FinalizedVersionLevel: 0	Epoch: 408
Feature: kraft.version	SupportedMinVersion: 0	SupportedMaxVersion: 1	FinalizedVersionLevel: 1	Epoch: 408
Feature: metadata.version	SupportedMinVersion: 3.3-IV3	SupportedMaxVersion: 4.3-IV0	FinalizedVersionLevel: 3.9-IV0	Epoch: 408
Feature: share.version	SupportedMinV…

- **Rion Williams:** I'd be interested in taking this if we elect to make a change. I'm not certain if more tabs would be the answer in terms of improving readability. A few options that come to mind off the top of my head would be:
 *Indentation Approach*
 [code/log omitted]
 *Table Approach*
 [code/log omitted]
 The p…
- **Chia-Ping Tsai:** [~rionmonster] Thanks for the feedback. I think a new configuration is overkill and it requires a KIP. I don't recall us having a specific rule for compatibility of console output. Let's start a thread on the dev channel for further feedback
- **Chia-Ping Tsai:** discussion: https://lists.apache.org/thread/jwcn88o4f4c19x1onymxmkddk3dcsckf
- **Rion Williams:** [~chia7712] 
 Totally makes sense!
- **Chia-Ping Tsai:** [~rionmonster] I assume you are already aware of the conclusion. Please take over this JIRA ticket, and feel free to ping me when you have a patch
- _…3 more comments_

## KAFKA-19942: Clean up StreamThread and StoreChangelogReader Test
Sub-task · Resolved (Resolved) · Blocker · components: streams, unit tests · created 2025-11-30 · resolved 2025-12-02

Clean up StreamThreadTest.java and StoreChangelogReaderTest.java to always use StateUpdater.
We also update the config to always have stateupdater enabled.


## KAFKA-19943: Stale values in State Store after tombstone was compacted
Bug · Resolved (Fixed) · Major · components: streams · labels: KIP · created 2025-11-30 · resolved 2026-03-09

h3. *Proposed solution*
*KIP:* [KIP-1259|https://cwiki.apache.org/confluence/display/KAFKA/KIP-1259%3A+Add+configuration+to+wipe+Kafka+Streams+local+state+on+startup]
Add new property to remove local files when starting app
h3. *Summary*
When a Kafka Streams application with a local *state store* (backed by RocksDB) restarts after a period exceeding the changelog topic's {*}{{delete.retention.ms}}{*}, it can lead to previously deleted entities "magically" reappearing. This happens because th…

- **Uladzislau Blok:** [~mjsax] [~lucasbru] We've run into an issue with state store recovery after failover. Are either of you aware of this specific behavior?
- **Matthias J. Sax:** This is a known issue. The root cause is the mixing of wall-clock time and event-time semantics. Kafka Streams expires data in windowed stores only base on stream-time (what is IMHO correct). The broker uses a weird mix of event-time and wall-clock time though, comparing a records timestamp to it's…
- **Uladzislau Blok:** Thanks for the response. AFAIU StreamsConfig#windowstore.changelog.additional.retention.ms is related to window store only. In this case we're using just key value store (Created manually and accessed from custom Processor). How can we address this issue then? Use window store every time as a work a…
- **Matthias J. Sax:** If you are using a KV-store, there should not be any retention time, but the changelog topic should be configured with compaction, which ensures that no matter how old a record gets, it's not deleted as long as it's the newest for a key.
 Kafka Streams should create the topic for you with the right…
- **Uladzislau Blok:** I'm talking about {*}_delete.retention.ms_{*}, so retention time of *tombstones*
 We have compacted chanelog topic created by KS with default *_delete.retention.ms_* (1 day). The issue is *not that we lost live entities, but removed entities become available* after fail-over to second k8s cluster. T…
- _…11 more comments_

## KAFKA-19944: Share group offset information following topic deletion is untidy
Improvement · Resolved (Fixed) · Minor · components: tools · created 2025-11-30 · resolved 2025-12-03

When a topic which had been consumed in a share group is deleted, the output from kafka-share-groups.sh --describe --offsets displays an empty table consisting of only a header, rather than a more helpful message like "Share group SG1 has no offset information.". The code works correctly, but the output could be nicer.


## KAFKA-19945: StreamsGroupHearbeat response should always set the status
Sub-task · Resolved (Fixed) · Major · components: streams · created 2025-12-01 · resolved 2025-12-05

The status field should always set in the response, even when empty, to ensure that the status gets reset on the client.
We are not doing this due to an oversight - it is defined as nullable, and is null when not set. So status does not clear correctly on the client, which ignores the field if it's null. 
This mostly has no effect, since we are logging the status, but it is still confusing.


## KAFKA-19946: Reduce unnecessary work in share session handler
Improvement · Resolved (Fixed) · Minor · components: clients · created 2025-12-01 · resolved 2025-12-03

The share session handler does a lot of work to keep track of the share session topic-partitions. In some cases, this can be avoided.


## KAFKA-19994: TaskManager may not close all tasks on task timeouts
Bug · Resolved (Fixed) · Blocker · components: streams · created 2025-12-15 · resolved 2025-12-16

When a {{TimeoutException}} occurs while trying to put multiple active tasks back into running, we will add the timed out task back to the state updater, so that it gets properly closed during unclean shutdown of the thread.
However, if we run into a Task timeout (failing to make progress for a long time), we will rethrow a StreamsException wrapping the TimeoutException we have drained multiple tasks from the state updater, they will be lost, and not added back to the state updater, and therefo…


## KAFKA-19995: Record copy lag metrics during failures
Task · Resolved (Fixed) · Major · components: Tiered-Storage · created 2025-12-15 · resolved 2025-12-18

When tiered storage segment copies are failing with
any outer-level exception, the RemoteCopyLagBytes
and RemoteCopyLagSegments metrics are not emitted. This makes it
impossible to detect growing lag during copy failures.


## KAFKA-19996: The conflicts between ExpandIsr and ShrinkIsr
Bug · Patch Available · Major · created 2025-12-15

Thanks to [~mjd95] to report the following issue.
In the Partition.scala, the condition for the ISR expand and shrink does not match, which can cause a follower flapping in and out of ISR when:
 # The partition is under min-isr which means the HWM can't advance.
 # The replication is slow.
 # The follower is far behind the LEO, but it is at/above the HWM.
Due to the "conflict" between the ISR expand and shrink:
 * Shrink ISR, attempted on a schedule, triggers if the follower's LEO has not…

- **Yunseop Eom:** PR opened: https://github.com/apache/kafka/pull/23024
 Prevented premature ISR expansion under min ISR by requiring the follower to satisfy the existing caught-up check, while preserving leader-epoch expansion when the partition is not under min ISR. Added regression coverage for a follower that rea…
- **Yunseop Eom:** Update on PR #23024: https://github.com/apache/kafka/pull/23024
 The PR requires the existing caught-up check before expanding ISR while a partition is under min ISR, preventing a follower with only a stale high watermark from entering ISR prematurely. The non-min-ISR leader-epoch behavior is preser…
- **Yunseop Eom:** PR #23024 is open and ready for maintainer review: https://github.com/apache/kafka/pull/23024

## KAFKA-19997: Improve handling and visibility of invalid dynamic configurations
Improvement · Open · Major · labels: need-kip · created 2025-12-16

from: https://github.com/apache/kafka/pull/20334#discussion_r2621722784
Warning messages for invalid dynamic configurations are easily overlooked and difficult to monitor. Therefore, I propose two improvements: 
1) introduce a new configuration, "dynamic.config.failure.policy ", to allow users to halt the server upon validation failure if desired 
2) add a new metric, `InvalidConfigCount`, to expose the invalid configurations via JMX

- **Jimmy Wang:** Hi [~chia7712] ,
 I noticed this issue might need a KIP, and I think I can help with this, thanks!
- **Chia-Ping Tsai:** [~jimmywang611] thanks for asking, but [~taijuwu] is already working on it
- **Jimmy Wang:** Noted, thanks for letting me know :).

## KAFKA-19998: API Versions response should return latest committed kraft version, not latest version on controllers
Bug · Open · Major · components: kraft · created 2025-12-16

Easiest approach is to expose this from the raft layer.


## KAFKA-19999: Transaction coordinator livelock caused by invalid producer epoch
Bug · Resolved (Fixed) · Blocker · created 2025-12-16 · resolved 2025-12-28

*case 1: during recovery*
When a Transaction Coordinator fails over and reloads transactions in PREPARE_COMMIT or PREPARE_ABORT state from the transaction log, it currently reuses the logged producer epoch to send the transaction markers.
In Transaction V2, brokers enforce strict epoch monotonicity for control batches (markers), requiring marker_epoch > current_epoch. Consequently, the broker rejects the recovery marker with InvalidProducerEpochException.
[code/log omitted]
The coordinator h…

- **Chia-Ping Tsai:** ping [~junrao] [~jolshan]
- **Chia-Ping Tsai:** We should introduce a flag (e.g., isPendingComplete) to PendingCompleteTxn to indicate that INVALID_PRODUCER_EPOCH should be treated as an idempotent success rather than a fatal error. This flag will be enabled in two scenarios: during coordinator recovery (case 1), or when retrying a marker request…
- **Justine Olshan:** > In Transaction V2, brokers enforce strict epoch monotonicity for control batches (markers), requiring marker_epoch > current_epoch. Consequently, the broker rejects the recovery marker with InvalidProducerEpochException.
 This is not true for 4.0 and 4.1 right? This change was introduced in 4.2? h…
- **Justine Olshan:** But I think your idea makes sense. I'm wondering if there is a clearer way to indicate this for an idempotent retry.
- **Justine Olshan:** I think it would be preferable to check the idempotency on the log side. Ie, if we get a tv2 marker with the same epoch + we haven't opened a new transaction, we can just not return any error.
- _…6 more comments_

## KAFKA-20000: Optimize retry backoff for CONCURRENT_TRANSACTIONS to improve TV2 throughput
Improvement · In Progress · Major · created 2025-12-16

Transaction V2 introduces frequent state transitions (epoch bumps) that briefly reject concurrent requests with CONCURRENT_TRANSACTIONS. The default client retry backoff (100ms) is excessive for these transient locks, leading to unnecessary latency and degraded throughput. Reducing the backoff allows faster retries and smoother performance during state transitions.

- **Chia-Ping Tsai:** The simple improvement is to modify TxnOffsetCommitHandler in TransactionManager.java. When receiving CONCURRENT_TRANSACTIONS, override the default retryBackoffMs with a smaller fixed value (e.g., 20ms) to expedite retries, similar to the existing logic in AddPartitionsToTxnHandler
- **Chia-Ping Tsai:** ping [~jolshan]
- **Justine Olshan:** Hey, I think this backoff is somewhat dependent on the system right? Depending on how quickly inter-broker requests occur 20ms could be too frequent as well right? For AddPartitionsToTxnHandler we had a config. Is this not working correctly for offset commits?
 From KIP-890:
 > Feb 2025. Adding addi…
- **Chia-Ping Tsai:** {quote}
 AddPartitionsToTxnHandler we had a config. Is this not working correctly for offset commits?
 {quote}
 Configs like `add.partitions.to.txn.retry.backoff.max.ms` and `add.partitions.to.txn.retry.backoff.ms` apply specifically to the produce path (KafkaApis#handleProduceRequest -> ReplicaMana…
- **Francis Godinho:** Reading the thread, I think introducing 2 new configs make sense. It solves the unnecessarily long backoff, but also addresses the system dependent aspect. [~chia7712], are you planning on implementing this? I would love to take a stab it otherwise!
- _…19 more comments_

## KAFKA-20001: Remove deprecated broker-side usage of num.partitions and default.replication.factor for topic auto-creation in 5.0.0
Improvement · Open · Major · components: config · created 2025-12-17

KIP-1211 _“Align the behavior of num.partitions and default.replication.factor for topic creation”_ deprecates the usage of {{num.partitions}} and {{default.replication.factor}} in {{broker.properties}} for normal topic auto creation. In the 4.x line, we kept backward compatibility by:
 * Applying the broker-side values only when they are explicitly present in {{broker.properties}} in {{DefaultAutoTopicCreationManager.}}
 * Emitting warnings in {{KafkaConfig}} when these configs are set in the…


## KAFKA-20002: Reset-by-duration should not hand back task to state-updater
Bug · Resolved (Fixed) · Critical · components: streams · created 2025-12-17 · resolved 2025-12-20

When adding support for "reset by duration" we introduced a bug, and incorrectly hand an active task back to the state updater.


## KAFKA-20003: Buffer released too early in MemoryPool
Bug · Resolved (Won't Fix) · Minor · components: core · created 2025-12-17 · resolved 2025-12-19

https://issues.apache.org/jira/browse/KAFKA-10386 we introduced Type.COMPACT_RECORDS in SchemaGenerator. However, we forgot to add Type.COMPACT_RECORDS to ApiKeys.retainsBufferReference(). This can cause the buffer in MemoryPool to be released too early, leading the data corruption and potential other weird problems. 
This issue is already fixed via https://issues.apache.org/jira/browse/KAFKA-19634, but the changes are large. We probably should just fix the issue in ApiKeys.retainsBufferReferen…

- **Chia-Ping Tsai:** There is another issue related to buffer release (KAFKA-19123). Perhaps we can fix them together in that patch
- **Jun Rao:** This doesn't seem to create a real issue since ApiKeys.requiresDelayedAllocation is set across all versions of Schema. So, as long as one version of the schema contains Type.RECORDS, ApiKeys.requiresDelayedAllocation is set correctly. An existing test ProtoUtilsTest covers the relevant schemas and d…
- **Jun Rao:** This issue is not causing a real problem in 4.2.0. If it becomes a problem in the future, an existing test will expose the problem. So, closing it for now.

## KAFKA-20004: Ensure PRs are only opened against "markdown" branch in kafka-site
Task · Open · Major · created 2025-12-17

Now that "markdown" is the default branch in kafka-site, we need to make sure future PRs do not target the asf-site or asf-staging deployment branches.


## KAFKA-20104: Inquiry about migrating from ZooKeeper to KRaft
Wish · Open · Minor · components: core · created 2026-01-30

Hi everyone,
I’m trying to migrate a test cluster from ZooKeeper to KRaft in-place (i.e., not provisioning three new controller-only nodes first and then pointing the existing brokers to them). I hit a problem and would appreciate any pointers.
What I did
- Enabled zookeeper.metadata.migration.enable on each existing broker and set the controller quorum settings so each broker acts as a controller+broker (process.roles=broker,controller).
- Rolled the three nodes.
Relevant broker configurat…


## KAFKA-20105: Move FetchSessionTest to server module
Sub-task · Resolved (Fixed) · Minor · created 2026-01-30 · resolved 2026-02-04


## KAFKA-20106: Improve behaviour of consumer assignment API under async reconciliations
Task · Resolved (Fixed) · Blocker · components: clients, consumer · created 2026-01-30 · resolved 2026-03-27

With the new rebalance protocol and the AsyncConsumer implementation, the client reconciles assignments in the background as it received them from the broker.
This leads to new interactions of the assignment API with others like seek() or position(). Taking seek as an example, given that the assignment can change in the background in between calls to assignment() and seek(), applications can hit IllegalStateException "No current assignment for partition t0" on seek() if the partition got unassi…

- **Matthias J. Sax:** Changed priority to blocker for this ticket, as I think we need to complete for for 4.3 release if we also want to do KIP-1274 with AK 4.3.
- **Lianet Magrans:** Totally agree. Opened the patch already.
- **Lianet Magrans:** All merged into 4.3
 (first PR made it before the branch cut, second PR cherry-picked [https://github.com/apache/kafka/commit/aa736157d18ec470c0b97e8dddb3eda80e6fb150] )

## KAFKA-20107: constraint on segment.bytes is only enforced in static broker config, but not in topic config
Bug · Open · Major · components: config · created 2026-01-30

[https://github.com/apache/kafka/pull/18140#issuecomment-2758776560]
In [KIP-1030|https://cwiki.apache.org/confluence/display/KAFKA/KIP-1030%3A+Change+constraints+and+default+values+for+various+configurations], we added a local limit for segment.bytes. However, it's only enforced in static broker config, but not in dynamic topic config. We should make the behavior consistent.

- **Jun Rao:** [~taijuwu] : Thanks for your interest in the jira. We are discussing some followup items in KIP-1030 in the mailing list. We probably want to wait for that discussion to conclude before implementing this.
- **TaiJuWu:** [~junrao] , Thanks for your information, I will wait we get conclusion.

## KAFKA-20108: [Build regression] Gradle task 'aggregatedJavadoc' fails in trunk
Bug · Resolved (Not A Problem) · Minor · components: build · labels: Gradle, Regression, gradle, regresion, regression · created 2026-01-31 · resolved 2026-01-31

*Note:* caused by a Gradle version upgrade from 8 to 9: KAFKA-19174
*How to reproduce:* 
* git checkout trunk 
* git checkout c6bbbbe24d96e81ad0856ccb81d1b4bc1269b68b
* git log -2 --oneline
{quote} 
c6bbbbe24d (HEAD) KAFKA\-19174 Gradle version upgrade 8 -->> 9 (#19513)
f5a87b3703 KAFKA\-19748: Add a note in docs about memory leak in Kafka Streams 4.1.0  (#20639)
{quote} 
* Gradle task: *./gradlew aggregatedJavadoc* fails (x):
{quote}
> Task :aggregatedJavadoc FAILED
[Incubating] Pro…

- **Dejan Stojadinović:** Ok, I have to reply to my self - and it will be quite funny, so to say :)
 This issue was actually resolved by [~chia7712] and me :D here: https://github.com/apache/kafka/pull/20683
 This was a false alarm; closing as _*Not a problem*_

## KAFKA-20109: Complete Kafka cluster dies on incorrect SSL config of a single controller
Bug · In Progress · Major · components: config, controller · created 2026-02-02

Hello,
we've recently run into a bug in Apache Kafka in Kraft mode where a whole mtls-enabled cluster (controllers + brokers) die if a single controller is (re)started with bad ssl principal mapping rules.
The bad config of course was appllied unintentionally when doing some changes in the config management of the system, basically it led to {{ssl.principal.mapping.rules}} missing for the controller listener on that one node. As soon as this single controller was restarted, the whole cluster d…

- **Gergely Harmadás:** Hi [~svdewitmam], I have started looking at the issue, feel free to assign it to me.
- **Sven Dewit:** [~harmadasg] sorry i'm not able to do that.
- **Gergely Harmadás:** Hi [~svdewitmam], here is my analysis:
 Before going into the details note that
  * misconfigured {{ssl.principal.mapping.rules}} config means that a given broker/controller is not able to properly extract the principal names of the other brokers/controllers from the incoming requests
  * since not…
- **Sven Dewit:** [~harmadasg] thanks for your analysis. My guess so far was that the issue lies within the "asymmetrical" nature of the outcome of the misconfigured controller: while the controller cannot authorize incoming connections from other nodes, the other nodes will happily accept connections from the miscon…
- **Gergely Harmadás:** [~svdewitmam]
 {quote}while the controller cannot authorize incoming connections from other nodes, the other nodes will happily accept connections from the misconfigured controller
 {quote}
 That is correct as the principal mapping works as expected on the other nodes.
 I have also tested with 4.2 a…
- _…1 more comments_

## KAFKA-20110: Fix generated doc and Javadoc for dynamic configs
Bug · Resolved (Fixed) · Minor · created 2026-02-02 · resolved 2026-02-12

It seems that on [1], one can't see a few broker configurations (i.e., follower.replication.throttled.rate, leader.replication.throttled.rate , replica.alter.log.dirs.io.max.bytes.per.second.
[1] - [https://kafka.apache.org/41/configuration/]


## KAFKA-20111: Describing group configs for pre-4.1 broker with later kafka-configs.sh fails
Bug · Resolved (Fixed) · Major · components: tools · created 2026-02-02 · resolved 2026-02-09

% bin/kafka-configs.sh --bootstrap-server localhost:9092 --entity-type groups --describe
Error while executing config command with args '--bootstrap-server localhost:9092 --entity-type groups --describe'
java.util.concurrent.ExecutionException: org.apache.kafka.common.errors.UnsupportedVersionException: The v0 ListConfigResources only supports CLIENT_METRICS
	at java.base/java.util.concurrent.CompletableFuture.reportGet(CompletableFuture.java:396)
	at java.base/java.util.concurrent.Completab…

- **Chia-Ping Tsai:** trunk: [https://github.com/apache/kafka/commit/5acd1ffe2071ce575af6695547ec8e0ee951e33c]
 4.2: https://github.com/apache/kafka/commit/9f8bd7394dd82bbc54ff472a9ad49f22e9f0a517
 4.1: https://github.com/apache/kafka/commit/9d24eec731d9ffb62fddc3a7869c87d51196a7e0

## KAFKA-20112: Flaky testAsyncConsumerMaxPollIntervalMsDelayInRevocation
Test · Resolved (Fixed) · Major · components: clients, consumer · created 2026-02-02 · resolved 2026-03-13

Has been flaky on trunk 
https://develocity.apache.org/scans/tests?search.relativeStartTime=P28D&search.rootProjectNames=kafka&search.tags=trunk&search.timeZoneId=America%2FToronto&tests.container=org.apache.kafka.clients.consumer.PlaintextConsumerPollTest&tests.sortField=FLAKY&tests.test=testAsyncConsumerMaxPollIntervalMsDelayInRevocation()%5B1%5D

- **Lianet Magrans:** Haven't had the time to look into this in detail, but seems the failure comes from a timeout when closing the consumer implicitly with the try (not from the core logic being tested, which is the revocation callback on a rebalance). It will probably be helpful to try to repro with logging enabled for…
