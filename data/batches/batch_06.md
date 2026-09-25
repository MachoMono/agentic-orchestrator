## KAFKA-17221: Flaky test DedicatedMirrorIntegrationTest::testMultiNodeCluster
Test · In Progress · Major · components: mirrormaker · created 2024-07-30

This test has failed at least once: [https://ge.apache.org/s/icsclaee3pdhg/tests/task/:connect:mirror:test/details/org.apache.kafka.connect.mirror.integration.DedicatedMirrorIntegrationTest/testMultiNodeCluster()?top-execution=1]
After examining the logs, it looks like no MM2 node ever attempted to write connector configs to the config topic ([this log message|https://github.com/apache/kafka/blob/1084d3b9c95aecccbe3c82e84ae4c8f406fc68e1/connect/mirror/src/main/java/org/apache/kafka/connect/mirr…


## KAFKA-17222: Remove the subclass of KafkaMetricsGroup
Improvement · Resolved (Fixed) · Minor · created 2024-07-30 · resolved 2024-08-06

There are subclass of KafkaMetricsGroup which have override `metricName` [0][1][2]. They are used to keep metrics compatibility. Now, KafkaMetricsGroup has the new constructor which can define the package and class name, and so we don't need to override the `metricName` anymore.
[0] https://github.com/apache/kafka/blob/9e06767ffa80b26791c3bff6bc9b10b6612ce7d2/core/src/main/scala/kafka/log/UnifiedLog.scala#L116
[1] https://github.com/apache/kafka/blob/9e06767ffa80b26791c3bff6bc9b10b6612ce7d2/st…


## KAFKA-17223: Retrying the call after encoutering UnsupportedVersionException will cause ConcurrentModificationException
Bug · Resolved (Fixed) · Minor · components: admin, clients · created 2024-07-31 · resolved 2024-08-08

[code/log omitted]
The steps producing above error are shown below.
1. maybeDrainPendingCall[0] encounter error when calling `call.nodeProvider.provide();`[1]
2. `runnable.pendingCalls.add(this)`[2] adds the call back to `pendingCalls`
3. `pendingIter.remove();` tries to remove item from the modified array list.
IMHO, we should add call back to `newCalls` rather than `pendingCalls`.  This approach is to revert a part of KAFKA-12432
[0] https://github.com/apache/kafka/blob/trunk/clients/src…

- **PoAn Yang:** Hi [~chia7712], if you're not working on this, may I take it? Thank you.
- **Chia-Ping Tsai:** [~cmccabe] Could you please take a look? It seems to me looping the modified list is error-prone, but I'm not sure why KAFKA-12432 add the retryable call back to `pendingCalls` rather than `newCalls`.
- **Chia-Ping Tsai:** [~yangpoan] sure, but we need to discuss the solution before filing the PR.
- **PoAn Yang:** I create a draft PR to avoid modifying `runnable.pendingCalls.add(this);` to `runnable.newCalls.add(this);`. The step is like following:
 [https://github.com/apache/kafka/pull/16753]
  # Use for-loop instead of iterator to check `pendingCalls`.
  # Use a list `toRemove` to collect removed calls in `…

## KAFKA-17436: Follower index dump mismatch
Bug · Open · Major · components: core · created 2024-08-28

When writing data, the starting position and the last offset of the current fetch data will be written to the index. However, when dumping the index, the starting position and the last offset of a batch are verified. Therefore, if the follower fetches multiple batches, it will cause problems with the index file.
Reproduction：
Unit test in DumpLogSegmentsTest
[code/log omitted]
System test:
 # start server and produce records
 # stop follower and delete all data in follower
 # start follow…


## KAFKA-17437: Upgrade commons-validator from 1.7 to 1.9.0
Improvement · Resolved (Fixed) · Minor · components: connect, core · created 2024-08-28 · resolved 2024-09-01

We are using Apache Kafka Connect in a critical environment, where our application security engineers control the used software (BOMs). The actual Kafka version (3.8.0) depends on {{commons-validator:commons-validator:1.7}}, which has vulnerabilities listed [here|https://mvnrepository.com/artifact/commons-validator/commons-validator/1.7]. I know, that this CVE doesn't apply to Kafka, because it is related to unit testing, but it should not be so difficult to upgrade commons-validator from 1.7 to…

- **Viktor Somogyi-Vass:** [~gira1] I created a PR for you. Usually these changes are quite straightforward if you want to do it next time :)

## KAFKA-17438: Fix raft/README.md to use kraft.version 1
Sub-task · Open · Major · created 2024-08-28

Need to upated both raft/README.md and raft/config/kraft.properties. Making sure that it works of course.


## KAFKA-17439: Make polling for new records an explicit action/event in the new consumer
Bug · Resolved (Fixed) · Major · components: clients, consumer · labels: consumer-threading-refactor, kip-848-client-support · created 2024-08-28 · resolved 2024-10-28

Presently, the new consumer polls the FetchRequestManager many, many times a second and creates fetch requests for any fetchable partitions. In order to more closely mirror how the existing consumer processes fetches, we should mirror the points at which fetch requests are sent in the new consumer.


## KAFKA-17440: Convert QuorumTestHarness to use PreboundSocketFactoryManager
Improvement · Open · Major · created 2024-08-28


## KAFKA-17441: Add RETRY option to other exception handlers
Improvement · Open · Major · components: streams · labels: needs-kip · created 2024-08-28

In kip-1065 we added a RETRY response option to the ProductionExceptionHandler.
However, retrying an action instead of either crashing or dropping records would be useful for the other exception handlers as well. We should consider a followup KIP to add a RETRY response option to the ProcessingExceptionHandler and/or DeserializationExceptionHandler


## KAFKA-17442: Implement persister error handling and make write calls async
Sub-task · Resolved (Fixed) · Major · created 2024-08-29 · resolved 2024-09-02


## KAFKA-17443: Create a tool to manipulate share-group state snapshots for recovery purposes
Sub-task · Resolved (Won't Fix) · Major · created 2024-08-29 · resolved 2025-09-18


## KAFKA-17444: High memory allocation rate for FetchSession.update 
Improvement · Open · Major · components: core · created 2024-08-30

!image-2024-08-30-10-34-33-011.png|width=757,height=241!
when single node 7w fetch qps, 1000+ consumer fetch connection the touch compare logic will consume a lot memory allocate 8%.


## KAFKA-17445: Kafka streams keeps rebalancing with the following reasons
Bug · Open · Major · components: streams · created 2024-08-30

We recently upgraded Kafka streams version to 3.8.0 and are seeing that the streams app keeps rebalancing and does not process any events
We have explicitly set the config 
GROUP_INSTANCE_ID_CONFIG
This is what we see on the broker logs:
[GroupCoordinator 2]: Preparing to rebalance group \{consumer-group-name} in state PreparingRebalance with old generation 24781 (__consumer_offsets-29) (reason: Updating metadata for static member {} with instance id {}; client reason: rebalance failed due t…

- **Bruno Cadonna:** [~rohitbobade] It is not clear to me what you tried to achieve by setting {{group.instance.id}}. Could yo please elaborate?
 Did you increase {{session.timeout.ms}} as described in the config definition (https://kafka.apache.org/documentation/#consumerconfigs_group.instance.id)
 Could you describe t…
- **Rohit Bobade:** [~cadonna]  we set the group instance id for sticky partition assignment. Initially the session timeout was set to 8 mins. After upgrading to 3.8.0 - we saw that the partitions were assigned only to a 2 pods out of 20.
 We have set the acceptable recovery lag as 0. My understanding is that the defau…
- **Rohit Bobade:** Acceptable recovery lag was set to 0 because of these 2 issues - 
 https://issues.apache.org/jira/browse/KAFKA-13269
 https://issues.apache.org/jira/browse/KAFKA-14172
 Is it safe to set the acceptable recovery lag to default?
- **Matthias J. Sax:** Setting acceptable recovery lag to zero could imply that standby tasks are never promoted to active, because they can only be promoted if they reach lag zero – however, if active tasks are constantly writing into the changelog log, reaching lag zero might be impossible (it might only be possible to…
- **Rohit Bobade:** Yes Agreed! that makes sense [~mjsax] ! We updated the acceptable recover lag to be default (10,000)
- _…2 more comments_

## KAFKA-17446: Kafka streams stuck in rebalancing
Bug · Open · Major · created 2024-08-30

Kafka streams stuck in endless rebalancing with the following error:
org.apache.kafka.streams.errors.LockException: stream-thread task [0_1] Failed to lock the state directory for task 0_1
org.apache.kafka.streams.processor.internals.TaskManager - stream-thread Encountered lock exception. Reattempting locking the state in the next iteration.

- **Bruno Cadonna:** [~rohitbobade] Could you please share some more details? Logs preferably on {{DEBUG}} level would be great!
- **A. Sophie Blee-Goldman:** [~rohitbobade] is this ticket a duplicate of https://issues.apache.org/jira/browse/KAFKA-17445 ? Can we close this one?

## KAFKA-17575: TestUtils.tempDirectory registers two shutdown hooks for the same thing
Bug · Resolved (Fixed) · Major · created 2024-09-18 · resolved 2024-09-23

TestUtils.tempDirectory registers a shutdown hook to clean up the temporary directory on JVM exit. But it also calls file.deleteOnExit, which essentially does the same thing. There's no reason to do both, setting up a shutdown hook via Exit.addShutdownHook should be good enough.

- **Ken Huang:** Hello [~srdo] , If you wouldn't work on this, may I take this issue, Thanks you
- **Chia-Ping Tsai:** [~m1a2st] there is already a PR for it. it would be great if you can take a look :)
- **Ken Huang:** Thanks for [~chia7712] reminder, I will take a look this PR.

## KAFKA-17576: Fix all references to kraft/server.properties to use reconfig-server.properties
Sub-task · Resolved (Fixed) · Major · components: docs, kraft · created 2024-09-18 · resolved 2024-11-07

When this issue was created these are all of the places where server.properties is referenced:
[code/log omitted]

- **Ken Huang:** Hello [~jsancio] , If you wouldn't work on this, may I take this issue, Thanks you

## KAFKA-17577: May be record metrics on UnknownSubscriptionIdException
Sub-task · Open · Major · created 2024-09-18

h3. Handling {{UnknownSubscriptionIdException}} (USIE)
When a broker changes telemetry subscriptions and a client attempts to report metrics with an outdated subscription ID, the broker throws {{UnknownSubscriptionIdException}} (USIE). In this case, the metrics payload is discarded, leading to a potential data gap.
If the client is using delta temporality (incremental metrics), this gap is reflected in external monitoring systems, which will observe a dip, potentially treating the next set of…


## KAFKA-17578: Remove partitionRacks from TopicMetadata
Sub-task · Resolved (Fixed) · Major · labels: kip-848 · created 2024-09-19 · resolved 2024-09-25

The ModernGroup#subscribedTopicMetadata takes too much memory due to 
partitionRacks:
/**
Map of every partition Id to a set of its rack Ids, if they exist.
If rack information is unavailable for all partitions, this is an empty map.
*/
private final Map<Integer, Set<String>> partitionRacks;
This is not being used at the moment as the consumer protocol does not support rack aware assignments.
A heap dump from a group with 500 members, 2K subscribed topic partitions shows
654,400 bytes u…

- **PoAn Yang:** Hi [~jeffkbkim], if you're not working on this issue, may I take it? Thank you.
- **Jeff Kim:** [~yangpoan] sure!
- **David Jacot:** [~yangpoan] Please ping me when you have a PR out. I'd like to review this one.
- **PoAn Yang:** Hi [~jeffkbkim] and [~dajac], there are 200+ references to TopicMetadata. Do we want to fully remove partitionRacks? Or we can create a new TopicMetadata constructor which always set empty partitionRacks to TopicMetadata. And we only need to change production code and related test cases? Thank you.
- **Jeff Kim:** [~yangpoan] We do plan to implement rack aware server side assignors as part of 4.1 but we need to find a way to minimize the memory usage so we need to probably change it anyways. Let's remove it cc [~dajac]
- _…2 more comments_

## KAFKA-17579: Dynamic LogCleaner configurations are not picked up upon restart
Bug · Resolved (Fixed) · Major · created 2024-09-19 · resolved 2024-09-20

Dynamic configurations for the LogCleaner are not applied upon a restart.
Reproduction steps:
 # Create a 1-broker cluster
 # Change the number of log.cleaner.threads to 2
 # Bounce the broker
 # Observe the server.logs - you will notice that only 1 log cleaner thread has been instantiated
Proposed solution:
 # Change immutable variables `val` to methods `def`
 # Add unit/integration tests which test reconfiguration of the LogCleaner

- **Christo Lolov:** This has been picked up by Jason Taylor. His Jira account is still being reviewed hence I will assign the ticket once it is approved.

## KAFKA-17580: Java 21 spurious compilation failure in streams:compileTestJava
Bug · Resolved (Cannot Reproduce) · Minor · components: build, streams · created 2024-09-19 · resolved 2025-10-16

On a trunk build with Java 21, we saw a very strange looking compilation error during the streams:compileTestJava task.
[code/log omitted]
CI Job: [https://github.com/apache/kafka/actions/runs/10928260916/job/30336275918]
Logs are attached.

- **Matthias J. Sax:** [~davidarthur] – did we see this more than once? Not sure how to investigate this? I could compile the code locally using Java21 – and if we don't see this failing regularly, I am not sure what do to with this ticket?
- **David Arthur:** As far as I know we've only seen this one. I don't have a good idea how to investigate this. Nonetheless, I'd like to keep the ticket open so we can collect logs of any future occurrences.
- **Matthias J. Sax:** [~davidarthur] It's a few month now. Should we close this?

## KAFKA-17581: AsyncKafkaConsumer can't unsubscribe invalid topics
Bug · Resolved (Fixed) · Major · components: clients, consumer · labels: consumer-threading-refactor, kip-848-client-support · created 2024-09-19 · resolved 2024-09-27

When consumer subscribes an invalid topic name like " this is test", classic consumer can unsubscribe without error. However, async consumer can't. We can use following integration test to validate:
[code/log omitted]

- **Kirk True:** [~yangpoan]—this is a good catch! Where in the new consumer is the exception thrown? I’d want to look at the existing consumer to see how it handles this case.
- **PoAn Yang:** Hi [~kirktrue], here is related Jira and PR:
 * https://issues.apache.org/jira/browse/KAFKA-16764
 * https://github.com/apache/kafka/pull/16043

## KAFKA-17582: Unpredictable consumer position after transaction abort
Bug · Open · Critical · components: clients, consumer, documentation · labels: abort, offset, transaction · created 2024-09-19

With the official Kafka Java client, version 3.8.0, the position of consumers after a transaction aborts appears unpredictable. Sometimes the consumer moves on, skipping over the records it polled in the aborted transaction. Sometimes it rewinds to read them again. Sometimes it rewinds *further* than the most recent transaction.
Since the goal of transactions is to enable "exactly-once semantics", it seems sensible that the consumer should rewind on abort, such that any subsequent transactions…

- **Kyle Kingsbury:** I've done some more digging here, and written a Jepsen test specifically for rewind-vs-advance behavior: [https://github.com/jepsen-io/redpanda/blob/main/src/jepsen/redpanda/workload/abort.clj]. Try something like:
 {{lein run test --db kafka -w abort --safe --concurrency 5n --sub-via assign --rate…
- **Justine Olshan:** Hi [Kyle Kingsbury|https://issues.apache.org/jira/secure/ViewProfile.jspa?name=aphyr]. Thanks for taking a look at transactions through Jepsen testing! I’m familiar with the framework and think it is super useful for testing distributed systems. 
 Can you clarify the test setup? It’s a little unclea…
- **Kyle Kingsbury:** Hi Justine! Thanks for your detailed answer.
 Yes, this behavior occurs with a transaction that reads from a single topic-partition and writes back to that same topic-partition. I'm not sure what happens when it reads from a different topic-partition than the one it's writing to–if the behavior woul…
- **Justine Olshan:** You are correct in that there isn't a great single source of truth. I've created https://issues.apache.org/jira/browse/KAFKA-17671 to improve the documentation. If there are any specific items/questions that should be included in the documentation, please comment on that ticket.
 (And to answer your…
- **Kyle Kingsbury:** Thanks Justine–I think having central docs will go a long way towards making transactions easier to understand.
 I'd also like to encourage the Kafka team to reconsider this behavior. People use Kafka transactions to get "exactly-once" semantics, and if they leave out this manual-rewind step, they'r…
- _…1 more comments_

## KAFKA-17583: kafka-config script cannot set `cleanup.policy=delete,compact`
Bug · Resolved (Fixed) · Major · created 2024-09-20 · resolved 2024-11-11

Kafka-config.sh cannot set configs with "," in the value, because we split the option value with "," [here|https://github.com/apache/kafka/blob/3783385dc1cc27246cf09ec791e4b43f577a26ea/core/src/main/scala/kafka/admin/ConfigCommand.scala#L300].
[code/log omitted]

- **Lin Siyuan:** Can I have this ticket
- **Luke Chen:** [~linsiyuan], assigned to you. Thanks.

## KAFKA-17584: Fix incorrect synonym handling for dynamic log configurations
Bug · Resolved (Fixed) · Blocker · created 2024-09-20 · resolved 2024-09-26

Updating certain dynamic configurations (for example `message.max.bytes`) causes retention based on time to reset to the default value (source code) for log.retention.ms. This poses a durability issue if users have set their retention by using log.retention.hours or log.retention.minutes. In other words, if a user has set log.retention.hours=-1 (infinite retention) and they dynamically change `message.max.bytes` their retention will immediately change back to the default of 604800000 ms (7 days)…

- **Federico Valeri:** I can confirm the issue as described. I reproduced with trunk, 3.9.0-rc0, and currently supported releases.
- **Matthias J. Sax:** [~christo_lolov] – why is "affects version" set to 3.9.0 while fix version includes 3.8.1? "affects version" should be the earliest version which has this bug.
 It seem we should at least update it to 3.8.0, but I am wondering if we want to cherry-pick this for 3.7.2 release that we plan to do?
- **Colin McCabe:** [~mjsax]: Going from memory, this particular bug goes all the way back to the earliest 3.0 releases. I didn't bother cherry-picking to 3.7 since I didn't think anyone would make another 3.7 release. There's no reason why it couldn't be ported back to that release, though.
- **Christo Lolov:** [~mjsax] Apologies for the delay, I was taking some time off from computers :). At the time of discovering the bug 3.9.0 was undergoing its release candidates, hence I put 3.9.0 as affected version. As Colin correctly mentioned, this is present in all Kafka versions at least since 3.0.
- **Matthias J. Sax:** Thanks. I tried to cherry-pick to 3.7 branch, but it does not cherry-pick cleanly. Should we include it in 3.7.2? If yes, would be great to get some help from people who know this code better. I am also fine with just leave it as is, and not include in 3.7.2. Thoughts?
- _…2 more comments_

## KAFKA-17585: `offsetResetStrategyTimestamp` should return `long` instead of `Long`
Improvement · Resolved (Fixed) · Trivial · created 2024-09-20 · resolved 2024-09-24

the null behavior was removed by [https://github.com/apache/kafka/commit/2b233bfa5f35bf237effe8c5202fd2b80c601943,] so we can return long and then remove the null check to simplify the code.

- **kangning.li:** [~chia7712]  I am interested in this issue.Cloud you assign it to me?

## KAFKA-17782: Fix ConsumerProtocolTest#deserializeOldSubscriptionVersion
Test · Resolved (Done) · Major · components: clients · created 2024-10-12 · resolved 2024-10-14

The expected code should be `assertEquals(toSet(subscription.topics()), toSet(parsedSubscription.topics()));`
https://github.com/apache/kafka/blob/ca422268649136b7207c0843fea28d594c761fe9/clients/src/test/java/org/apache/kafka/clients/consumer/internals/ConsumerProtocolTest.java#L156

- **Lin Siyuan:** Incorporated into  https://github.com/apache/kafka/pull/17479  processing together

## KAFKA-17783: Remove sharePartition from SharePartitionManager if the partition is deleted or becomes a follower
Sub-task · Resolved (Fixed) · Major · created 2024-10-13 · resolved 2024-12-04

In reference to comment [https://github.com/apache/kafka/pull/17437#discussion_r1795840636] , in the case when a partition is deleted or becomes a follower, we probably also want to remove the sharePartition from {{SharePartitionManager}} to free up the space

- **Andrew Schofield:** I believe some of this has been done in the handling of the error codes from the replica manager.
- **Jun Rao:** merged the PR to trunk

## KAFKA-17784: Mirror Maker2 Pod CrashLoopbackOff
Bug · Open · Blocker · components: mirrormaker · created 2024-10-13

When I use k8s deployment with mirrormaker v3.7.1, and deploy one kafka node in each data center, I always got the crashloopbackoff error, please see the attachment. 
The configuration of mirrormaker is:
```configuration
clusters = idca, idcb
idca.bootstrap.servers = 192.168.2.146:13399
idcb.bootstrap.servers = 192.168.2.147:13399
idca->idcb.enabled = true
idca->idcb.topics = .*
idcb->idca.enabled = true
idcb->idca.topics = .*
replication.factor=1
tasks.max=6
emit.checkpoints.interva…

- **Greg Harris:** [~yitian998] Here's the error causing the shutdown: 
 [code/log omitted]
- **George Yang:** Thank you [~gharris1727].
 The error indicates that the topic used for storing offset information (mm2-offsets.idcb.internal) does not have the correct cleanup policy. I'm not entirely sure if this theory is accurate, but it seems that Kafka MirrorMaker 2 requires the topic to have a cleanup.policy=…
- **Greg Harris:** > However, I have set the broker configuration log.cleanup.policy=delete. Will this conflict with the above topic-specific setting?
 The topic-specific setting will take precedence.
 > Additionally, is there another way to set cleanup.policy=compact without using the kafka-configs.sh command, such a…
- **George Yang:** > These topics, if created by MirrorMaker, should have the cleanup policy already set-up. 
 [~gharris1727] , 
 To my surprise, the topic {{mm2-offsets.idcb.internal}} was supposed to be created automatically by MirrorMaker. The issue where the MirrorMaker pod went into a CrashLoopBackOff state occur…
- **Zhijian Chen:** In the MirrorMaker scenario, a MirrorMaker process runs multiple Herders, each handling different source cluster events.
 Now if one Herder has an exception, it will cause the MirrorMaker process to exit, causing other Herders that don't have problems to exit, affecting all of them, which I think is…

## KAFKA-17785: Kafka protocol documentation should include tagged field information
Improvement · Resolved (Fixed) · Major · components: documentation · created 2024-10-13 · resolved 2024-10-24

The Kafka documentation includes a description of the Kafka protocol ([https://kafka.apache.org/protocol]). This is useful to someone wanting to understand the details of the protocol. However, in the area of tagged fields, the documentation is not helpful.
Tagged fields provide a way of supplying optional data in a request or response. Modern requests and responses usually permit tagged fields, although they are relatively rarely used in practice.
One RPC in which tagged fields contain import…


## KAFKA-17786: align the low bound of ducktape version for 3.8.x
Sub-task · Resolved (Fixed) · Major · created 2024-10-14 · resolved 2024-10-14

- **Josep Prat:** Done via https://github.com/apache/kafka/pull/17482

## KAFKA-17787: Remove --zookeeper option and logic from ConfigCommand
Sub-task · Resolved (Fixed) · Major · components: tools · created 2024-10-14 · resolved 2024-11-11

- **Cheng-Yan Wang:** Hi [~mimaison], I'd love to work on this issue, could you assign it to me?
- **Mickael Maison:** Yes feel free to grab it. You have permissions to assign issues to yourself, just click on "Assign to me" next to Assignee on the right side.
- **Cheng-Yan Wang:** [~mimaison] Sounds great, thanks!

## KAFKA-17788: During ZK migration, always include control.plane.listener.name in advertisedBrokerListeners
Bug · Resolved (Fixed) · Blocker · created 2024-10-14 · resolved 2024-10-15

When testing migration with Kafka 3.9.0-RC2, the broker fail to start when they are first rolled to start the migration with the following error:
[code/log omitted]
This is despite our configuration having the {control.plane.listener.name} properly configured:
[code/log omitted]
It looks like 3.9.0-RC2 filters out the control plane listener (maybe because it is used by the KRaft controllers as well?) and runs into this error. This worked fine in 3.8.0, so this seems like a regression in 3.9.…

- **Colin McCabe:** After looking through the attached file, I can say that this is a misconfiguration. control.plane.listener is a totally separate concept from control.plane.listener.name. They should never be set to the same value. The controller listener must have a different name and value than the control plane l…
- **Colin McCabe:** Update:
 Kafka wants to divide up all listeners into either broker listeners or controller listeners. The sets are disjoint: a listener can't be both.
 BrokerServer will try to open the ports that belong to the broker; ControllerServer will try to open the ports that belong to the controller. You ob…

## KAFKA-17789: State updater stuck when starting with empty state folder
Bug · Resolved (Cannot Reproduce) · Critical · components: streams · created 2024-10-14 · resolved 2026-05-04

In an application with multiple clients, each having multiple threads, when the app is started with an empty storage (without resetting the whole application), only a part of the clients are restoring the changelog topics.
Those non-restoring clients are also not able to shutdown gracefully.
Reproduction steps
> I'm putting all the actual details, while I'm going to make a project to reproduce it locally, and I'll link it inside this ticket.
 * Having the app in a kubernetes environment, wit…

- **Lucas Brutschy:** [~chuckame] did you have time to provide a local reproduction environment for this? We haven't observed this behavior in our own tests. A reproduction would be extremely helpful. Thanks!
- **Nikita Shupletsov:** I wonder if it could be related to https://issues.apache.org/jira/browse/KAFKA-19831 or https://issues.apache.org/jira/browse/KAFKA-19960 or https://issues.apache.org/jira/browse/KAFKA-19994 or something similar where we didn't close some tasks correctly which left some stores not closed, hence the…
- **Guang Zhao:** I'm trying to reproduce the problem locally -- may I ask for more context in the original setting please --
 - did the non-restoring clients eventually start restoring on their own (given enough time), or did they remain permanently stuck at zero restorations?
 - similarly, when trying to stop the s…
- **Matthias J. Sax:** [~chuckame] – can you help on this? Or maybe confirm that the issue was fixed already (eg, with 4.2.0 release)?
 If we cannot reproduce, we might just want to close the ticket for now, and "hope" that the other fixes do indeed cover it (and if not, well, we can always file a new ticket, or re-open t…
- **Nikita Shupletsov:** Hi [~chuckame] 
 I would like to ping you one more time.
 We haven't been able to reproduce the issue, so we would like to close the ticket.
- _…5 more comments_

## KAFKA-17790: Document that control.plane.listener should be removed before ZK migration is finished
Bug · Resolved (Fixed) · Major · created 2024-10-14 · resolved 2024-10-15


## KAFKA-17791: Dockerfile should use `requirements.txt` to ensure dependencies
Improvement · Resolved (Fixed) · Major · created 2024-10-14 · resolved 2024-11-15

see https://github.com/apache/kafka/pull/17481#issuecomment-2411631883


## KAFKA-17792: header parsing ends up timing out and using large quantities of memory if the string looks like a number
Bug · Resolved (Fixed) · Blocker · components: connect · created 2024-10-14 · resolved 2025-01-27

{color:#172b4d}We have trace headers such as:{color}
{color:#172b4d}"X-B3-SpanId": "74320e6e26adc8f8"{color}
{color:#172b4d}if however the value happens to be: "407127e212797209"{color}
{color:#172b4d}This is then treated as a numeric value and it tries to convert this as a numeric representation and an exact value using BigDecimal{color}
we end up with the trace:
    BigDecimal.setScale(int, RoundingMode) line: 2876    
    Values$ValueParser.parseAsExactDecimal(BigDecimal) line: 1044…

- **Martin Sillence:** I feel there are a few options
  * make the schema expicit
  * an exclude list
  * a limit on the number of digits
 The latter is the least intrusive but possibly the worst in terms of suprises but to quantifiy it:
 positive exponents:
 [code/log omitted]
 negative exponents:
 [code/log omitted]
 so…
- **Martin Sillence:** https://github.com/apache/kafka/pull/17510

## KAFKA-17987: Remove assorted ZK-related files
Sub-task · Resolved (Fixed) · Major · created 2024-11-12 · resolved 2024-11-13

- **Mickael Maison:** Opened https://github.com/apache/kafka/pull/17811 to also remove the Windows scripts.

## KAFKA-17988: Fix flaky ReconfigurableQuorumIntegrationTest.testRemoveAndAddSameController
Bug · Resolved (Fixed) · Major · created 2024-11-12 · resolved 2024-11-24

https://ge.apache.org/scans/tests?search.rootProjectNames=kafka&search.timeZoneId=Asia%2FTaipei&tests.container=kafka.server.ReconfigurableQuorumIntegrationTest&tests.test=testRemoveAndAddSameController()

- **Kevin Wu:** Submitted a PR that fixes this.

## KAFKA-17989: Fix flaky ShareConsumerTest#testAcknowledgeCommitCallbackCallsShareConsumerWakeup
Bug · Open · Major · created 2024-11-12

https://ge.apache.org/scans/tests?search.rootProjectNames=kafka&search.timeZoneId=Asia%2FTaipei&tests.container=kafka.test.api.ShareConsumerTest

- **Lianet Magrans:** +1, seeing this on PRs now (flaky in trunk https://ge.apache.org/scans/tests?search.buildOutcome=failure&search.relativeStartTime=P28D&search.rootProjectNames=kafka&search.tags=trunk&search.timeZoneId=America%2FToronto&tests.container=kafka.test.api.ShareConsumerTest&tests.test=testAcknowledgeCommit…
- **Andrew Schofield:** This test does not seem to be flaky any longer.

## KAFKA-17990: Fix flaky ShareConsumerTest#testShareAutoOffsetResetDefaultValue
Bug · Resolved (Fixed) · Major · created 2024-11-12 · resolved 2025-12-04

https://ge.apache.org/scans/tests?search.rootProjectNames=kafka&search.timeZoneId=Asia%2FTaipei&tests.container=kafka.test.api.ShareConsumerTest

- **Andrew Schofield:** Hi [~chia7712], I'd like to take this issue over.
- **Chia-Ping Tsai:** [~schofielaj] thanks for your help!
- **Andrew Schofield:** This test seems to be non-flaky now. Will run a few PR builds to get a stronger signal before removing the flaky designation.
- **Andrew Schofield:** This test is no longer flaky.

## KAFKA-17991: Timed calls to future.get in DefaultStatePersister and test improvements
Sub-task · Resolved (Fixed) · Major · created 2024-11-12 · resolved 2024-11-14


## KAFKA-17992: Remove `getUnderlying` and `isKRaftTest` from ClusterInstance
Improvement · Resolved (Fixed) · Trivial · created 2024-11-12 · resolved 2024-11-14

they are unused

- **Lin Siyuan:** Hi [~chia7712]  , If you are not start working on this issue, I would like to handle it.
- **Chia-Ping Tsai:** [~linsiyuan] Sorry that we are working on that :_

## KAFKA-17993: reassign partition tool stuck with uncaught exception: 'value' field is too long to be serialized
Bug · Patch Available · Major · components: clients · created 2024-11-12

Running the reassignment script when a topic had 5000 partitions, with both throttle options being set, the tool remained stuck with an exception
The same json file previously passed the --verify step
Reproduced on today's trunk (4.0), here's the Stack trace for 3.9.1-SNAPSHOT :
{{[2024-11-12 16:15:43,516] ERROR Uncaught exception in thread 'kafka-admin-client-thread | reassign-partitions-tool': (org.apache.kafka.common.utils.KafkaThread)}}
{{java.lang.RuntimeException: 'value' field is too…

- **Edoardo Comar:** on the topic with 5000 partitions the IncrementalAlterConfigRequest for {color:#00627a}modifyTopicThrottles {color}looks like :
 {{{color:#000000}AlterConfigOp{opType=SET, configEntry=ConfigEntry(name=leader.replication.throttled.replicas, {color}}}
 {{{color:#000000}value=0:0,0:1,0:2,1000:0,1000:1,…
- **Edoardo Comar:** https://github.com/apache/kafka/pull/17816
- **Edoardo Comar:** Withe the patched client, the Quorum controller may encounter a ConfigRecord that is too large :
 see https://issues.apache.org/jira/browse/KAFKA-18020

## KAFKA-17994: Checked exceptions are not handled when deserializing kafka stream record
Bug · Resolved (Fixed) · Blocker · components: streams · created 2024-11-12 · resolved 2024-11-15

When we got a PR to upgrade kafka clients 3.8.1 -> 3.9.0, we saw some failing tests. They were relating to using a DeserializationExceptionHandler with 'log and continue' strategy, however on newest version the stream was just crashing when Jackson was trying to deserialize a faulty json and this handler was not invoked.
In this [KIP-1033|https://cwiki.apache.org/confluence/display/KAFKA/KIP-1033%3A+Add+Kafka+Streams+exception+handler+for+exceptions+occurring+during+processing], specifically in…

- **Matthias J. Sax:** Thanks for filing this ticket. – Can you share your Json `Deserializer` code? What I don't understand right now is, how a checked exception could be thrown? The interface does not declare any exceptions, and thus only `RuntimeException` should be allowed: [https://github.com/apache/kafka/blob/trunk/…
- **Ilya:** Hi [~mjsax] . We use Kotlin and it doesnt have checked exceptions at compile time, so even deserializer like this would compile:
 [code/log omitted]
 And the error in runtime would be exactly that without wrapping:
 [code/log omitted]
 I suppose, its the same problem for Scala. And its also technica…
- **Matthias J. Sax:** Ah. Thanks for clarification. That's helpful.
 I agree that we should fix this... As it's a regression, I'll mark is as blocker for 3.9.1 and 4.0.0.
 Current work-around for 3.9.0 would be adding `try-catch` and re-throw as `RuntimeException`.
- **Chia-Ping Tsai:** trunk: https://github.com/apache/kafka/commit/f02c28b21dc4d89e1d7f2e16f8f9e067a9575e61
 3.9: https://github.com/apache/kafka/commit/2127ae63290e1309e0d1ebbc84f6ef3a6f81bae2

## KAFKA-17995: Large value for `retention.ms` could prevent remote data cleanup in Tiered Storage
Bug · Resolved (Fixed) · Major · components: Tiered-Storage · labels: newbie · created 2024-11-12 · resolved 2024-11-14

If a user has configured value of "retention.ms" to a value > current unix timestamp epoch, then at this line of code [1] , cleanupUntilMs becomes negative. This is because cleanupUntilMs is calculated as (current unix epoch ms - retention.ms) [1]. 
This leads to cleaner failures at [https://github.com/apache/kafka/blob/5a5239770ff3565233e5cbecf11446e76339f8fe/core/src/main/java/kafka/log/remote/RemoteLogManager.java#L2218] and hence, all cleaning for that topic partition stops.
[1] [https://g…

- **PoAn Yang:** Hi [~divijv], if you're not working on this, may I take it? Thank you.
- **Divij Vaidya:** Hi [~yangpoan] 
 Sure. Please feel free to assign it to yourself.

## KAFKA-17996: kafka-metadata-quorum.sh add-controller cause the new added controller to crash with java.lang.IllegalArgumentException
Bug · Resolved (Fixed) · Major · components: controller, kraft · created 2024-11-12 · resolved 2025-04-09

`kafka-metadata-quorum.sh --bootstrap-server 127.0.0.1:9092 --command-config controller.properties add-controller` update the metadata successfully and if I ran `kafka-metadata-quorum.sh --bootstrap-server 127.0.0.1:9092 describe --status` I can see the new controller get upgraded from observer to voter.
However the new added controller crashes immediately once we ran `add-controller` with `java.lang.IllegalArgumentException`
```
2024-11-12 14:38:21 java.lang.IllegalArgumentException: Unexpec…

- **Luke Chen:** [~omnia_h_ibrahim] , do you have any update for this ticket? If no, I'm going to remove it from 3.9.1 release. Thanks.
- **Luke Chen:** Removing fix version until it has progress.
- **Omnia Ibrahim:** I believe someone already fixed this in another Jira
- **Luke Chen:** Thanks [~omnia_h_ibrahim] !

## KAFKA-17997: Remove deprecated config log.message.timestamp.difference.max.ms
Improvement · Resolved (Fixed) · Major · labels: breaking, newbie · created 2024-11-12 · resolved 2024-11-28

_[log.message.timestamp.difference.max.ms|https://kafka.apache.org/documentation.html#brokerconfigs_log.message.timestamp.difference.max.ms]_ was deprecated as part of KIP 937. We need to remove it from 4.0.
The exit criteria for this Jira should be:
1. Remove the configuration from the code and associated tests.
2. Update documentation at [https://github.com/apache/kafka/blob/trunk/docs/upgrade.html#L25] to add the removed configuration
[1] [https://cwiki.apache.org/confluence/display/KAFKA…

- **Swikar Patel:** Anybody working on it?
- **Hyunsang Han:** I'm currently working on this issue. Would it be okay if I proceed to submit a PR?
 I'm new to contributing to Apache projects. :)
- **Hyunsang Han:** I have submitted a PR: https://github.com/apache/kafka/pull/17928

## KAFKA-18064: SASL mechanisms that do support neither integrity nor confidentality should throw exception on wrap/unwrap
Bug · Resolved (Fixed) · Major · components: security · created 2024-11-21 · resolved 2025-01-14

wrap/unwrap should throw an exception unless a non-auth QOP has been negotiated.
SCRAM only supports auth QOP, so wrap/unwrap should always throw IllegalStateException.
[https://docs.oracle.com/en/java/javase/23/docs/api/java.security.sasl/javax/security/sasl/SaslClient.html#unwrap(byte%5B%5D,int,int)]

- **Istvan Toth:** This also applies to the other mechanims in the code base.
- **Istvan Toth:** Merged to trunk.

## KAFKA-18065: be helpful when throwing ConcurrentModificationException out of consumers
Improvement · Resolved (Won't Fix) · Minor · created 2024-11-22 · resolved 2024-11-22

from https://github.com/apache/kafka/pull/8193

- **Chu Cheng Li:** Hi [~chia7712] 
 I think this has been finished, see below links:
 1. [ClassicKafkaConsumer#acquire|https://github.com/peterxcli/kafka/blob/38aca3a045474a9e52ae25bde28d8a013b04f92b/clients/src/main/java/org/apache/kafka/clients/consumer/internals/ClassicKafkaConsumer.java#L1222-L1231]
 2. [AsyncKafk…
- **Chia-Ping Tsai:** [~peterxcli] thanks for your inforamtion

## KAFKA-18066: Misleading/mismatched StreamThread id in logging
Bug · Resolved (Fixed) · Minor · components: streams · labels: newbie, newbie++ · created 2024-11-22 · resolved 2025-07-29

While debugging a test application I was confused to see a number of log lines where the StreamThread name appeared twice but had a different thread id/index in the same message. For example:
[code/log omitted]
Generally you would expect that the actual Logger prefix (the first thread name, in this case StreamThread-1) is the same as the LogContext prefix (the second thread name, ie the StreamThread-3 in this example). I dug into it and figured out that this happens for all of the messages log…

- **Chu Cheng Li:** Hi [~ableegoldman], may I take this ticket? Thanks!
- **A. Sophie Blee-Goldman:** [~peterxcli]  Go for it!
- **Chu Cheng Li:** Hi [~ableegoldman] 
 I’m working on this and would like to hear your thoughts.:D
 Currently, if we move the *creation* logic directly into the {{StreamThread}} constructor, it becomes harder to refactor tests that use mocks. For reference, see the [current test cases|https://github.com/peterxcli/kaf…
- **Uladzislau Blok:** Hey [~peterxcli],
 Are you still looking into that? If not I could pick this up
- **Chu Cheng Li:** Sure
- _…3 more comments_

## KAFKA-18067: Kafka Streams can leak Producer client under EOS
Bug · Resolved (Fixed) · Major · components: streams · labels: newbie, newbie++ · created 2024-11-22 · resolved 2025-04-03

Under certain conditions Kafka Streams can end up closing a producer client twice and creating a new one that then is never closed.
During a StreamThread's shutdown, the TaskManager is closed first, through which the thread's producer client is also closed. Later on we call #unsubscribe on the main consumer, which can result in the #onPartitionsLost callback being invoked and ultimately trying to reset/reinitialize the StreamsProducer if EOS is enabled. This in turn includes closing the current…

- **TengYao Chi:** Hi [~ableegoldman] 
 I would like to give it a try, may I have this issue ?
- **A. Sophie Blee-Goldman:** imo we should just add a "closed" flag to the StreamsProducer and skip the reset method entirely if its already been closed.
- **A. Sophie Blee-Goldman:** [~frankvicky] Go for it!
- **Bruno Cadonna:** We had to revert the fix for this bug (https://github.com/apache/kafka/pull/19078) because it introduces a blocking bug for AK 4.0. 
 The issue is that the fix prevented Kafka Streams from re-initializing its transactional producer under exactly-once semantics. That led to an infinite loop of {{Prod…
- **A. Sophie Blee-Goldman:** thanks for catching this. [~frankvicky] since we had to revert the initial fix, want to revisit this issue and retry? Seems like we should not piggyback on the existing #close method to set the "dont reinitialize" flag, since it's not only called during shutdown but also during the `#resetProducer`…
- _…1 more comments_

## KAFKA-18068: Fixing typo in ProducerConfig
Bug · Resolved (Fixed) · Minor · labels: kip · created 2024-11-22 · resolved 2025-08-07

Fix typos:
{{PARTITIONER_ADPATIVE_PARTITIONING_ENABLE_CONFIG}}
{{PARTITIONER_ADPATIVE_PARTITIONING_ENABLE_DOC}}
Also end of line whitespaces needs removing in descriptions.

- **João Pedro Fonseca:** I have labeled it as need-kip based on [~chia7712]'s comment in PR. :)
- **Chia-Ping Tsai:** [~mingyen066] it would be useful if we can check other typo in this KIP.
- **Ming-Yen Chung:** [~chia7712] I’ve checked the other config variables and didn’t find any with typos.

## KAFKA-18069: Out of order output from windowed aggregations
Bug · Open · Major · components: streams · created 2024-11-22

We have an input topic which sends many messages to the topic every 250ms. (say 10k). The key is unique id from a set of IDs. So every set of messages at the 250ms mark will have some subset of the overall keys (product-ids etc)
We have a kafka streams app running windowed aggregations over it. Aggregations use grouping by the same key as the key of the input topic. And aggregate for 10s windows over it, resulting in 1 value for each key for every 10 second window.
We are using suppression for…

- **Khoa Nguyen:** Hi [~rhishikeshj], can I take this one?
- **Rhishikesh Joshi:** Hi [~khoanetapp] 
 Thanks that would be very helpful. Unfortunately I don't have the expertise to take this one on anyway.
 But if you need any help or more information, I can definitely help you.
- **Khoa Nguyen:** Thanks! let me try to replicate this first.

## KAFKA-18070: Update kafka-metadata-quorum.sh output in docs to match post-KIP-853 appearance
Bug · Resolved (Fixed) · Major · created 2024-11-22 · resolved 2024-12-02

- **Kuan Po Tseng:** I can assist with this. May I take over?

## KAFKA-18071: Avoid unneeded background event to refresh regex if no subscription pattern in use
Improvement · Resolved (Fixed) · Minor · components: clients, consumer · labels: consumer-threading-refactor · created 2024-11-22 · resolved 2024-11-25

With the new consumer, the poll loop currently generates an 
UpdatePatternSubscriptionEvent on each poll iteration, that is processed in the background to re-eval the subscription regex against the latest metadata (if there is new metadata).
If the consumer is not subscribed to a pattern, we still generate this event, and early return in the background thread if !hasSubscriptionPattern. We should consider short-circuiting this on the app thread, to avoid generating the event and blocking on it…


## KAFKA-18072: Data corruption in netty version to 4.1.111.Final
Bug · Resolved (Fixed) · Major · components: connect · created 2024-11-22 · resolved 2024-11-22

By upgrading to 4.1.111.Final in KAFKA-17046 this introduced data corruption for grpc-java package (see the discussion in [netty|https://github.com/netty/netty/issues/14126] and [grpc-java|https://github.com/grpc/grpc-java/issues/11284] issues. This can affect kafka connect connectors that rely on netty dependencies that are supplied at runtime by the Kafka image. Two such examples are debezium-vitess-connector and debezium-spanner, but there may be others. We should upgrade to 4.1.112.Final whe…

- **Tom Thornton:** This was fixed by https://github.com/apache/kafka/pull/17860

## KAFKA-18073: Data loss when exception is raised from Kafka Connect record conversion call
Bug · Resolved (Fixed) · Major · components: connect · labels: connect · created 2024-11-23 · resolved 2025-01-09

We are experiencing data loss when Kafka Connect source connector fails to send data to Kafka topic after receiving a retriable exception from a schema registry (when converting the record).
Kafka cluster & connect details:
 # Kafka Connect version: 3.8.1
 # Kafka Version 3.6.1
 # Cluster size: 16 brokers
 # Number of partitions in Kafka data topic: 32
 # Number of partitions in offsets topic: 
 # Replication Factor: 4
 # Min In Sync Replicas: 2
 # Unclean leader election disabled
 # U…

- **Tom Thornton:** Perhaps [~cegerton] any ideas on this? I saw your name in the Git history for the files that handle this logic
- **Tom Thornton:** The issue appears to be from errors.tolerance. We do not specify a config so it defaults to "none"
 [code/log omitted]
 However the connector is still skipping messages, as we see the Grafana metric 
 kafka_connect_task_error_metrics_total_records_skipped will start reporting skipped records when we…
- **Tom Thornton:** https://github.com/apache/kafka/pull/18146
- **Greg Harris:** Hmm, yeah this is a regression introduced by KAFKA-6738, added to 2.0.0. The PR and KIP say that it's backwards-compatible, but <2.0 RetriableExceptions caused tasks to fail, and >= 2.0 RetriableExceptions cause the record to be dropped.
 I think you can work-around this with a config: [https://kafk…
- **Tom Thornton:** [~gharris1727] Can we also backport to the other supported releases of 3.9, 3.8, and 3.7? I am happy to put out the PR to each respectively named branch.
- _…2 more comments_

## KAFKA-18074: Add kafka client compatibility matrix
Task · Resolved (Fixed) · Blocker · created 2024-11-23 · resolved 2025-03-12

in 4.0 we have many major breaking changes - JDK upgrade and protocol cleanup - that may confuse users in rolling upgrade and setup env. Hence, we should add a matrix for all our client modules - client, streams, and connect
the matrix consists of following item.
1. supported JDKs
2. supported broker versions

- **Ken Huang:** Hello, [~chia7712] , if you wont work on this, may I take the issue? Thank you.
- **Ken Huang:** JDK Compatibility Across Kafka Versions
 ||*Module*||*Kafka Version*||*Java 8*||*Java 11*||*Java 17*||*Java 23*||
 |*Client*|4.0.0|❌|✅|✅|✅|
 |*Streams*|4.0.0|❌|✅|✅|✅|
 |*Connect*|4.0.0|❌|❌|✅|✅|
 |*Server*|4.0.0|❌|❌|✅|✅|
 Server Compatibility
 ||*KRaft Cluster Version*||*Compatibility 4.0 Server (dyn…
- **Ismael Juma:** I made this a top level issue instead of a sub-task of KAFKA-14560 because it's broader than KAFKA-14560.
- **ASF GitHub Bot:** m1a2st opened a new pull request, #669: URL: https://github.com/apache/kafka-site/pull/669    After merge https://github.com/apache/kafka/pull/18091, we need to add footer for `compatibility-summary`
- **ASF GitHub Bot:** frankvicky commented on PR #669: URL: https://github.com/apache/kafka-site/pull/669#issuecomment-2716382989    before:
    ![image](https://github.com/user-attachments/assets/5961bf47-3e0d-4b38-b596-dd1b05e0ed77)
    after:
    ![image](https://github.com/user-attachments/assets/1224757b-78a2-4029-a…
- _…1 more comments_

## KAFKA-18264: Remove NotLeaderForPartitionException
Improvement · Resolved (Fixed) · Minor · created 2024-12-16 · resolved 2024-12-18

It is deprecated by KAFKA-10223 (4 years ago)

- **Nick Guo:** Hi [~chia7712] ,if you are not working on this,may I take over this?
- **Chia-Ping Tsai:** trunk: [https://github.com/apache/kafka/commit/21b7bb2265951d55efb8c0cb93340b664a5783a6]
 4.0: https://github.com/apache/kafka/commit/5a6e1204dd533af9f6f8072fe80330c5ea9f6fa7

## KAFKA-18265: Optimizing SharePartition locking to improve fetch speed
Sub-task · Resolved (Fixed) · Major · created 2024-12-16 · resolved 2025-11-18


## KAFKA-18266: Re-order validation for TimeIndex sanity check
Improvement · Resolved (Not A Problem) · Minor · labels: newbie · created 2024-12-16 · resolved 2025-01-20

Currently, when validating the sanity of TimeIndex, we perform multiple validations. With this change, we want to re-order the validations such that the expensive ones are performed at the end. 
i.e., we want to do [https://github.com/apache/kafka/blob/9cc1547672a8b261c08f453f45277265dfb44808/storage/src/main/java/org/apache/kafka/storage/internals/log/TimeIndex.java#L79] after [https://github.com/apache/kafka/blob/9cc1547672a8b261c08f453f45277265dfb44808/storage/src/main/java/org/apache/kafka/…

- **Pramithas Dhakal:** Hi [~jaytee] , if you're not working on this, may I take it? Thank you.
- **Jason Taylor:** Sure [~pramithas] i'll reassign it to you as I still have other open PR's i need to prioritise.
 Weirdly it won't let me assign it to you. [~divijvaidya] can u reassign please?

## KAFKA-18267: Add test for CloseOption
Test · Resolved (Fixed) · Minor · created 2024-12-16 · resolved 2025-05-03


## KAFKA-18268: Add metric for log cleaner thread busy percentage
Improvement · Open · Major · components: log cleaner · labels: kip · created 2024-12-16

*Background*
The number of cleaner threads (responsible for cleaning up/compacting topics which contains "compact") is configured using [https://kafka.apache.org/documentation.html#brokerconfigs_log.cleaner.threads] 
*Problem*
When the number of threads is in-adequate to handle the compaction load, the user will notice an increase in  `max-compaction-delay-secs` metric. However, an increase in this metric does not necessarily mean that the threads are overloaded. For example, this metric coul…


## KAFKA-18269: Remove deprecated protocol APIs support in 4.0 (KIP-724, KIP-896)
Sub-task · Resolved (Fixed) · Major · created 2024-12-16 · resolved 2024-12-21


## KAFKA-18270: SaslHandshake v0 and FindCoordinator v0 incorrectly tagged as deprecated
Sub-task · Resolved (Fixed) · Major · created 2024-12-16 · resolved 2024-12-21


## KAFKA-18271: Trigger CI when a PR is marked "ready for review"
Improvement · Open · Minor · components: build · created 2024-12-16

- **Ken Huang:** Hello, [~davidarthur]  , if you wont work on this, may I take the issue? Thank you

## KAFKA-18272: Deprecated protocol api usage should be logged at info level
Sub-task · Resolved (Fixed) · Major · created 2024-12-16 · resolved 2024-12-28

This would still be disabled by default while making it possible to enable them without enabling request logging for non deprecated apis.


## KAFKA-18273: Implement kafka-share-groups.sh --describe --verbose
Sub-task · Resolved (Fixed) · Major · created 2024-12-16 · resolved 2025-01-02

This is the share groups part of KIP-1099.


## KAFKA-18274: Failed to restart controller in testing due to closed socket channel
Bug · Resolved (Fixed) · Major · created 2024-12-17 · resolved 2025-01-13

In fact, there are three issues of restarting controller in testing.
1. we don't rebuild the metrics of `SharedServer` [0] - it causes NPE
2. we return the closed server socket [1]
3. we should return the new server socket bound with same port
```
            if (socketChannel != null && socketChannel.isOpen()) {
                return socketChannel;
            }
            // bind the server socket with same port
            if (socketChannel != null) {
                socketAddress…


## KAFKA-18388: test-kraft-server-start.sh should use log4j2.yaml
Improvement · Resolved (Fixed) · Blocker · created 2025-01-01 · resolved 2025-01-06

as title, and we should remove kraft-log4j.properties as well

- **PoAn Yang:** Hi [~chia7712], may I take this issue if you're not working on it? Thanks.
- **Chia-Ping Tsai:** trunk: https://github.com/apache/kafka/commit/a52aedd6ff9ade0230c0f41b473e8fbdfa2e0345
 4.0: https://github.com/apache/kafka/commit/efdfa0184259a41e0c22359df36a169c8d97214d

## KAFKA-18389: Do not lose votedKey on transition to LeaderState
Improvement · Patch Available · Minor · components: kraft · created 2025-01-02

After KAFKA-17642 is merged in, all epoch state transitions (other than the transition to Leader) will preserve votedKey and leaderId state. We should make the transition to LeaderState consistent with this.

- **Yunseop Eom:** Hi,
 I opened a PR for this issue:
 https://github.com/apache/kafka/pull/22203
 The patch preserves the candidate `votedKey` when transitioning to `LeaderState`. Previously, `LeaderState.election()` returned an elected-leader state with an empty `votedKey`, so the candidate's self-vote could be drop…
- **Yunseop Eom:** Follow-up on PR #22203: https://github.com/apache/kafka/pull/22203
 The latest commit, da42f3920a, removes the stale unrelated transition comment requested in review. The branch also contains the votedKey toString assertion, focused candidate-to-leader regression coverage, and concise LeaderState Ja…
- **Yunseop Eom:** PR #22203 is open and ready for maintainer review: https://github.com/apache/kafka/pull/22203

## KAFKA-18390: Use LinkedHashMap instead of Map in creating MetricName and SensorBuilder
Improvement · Open · Major · created 2025-01-02

see https://github.com/apache/kafka/pull/18232#discussion_r1900425014

- **Mickael Maison:** Moving to the next release as we're now in code freeze for 4.1.0.
- **Christo Lolov:** Moving to 4.3 since we are past the code freeze for 4.2! Let me know if I have misunderstood something!
- **Mickael Maison:** Moving to the next release as we're now in code freeze for 4.3.0.
- **Omnia Ibrahim:** Moving to 4.5 as we are now in 4.4.0 code freeze
- **Omnia Ibrahim:** I can see one PR merged and 2 closed so if this still no done I will move it to 4.5 feel free to change it back to 4.4 if you believe it is done and merged

## KAFKA-18391: Skip running "Flaky Test Report" job on forks
Improvement · Resolved (Fixed) · Minor · components: core · created 2025-01-02 · resolved 2025-01-17

Job
[code/log omitted]
keeps running and failing on forked repositories due to missing secrets
[code/log omitted]
Update ci to skip the run on forked repositories to decrease number of unnecessary emails and failed builds. 
!image-2025-01-02-12-28-26-839.png!


## KAFKA-18392: Require client-generated member IDs for ShareGroupHeartbeat
Sub-task · Resolved (Fixed) · Major · created 2025-01-02 · resolved 2025-01-22

This implements KIP-1082 for share groups.


## KAFKA-18393: Remove code deprecated to implement KIP-1043
Sub-task · Open · Blocker · components: clients · created 2025-01-02

The following deprecated code is removed in AK 5.0 (all in o.a.k.clients.admin package):
* Admin.listConsumerGroups
* ConsumerGroupDescription constructors
* ConsumerGroupDescription.state()
* ListConsumerGroupsOptions
* ListConsumerGroupsResult
* ConsumerGroupState
* ConsumerGroupListing


## KAFKA-18394: Formalize durable and in-memory election state changes
Improvement · Open · Major · components: kraft · created 2025-01-02

We essentially have two paths of epoch state transitions - 
1. one which involves updating on-disk election state and then in-memory epoch state (which includes in-memory election state changes)
2. one which does not involve any changed election state and just needs an in-memory epoch state change 
For the second case, we should explicitly check no persisted or in-memory election state has changed. For the first case, we should have the in-memory election state derive from the persisted elect…


## KAFKA-18395: Initialize KafkaRaftMetrics without QuorumState to prevent circularity
Improvement · Open · Major · components: kraft · created 2025-01-03

To implement https://issues.apache.org/jira/browse/KAFKA-16524, `QuorumState` needs to be removed from `KafkaRaftMetrics` constructor to avoid a circularity. That PR's approach is to move `QuorumState` to a `KafkaRaftMetrics#initialize` method for now.


## KAFKA-18396: Migrate log4j1 configuration to log4j2 in KafkaDockerWrapper
Improvement · Resolved (Fixed) · Blocker · created 2025-01-03 · resolved 2025-02-11

After log4j migration, we need to update the logging configuration in {{KafkaDockerWrapper}} from log4j1 to log4j2.

- **David Jacot:** [~frankvicky] Is this something that we must do in 4.0?
- **TengYao Chi:** Hi [~dajac] 
 In short, this is not a must-do item for version 4.0, as `log4j-1.2-api` already provides log4j1 compatibility mode for log4j2.
 The reason why this issue hasn't been addressed yet:
 In log4j1, we used properties files as the configuration format, which has a flat structure where new c…
- **Chia-Ping Tsai:** [~frankvicky] I think this is a blocker issue as by default we mount the log4j2 yaml - and users will expect those envs should work as before.
- **TengYao Chi:** I will try to get this done before next week.

## KAFKA-18397: Fix the scenario where acknowledgement callback is being called on null acknowledgements
Sub-task · Resolved (Fixed) · Major · created 2025-01-03 · resolved 2025-01-08

- **Shivsundar R:** [~peterxcli] , I have a fix for this, can I take this ticket up?
- **Chu Cheng Li:** Sure, thanks!

## KAFKA-18398: Log a warning if actual topic configs are inconsistent with the required topic configs
Task · Open · Major · components: streams · labels: kip1071 · created 2025-01-03

- **Matthias J. Sax:** I think we need to be careful with this ticket – cf the one I just linked.
 In general, we should really define what it absolutely necessary to check, and limit to these cases. Kafka Streams as always benefited to have good defaults, but not enforce them and give advanced users ways to change stuff.…
- **Lucas Brutschy:** It seems to me the linked ticket is all the more a reason to log a warning, right? If a certain internal topic is configured incorrectly because the topology was evolved, the user may want to fix that.
 [~mjsax] Do you suggest to not log a warning at all? Or do you think there is a subset of configs…
- **Matthias J. Sax:** I think there is two things:
  * Is there any actually _invalid_ configs, which we should disallow? For this case, we should maybe log a WARN (or even fail)?
  * If there is diff between code and configs, but it's a totally valid config, we should not log but just apply the config to the topic, and…
- **Lucas Brutschy:** Yes, we could make this slightly less annoying by distinguishing the invalid configs from non-default configs. Maybe it would still be good to output an "INFO" log for the non-default ones, as people may want to know about it. It also seems to be a "good" log message. It's perfectly clear and would…

## KAFKA-18595: Remove AuthorizerUtils#sessionToRequestContext
Sub-task · Resolved (Fixed) · Major · created 2025-01-19 · resolved 2025-01-22

This methods is unused since we are removing zk.

- **Christo Lolov:** The PR has been reviewed and merged both in trunk and 4.0

## KAFKA-18596: Cleanup LogConfig
Improvement · Closed (Fixed) · Major · created 2025-01-19 · resolved 2025-01-19

- **TengYao Chi:** I think this is a duplicate with 18544
 https://issues.apache.org/jira/browse/KAFKA-18544
 You can open a PR and link the old issue.

## KAFKA-18597: max-buffer-utilization-percent is always 0
Bug · Resolved (Fixed) · Minor · created 2025-01-19 · resolved 2025-01-27

see [https://github.com/apache/kafka/blob/516d5240b98916feb3e51c8a143dede05a4edad1/core/src/main/scala/kafka/log/LogCleaner.scala#L127]
  private def maxOverCleanerThreads(f: CleanerThread => Double): Int =
    cleaners.foldLeft(0.0d)((max: Double, thread: CleanerThread) => math.max(max, f(thread))).toInt
  /* a metric to track the maximum utilization of any thread's buffer in the last cleaning */
  metricsGroup.newGauge(MaxBufferUtilizationPercentMetricName,
    () => maxOverCleanerThreads…

- **Chia-Ping Tsai:** trunk: https://github.com/apache/kafka/commit/356f0d815cf99668e5acea427004bf01d8068439
- **Chia-Ping Tsai:** 3.9: [https://github.com/apache/kafka/commit/85658e5e33f550c6953ae58e37cc1808fd56b879]
 3.8: https://github.com/apache/kafka/commit/5ea660bf940a3d26cbcad414c2e523871543b94d

## KAFKA-18598: Remove ControllerMetadataMetrics zk related Metrics
Sub-task · Resolved (Fixed) · Blocker · created 2025-01-19 · resolved 2025-01-22

- **Christo Lolov:** The PR has been reviewed and merged both in trunk and in 4.0

## KAFKA-18599: Remove optional ForwardingManager in ApiVersionManager
Sub-task · Resolved (Fixed) · Major · created 2025-01-19 · resolved 2025-01-22

- **Ming-Yen Chung:** Hi [~chia7712] , Could you assign this ticket to me?

## KAFKA-18600: Cleanup NetworkClient zk related logging
Bug · Resolved (Fixed) · Major · created 2025-01-19 · resolved 2025-08-26


## KAFKA-18601: Assume a baseline of 3.3 for server protocol versions
Improvement · Resolved (Fixed) · Blocker · created 2025-01-19 · resolved 2025-02-19

3.3.0 was the first KRaft release that was deemed production-ready and also when KIP-778 (KRaft to KRaft upgrades) landed. Given that, it's reasonable for 4.x to only support upgrades from 3.3.0 or newer (the metadata version also needs to be set to "3.3" or newer before upgrading).


## KAFKA-18602: Incorrect FinalizedVersionLevel reported for dynamic KRaft quorum.
Bug · In Progress · Critical · components: controller, kraft · created 2025-01-20

*Environment:*
 * Kafka Version: kafka_2.12-3.9.0
 * Cluster Setup: 3-node KRaft controller quorum
 * Configuration File: {{dynamic.prop}}
[code/log omitted]
h3. Steps to Reproduce
 # Set up a 3-node KRaft controller quorum with the following parameters:
{{cluster_id="kr_0N6BSTUGeZdoBYBEpTQ"}}
{{controller_0_uuid="6fK9_aH-QAilLw-TBICXKw"}}
{{controller_1_uuid="twtzspDcQuOneF5cTtDMjQ"}}
{{controller_2_uuid="zytzspDcQuOneE5dTtDMjR"}}
 # Format the storage on each controller node: 
kafk…

- **PoAn Yang:** Hi [~abasilbr], if you're not working on this, may I take it? Thanks.
- **Aldan Brito:** hi [~yangpoan] ,
 yes you can
- **José Armando García Sancio:** Hi [~abasilbr] [~yangpoan] , I think this is duplicated by KAFKA-18920. I cherry picked that 3.9.1. If you agree, should we close this issue?
- **PoAn Yang:** Yes, I think we can close this. Thanks.

## KAFKA-18603: Maintain batch ordering in clients as per fetchBatchSize in ShareAcknowledgeRequests.
Sub-task · Resolved (Won't Fix) · Major · created 2025-01-20 · resolved 2025-02-17

After fetchBatchSize was implemented in the broker, we need to maintain the batch ordering in clients after we merge batches while sending ShareAcknowledge requests.

- **Shivsundar R:** The broker changes introduced here - https://issues.apache.org/jira/browse/KAFKA-18452 already fixes the issue. There is no change required in the clients side.

## KAFKA-18604: Update transaction coordinator
Sub-task · Resolved (Fixed) · Major · created 2025-01-20 · resolved 2025-01-21


## KAFKA-18605: Remove UnifiedLog#assignTopicId
Bug · Open · Major · created 2025-01-20

This method only used for ZK clusters when we update and start using topic IDs on existing topics


## KAFKA-18765: Custom StreamsPartitioner for auto-repartitioning
Improvement · Open · Minor · components: streams · labels: needs-kip · created 2025-02-10

There is currently no way to configure the {{StreamsPartitioner}} used by auto-repartitioning when using the Kafka Streams DSL. The default {{StreamsPartitioner}} is always used.
This can create a problem for users, whereby joining/aggregating with a stream/table that has been partitioned with a custom partitioner may not work as expected, if the user does not explicitly {{repartition()}} the stream first with the custom {{{}StreamsPartitioner{}}}.

- **Nicholas Telford:** A simple solution might be to add an optional {{Joined<K, V, VO> withAutoStreamPartitioner(StreamPartitioner partitioner)}} to {{Joined}} and friends, that enables the configuration of the automatic repartitioning, but only if auto-repartitioning takes place (i.e. it does not force a repartition if…

## KAFKA-18766: Docs: Make usage of allow.everyone.if.no.acl.found config clearer
Improvement · Resolved (Fixed) · Minor · components: documentation · labels: newbie · created 2025-02-10 · resolved 2026-05-20

h2. *Motivation*
In the documentation today, we have the following sentence:
{quote}By default, if no ResourcePatterns match a specific Resource R, then R has no associated ACLs, and therefore no one other than super users is allowed to access R. If you want to change that behavior, you can include the following in server.properties.
{quote}
Although, it is correct, I have observed users being confused by it. I think could me made clearer that default is deny and this property is a way to ch…

- **Mingdao Yang:** Hi [~divijvaidya] I'd be interested in working on this one if that's alright. Can I take this up?
- **Divij Vaidya:** [~mingdaoy] of course. In general, you don't need to ask for permission to pick up tasks. If you see a Jira with "unassigned" assignee, you can feel free to assign it to yourself and start working on it.
- **oshione gabriel esiemokhai:** Hello [~divijvaidya] please could you check the pull request submitted

## KAFKA-18767: Add client side config check for shareConsumer
Sub-task · Resolved (Fixed) · Major · components: clients, consumer · labels: queues-for-kafka · created 2025-02-10 · resolved 2025-02-18

See [https://cwiki.apache.org/confluence/display/KAFKA/KIP-932%3A+Queues+for+Kafka#KIP932:QueuesforKafka-Configuration]
Base on describe
```
The existing consumer configurations apply for share groups with the following exceptions:
 * {{auto.offset.reset}} : this is handled by a dynamic group configuration {{share.auto.offset.reset}} 
 * {{enable.auto.commit}}  and {{auto.commit.interval.ms}} : share groups do not support auto-commit
 * {{group.instance.id}} : this concept is not supported…

- **TaiJuWu:** If this is not legal, feel free to close this.
- **Lianet Magrans:** I think you have a good point! I was just working on the reconciliation path, and landed on this exact area this morning (related to the auto.commit). The config seems to be allowed, which is confusing (even though in practice there is no CommitReqMgr in place to auto-commit, and the ShareMembership…
- **TaiJuWu:** [~lianetm] Thanks for confirm!

## KAFKA-18768: Backport KAFKA-806 to 4.0
Sub-task · Resolved (Duplicate) · Major · created 2025-02-10 · resolved 2025-03-20

This is an enhancement, but it's not essential for 4.0.0.

- **PoAn Yang:** PR: https://github.com/apache/kafka/pull/18842
- **Chia-Ping Tsai:** https://github.com/apache/kafka/commit/4dd893ba212d05fb2201d884d962f0c0f81ebb10

## KAFKA-18769: Handle leader changes in client to ensure we do not send requests to the previous leader
Sub-task · Resolved (Fixed) · Major · created 2025-02-10 · resolved 2025-02-12

Handle leader changes in client to ensure we do not send requests to the previous leader. Currently we do try to send acknowledgements for records fetched from a previous leader. Now we will instead fail these acknowledgments with NOT_LEADER_OR_FOLLOWER exception in the clients itself.
This is in continuation to https://issues.apache.org/jira/browse/KAFKA-18618.


## KAFKA-18770: Fix flaky initializationError in ReplicationQuotasTest/RequestQuotaTest (thread leak)
Bug · Resolved (Fixed) · Major · components: core · labels: flaky-test · created 2025-02-10 · resolved 2025-02-10

An unexpected thread was detected in the recent CI.
 * ReplicationQuotasTest#initializationError
 * RequestQuotaTest#initializationError
[code/log omitted]
Failed CI:
 * [https://github.com/apache/kafka/actions/runs/13203924058]
 * [https://github.com/apache/kafka/actions/runs/13237077533/job/36944376672]

- **Chia-Ping Tsai:** The root cause of the test failures lies in the failure to close the {{ReplicaManager}} within the {{testDelayedShareFetchPurgatoryOperationExpiration}} method. This omission results in an unreleased thread from the purgatory, leading to subsequent integration test failures due to thread leaks.
- **Chia-Ping Tsai:** It is related to PR: https://github.com/apache/kafka/pull/18725/files#r1949798227

## KAFKA-18771: Flaky test KRaftClusterTest .testDescribeQuorumRequestToControllers
Test · Reopened · Critical · components: core, kraft, unit tests · labels: flaky-test · created 2025-02-10

Seeing this test failing very frequently on PR builds as flaky (so a re-run usually passes). But it very high noise ratio and we should look into it.

- **PoAn Yang:** Hi [~showuon], the test case was introduced by your PR https://github.com/apache/kafka/commit/612e1299e46ee72bcf763257e0d99dd9a2c48bf6. I can fix it by replacing shutdown raft client with shutdown the controller. Do you know why we want to shutdown raft client directly? If it's not required, I can f…
- **Luke Chen:** [~yangpoan] , I shutdown the client only because IIRC, if I shutdown the node, it won't get `
 NOT_LEADER_OR_FOLLOWER` error and retry. Is that what you saw?
- **PoAn Yang:** > Is that what you saw?
 No, I can run the test without error.
- **Lianet Magrans:** Hey folks, I'm seeing this failing again on PRs, e.g., [https://github.com/apache/kafka/actions/runs/27844911513/job/82413318361?pr=22629]
- **PoAn Yang:** Hi [~lianetm], I will take a look. Thank you.
- _…2 more comments_

## KAFKA-18772: Define share group config defaults for Docker
Sub-task · Resolved (Resolved) · Major · components: docker · created 2025-02-11 · resolved 2025-02-14

docker/examples/fixtures/file-input/server.properties is the Docker equivalent of config/server.properties. We should put the same values for share groups in the Docker config file. Also check the rest of the Docker resources to make sure none have been missed.

- **Jimmy Wang:** Hi [~schofielaj], I will handle this ticket, thanks.

## KAFKA-18773: Migrate the log4j1 config to log4j 2 for native image and README
Bug · Resolved (Fixed) · Blocker · created 2025-02-11 · resolved 2025-02-18

the script of native image is still using log4j1 properties
[https://github.com/apache/kafka/blob/trunk/docker/native/launch#L45]
[https://github.com/apache/kafka/blob/trunk/docker/native/launch#L51]
Also, the README should be updated too

- **PoAn Yang:** Hi [~chia7712], may I take the issue, if you're not working on it? Thank you.
- **Chia-Ping Tsai:** trunk: https://github.com/apache/kafka/commit/1132f08c57d46e80bc502965aa6d6330f85857bc
 4.0: https://github.com/apache/kafka/commit/546d9ce39bde54a393573a62babe3b0217b49052

## KAFKA-18774: Enhance the docs of adding/removing dynamic voter
Sub-task · Open · Minor · created 2025-02-11

in the section "Add New Controller" ([https://kafka.apache.org/documentation/#kraft_reconfig_add)] (and subsequent "Remove Controller") ,  we should remind users that the node running the command must be able to access the metadata folder defined by the `controller.properties`

- **Mingdao Yang:** Hi Chia-Ping, I'm interested in taking this one up, if that's alright.

## KAFKA-18775: MetadataQuorumCommand `add-controller`/`remove-controller` should get directory id and endpoint by Admin
Sub-task · Open · Major · labels: need-kip · created 2025-02-11

Currently, users are required to provide controller.properties to the MetadataQuorumCommand. This necessitates the MetadataQuorumCommand to parse the config to obtain the metadata local path and endpoint for adding or removing voters. This approach has several drawbacks:
1. Limited Accessibility: The node executing the tool must have direct access to the metadata path of the node being added or removed. This restricts the ability to use node A to manage node B, as node A may not have access to…

- **Kuan Po Tseng:** Hi [~chia7712] , are you working on this issue? If not, may I take over it? Thank you!

## KAFKA-18963: Error reading field 'user_data': java.nio.BufferUnderflowException
Bug · Open · Major · components: clients · created 2025-03-12

[code/log omitted]


## KAFKA-18964: Allow to set weights for controller nodes for leader election
Improvement · Open · Major · labels: needs-kip · created 2025-03-12

In the stretch cluster environment, the nodes are located in different data center for disaster recovery. So the backup cluster controller nodes should be served as the follower. Only when the disaster happened, the controller nodes in backup cluster need to be elected as leader. In our current design, the candidate node is randomly chosen. We can consider to apply the "weight" to the controller nodes to achieve the situation mentioned above.

- **TengYao Chi:** Hi [~showuon] 
 I'd like to take over this one.
 Do you think this needs a KIP?
- **Luke Chen:** Yes, this needs a KIP, and need some discussion about what are the good solutions for it. Thanks [~frankvicky] .
- **Luke Chen:** [~frankvicky] , forgot to say, welcome to propose your idea or share your thought!

## KAFKA-18965: Improve release validation for kafka-clients
Improvement · Patch Available · Major · components: build, clients, release · created 2025-03-12

It would be nice if we could improve (and automate!) some of the release validation for kafka-clients.
We can create sample projects which consume kafka-clients in different ways (Gradle, Maven, SBT, etc). This will let us validate several things
 * Downstream projects can be built with new JAR
 * Downstream projects can be run with new JAR
 * Our shaded dependencies are working properly (and not conflicting with the consuming project's dependencies)
 * Licenses are properly included in the…

- **Mickael Maison:** Moving to the next release as we're now in code freeze for 4.1.0.
- **Christo Lolov:** Moving to 4.3 since we are past the code freeze for 4.2! Let me know if I have misunderstood something!
- **Shekhar Prasad Rajak:** https://github.com/apache/kafka/pull/21915
- **Mickael Maison:** Moving to the next release as we're now in code freeze for 4.3.0.
- **Omnia Ibrahim:** Moving to 4.5 as we are now in 4.4.0 code freeze

## KAFKA-18966: Don't honor controller_num_nodes_override in combined controller test mode
Bug · Open · Major · created 2025-03-12

I found some flaky tests caused by the following test setup:
 # Using combined controller mode which means the broker will also host the controller.
 # Using 1 controller node. This is very common among the tests.
 # Testing hard bounce.
When the broker which hosts the controller is down, the whole controller service is down as well. It can take a long time to elect a new leader even if ISR has good candidates. This downtime costs unnecessary extra test time(due to unavailable partition) and…


## KAFKA-18967: Additional MetadataSchemaCheckerTool tests
Improvement · Patch Available · Major · created 2025-03-12

The tests for verify-evolution and verify-evolution-git test the same schemas against each other.
(KAFKA-18955 found a few bugs and we should confirm the above tests would have hit those bugs or write additional tests if not)

- **Yunseop Eom:** Update on PR #22946: https://github.com/apache/kafka/pull/22946
 The PR adds schema-evolution coverage with distinct parent and child specifications, exercises common-struct evolution through MetadataSchemaCheckerTool, and verifies that a field present in both message versions but missing from the c…
- **Yunseop Eom:** PR #22946 is open and ready for maintainer review: https://github.com/apache/kafka/pull/22946

## KAFKA-18968: Workflow Requested not working for pull_request_reviewed events
Bug · Open · Major · components: build · created 2025-03-12

We use the Workflow Requested workflow to automatically approve workflows from the community if the "ci-approved" label is set. 
Due to a quirk (deficiency) of the GitHub events schema, there is no easy way to determine the Pull Request for a given workflow. We previously did the following for pull_request events:
[code/log omitted]
However, this does not work with pull_request_reviewed events since the HEAD_REPO is set to apache/kafka instead of the PR's origin repository (another annoying "…


## KAFKA-18969: Rewrite ShareConsumerTest#setup by beforeEach and move ShareConsumerTest to clients-integration-tests module 
Improvement · Resolved (Fixed) · Major · created 2025-03-12 · resolved 2025-03-18

Using BeforeEach can ensure the `setup` is executed for each test case. Also, ShareConsumerTest can be moved from core module to clients-integration-tests module.


## KAFKA-18970: [kafka-clients] Gradle module metadata publication should be enabled
Task · Patch Available · Minor · components: build, clients · labels: Gradle, gradle, help-wanted, up-for-grabs · created 2025-03-12

(!) _*Prologue:*_ see this github  PR [https://github.com/apache/kafka/pull/18018#discussion_r1968540211]
(i) *_More details:_* while changing shadow plugin (KAFKA-18142) we were forced to disable Gradle module metadata publication for _*clients*_ submodule (i.e. for _*kafka-clients*_ artifacts):
 * [https://docs.gradle.org/8.10.2/userguide/publishing_gradle_module_metadata.html#sub:disabling-gmm-publication]
 * [https://github.com/apache/kafka/commit/e3080684c08c1832b172f9ec3183a2c238306ff2#…

- **Yunseop Eom:** Update on PR #22948: https://github.com/apache/kafka/pull/22948
 The PR enables Gradle Module Metadata publication for kafka-clients so Gradle consumers can resolve published variants and capabilities.
 Validation completed:
 - :clients:generateMetadataFileForMavenJavaPublication
 - :clients:check e…
- **Yunseop Eom:** PR #22948 is open and ready for maintainer review: https://github.com/apache/kafka/pull/22948

## KAFKA-18971: Update AK system tests for AK 4.0
Task · Resolved (Won't Do) · Major · components: streams · created 2025-03-12 · resolved 2025-04-02

Update AK system tests and add new “upgrade_from” version to {{StreamsConfig}}

- **Matthias J. Sax:** Seems this is already done: [https://github.com/apache/kafka/pull/19239]
- **Alieh Saeedi:** Already done!

## KAFKA-18972: Custom Processor supplied on addReadOnlyStateStore is not used when restoring state from topic
Bug · Patch Available · Major · components: streams · created 2025-03-12

As a Streams Developer, I have added a custom read-only state store ([KIP-813|https://cwiki.apache.org/confluence/display/KAFKA/KIP-813%3A+Shareable+State+Stores]) via {{Topology#addReadOnlyStateStore(_)}} to my Topology, using a custom Processor for state updates ({{{}ProcessorSupplier<KIn, VIn, Void, Void> stateUpdateSupplier{}}}).
*Expected behaviour:* As per JavaDocs, "the Processor should contain logic to keep the StateStore up-to-date". Therefore, it should be used for processing and pers…


## KAFKA-18973: Review MetadataSchemaCheckerToolTest.testVerifyEvolutionGit requiring git project
Test · Resolved (Fixed) · Major · created 2025-03-13 · resolved 2025-10-22

While testing a release candidate we noticed that the fact that the test testVerifyEvolutionGit requires a git directory, causes that running tests on a release source folder after download doesn't work anymore (as it used to in previous versions). As of 4.0 it fails with: {_}java.lang.RuntimeException: Invalid directory, need to be within a Git repository{_}.
This started failing on 4.0 which is the first release to include this test.

- **PoAn Yang:** Hi [~lianetm], if you're not working on this, may I take it? Thanks.
- **Lianet Magrans:** Sure, thanks!
- **Mickael Maison:** Moving to the next release as we're now in code freeze for 4.1.0.
- **Arpit Goyal:** [~yangpoan]  I am unasisgning it , as i see no activity in the last 2 month.
- **Arpit Goyal:** https://github.com/apache/kafka/pull/20703
- _…1 more comments_

## KAFKA-19130: Do not add fenced brokers to BrokerRegistrationTracker on startup
Bug · Resolved (Fixed) · Minor · created 2025-04-11 · resolved 2025-07-01

When the controller starts up (or becomes active after being inactive), we add all of the
registered brokers to BrokerRegistrationTracker so that they will not be accidentally fenced the
next time we are looking for a broker to fence. We do this because the state in
BrokerRegistrationTracker is "soft state" (it doesn't appear in the metadata log), and the newly
active controller starts off with no soft state. (Its soft state will be populated by the brokers
sending heartbeat requests to it…

- **Mickael Maison:** The PR has been merged, marking as resolved.

## KAFKA-19131: Exception thrown while updating the RemoteLogReader threads
Bug · Resolved (Fixed) · Minor · created 2025-04-12 · resolved 2025-04-25

RemoteLogManager throws error when increasing the thread count for remote reads. 
Command:
[code/log omitted]
Exception:
[code/log omitted]
https://sourcegraph.com/github.com/apache/kafka/-/blob/storage/src/main/java/org/apache/kafka/storage/internals/log/RemoteStorageThreadPool.java?L43

- **Kamal Chandraprakash:** [~yangpoan] 
 Are you working on this issue? Thanks!
- **PoAn Yang:** [~ckamal] yes, I'm working on it. I will create a PR today. Thanks.

## KAFKA-19132: Move FetchSession and related classes to server module
Sub-task · Resolved (Fixed) · Minor · created 2025-04-12 · resolved 2026-01-29

https://github.com/apache/kafka/blob/trunk/core/src/main/scala/kafka/server/FetchSession.scala


## KAFKA-19133: Support fetching for multiple remote fetch topic partitions in a single share fetch request
Sub-task · Resolved (Fixed) · Major · created 2025-04-12 · resolved 2025-05-05

As part of KAFKA-19019, we are adding support for remote storage fetch for share groups.
However, there is a limitation in remote storage fetch for consumer groups ([mailing list thread|https://lists.apache.org/thread/m03mpkm93737kk6d1nd6fbv9wdgsrhv9]) that we can only perform remote fetch for a single topic partition in a fetch request. Since, the logic of share fetch requests is largely based on how consumer groups work, we are following the same logic.
As part of this JIRA, we should be abl…


## KAFKA-19134: Implementation of a Simple, Low-Latency Bounded Shared Buffer
New Feature · Open · Major · created 2025-04-12

Using the shared buffer in the network threads can reduce the GC count (and elapsed time). The attached patch offers a simple memory pool based on ConcurrentSkipListMap, and in my small env (1000000000 records), the GC time is reduced from 127.808 ms to 93.608 ms), and the created bytes are reduced from 40GB to 2GB.

- **Chia-Ping Tsai:** will file a KIP with more details later

## KAFKA-19135: Add IQ Support - move from feature branch
Sub-task · Resolved (Fixed) · Major · components: streams · created 2025-04-13 · resolved 2025-04-30

This initial ticket for IQ support is for moving IQ support from feature branch to trunk


## KAFKA-19136: Move metadata-related configs from KRaftConfigs to MetadataLogConfig
Improvement · Resolved (Fixed) · Minor · created 2025-04-14 · resolved 2025-04-17

Most config class consists of definition and POJO, so we should merge MetadataLogConfig with KRaftConfigs

- **Chia-Ping Tsai:** # rename KRaftConfigs to KRaftConfig
  # move related getters from KafkaConfig to KRaftConfig
  # move variables from MetadataLogConfig to KRaftConfig
  # remove MetadataLogConfig
- **Ismael Juma:** Hmm, there are two separate things:
  # Server configs related to kraft (things like process.roles)
  # Metadata related configs
 I don't think these should be the same. `1` should to be in `server` while `2` should be in `metadata`.
- **Chia-Ping Tsai:** [~ijuma] thanks for quick response. you are right that KRaftConfigs has some server-related configs, so merging them is not good idea. We should extract the metadata-related configs from KRaftConfigs to MetadataLogConfig.  Also, we can move node.id from MetadataLogConfig to KafkaMetadataLog's constr…

## KAFKA-19137: Use `StandardCharsets.UTF_8` instead of `StandardCharsets.UTF_8.name()`
Improvement · Resolved (Fixed) · Minor · created 2025-04-14 · resolved 2025-04-15

The checked exception {{UnsupportedEncodingException}} for {{StandardCharsets.UTF_8.name()}} can be avoided by using {{StandardCharsets.UTF_8}} directly.

- **kangning.li:** [~chia7712]    If you have not started on this issue, cloud you assign it to me ?

## KAFKA-19138: Kafka service is continuously restarting in one of the nodes in 3 node cluster
Bug · Open · Major · created 2025-04-14

Apache.kafka.controller.ReplicationControlManager)
Apr 10 07:23:12 localhost kafka[1303882]: [2025-04-10 04:23:12,167] ERROR Encountered fatal fault: Error loading metadata log record from offset 9930471116 (org.apache.kafka.server.fault.ProcessTerminatingFaultHandler)
Apr 10 07:23:12 localhost kafka[1303882]: java.lang.IllegalStateException: Tried to change broker 3, but the given epoch, 9915562, did not match the current broker epoch, 9914910
Apr 10 07:23:12 localhost kafka[1303882]: #011at…


## KAFKA-19139: Plugin#wrapInstance should use LinkedHashMap instead of Map 
Sub-task · Resolved (Fixed) · Major · created 2025-04-14 · resolved 2025-05-11

See discussion: https://github.com/apache/kafka/pull/19050#discussion_r2041133707

- **Ken Huang:** Hi [~mimaison], just to confirm—should I update the KIP page and then send an email to the vote thread?
- **Mickael Maison:** Yes

## KAFKA-19140: ConnectAssignor#performAssignment second parameter can be replace from String to ConnectProtocolCompatibility
Improvement · Resolved (Fixed) · Minor · created 2025-04-14 · resolved 2025-06-19

The protocol type; for Connect assignors this is "eager", "compatible", or "sessioned"
It is as same as ConnectProtocolCompatibility, thus we could change to use ConnectProtocolCompatibility

- **Atul Sharma:** Hi [~m1a2st]... if you are not looking into this can i pick this up?
- **Ken Huang:** Sorry [~atusharm], I will do this one, feel free to grab another issue.

## KAFKA-19246: OffsetFetch API does not return group level errors correctly with version 1
Bug · Resolved (Fixed) · Blocker · created 2025-05-06 · resolved 2025-06-26

The OffsetFetch API with version 1 does not correctly return group level errors such as NOT_COORDINATOR. The following test case demonstrate the issue.
[code/log omitted]
Here is the output:
[code/log omitted]
The issue is here: https://github.com/apache/kafka/pull/19642#discussion_r2074839488.

- **Mickael Maison:** [~dajac] Are you still planning to get this in 4.1.0?
- **David Jacot:** [~mimaison] I completely forgot about it. I actually have an approved PR ready to be merged for it. Do you mind if I cherry-pick it to 4.1 branch?
- **Mickael Maison:** If it's ready and low risk, go for it.
- **David Jacot:** [~mimaison] Done!
- **Mickael Maison:** Thanks!

## KAFKA-19247: Move SchedulerTest to server-common module
Improvement · Resolved (Duplicate) · Major · created 2025-05-06 · resolved 2025-05-06

Move SchedulerTest to server common module and rewrite to Java

- **Ken Huang:** Duplicate with KAFKA-19182

## KAFKA-19248: Plugins Test for Multiversioning in Kafka Connect
Improvement · Resolved (Fixed) · Major · components: connect · created 2025-05-06 · resolved 2025-07-09

Add tests for plugin level isolation for Kafka connect (KIP-891).

- **Mickael Maison:** The PR is merged, marking this as resolved
