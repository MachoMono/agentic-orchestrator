## KAFKA-14011: Reduce retention.ms from default 7 days to 1 day (Make it configurable) for the dead letter topic created for error handling via sink connector
Improvement · Open · Major · components: config, connect · created 2022-06-20

We are creating a sink connector along with the error handling mechanism , so if in case if there is bad record it is routed to error queue , The properties used while creating the sink connector are as following
 'errors.tolerance'='all',
 'errors.deadletterqueue.topic.name' = 'error_dlq',
 'errors.deadletterqueue.topic.replication.factor'= -1,
 'errors.log.include.messages' = true,
 'errors.log.enable' = true,
 'errors.deadletterqueue.context.headers.enable' = true
*now is there any way…

- **Jordan Moore:** "topic.creation" configs are only available for source connectors, for topics that source connectors will write to, not dead letter topics. "admin" prefix will only attempt to modify the AdminClient config, which does not include any topic configs, such as retention time. 
 If you are allowing the b…

## KAFKA-14012: passing a "method" into the `Utils.closeQuietly` method cause NPE
Bug · Resolved (Fixed) · Major · components: connect · created 2022-06-20 · resolved 2022-08-20

Utils.closeQuietly method accepts `AutoCloseable` object, and close it. But there are some places we passed "method" into Utils.closeQuietly, which causes the object doesn't get closed as expected. 
I found it appeared in:
- WorkerConnector
- AbstractWorkerSourceTask
- KafkaConfigBackingStore

- **Chris Egerton:** [~showuon] when does this no-op occur? The bugs that I've found related to {{Utils::closeQuietly}} have been NPEs caused by method references of null objects; I believe as long as the object is non-null and the correct method is referenced, things should go smoothly.
- **Luke Chen:** You're right, it will be NPE after passing in the "method" as parameter. Thanks for correction. I've updated the JIRA.

## KAFKA-14013: Limit the length of the `reason` field sent on the wire
Improvement · Resolved (Fixed) · Blocker · created 2022-06-20 · resolved 2022-07-12

KIP-800 added the `reason` field to the JoinGroupRequest and the LeaveGroupRequest as I mean to provide more information to the group coordinator. In https://issues.apache.org/jira/browse/KAFKA-13998, we discovered that the size of the field is limited to 32767 chars by our serialization mechanism. At the moment, the field either provided directly by the user or constructed internally is directly set regardless of its length.
Given the purpose of this field, it seems acceptable to only sent the…


## KAFKA-14014: Flaky test NamedTopologyIntegrationTest.shouldAllowRemovingAndAddingNamedTopologyToRunningApplicationWithMultipleNodesAndResetsOffsets()
Test · Resolved (Fixed) · Critical · components: streams · labels: flaky-test · created 2022-06-21 · resolved 2023-11-27

[code/log omitted]
https://ci-builds.apache.org/job/Kafka/job/kafka-pr/job/PR-12310/2/testReport/junit/org.apache.kafka.streams.integration/NamedTopologyIntegrationTest/Build___JDK_11_and_Scala_2_13___shouldAllowRemovingAndAddingNamedTopologyToRunningApplicationWithMultipleNodesAndResetsOffsets/
https://ci-builds.apache.org/job/Kafka/job/kafka-pr/job/PR-12310/2/testReport/junit/org.apache.kafka.streams.integration/NamedTopologyIntegrationTest/Build___JDK_17_and_Scala_2_13___shouldAllowRemoving…

- **Matthew de Detrich:** So interestingly I worked on another ticket that reported the exact same test as being flaky (see https://issues.apache.org/jira/browse/KAFKA-13531) and I couldn't reproduce any flakiness (hence the reason why that ticket is closed).
 I rebased my fork of Kafka to the latest version in trunk and sta…
- **Matthew de Detrich:** Okay so I just noticed the linked builds with different JDK versions (11/17 versus my 16) so I will rerun the tests using those JDK versions to see if I can simulate the CI.
- **Matthew de Detrich:** So I ran the tests overnight with JDK 11 and have no failure with ~10k runs, I suspect that JDK 17 will also provide the same result.
 This means that a few more possibilities are opened up when it comes to why I may not be able to reproduce the failure locally
 1. This is gradle specific (going to…
- **Bruno Cadonna:** [~mdedetrich-aiven] Thank you for looking into this!
 KAFKA-13531 reported the same test but the failure was different. It could also be that the test was refactored and the message changed.
 I saw this failure a lot in the CI builds.
 I would bet on point 3 in your list. However, I would also not e…
- **Matthew de Detrich:** [~cadonna] So I did some debugging on this ticket over the past week and I found out some interesting things.
 To start off with I did manage to predictably replicate the test's flakiness and it does appear to be related to load, i.e. the test is more flaky the less CPU resources it has. I am using…
- _…6 more comments_

## KAFKA-14015: ConfigProvider with ttl fails to restart tasks
Bug · Resolved (Fixed) · Major · components: connect · created 2022-06-21 · resolved 2022-09-06

According to the [KIP-297|https://cwiki.apache.org/confluence/display/KAFKA/KIP-297%3A+Externalizing+Secrets+for+Connect+Configurations#KIP297:ExternalizingSecretsforConnectConfigurations-SecretRotation]:
{quote} * When the Herder receives the onChange() call, it will check a new connector configuration property config.reload.action which can be one of the following:
 ** The value restart, which means to schedule a restart of the Connector and all its Tasks. This will be the default.
 ** The…

- **Sagar Rao:** [~rozza] , Thanks for filing this issue. There seems to be a mismatch in what the KIP talks about and what's happening in the code indeed. I think the `restartConnectorAndTasks` was added well after the KIP was written. Just curious, have you noticed that tasks continue working with outdated configu…
- **Yash Mayya:** Hm this looks like it maybe a bug in the StandaloneHerder. In the DistributedHerder, [restartConnector calls startConnector|https://github.com/apache/kafka/blob/38103ffaa962ef5092baffb884c84f8de3568501/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/distributed/DistributedHerder.java#…
- **Yash Mayya:** In essence, this should work as expected when Connect is being run in distributed mode. In standalone mode, it looks like there is a similar flow [here|https://github.com/apache/kafka/blob/38103ffaa962ef5092baffb884c84f8de3568501/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/standal…

## KAFKA-14016: Revoke more partitions than expected in Cooperative rebalance
Bug · Resolved (Fixed) · Major · components: clients · labels: new-rebalance-should-fix · created 2022-06-23 · resolved 2023-05-03

In https://issues.apache.org/jira/browse/KAFKA-13419 we found that some consumer didn't reset generation and state after sync group fail with REABALANCE_IN_PROGRESS error.
So we fixed it by reset generationId (no memberId) when  sync group fail with REABALANCE_IN_PROGRESS error.
But this change missed the reset part, so another change made in https://issues.apache.org/jira/browse/KAFKA-13891 make this works.
After apply this change, we found that: sometimes consumer will revoker almost 2/3 of…

- **Guozhang Wang:** Thanks [~aiquestion] for filing this ticket! Also cc [~kirktrue] [~philipnee] to bring to their radar.
- **Guozhang Wang:** In the long run, as we refactored our rebalance protocol (KIP incoming :) this issue should be gone as we would not have REBALANCE_IN_PROGRESS anymore, since the brokers take full responsibility on the installation of the new assignment.
 At the moment, though, I feel changing the broker code may no…
- **Shawn Wang:** [~guozhang] do you mean, set assignment's generation to current generation if client get a REBALANCE_IN_PROGRESS in syncGroupResponse?
 Yes, I think that can work.  Client will ignore 1 round of assignment
  * if the assignment is adding partition: the partition will be paused 1 more round of rebala…
- **A. Sophie Blee-Goldman:** Hey, I realize there's a lot of history leading up to this issue and the associated "fix", so forgive me for missing anything while I'm getting up to speed – but taking a step back, before we jump into the discussion about alternative fixes for KAFKA-13891 can we flesh out the actual underlying prob…
- **Luke Chen:** [~ableegoldman] , thanks for the comment. Yes, we have the logic in sticky assignor to protect multiple consumer claiming the same partition in the same highest generation. The original thought is that the same logic didn't exist in custom assignor. But after [KIP-792|https://cwiki.apache.org/conflu…
- _…14 more comments_

## KAFKA-14017: File source connector should implement KIP-618 APIs
Improvement · Resolved (Done) · Minor · components: connect · created 2022-06-24 · resolved 2022-12-01

The file source connector that comes out of the box with Kafka Connect should implement the new APIs added by KIP-618, as an example for both connector developers and Connect users.


## KAFKA-14018: Kafka SSL can't support p12 certificate using sha256 on jdk8
Improvement · Open · Minor · components: clients · created 2022-06-24

Our partner changed the encryption algorithm of the p12  certificate from SHA1 to SHA256 for some reason. As a result, Kafka reported a connection error due to the wrong password.But we found the root cause is that the keytool of JDK8 does not support this encryption format.
I would like to open a PR to contribute some code to support this case


## KAFKA-14019: removeMembersFromConsumerGroup can't delete all members when there is no members already
Bug · Open · Minor · created 2022-06-24

The root cause is that the method fetch no member from server, so it fails to construct RemoveMembersFromConsumerGroupOptions (it can't accept empty list)
It seems to me deleting all members from a "empty" list is valid.

- **Kvicii.Yu:** [~chia7712]  hi, your meaning we need change this RemoveMembersFromConsumerGroupOptions#removeAll method? If we do this, what correct things we can do?

## KAFKA-14020: Performance regression in Producer
Bug · Resolved (Fixed) · Blocker · components: producer  · created 2022-06-24 · resolved 2022-07-20

[https://github.com/apache/kafka/commit/f7db6031b84a136ad0e257df722b20faa7c37b8a] introduced a 10% performance regression in the KafkaProducer under a default config.
The context for this result is a benchmark that we run for Kafka Streams. The benchmark provisions 5 independent AWS clusters, including one broker node on an i3.large and one client node on an i3.large. During a benchmark run, we first run the Producer for 10 minutes to generate test data, and then we run Kafka Streams under a nu…

- **John Roesler:** {color:#1d1c1d}FYI, just setting the partitioner back to the {color}{{DefaultPartitioner}}{color:#1d1c1d} does not appear to help. The throughput of that test was 105k±2k records per second.{color}
 {color:#1d1c1d}Code under test: {color}[https://github.com/apache/kafka/commit/6c67adb8beedafca0316d1…
- **John Roesler:** Hey [~alivshits] , thanks for your work on [https://github.com/apache/kafka/pull/12365] .
 I've just re-run the same benchmark above and confirmed that your PR fixes the perf regression. Thank you!
 As a reminder, this was the baseline for "good" performance:
 Commit: [{{e3202b9}}|https://github.com…
- **Jun Rao:** merged the PR to 3.3.

## KAFKA-14072: Crashed MirrorCheckpointConnector appears as running in REST API
Bug · Resolved (Fixed) · Major · components: connect, mirrormaker · created 2022-07-12 · resolved 2023-01-06

In one cluster I had a partially crashed MirrorCheckpointConnector instance. It had stopped mirroring offsets and emitting metrics completely but the connector and its single task were still reporting as running in the REST API.
Looking at the logs, I found this stacktrace:
[code/log omitted]
Not sure if it's related but prior this exception, there's quite a lot of:
[code/log omitted]
and some users had started consumers in the target cluster hence causing these log lines:
[code/log omitte…

- **Mickael Maison:** This looks like it's the same issue as KAFKA-14545

## KAFKA-14073: Logging the reason for creating a snapshot
Improvement · Resolved (Fixed) · Minor · labels: kraft, newbie · created 2022-07-13 · resolved 2022-09-13

So far we have two reasons for creating a snapshot. 1. X bytes were applied. 2. the metadata version changed. we should log the reason when creating snapshot both in the broker side and controller side. see https://github.com/apache/kafka/pull/12265#discussion_r915972383

- **Ashmeet Lamba:** Hi, I am new to Kafka and noticed that this issue is tagged as newbie. I would like to pick this issue up.
 I have gone through the PR attached. I also did go through the KRaft's README.
 Reading through the code base I believe the changes required would be in this file - [BrokerMetadataListener|htt…

## KAFKA-14074: Restarting a broker during re-assignment can leave log directory entries in ZK mode
Bug · Open · Major · created 2022-07-14

Re-starting a broker while replicas are being assigned away from the broker can result in topic partition directories being left in the broker’s log directory. This can trigger further problems if such a topic is deleted and re-created. These problems occur when replicas for the new topic are placed on a broker that hosts a “stale” topic partition directory of the same name, causing the on-disk topic partition state held by different brokers in the cluster to diverge.
We have also been able to…

- **Justine Olshan:** Thanks for bringing this up [~prestona]. This issue has been brought to my attention for ZK clusters but not KRaft as well. KRaft was built to better handle this issue it seems. I have been looking into ways to mitigate the issue in ZK clusters.
- **Justine Olshan:** Is this the same issue as https://issues.apache.org/jira/browse/KAFKA-13972?
- **Adrian Preston:** Thanks for pointing out KAFKA-13972, [~jolshan]. Unfortunately I don't think this is exactly the same problem. I've built the branch corresponding to the pull request in KAFKA-13972 ([https://github.com/apache/kafka/pull/12271)], and can still reproduce the stray topic partition directories problem…

## KAFKA-14075: Consumer Group deletion does not delete pending transactional offset commits
Bug · Open · Major · created 2022-07-14

In [GroupMetadata.removeAllOffsets()|https://github.com/apache/kafka/blob/trunk/core/src/main/scala/kafka/coordinator/group/GroupMetadata.scala#L729-L740] we pass in the offsets cache to delete pendingTransactionalOffsetCommits upon group deletion. So only transactional offset commits for topic partitions already in the offsets cache will be deleted.
However, we add a transactional offset commit to the offsets cache only after the commit/abort marker is written to the log in [GroupMetadata.comp…


## KAFKA-14076: Fix issues with KafkaStreams.CloseOptions
Bug · Resolved (Fixed) · Blocker · created 2022-07-14 · resolved 2022-07-21

The new `close(CloseOptions)` function has a few bugs.  ([https://github.com/apache/kafka/blob/trunk/streams/src/main/java/org/apache/kafka/streams/KafkaStreams.java#L1518-L1561)]
Notably, it needs to remove CGs per StreamThread.

- **Jim Hughes:** CloseOptions was introduced in https://github.com/apache/kafka/commit/9dc332f5ca34b80af369646f767c40c6b189f831.
- **Matthias J. Sax:** Marking this as blocker for 3.3, because this fixes KIP-812 which has a broken implementation right now. We need to either get this merger or revert the KIP.

## KAFKA-14077: KRaft should support recovery from failed disk
Bug · Resolved (Fixed) · Blocker · components: kraft · created 2022-07-14 · resolved 2024-11-12

If one of the nodes in the metadata quorum has a disk failure, there is no way currently to safely bring the node back into the quorum. When we lose disk state, we are at risk of losing committed data even if the failure only affects a minority of the cluster.
Here is an example. Suppose that a metadata quorum has 3 members: v1, v2, and v3. Initially, v1 is the leader and writes a record at offset 1. After v2 acknowledges replication of the record, it becomes committed. Suppose that v1 fails be…

- **A. Sophie Blee-Goldman:** [~hachikuji] [~jagsancio] what's the status here, can we bump this to 3.5.0 or is someone working on this as an active blocker for 3.4?
- **Mickael Maison:** The associated KIP is not voted yet, so moving to 3.6.0.
- **Stanislav Kozlovski:** I asked [~jagsancio] and [~hachikuji] for what we should target. As there hasn't been much movement non this KIP from what I can tell in the discussion thread since 2022, I will remove the Fix Version to avoid having to bump it every release
- **Colin McCabe:** KIP-853 shipped in Apache Kafka 3.9

## KAFKA-14078: Replica fetches to follower should return NOT_LEADER error
Bug · Resolved (Fixed) · Major · created 2022-07-15 · resolved 2022-07-25

After the fix for KAFKA-13837, if a follower receives a request from another replica, it will return UNKNOWN_LEADER_EPOCH even if the leader epoch matches. We need to do epoch leader/epoch validation first before we check whether we have a valid replica.


## KAFKA-14079: Source task will not commit offsets and develops memory leak if "error.tolerance" is set to "all"
Bug · Resolved (Fixed) · Critical · components: connect · created 2022-07-16 · resolved 2022-07-18

KAFKA-13348 added the ability to ignore producer exceptions by setting {{error.tolerance}} to {{{}all{}}}.  When this is set to all a null record metadata is passed to commitRecord() and the task continues.
The issue is that records are tracked by {{SubmittedRecords}} and the first time an error happens the code does not ack the record with the error and just skips it so it will not have the offsets committed or be removed from SubmittedRecords before calling commitRecord(). 
This leads to a b…

- **Christopher L. Shannon:** I submitted a fix for the 3.2.x branch. The fix is relevant to 3.3.0 as well but a lot of refactoring was done for KAFKA-10000 so if the community agrees this is a good fix I can also create another PR for trunk to fix it there as well.
- **Chris Egerton:** [~cshannon] is it correct to say that, in addition to leaking resources, another consequence of this bug is that source tasks become unable to commit some or all source offsets? It might be worth updating the title to reflect that since, in addition to the increased memory utilization we'd expect fr…
- **Christopher L. Shannon:** [~ChrisEgerton] - I agree, I updated the title and description and pushed a new PR update.
- **Randall Hauch:** Following up with some additional detail:
 This issue can affect users that are upgrading to AK 3.2.0, even if they don't modify any Connect worker config or connector configurations. For example, if a user has a pre-AK 3.2.0 Connect installation running with one or more source connector configurati…
- **Randall Hauch:** Merged to the `3.3` branch with permission from the 3.3 release manager.

## KAFKA-14080: too many node disconnected message in kafka-clients
Bug · Open · Major · components: clients · created 2022-07-18

when upgrade kafka-clients from 3.0.1 to 3.1.1, there are a lot of "Node 0 disconnected" message in networkclient  per day per listener(20-30k)
think it is introduced by
[https://github.com/a0x8o/kafka/commit/cf22405663ec7854bde7eaa3f22b9818c276563f]
questions:
 # is it normal with so many "Node X disconnected" message at INFO level? my kafka server has any issue?
 # it mentioned a back-off configuration to reduce the message, but does it work?(still so many messages)

- **Philip Bourke:** same issue as https://issues.apache.org/jira/browse/KAFKA-13679
- **Nicolas Guyomar:** I'm only now noticing some bugs were created for that log, I submitted recently a PR to lower those idle connection disconnect logs at DEBUG with a more intuitive message [https://github.com/apache/kafka/pull/16089]

## KAFKA-14081: Cannot get my MetricsReporter implementation to receive meaningful metrics
Bug · Patch Available · Minor · components: clients · created 2022-07-18

I want to extract metrics from KafkaProducer to export them to our company monitoring solution. At first I went for implementing {{MetricsReporter}} and registering my implementation through the "metric.reporters" config property. The class is correctly registered as it receives metric updates through {{metricChange()}} while KafkaProducer is being used. The problem is that all the metric values are stuck at zero (NaN in older versions of Kafka), even the most trivial (e.g. 'record-send-total').…

- **Kirk True:** Would you be able to share steps and/or some code that reproduces the issue?
- **Gian Luca:** This is my report implementation:
 [code/log omitted]
 And this is the main class:
 [code/log omitted]
 On execution, the values of the 'request-total' metric are notified once (through the metricChange() method) with value 0.0, then no more updates happen.
- **Rens Groothuijsen:** I had a look at the source code, and it does appear that {{metricChange()}} is only being called when adding a metric, not when a metric changes. Given that the documentation of {{metricChange()}} says otherwise, I assume this was accidentally removed at some point.
- **Bruno Cadonna:** [~janlooka] what [~RensGroothuijsen] writes sounds correct! You can also look at the [JmxReporter|https://github.com/apache/kafka/blob/f46d4f4fce341326c06c0aa8b2d0d64982573658/clients/src/main/java/org/apache/kafka/common/metrics/JmxReporter.java#L140] for confirmation. The documentation of {{metric…
- **Gian Luca:** Hi Rens and Bruno, thanks for the explanation, now I understand. If I had looked at the JmxReporter before, then the function of {{metricChange()}} would have been clear. I was under the impression that a reporter can stay up to date about metrics and their values by simply listening to what is pass…
- _…1 more comments_

## KAFKA-14082: Mirror Maker 2.0 sync topic configs need more validly 
Wish · Open · Major · components: mirrormaker · created 2022-07-18

Mirror Maker 2.0 sync topic configs is undifferentiated,even if source topics' configs are same with target topics' configs.
It cause a lot logs and zookeeper config alter tasks prior to 3.0.0,after 3.0.0 due to configs undifferentiated sync still cause lots of unnecessary sync tasks


## KAFKA-14144: AlterPartition is not idempotent when requests time out
Bug · Resolved (Fixed) · Blocker · created 2022-08-05 · resolved 2022-08-09

[https://github.com/apache/kafka/pull/12032] changed the validation order of AlterPartition requests to fence requests with a stale partition epoch before we compare the leader and ISR contents.
This results in a loss of idempotency if a leader does not receive an AlterPartition response because retries will receive an INVALID_UPDATE_VERSION error.


## KAFKA-14145: Faster propagation of high-watermark in KRaft topic partitions
Sub-task · Resolved (Fixed) · Critical · components: kraft · created 2022-08-05 · resolved 2025-06-17

Typically, the HWM is increase after one round of Fetch requests from the majority of the replicas. The HWM is propagated after another round of Fetch requests. If the LEO doesn't change the propagation of the HWM can be delay by one Fetch wait timeout (500ms).
Looking at the KafkaRaftClient implementation we would have to have an index for both the fetch offset and the last sent high-watermark for that replica.
Another issue here is that we changed the KafkaRaftManager so that it doesn't set…

- **A. Sophie Blee-Goldman:** [~jagsancio]  moving this to 3.5.0 since we are past code freeze for 3.4
- **Mickael Maison:** We're past feature freeze for 3.5.0 so moving to 3.6.0.
- **Colin McCabe:** Moving to 3.7.
- **Stanislav Kozlovski:** Changing target fix version to 3.8 since this is not a blocker and we are cutting a 3.7 RC
- **Josep Prat:** Changing target fix version to 3.9 since this is not a blocker and we are past code freeze
- _…2 more comments_

## KAFKA-14146: KIP-840: Config file option for MessageReader/MessageFormatter in ConsoleProducer/ConsoleConsumer
Improvement · Resolved (Fixed) · Minor · components: tools · created 2022-08-08 · resolved 2022-12-02

Jira for [KIP-840|https://cwiki.apache.org/confluence/x/bBqhD]

- **Alexandre Garnier:** Cf. PR on GitHub.
- **A. Sophie Blee-Goldman:** Moved to 3.5 since it looks like this KIP isn't going to make 3.4

## KAFKA-14147: Some map objects in KafkaConfigBackingStore grow in size monotonically
Bug · Resolved (Fixed) · Minor · components: connect · created 2022-08-08 · resolved 2022-08-22

Similar to https://issues.apache.org/jira/browse/KAFKA-8869
{{deferredTaskUpdates, connectorTaskCountRecords and connectorTaskConfigGenerations in KafkaConfigBackingStore are never updated when a connector is deleted, thus growing monotonically.}}


## KAFKA-14148: Outdated doc for reset-offsets option
Improvement · Resolved (Fixed) · Minor · components: admin · created 2022-08-08 · resolved 2022-08-16

!image-2022-08-08-19-19-34-873.png!
--by-period should be --by-duration, and --to-offset show be added


## KAFKA-14149: Broken DynamicBrokerReconfigurationTest in 3.2 branch
Bug · Resolved (Fixed) · Major · created 2022-08-08 · resolved 2022-08-25

The backport of [https://github.com/apache/kafka/pull/12455] does not work in 3.2. The following tests are failing:
DynamicBrokerReconfigurationTest.testConfigDescribeUsingAdminClient(String).quorum=kraft
DynamicBrokerReconfigurationTest.testConsecutiveConfigChange(String).quorum=kraft
DynamicBrokerReconfigurationTest.testKeyStoreAlter(String).quorum=kraft
DynamicBrokerReconfigurationTest.testLogCleanerConfig(String).quorum=kraft
DynamicBrokerReconfigurationTest.testTrustStoreAlter(String).…


## KAFKA-14150: Allocation of initial partitions is deterministic and produces a leader bias when a broker is offline
Improvement · Open · Minor · created 2022-08-09

Observation of our current cluster suggests that with N brokers, the first N partitions are always allocated in a round-robin format with a random offset. The preferred leader is always the first in a given replica list (and hence is allocated round-robin, too). Subsequent brokers are allocated using some shuffle on the list, again in a round-robin, which I think is fine and doesn't show the bias I detail below. Suppose every topic has as many partitions as there are brokers and replication fact…


## KAFKA-14151: Add validation to fail fast when base offsets are incorrectly assigned to batches
Improvement · Open · Major · components: log · created 2022-08-09

We saw a case where records with incorrect offsets were being written to log segment on-disk data due to environmental issues (bug in old version JVM JIT). We should consider adding additional validation to detect this scenario and fail fast.


## KAFKA-14152: Add logic to fence kraft brokers which have fallen behind in replication
Improvement · Open · Major · created 2022-08-09

When a kraft broker registers with the controller, it must catch up to the current metadata before it is unfenced. However, once it has been unfenced, it only needs to continue sending heartbeats to remain unfenced. It can fall arbitrarily behind in the replication of the metadata log and remain unfenced. We should consider whether there is an inverse condition that we can use to fence a broker that has fallen behind.

- **Deng Ziming:** > it must catch up to the current metadata before it is unfenced.
 Currently, we have changed the behavior to unfence a broker when it catch up to it's own RegisterBrokerRecord.

## KAFKA-14153: UnknownTopicOrPartitionException should include the topic/partition in the returned exception message
Improvement · Open · Minor · created 2022-08-09

Exception would be more useful if it included the topic or partition that was not found. Message right now is just 
`This server does not host this topic-partition.`
Background: [https://github.com/apache/kafka/pull/12479#discussion_r938988993]


## KAFKA-14154: Persistent URP after controller soft failure
Bug · Resolved (Fixed) · Blocker · created 2022-08-09 · resolved 2022-08-15

We ran into a scenario where a partition leader was unable to expand the ISR after a soft controller failover. Here is what happened:
Initial state: leader=1, isr=[1,2], leader epoch=10. Broker 1 is acting as the current controller.
1. Broker 1 loses its session in Zookeeper.  
2. Broker 2 becomes the new controller.
3. During initialization, controller 2 removes 1 from the ISR. So state is updated: leader=2, isr=[2], leader epoch=11.
4. Broker 2 receives `LeaderAndIsr` from the new control…

- **Artem Livshits:** > 1. Broker 1 loses its session in Zookeeper. 
 I think if we treat this error as fatal (fence itself or maybe just flush and restart), it should handle a whole class of split brain issues.  ZK timeouts are generally set such that the client would timeout before the ephemeral zknode is removed, so t…

## KAFKA-14187: kafka-features.sh: add support for --metadata
Bug · Resolved (Fixed) · Blocker · created 2022-08-29 · resolved 2022-08-30

Fix the kafka-features.sh command so that we can upgrade to the new version as expected.


## KAFKA-14188: Quickstart for KRaft
Task · Resolved (Fixed) · Blocker · components: documentation · labels: documentation, kraft · created 2022-08-29 · resolved 2022-09-08

Either:
 # Improve the quick start documentation to talk about both KRAft and ZK
 # Create a KRaft quick start that is very similar to the ZK quick start but uses a different startup process.


## KAFKA-14189: Improve connection limit and reuse of coordinator and leader in KafkaConsumer
Improvement · Open · Major · components: clients · created 2022-08-30

The connection id of connection with coordinator in KafkaConsumer is Integer.MAX_VALUE - coordinator id, which is different with connection id of partition leader. So the connection cannot be reused when coordinator and leader are in the same broker, which means we need two seperated connections with the same broker. Suppose such case, a consumer has connected to the coordinator and finished Join and Sync, and wants to send FETCH to leader in the same broker. But the connection count has reached…

- **Von Gosling:** I'd like to hear some suggestions from [~junrao]. Do we have the possibility to reuse the same connection in such conditions?
- **Guozhang Wang:** Hi [~aglicacha] [~vongosling]
 The main motivation for using two connection sockets for the coordinator and partition leader is to not block coordination related requests such as join/sync by fetching requests (which could be long polling, and during that time we cannot send other requests using the…

## KAFKA-14190: Corruption of Topic IDs with pre-2.8.0 ZK admin clients
Bug · Resolved (Won't Fix) · Major · components: admin, core, zkclient · created 2022-08-30 · resolved 2024-10-15

h3. Scope
The problem reported below has been verified to occur in Zookeeper mode. It has not been attempted with Kraft controllers, although it is unlikely to be reproduced in Kraft mode given the nature of the issue and clients involved.
h3. Problem Description
The ID of a topic is lost when an AdminClient of version < 2.8.0 is used to increase the number of partitions of that topic for a cluster with version >= 2.8.0. This results in the controller re-creating the topic IDs upon restart, e…

- **Ismael Juma:** Thanks for the JIRA. To clarify, the issue is not using an older topics command, it's using an older topics command _with the_ –zookeeper flag, right? That is, they can use older topics command with the --bootstrap-server flag and the problem would not occur?
- **Ismael Juma:** {quote}The ID of a topic is lost when an AdminClient of version < 2.8.0 is used to increase the number of partitions of that topic for a cluster with version >= 2.8.0
 {quote}
 Is the above actually true? The command you outlined doesn't use admin client at all, it updates zookeeper directly.
- **Alexandre Dupriez:** Hi Ismael,
 Thanks for the follow-up. You are right that the problem requires to use the {{--zookeeper}} flag (which has been removed from the newest versions). If topic changes are applied via broker RPCs, no topic ID is lost. This brings us to your second comment: indeed it requires modifying the…
- **Ismael Juma:** `AdminZkClient` is an internal class and compatibility was never offered (or should have been expected) for that. The `–zookeeper` flag for for `TopicCommand` has been deprecated since Apache Kafka 2.2.0 ([https://github.com/apache/kafka/blob/2.2.0/core/src/main/scala/kafka/admin/TopicCommand.scala#…
- **Divij Vaidya:** Adding reports of users facing this bug which would help us determine priority of fixing this.
 1. User on mailing list [https://lists.apache.org/thread/jzk4tyd1xs1wwj0bpkdnxpw0m152qw1f]
 2. User on #kafka channel [https://the-asf.slack.com/archives/CE7HWJPHA/p1671529649633529]
- _…4 more comments_

## KAFKA-14191: Add end-to-end latency metrics to Connectors
Improvement · Open · Major · components: connect, metrics · labels: connect, needs-kip · created 2022-08-30

Request to add latency metrics to connectors to measure transformation latency and e2e latency on the sink side.
KIP: https://cwiki.apache.org/confluence/display/KAFKA/KIP-864%3A+Add+End-To-End+Latency+Metrics+to+Connectors


## KAFKA-14192: Move registering and unregistering changelogs to state updater
Improvement · Resolved (Duplicate) · Major · components: streams · created 2022-08-31 · resolved 2026-05-04

Currently, we register and unregister changelogs when we initialize and close/recycle a task. 
When we will remove the old code path for restoration and we will only use the state updater, we should consider to move registering and unregistering changelogs inside the state udpater. In such a way, we would put registering and unregistering changelogs in one place and we would only have changelog registered when it is actually needed, i.e., during restoration of active tasks and updating of stand…

- **Nikita Shupletsov:** Looks like it was done in [https://github.com/apache/kafka/pull/12638] as a part of https://issues.apache.org/jira/browse/KAFKA-10199
 [~cadonna] could you please confirm? or is there anything else needed? thank you in advance!
- **Bruno Cadonna:** [~nikita-shupletsov] I do not actively develop Kafka Streams anymore. Maybe [~lucasbru] or [~mjsax] can answer your question.
- **Nikita Shupletsov:** Had a chat with [~mjsax] , it's indeed a duplicate. resolving the ticket

## KAFKA-14193: Connect system test ConnectRestApiTest is failing
Bug · Resolved (Fixed) · Major · components: connect · created 2022-08-31 · resolved 2022-09-08

[ConnectRestApiTest|https://github.com/apache/kafka/blob/trunk/tests/kafkatest/tests/connect/connect_rest_test.py] is currently failing on `trunk` and `3.3` with the following assertion error:
[code/log omitted]
On closer inspection, this is because of the new source connector EOS related configs added in [https://github.com/apache/kafka/pull/11775.] Adding the following new configs - 
[code/log omitted]
in the expected config defs [here|https://github.com/apache/kafka/blob/6f4778301b1fcac1e…


## KAFKA-14194: NPE in Cluster.nodeIfOnline
Bug · Resolved (Fixed) · Major · components: clients · created 2022-09-01 · resolved 2022-09-05

When utilizing rack-aware Kafka consumers and the Kafka broker cluster is restarted an NPE can occur during transient metadata updates.


## KAFKA-14195: Fix KRaft AlterConfig policy usage for Legacy/Full case
Bug · Resolved (Fixed) · Blocker · created 2022-09-01 · resolved 2022-09-02

The fix for https://issues.apache.org/jira/browse/KAFKA-14039 adjusted the invocation of the alter configs policy check in KRaft to match the behavior in ZooKeeper, which is to only provide the configs that were explicitly sent in the request. While the code was correct for the incremental alter configs case, the code actually included the implicit deletions for the legacy/non-incremental alter configs case, and those implicit deletions are not included in the ZooKeeper-based invocation. The imp…


## KAFKA-14196: Duplicated consumption during rebalance, causing OffsetValidationTest to act flaky
Bug · Resolved (Fixed) · Blocker · components: clients, consumer · labels: new-consumer-threading-should-fix · created 2022-09-02 · resolved 2022-09-13

Several flaky tests under OffsetValidationTest are indicating potential consumer duplication issue, when autocommit is enabled.  I believe this is affecting *3.2* and onward.  Below shows the failure message:
[code/log omitted]
After investigating the log, I discovered that the data consumed between the start of a rebalance event and the async commit was lost for those failing tests.  In the example below, the rebalance event kicks in at around 1662054846995 (first record), and the async commi…

- **Philip Nee:** If I understand this correctly: Seems like this is introduced in https://issues.apache.org/jira/browse/KAFKA-14024, which originated from https://issues.apache.org/jira/browse/KAFKA-13310.  I think the cause of the flakiness/duplication is, the consumer is busy waiting for the prior async commit to…
- **Philip Nee:** Kind of originated from this commit: https://github.com/apache/kafka/pull/12349/files
- **Luke Chen:** [~pnee] , thanks for the analysis. Yes, we forgot about during the following poll, the offset might advance while we're waiting for the old async offset commit completion.
 Actually, while checking the code, even if we don't do the change for KAFKA-14024,and KAFKA-13310, (that is, changing sync comm…
- **Philip Nee:** Thanks Luke, per your suggestion, could you elaborate more about the reason to terminate the poll?
 I've got a few questions to clarify here:
  # I don't think we need to pause the fetch if the previous async commit (autocommit) hasn't yet go through, for the normal situation (not rebalancing)? Beca…
- **Guozhang Wang:** [~pnee] Thanks for reporting this. While reviewing KAFKA-13310 I have realized this, but as Luke said this is not a new regression (we would potentially have duplicates even before this, since as we commit sync, and if the commit fails, we still log a warning and move forward with the revocation, in…
- _…8 more comments_

## KAFKA-14197: Kraft broker fails to startup after topic creation failure
Bug · Resolved (Duplicate) · Blocker · components: kraft · created 2022-09-02 · resolved 2022-09-06

In kraft ControllerWriteEvent, we start by trying to apply the record to controller in-memory state, then sent out the record via raft client. But if there is error during sending the records, there's no way to revert the change to controller in-memory state[1].
The issue happened when creating topics, controller state is updated with topic and partition metadata (ex: broker to ISR map), but the record doesn't send out successfully (ex: RecordBatchTooLargeException). Then, when shutting down th…

- **Luke Chen:** I think we should have a way to notify ReplicationControlManager the topic doesn't get created successfully, so that it won't send out the partitionChangeRecords while controlled shutdown. But I don't have a good idea how we can achieve that gracefully.
 cc [~hachikuji]  [~cmccabe] [~jsancio] [~deng…
- **Deng Ziming:** Basically, a record will be persisted after being applied, it is similar to a transaction. if there is an unexpected exception between persisting and applying we should call `QuorumController.renounce` to revert the memory state when calling`snapshotRegistry.revertToSnapshot(lastCommittedOffset)`. m…
- **Luke Chen:** Thanks for the hint! I'll take a look!
- **Luke Chen:** OK, I've checked, there's the problem: the exception: *RecordBatchTooLargeException* thrown from BatchAccumulator#append is one of {*}ApiException{*}, and that will enter [here|https://github.com/apache/kafka/blob/trunk/metadata/src/main/java/org/apache/kafka/controller/QuorumController.java#L446] w…
- **Luke Chen:** And one silly question: Why don't we do renounce for ApiExceptions? Shouldn't we revert the controller memory state for all error cases?
- _…2 more comments_

## KAFKA-14261: Dependency Vulnerability Scan Results (Mend/WhiteSource)
Bug · Open · Major · components: security · created 2022-09-26

The Kafka repository was scanned with Mend's (formerly WhiteSource) SCA (software composition analysis) tool for 3rd party dependency vulnerabilities. We scanned Kafka version 3.2.3 on 9/20. 
The scan result detected the following instances of vulnerability severities:
 * 12 highs
 * 12 mediums
 * 1 low
We would like to submit the Mend findings (attached to this ticket) as a bug with the request to update to non-vulnerable library versions. In the attached spreadsheet, column W "Top Fix" ha…


## KAFKA-14262: Delete MirrorMaker v1
Task · Resolved (Fixed) · Major · components: mirrormaker · created 2022-09-27 · resolved 2024-08-28

As per [KIP-720|https://cwiki.apache.org/confluence/display/KAFKA/KIP-720%3A+Deprecate+MirrorMaker+v1], MirrorMaker is due to be deleted in Kafka 4.0


## KAFKA-14263: Investigate flaky upgrade_test.py (missing messages)
Test · Open · Major · created 2022-09-27

During system tests, we occasionally see flaky failures of upgrade_test.py. 
Here is one such recent failure on the 3.3 branch:
[code/log omitted]
[code/log omitted]
It would be good to try and reproduce these types of failures and see how we can make the test more robust.


## KAFKA-14264: Refactor coordinator code
Sub-task · Resolved (Fixed) · Major · components: clients, consumer · labels: consumer-threading-refactor · created 2022-09-28 · resolved 2023-02-27

To refactor the consumer, we changed how the coordinator is called.  However, there will be a time period where the old and new implementation need to coexist, so we will need to override some of the methods and create a new implementation of the coordinator.  In particular:
 # ensureCoordinatorReady needs to be non-blocking or we could just use the sendFindCoordinatorRequest.
 # joinGroupIfNeeded needs to be broken up into more find grain stages for the new implementation to work.
We also ne…

- **Kirk True:** [~pnee] can you fill in the details on the fixed versions? Thanks!

## KAFKA-14265: Prefix ACLs may shadow other prefix ACLs
Bug · Resolved (Fixed) · Blocker · created 2022-09-29 · resolved 2022-09-29

Prefix ACLs may shadow other prefix ACLs. Consider the case where we have prefix ACLs for foobar, fooa, and f. If we were matching a resource named "foobar", we'd start scanning at the foobar ACL, hit the fooa ACL, and stop -- missing the f ACL.
To fix this, we should re-scan for ACLs at the first divergence point (in this case, f) whenever we hit a mismatch of this kind.


## KAFKA-14266: MirrorSourceTask will stop mirroring when get corrupt record
Bug · Closed (Works for Me) · Critical · components: connect · created 2022-09-29 · resolved 2022-10-11

The mirror task will keeping throwing this error when got a corrupt record
[code/log omitted]
In the poll function of {*}MirrorSourceTask{*}, when the task got {*}KafkaException{*}, it only print a warn level log and return null.
[code/log omitted]
In the next poll round, the consumer will keep throwing exception because it has received a corrupt record. Which makes the  *MirrorSourceTask* cannot get next records and be blocked on the same offset.
[code/log omitted]
As this issue will not…

- **Chris Egerton:** [~LucentWong] would monitoring the consumer lag metric help in this case? I believe that would allow users to detect when MM2 is lagging behind on consumption from the source cluster; it may not highlight this specific issue, but it would still indicate a general issue with the MM2 cluster.
 I'm hes…
- **Yu Wang:** [~ChrisEgerton] I am afraid monitoring lag now working in this case. Actually, we are monitoring both *records-age* from MirrorSourceTask and *records-lag* from KafkaConsumer.
 It's not work because MirrorSourceTask only refresh the *records-age* metrics after success poll from consumer, but it thro…
- **Yu Wang:** [~ChrisEgerton] for this issue, as the KafkaConsumer always return before fetch data from broker, it can use kafka consumer's *select-rate == 0* to alert it.
- **Chris Egerton:** That's good to hear, thanks [~LucentWong]!

## KAFKA-14267: CVE-2022-36944 - Scala deserialization bug
Bug · Open · Major · created 2022-09-29

[https://nvd.nist.gov/vuln/detail/CVE-2022-36944]
This is marked as CRITICAL severity vulnerability with a 9.8 score (out of 10). 
{quote}Scala 2.13.x before 2.13.9 has a Java deserialization chain in its JAR file. On its own, it cannot be exploited. There is only a risk in conjunction with LazyList object deserialization within an application. In such situations, it allows attackers to erase contents of arbitrary files, make network connections, or possibly run arbitrary code (specifically, F…

- **Zach Fry:** Upon some investigation, I wasn't able to find anywhere in the Kafka codebase that uses `LazyList` data structures. Though it would be great if a maintainer can confirm that this is the case.

## KAFKA-14268: When aggregating on a KGroupedStream allow an InitializerWithKey
Improvement · Open · Minor · components: streams · created 2022-09-29

Sometimes when aggregating on a KGroupedStream I would like to have an initial value which change depending on the key.
A workarround is to have a dummy value in the initializer which can be checked for and replaced in the aggregator, but that implies some performance loss caused by the check.
My proposal is to add yet another overload for {{aggregate}} which has instead of an {{Initializer}} an {{{}InitializerWithKey{}}}. The {{apply}} method of {{InitializerWithKey}} would have the key as in…


## KAFKA-14269: Partition Assignment Strategy - Topic Round Robin Assignor
Wish · Resolved (Abandoned) · Major · components: clients · created 2022-09-30 · resolved 2022-10-26

*The context :*
I have :
 * only one type of message per topic
 * the same number of consumers and topics
 * each consumer subscribes to all topics in the same microservice
 * a strategy where I stopped the consumer if the consumption failed
*The need :*
I would like to have a Topic Round Robin Assignor in order to assign all partitions of same topic to exactly one consumer, therefore I will be able to continue the consumption of one topic even if one failed.
If there are exactly the sam…

- **Guozhang Wang:** Hello [~mathieu.amblard], thanks for reporting this use case.
 I'm wondering in your scenario if all topics have the same num. partitions, and have similar data traffic as well? I'm asking this because one of the primarily goals of partition assignors is to achieve workload balance, so if topics hav…
- **Mathieu Amblard:** Hello [~guozhang] ,
 Thanks for your comment that's a good question,
 All topics have not the same number of partition, they are sized accordingly to the data traffic.
 If we have to consume a large amount of data, we simply scale up the number of pods (so the number of consumer). Using this partiti…
- **Mathieu Amblard:** Too specific use case, the KIP-874 has been rejected.

## KAFKA-14270: Kafka Streams logs exception on startup
Bug · Resolved (Fixed) · Minor · components: streams · created 2022-09-30 · resolved 2022-10-04

Kafka Streams expects a version resource at /kafka/kafka-streams-version.properties. It is read by {{{}ClientMetrics{}}}, initialised by
[https://github.com/apache/kafka/blob/3.3.0/streams/src/main/java/org/apache/kafka/streams/KafkaStreams.java#L894]
When the resource is not found,
[https://github.com/apache/kafka/blob/3.3.0/streams/src/main/java/org/apache/kafka/streams/internals/metrics/ClientMetrics.java#L55]
logs a warning at startup:
org.apache.kafka.streams.internals.metrics.ClientMe…

- **Guozhang Wang:** Thanks for filing the bug [~eikemeier], will take a look.
 From your description, it seems whenever Kafka Streams is started, with whatever integration tooling besides groovy, it will always log a warning?
- **Oliver Eikemeier:** Yes. Sorry about the “Groovy” tag, the Gradle build script is written in Groovy, so this fix is in Groovy code.
- **Bruno Cadonna:** [~eikemeier] Thanks for the fix!
 I tested your code manually and merged your PR.
 I also added you o the contributors group in Jira so that I could assign this ticket to you.

## KAFKA-14271: Topic recreation fails in KRaft mode when topic contains collidable characters
Bug · Resolved (Duplicate) · Major · components: kraft · created 2022-09-30 · resolved 2022-12-12

We recently updated one of our clusters from 3.2.0 to 3.3.0 (primarily to get the fix for KAFKA-13909). This cluster is running KRaft mode.
This is a cluster used for some integration tests - each test deletes the topics it uses before the test to ensure a clean slate for the test; the brokers get restarted in-between tests, but the broker data isn't deleted.
With 3.3.0, this semi-crashes Kafka. The brokers stay running, but the topic creation fails:
[code/log omitted]
This appears to be bec…

- **Jeffrey Tolar:** It's possible this isn't specific to KRaft-mode; I haven't tried reproducing it with a Zookeeper-based cluster.
 edit: after a quick script update, it looks like Zookeeper-mode is unaffected
 [code/log omitted]
- **Jeffrey Tolar:** Haven't tested the patch yet, but KAFKA-14337 appears to be the same as this issue; that was fixed with https://github.com/apache/kafka/pull/12790

## KAFKA-14313: Kraft: immediately producing to new topics occasionally returns NOT_LEADER_FOR_PARTITION
Bug · Resolved (Won't Fix) · Major · components: kraft, producer  · created 2022-10-18 · resolved 2024-11-12

Related issue: KAFKA-14312
See the related issue for the full problem description. This issue is to track a _slightly_ less important issue.
In Kraft mode, if I create a topic, sometimes immediate produce requests are rejected with NOT_LEADER_FOR_PARTITION
Scenario:
 * Client creates topic
 * Client loads metadata for topic, receives leader 1
 * Client produces to broker 1
 * Client receives NOT_LEADER_FOR_PARTITION
If the client waits a little bit, the broker eventually does become the…

- **Deng Ziming:** Hello [~twmb] , Can you also provide your code or command if you are using a shell, then we can reproduce it locally.
- **Luke Chen:** [~dengziming] , the issue is discussed [here|https://github.com/twmb/franz-go/pull/223] . It's using franz-go client. FYI
- **Colin McCabe:** This isn't a bug. It results from metadata propagation delays. The client needs to retry NOT_LEADER_FOR_TOPIC_OR_PARTITION until the topic is created on the leader in question.

## KAFKA-14314: MirrorSourceConnector throwing NPE during `isCycle` check
Bug · Resolved (Fixed) · Blocker · components: mirrormaker · created 2022-10-18 · resolved 2022-10-28

We are using MirrorMaker to replicate topics across clusters in AWS. As the process is starting up, we are getting a NullPointerException when MirrorSourceConnector is calling `isCycle`.
Retrieving the `upstreamTopic` on [this line of code|https://github.com/apache/kafka/blob/cc582897bfb237572131369a598f7869220b43dc/connect/mirror/src/main/java/org/apache/kafka/connect/mirror/MirrorSourceConnector.java#L497] is returning null, which causes the NPE on the next line.

- **Mickael Maison:** Which replication policy are you using?
- **John Krupka:** We're using a custom replication policy. Here are the contents of the mm2-msc.json file. Is this what you're asking for? I'm new to this so I'm unsure exactly what all constitutes the policy.
 [code/log omitted]
- **Mickael Maison:** Thanks for the details.
 The ReplicationPolicy [javadoc|https://kafka.apache.org/33/javadoc/org/apache/kafka/connect/mirror/ReplicationPolicy.html#upstreamTopic-java.lang.String-] states that upstreamTopic can return null to indicate a topic is not remote. So this is a bug in MirrorSourceConnector.i…
- **John Krupka:** Thanks, Mickael. Sure I can do that. I thought it was a bug because it seems that `null` is a legitimate value here. We might have something misconfigured but even in that case it shouldn't blow up so I'll submit a PR a bit later today.
- **Mickael Maison:** Great, I'll assign this ticket to you then. Thanks!
- _…1 more comments_

## KAFKA-14315: Kraft: 1 broker setup, broker took 34 seconds to transition from PrepareCommit to CompleteCommit
Bug · Open · Minor · components: kraft · created 2022-10-18

I'm still looking into a PR failure in [my client|https://github.com/twmb/franz-go/pull/223] and noticed something a bit strange. I know that _technically_ I should be using RequireStableFetchOffsets in my transaction tests to prevent rebalances while a transaction is not finalized. I'll be adding that.
However, these tests have never failed against zookeeper mode. The client goes through a lot of efforts to avoid needing KIP-447 behavior, and the assumption with localhost testing is that thing…

- **Travis Bischel:** Note that I've also had requests repeatedly failing with CONCURRENT_TRANSACTIONS – for upwards of 40 seconds – my guess is that these are related.

## KAFKA-14316: NoSuchElementException in feature control iterator
Bug · Resolved (Fixed) · Major · created 2022-10-18 · resolved 2022-10-18

We noticed this exception during testing:
[code/log omitted]
The iterator `FeatureControlIterator.hasNext()` checks two conditions: 1) whether we have already written the metadata version, and 2) whether the underlying iterator has additional records. However, in `next()`, we also check that the metadata version is at least high enough to include it in the log. When this fails, then we can see an unexpected `NoSuchElementException` if the underlying iterator is empty.


## KAFKA-14317: ProduceRequest timeouts are logged as network exceptions
Bug · Resolved (Fixed) · Major · components: clients, logging, producer  · created 2022-10-18 · resolved 2023-03-09

In {{{}NetworkClient.handleTimedOutRequests{}}}, we disconnect the broker connection:
[code/log omitted]
This calls {{processDisconnection}} which calls {{{}cancelInFlightRequests{}}}:
[code/log omitted]
We create a new {{ClientResponse}} in which the {{disconnected}} flag is set.
We then complete the record batch In {{Sender.handleProduceResponse}} with:
[code/log omitted]
This seems like it could be confusing for customers that they would see network exceptions on a request timeout inst…

- **Kirk True:** This looks related to KAFKA-10228, but that Jira is still open and seems to suggest only a logging change.
 I _believe_ we want to change the behavior to complete the batch using a different {{Errors}} type.
- **Kirk True:** [~dajac] could you take another look at the PR? Thanks!

## KAFKA-14318: KIP-878: Autoscaling for Statically Partitioned Streams
New Feature · Reopened · Major · components: streams · labels: kip · created 2022-10-18

[KIP-878: Autoscaling for Statically Partitioned Streams|https://cwiki.apache.org/confluence/display/KAFKA/KIP-878%3A+Autoscaling+for+Statically+Partitioned+Streams]


## KAFKA-14319: Storage tool format command does not work with old metadata versions
Bug · Open · Major · created 2022-10-18

When using the format tool with older metadata versions, we see the following error:
[code/log omitted]
For versions prior to `3.3-IV0`, we should skip creation of the `bootstrap.checkpoint` file instead of failing.


## KAFKA-14320: Upgrade Jackson for CVE fix
Bug · Resolved (Fixed) · Minor · components: core · labels: security · created 2022-10-18 · resolved 2022-11-18

There is a CVE for Jackson:
Jackson: [CVE-2020-36518|https://nvd.nist.gov/vuln/detail/CVE-2020-36518] - Fixed by upgrading to 2.14.0+


## KAFKA-14321: max.compaction.lag.ms is not enforced accurately
Bug · Resolved (Duplicate) · Major · created 2022-10-19 · resolved 2022-10-19

Compaction only cleans data in non-active segments. When max.compaction.lag.ms is set, we use it to set segment.ms to force segment rolling by time. However, the current implementation of time-based segment roll is not precise. It only rolls a segment if the new record's timestamp differs from the timestamp of the first record in the segment by more than segment.ms. If we have a bunch of records appended within segment.ms and then stop producing new records, all those records could remain in the…

- **Jun Rao:** A potential solution is to implement the time based segment rolling based on segment creation time.
- **Jun Rao:** This actually duplicates KAFKA-10760. Closing this one.

## KAFKA-14322: Kafka node eating Disk continuously 
Bug · Open · Major · components: log, log cleaner · created 2022-10-19

We have 2.8.1 Kafka cluster in our Production environment. It has it continuously growing disk consumption and eating all disk space allocated and crash node with no disk space left
!image-2022-10-19-15-51-52-735.png|width=344,height=194!
!image-2022-10-19-15-53-39-928.png|width=470,height=146!
[Log partition=__consumer_offsets-41, dir=/var/lib/kafka/data/kafka-log0] Rolled new log segment at offset 10537467423 in 4 ms. (kafka.log.Log) [data-plane-kafka-request-handler-4]"
I can see that for…

- **Abhijit Patil:** Can this be assigned to some one or looked further.
- **Sergey Ivanov:** Hi,
 We faced similar problem.
 I described it in ticket KAFKA-14817, these may be related issues.

## KAFKA-14323: KRaft broker time based snapshots
New Feature · Resolved (Duplicate) · Major · created 2022-10-19 · resolved 2024-08-09

- **Mickael Maison:** We're past feature freeze for 3.5.0 so I'm moving this to 3.6.0.
- **Satish Duggana:** Moving it to 3.7.0 as we are near code freeze and it is not a blocker.
- **Stanislav Kozlovski:** Changing target fix version to 3.8 since this is not a blocker and we are cutting a 3.7 RC
- **Josep Prat:** Changing target fix version to 3.9 since this is not a blocker and we are past code freeze
- **Colin McCabe:** When we unified the broker and controller snapshot generation code paths, this ceased to be an issue. This happened in 3.5 I believe.

## KAFKA-14356: Make it possible to detect changes to SCRAM-SHA credentials using the Admin API
Improvement · Open · Major · created 2022-11-04

When using the Kafka Admin API to manage SCRAM-SHA credentials, the API seems to offer only three options:
 * Find out if given user has any credentials
 * Set SCRAM-SHA credentials
 * Delete SCRAM-SHA credentials
There is now way how to find out what the current credentials are. That makes sense as that can lead to the credentials being leaked which would be a security issue. However, there is also no way how to find out if the credentials changed since last time.
So if you have an externa…


## KAFKA-14357: Make it possible to batch describe requests in the Kafka Admin API
Improvement · Open · Major · created 2022-11-04

The Admin API has several methods to describe different objects such as ACLs, Quotas or SCRAM-SHA users. But these API seem to be usable only in one for the two modes:
 * Query or one users ACLs / Quotas / SCRAM-SHA credentials
 * Query all existing ACLs / Quotas / SCRAM-SHA credentials
But there seems to be no way how to batch the describe requests for multiple users. E.g. {_}describe ACLs of users Joe, John and Mike{_}. It would be nice to have such option as it might make it easier for app…

- **Mickael Maison:** I took a look at these APIs to see what can be done.
  * Scram Credentials
 It already possible to retrieve credential details for multiple users in a single call:
 [code/log omitted]
  * Quotas
  DescribeClientQuotasRequest/Response and Admin.describeClientQuotas() accepts multiple resources but th…
- **Mickael Maison:** Looking further into describeClientQuotas() it doesn't quite work like I thought. Some ClientQuotaFilterComponent can be additive, for example it's possible to describe quotas for a USER and CLIENT_ID combination. On the other hand it's not possible to combine them with an IP entity. For this reason…

## KAFKA-14358: Users should not be able to create a regular topic name __cluster_metadata
Bug · Resolved (Fixed) · Blocker · components: controller · created 2022-11-04 · resolved 2022-12-02

The following test passes and it should not:
[code/log omitted]
Result of this test:
[code/log omitted]
I think that this test should fail in both KRaft and ZK. We want this to fail in ZK so that it can be migrated to KRaft.


## KAFKA-14359: Idempotent Producer continues to retry on OutOfOrderSequence error when first batch fails
Task · Open · Major · created 2022-11-05

When the idempotent producer does not have any state it can fall into a state where the producer keeps retrying an out of order sequence. Consider the following scenario where an idempotent producer has retries and delivery timeout are int max (a configuration used in streams).
1. A producer send out several batches (up to 5) with the first one starting at sequence 0.
2. The first batch with sequence 0 fails due to a transient error (ie, NOT_LEADER_OR_FOLLOWER or a timeout error)
3. The secon…

- **Justine Olshan:** might be the same as https://issues.apache.org/jira/browse/KAFKA-7848
- **Justine Olshan:** also https://issues.apache.org/jira/browse/KAFKA-9199 offers a way to fix.

## KAFKA-14360: Documentation: Streams Security page has broken links
Bug · Resolved (Fixed) · Major · created 2022-11-05 · resolved 2022-11-15

A number of links on the 'Streams Security' page are 404-ing
https://kafka.apache.org/documentation/streams/developer-guide/security.html
* Kafka’s security features https://kafka.apache.org/documentation/documentation.html#security
* Java Producer and Consumer API https://kafka.apache.org/documentation/clients/index.html#kafka-clients

- **A. Sophie Blee-Goldman:** Weird, thanks for finding this – I'm guessing the first one is broken due to an extra '/documentation' in the link, it should presumably be directing to [https://kafka.apache.org/documentation/#security]
 As for the 2nd one, it's a little less clear what it should be pointing to – oddly there does n…
- **Shay Lin:** Thanks [~ableegoldman]. Here is an PR to fix this broken link [https://github.com/apache/kafka/pull/12857.] Thanks

## KAFKA-14361: Two versions of commons-lang3 in 3.3.1 binary distribution libs dir
Bug · Open · Minor · created 2022-11-06

Hi,
There are two versions of commons-lang3 in the libs dir:
[code/log omitted]
I'm not sure on the right fix but the 3.8.1 version comes from  `:connect:mirror`, If you add a compile dependency on 3.12.0 to :connect:mirror then only 3.12.0 will end up in the tarball.
Thanks!


## KAFKA-14362: Same message consumed by two consumers in the same group  after client restart
Bug · Resolved (Not A Bug) · Major · components: clients · created 2022-11-07 · resolved 2022-12-10

Trigger scenario:
Two Kafka client application instances on separate EC2 instances with one consumer each, consuming from the same 8 partition topic using the same group ID. Duplicate consumption of a handful of messages sometimes happens right after one of the application instances has been restarted.
Additional information:
Messages are produced to the topic by a Kafka streams topology deployed on four application instances. I have verified that each message is only produced once by enablin…

- **Mikael:** The main thing that has caught my attention is the tight loop of 'Failing OffsetCommit request since the consumer is not part of an active group' messages for the consumer that is not restarted. Could it have given up on committing the offset?
- **A. Sophie Blee-Goldman:** Hey [~Carlstedt] you're right about why this is happening, because of the restart a rebalance is kicked off which means that any further attempts to commit offsets by other members of the group will fail. After a rebalance, if for example a partition is reassigned from consumer A to consumer B, then…
- **Mikael:** I would have thought that an orderly rebalance wouldn't cause any duplication. I understand that an uncontrolled restart can cause duplication, but in this case it's a consumer that just leaves the group and then joins it again later. Surely it can't be expected behaviour to randomly duplicate messa…
- **A. Sophie Blee-Goldman:** {quote}I would have thought that an orderly rebalance wouldn't cause any duplication
 {quote}
 Well in general it shouldn't, actually, because even if the offset commit fails/is preventing while the rebalance is in progress, if any partitions are migrated from one consumer to another then the origin…
- **Mikael:** We are using KafkaMessageListenerContainer from spring-kafka, which registers a ConsumerRebalanceListener that commits all offsets in its onPartitionsRevoked() method. I have now changed the application logic to always commit offsets synchronously in the same thread that calls Consumer.poll(), but t…
- _…14 more comments_

## KAFKA-14363: Add new `group-coordinator` module
Sub-task · Resolved (Fixed) · Major · created 2022-11-07 · resolved 2022-11-09


## KAFKA-14364: Support evolving serde with Foreign Key Join
Improvement · Open · Major · components: streams · created 2022-11-07

The current implementation of Foreign-Key join uses a hash comparison to determine whether it should emit join results or not. See [https://github.com/apache/kafka/blob/807c5b4d282e7a7a16d0bb94aa2cda9566a7cc2d/streams/src/main/java/org/apache/kafka/streams/kstream/internals/foreignkeyjoin/SubscriptionResolverJoinProcessorSupplier.java#L94-L110]
As specified in KIP-213 ([https://cwiki.apache.org/confluence/display/KAFKA/KIP-213+Support+non-key+joining+in+KTable] ), we must do a comparison of thi…


## KAFKA-14365: Extract common logic from Fetcher
Sub-task · Resolved (Fixed) · Major · components: clients, consumer · labels: consumer-threading-refactor · created 2022-11-07 · resolved 2023-03-24

The {{Fetcher}} class is used internally by the {{KafkaConsumer}} to fetch records from the brokers. There is ongoing work to create a new consumer implementation with a significantly refactored threading model. The threading refactor work requires a similarly refactored {{{}Fetcher{}}}.
This task includes refactoring {{Fetcher}} by extracting out some common logic to allow forthcoming implementations to leverage it.


## KAFKA-14366: Kafka consumer rebalance issue, offsets points back to very old committed offset
Bug · Open · Major · components: consumer, offset manager · created 2022-11-08

Hi All,
We are facing an issue while the client consumer restart (again not all restarts are ending up with this issue) and during the re-balancing scenario, sometimes one of the partition offsets goes back a long way from the committed offset.
Scenario :
Assume we have 4 instances of consumer and restarts of consumer one after the other.
 # At the time of starting restarts assume the offset on partition 10 of a topic being consumed is pointing to 50000. (last offset of the topic and 0 lag)…

- **Philip Nee:** Hey [~Chetu] - thanks for reporting this, could you kindly provide the steps to reproduce this issue?
- **Chetan:** Hi [~pnee] I will detail the steps to recreate the scenario in a day. I am currently collecting all details and will share the findings in detail.
- **Chetan:** Hi [~pnee] ,
 We were able to finally recreate the scenario in a lower environment.
 1. Consumer node 1  stopped at 4:58 PM IST/11:28 UTC  and started at 5:00PM IST/11:30 UTC
 2. Consumer node 2 stopped at 5:04PM IST/11:34 UTC and started at 5:07PM IST/11:37 UTC
 3. Consumer node 3 stopped at 5:11PM…
- **Philip Nee:** Hey [~Chetu] - two questions
  # How do you setup your rebalance listener, as you aren't doing autocommit, are you calling commitSync upon onPartitionsRevoked?
  # How and where do you log the committed offset?  
 Thanks
 P
- **Chetan:** Hi [~pnee],
  # We have created a custom Listener from ConsumerRebalanceListener and onPartitionsRevoked() we are doing commitSync offset
  # Each message consumed is logged with partition, offset, and topic information in the application log.
 Do you see if there is any issue or if the way we do it…
- _…2 more comments_

## KAFKA-14430: optimize: -Dcom.sun.management.jmxremote.rmi.port=$JMX_PORT
Improvement · Resolved (Fixed) · Minor · created 2022-12-01 · resolved 2022-12-02

In case the server has a firewall or is run inside a container, exposing only 'com.sun.management.jmxremote.port' cannot fetch metrics, and when the RMI port is not specified, it is randomly generated by default. We should make the two ports consistent for metrics data reading.
[https://bugs.openjdk.org/browse/JDK-8035404?page=com.atlassian.jira.plugin.system.issuetabpanels%3Achangehistory-tabpanel]
[https://www.baeldung.com/jmx-ports]


## KAFKA-14431: TopologyTestDriver instantiation raised NPE in JUnit5
Bug · Resolved (Fixed) · Minor · created 2022-12-01 · resolved 2022-12-01

Library: *kafka-streams*
Version: *3.3.1*
Framework: *spring-boot:2.7.6*
Defining the following code in JUnit5 test method:
[code/log omitted]
The test *passes* with following {*}{color:#FF0000}errors{color}{*}:
[code/log omitted]
*Acceptance Criteria:*
Manage to check for nullability

- **Mehrdad Karami:** Saw already fixed in truck branch

## KAFKA-14432: RocksDBStore relies on finalizers to not leak memory
Bug · Resolved (Fixed) · Blocker · components: streams · created 2022-12-01 · resolved 2022-12-08

Relying on finalizers in RocksDB has been deprecated for a long time, and starting with rocksdb 7, finalizers are removed completely (see [https://github.com/facebook/rocksdb/pull/9523]). 
Kafka Streams currently relies on finalizers in parts to not leak memory. This needs to be resolved before we can upgrade to RocksDB 7.
See  [https://github.com/apache/kafka/pull/12809] .
This is a native heap profile after running Kafka Streams without finalizers for a few hours:
[code/log omitted]


## KAFKA-14433: Clear all yammer metrics when test harnesses clean up
Improvement · Resolved (Fixed) · Major · created 2022-12-01 · resolved 2022-12-02

We should clear all yammer metrics from the yammer singleton when the integration test harnesses clean up. This would avoid memory leaks in tests that have a lot of test cases.

- **David Arthur:** I did some investigation on this. Running {{./gradlew -PmaxParallelForks=1 :core:integrationTest}} to better capture the leaked objects, I took a heap dump after 30 minutes. Several KafkaRaftManager instances were hanging around.
 !image-2022-12-01-13-53-57-886.png!
 This anonymous function "Partiti…

## KAFKA-14434: Why is this project not maintained anymore?
Improvement · Closed (Invalid) · Major · created 2022-12-02 · resolved 2022-12-02

Why is this project not maintained anymore? Can I continue to use it and submit pr?

- **jianbin.chen:** Sorry, I submitted this to kafka by mistake, I meant to submit it to incubator-retired-gossip
- **jianbin.chen:** invalid

## KAFKA-14435: Kraft: StandardAuthorizer allowing a non-authorized user when `allow.everyone.if.no.acl.found` is enabled
Bug · Resolved (Fixed) · Critical · components: kraft · created 2022-12-02 · resolved 2023-02-21

When `allow.everyone.if.no.acl.found` is enabled, the authorizer should allow everyone only if there is no ACL present for a particular resource. But if there are ACL present for the resource, then it shouldn't be allowing everyone.
StandardAuthorizer is allowing the principals for which no ACLs are defined even when the resource has other ACLs.
This behavior can be validated with the following test case:
[code/log omitted]
In the above test, `User:Bob` should be DENIED but the above test ca…

- **Purshotam Chauhan:** This can be fixed by adding a flag `noResourceAcls` in `MatchingAclBuilder` class. We can set this flag inside the `if` block [here|https://github.com/apache/kafka/blob/trunk/metadata/src/main/java/org/apache/kafka/metadata/authorizer/StandardAuthorizerData.java#L523].

## KAFKA-14436: Initialize KRaft with arbitrary epoch
Sub-task · Resolved (Won't Fix) · Major · created 2022-12-02 · resolved 2023-03-24

For the ZK migration, we need to be able to initialize Raft with an arbitrarily high epoch (within the size limit). This is because during the migration, we want to write the Raft epoch as the controller epoch in ZK. We require that epochs in /controller_epoch are monotonic in order for brokers to behave normally.

- **Colin McCabe:** We decided to preserve and continue to use the ZK epoch instead. Closing.

## KAFKA-14437: Enhance StripedReplicaPlacer to account for existing partition assignments
Improvement · Open · Major · created 2022-12-02

Currently, in StripedReplicaPlacer we don’t take existing partition assignments into consideration when the place method is called. This means for new partitions added, they may get the same assignments as existing partitions. This differs from AdminUtils, which has some logic to try and shift where in the list of brokers we start making assignments from for new partitions added.
For example, lets say we had the following
[code/log omitted]
CreateTopics might return the following assignment f…

- **Andrew Grant:** I created a draft PR to illustrate the idea [https://github.com/apache/kafka/pull/12943|https://github.com/apache/kafka/pull/12943,]

## KAFKA-14438: Throw error when consumer configured with empty/whitespace-only group.id for AsyncKafkaConsumer
Task · Closed (Fixed) · Blocker · components: clients, consumer · labels: kip-848-client-support, kip-848-e2e, kip-848-preview · created 2022-12-02 · resolved 2023-12-04

Currently, a warning message is logged upon using an empty consumer groupId. In the next major release, we should drop the support of empty ("") consumer groupId.
cc [~hachikuji]
See [KIP-289|https://cwiki.apache.org/confluence/display/KAFKA/KIP-289%3A+Improve+the+default+group+id+behavior+in+KafkaConsumer] for more detail.

- **Kirk True:** +1
- **Kirk True:** [~pnee] - is this something you want to provide a patch for?
- **Philip Nee:** I think we could un-support the groupId="" after rolling out the new consumer?

## KAFKA-14439: Specify returned errors for various APIs and versions
Task · Open · Major · created 2022-12-02

Kafka is known for supporting various clients and being compatible across different versions. But one thing that is a bit unclear is what errors each response can send. 
Knowing what errors can come from each version helps those who implement clients have a more defined spec for what errors they need to handle. When new errors are added, it is clearer to the clients that changes need to be made.
It also helps contributors get a better understanding about how clients are expected to react and p…

- **Jason Gustafson:** Yeah, we've had so many compatibility breaks due to error code usage. Putting the errors into the spec would also enable better enforcement. One option could be something like this:
 [code/log omitted]
 Here "enum16" indicates a 2-byte enumeration where the values are provided in the `values` field.…
- **Ismael Juma:** I think it would also be useful for the server to indicate whether an error is retriable or not. That would make protocol evolution a lot more flexible.
- **Tom Bentley:** FWIW I spent some time on this a few years ago, see [KAFKA-7787|https://issues.apache.org/jira/browse/KAFKA-7787].
- **David Jacot:** +1 for having supported errors in the protocol.

## KAFKA-14440: Local state wipeout with EOS
Bug · Resolved (Duplicate) · Major · components: streams · created 2022-12-03 · resolved 2022-12-06

Hey,
I have a kafka streams service that aggregates events from multiple input topics (running in a k8s cluster). The topology has multiple FKJs. The input topics have around 7 billion events when the service was started from `earliest`.
The service has EOS enabled and 
[code/log omitted]
The problem I am having is with frequent local state wipe-outs, this leads to very long rebalances. As can be seen from the attached images, local disk sizes go to ~ 0 very often. These wipe out are part of…

- **Matthias J. Sax:** What you observe is behavior by-design (the design is no ideal...). Note that the local checkpoint files only contain metadata... And for EOS they are not updated regularly, but actually read on startup and deleted afterwards, and only written again on a clean stop.
 It's a known issue, but not a bu…
- **Abdullah alkhawatrah:** Makes sense. Thanks!

## KAFKA-14540: DataOutputStreamWritable#writeByteBuffer writes the wrong portion of the parameterized buffer
Bug · Resolved (Fixed) · Minor · created 2022-12-21 · resolved 2023-02-24

The method DataOutputStreamWritable#writeByteBuffer uses the buffer's position instead of its arrayOffset when writing the buffer to the output stream. As a result, the resulting buffer is corrupted.

- **Michael Marshall:** Fixed by https://github.com/apache/kafka/pull/13032

## KAFKA-14541: Profile produce workload for Apache Kafka
Improvement · In Progress · Major · created 2022-12-21

I have been profiling Kafka (3.4.0 / trunk right now) for a produce only workload and the [OpenMessaging|https://openmessaging.cloud/docs/benchmarks/] workloads. The goal is to get a better understanding of CPU usage profile for Kafka and eliminate potential overheads to reduce CPU consumption.
h2. *Setup*
R6i.16xl (64 cores)
OS: Amazon Linux 2
Single broker, One topic, One partition
Plaintext
Prometheus Java agent attached
[code/log omitted]
[code/log omitted]
h3. Producer setup:
[cod…

- **Ismael Juma:** Can you share a little more details regarding your producer setup, was it a single producer? Also, is there a reason why `linger.ms=0` and `batch.size=9000` was used for this benchmark? If you have a benchmark with reasonable throughput, you'd usually want those numbers to be higher.
- **Ismael Juma:** [code/log omitted]
 `duplicate` doesn't copy the buffer.

## KAFKA-14542: Deprecate OffsetFetch/Commit version 0 and remove them in 4.0
Improvement · Resolved (Duplicate) · Major · created 2022-12-21 · resolved 2025-03-20

We should deprecate OffsetFetch/Commit APIs and remove them in AK 4.0. Those two APIs are used by old clients to write offsets to and read offsets from ZK.
We need a small KIP for this.

- **Ismael Juma:** [https://cwiki.apache.org/confluence/display/KAFKA/KIP-896%3A+Remove+old+client+protocol+API+versions+in+Kafka+4.0] covers this and more.
- **David Jacot:** Addressed by https://issues.apache.org/jira/browse/KAFKA-14560.

## KAFKA-14543: Move LogOffsetMetadata to storage module
Sub-task · Resolved (Fixed) · Major · created 2022-12-21 · resolved 2022-12-28

- **Satish Duggana:** [~mimaison]
  `LogOffsetMetadata` refactoring to move to storage module is being done as part of https://issues.apache.org/jira/browse/KAFKA-14480.
 Glad to raise PR against https://issues.apache.org/jira/browse/KAFKA-14543 for that specific change if you have not yet started working on that.
- **Mickael Maison:** [~satish.duggana] I pretty much have the PR ready. I can open it today but otherwise if it's messing up your work too much, I can drop it and let you do it in https://issues.apache.org/jira/browse/KAFKA-14480
- **Mickael Maison:** I opened https://github.com/apache/kafka/pull/13038
- **Satish Duggana:** [~mimaison] Pulling these changes should not cause too much disruption in my branch. I will pull them once it is merged to trunk.

## KAFKA-14544: The "is-future" should be removed from metrics tags after future log becomes current log
Bug · Resolved (Fixed) · Minor · created 2022-12-21 · resolved 2022-12-26

we don't remove "is-future=true" tag from future log after the future log becomes "current" log. It causes two potential issues:
 # the metrics monitors can't get metrics of Log if they don't trace the property "is-future=true".
 # all Log metrics of specify partition get removed if the partition is moved to another folder again.


## KAFKA-14545: MirrorCheckpointTask throws NullPointerException when group hasn't consumed from some partitions
Bug · Resolved (Fixed) · Major · components: mirrormaker · created 2022-12-21 · resolved 2023-01-04

MirrorTaskConnector looks like it's throwing a NullPointerException when a consumer group hasn't consumed from all topics from a partition. This blocks the syncing of consumer group offsets to the target cluster. The stacktrace and error message is as follows:
[code/log omitted]
This seems to happen if the OffsetFetch call returns a OffsetFetchPartitionResponsePartition with a negative commitedOffset. Mirrormaker should handle this case more gracefully and still be sync over consumer offsets f…

- **Chris Solidum:** Adding a check for null values in [MirrorCheckpointTask.checkpointsForGroups |https://github.com/apache/kafka/blob/trunk/connect/mirror/src/main/java/org/apache/kafka/connect/mirror/MirrorCheckpointTask.java#L172]seems like the simplest fix for this issue.
- **Chris Solidum:** ended up making the change in checkpoint instead of checkpointsForGroups since it was easier to test there.

## KAFKA-14546: Allow Partitioner to return -1 to indicate default partitioning
Improvement · Open · Major · components: producer  · created 2022-12-21

Prior to KIP-794 it was possible to create a custom Partitioner that could delegate to the DefaultPartitioner.  DefaultPartitioner has been deprecated so we can now only delegate to BuiltInPartitioner.partitionForKey which does not handle a non-keyed message.  Hence there is now no mechanism for a custom Partitioner to fallback to default partitioning, e.g. for the non-keyed sticky case.
I would like to propose that KafkaProducer.partition(...) not throw IllegalArgumentException if the Partitio…

- **James Olsen:** [~viktorsomogyi] Is this on anyones' radar?  This will become a show-stopper if DefaultPartitioner is eventually removed.
- **James Olsen:** I'm still hoping for a solution to this issue.  I can understand the reluctance to allow a {{Partitioner}} to return {{RecordMetadata.UNKNOWN_PARTITION}} however there is another solution that would work.  As my requirement discussed above is to ensure consistent partitioning for each Topic using a…

## KAFKA-14547: Be able to run kafka KRaft Server in tests without needing to run a storage setup script
Improvement · Open · Major · components: kraft · created 2022-12-22

Currently kafka KRaft Server requires running kafka-storage.sh in order to start properly.
This makes setup much more cubersome for build tools like bazel to work properly.
One way to mitigate this is to configure the paths via kafkaConfig...

- **Ismael Juma:** Related KIP https://cwiki.apache.org/confluence/display/KAFKA/KIP-785%3A+Automatic+storage+formatting
- **Matthew de Detrich:** Ill have a look into this

## KAFKA-14548: Stable streams applications stall due to infrequent restoreConsumer polls
Bug · Resolved (Duplicate) · Major · components: streams · created 2022-12-22 · resolved 2022-12-27

We have observed behavior with Streams where otherwise healthy applications stall and become unable to process data after a rebalance (https://issues.apache.org/jira/browse/KAFKA-13405.) The root cause of which is that a restoreConsumer can be partitioned from a Kafka cluster with stale metadata, while the mainConsumer is healthy with up-to-date metadata. This is due to both an issue in streams and an issue in the consumer logic.
In StoreChangelogReader, a long-lived restoreConsumer is kept ins…

- **Greg Harris:** [~mjsax] as you had previously categorized https://issues.apache.org/jira/browse/KAFKA-13405 (which has the exact same cause and symptoms as this issue) as Not A Bug, do you think that the reasoning for the above tactical fix make sense?
- **Matthias J. Sax:** {quote}This is an anti-pattern, as frequent poll()s are expected to keep kafka consumers in contact with the kafka cluster.
 {quote}
 Well, not really. Note that the JavaDoc you quote is about a consumer that is part of a consumer group. However, the restore consumer is a "stand along" consumer and…
- **Greg Harris:** > Note that the JavaDoc you quote is about a consumer that is part of a consumer group. However, the restore consumer is a "stand along" consumer and not part of any group and thus periodic polling is not necessary. There is no consumer group, group management, or heart beating etc.
 Yes, I understa…
- **Greg Harris:** [~mjsax] Thanks for your patience on this issue. I will no longer be pursuing this specific change.
 I explored the above proposed fix more deeply, and it appears that it is not reasonable to add to streams. This is because it is illegal to call poll() on a consumer with no active subscriptions, whi…
- **Matthias J. Sax:** Thanks! – I have of course an interest to get this addressed. What client ticket would need to be tackled? Are they all linked to this ticket? If we understand what needs to be done, I am happy to make a case to get this prioritized. Also, what KIP did you refer to?
- _…2 more comments_

## KAFKA-14549: Move LogDirFailureChannel to storage module
Sub-task · Resolved (Fixed) · Major · created 2022-12-22 · resolved 2022-12-23


## KAFKA-14550: MoveSnapshotFile and CorruptSnapshotException to storage module
Sub-task · Resolved (Fixed) · Major · components: core · created 2022-12-23 · resolved 2023-01-02

- **Ismael Juma:** For some reason, I can't change the status of this ticket. It would be useful to set it to "Patch Available". Same for other tickets that have a PR.

## KAFKA-14594: Move LogDirsCommand to tools
Sub-task · Resolved (Fixed) · Major · created 2023-01-05 · resolved 2023-05-04


## KAFKA-14595: Move ReassignPartitionsCommand to tools
Sub-task · Resolved (Fixed) · Major · created 2023-01-05 · resolved 2023-11-01

- **Nikolay Izhikov:** Hello [~omnia_h_ibrahim] 
 Can I assign this ticket to myself? 
 I want to implement it and it seems that you working on another "move utility" ticket in the moment.
- **Omnia Ibrahim:** [~nizhikov] sure
- **Omnia Ibrahim:** Hi [~nizhikov], just a note, I moved the methods `{{{}TestUtils.setReplicationThrottleForPartitions{}}}` and `{{{}TestUtils.removeReplicationThrottleForPartitions`  from `{}}}{{{}TestUtils` to `{}}}{{{}ToolsTestUtils{}}}{{{}` {}}}{{ as they are used only }} by `TopicCommand` and `ReassignPartitionCo…
- **Nikolay Izhikov:** [~omnia_h_ibrahim] Thanks to let me know!
- **Nikolay Izhikov:** Hello
 To reduce changes and make them reviewable I propose to split task into several.
 As a first step it seems feasible to move value-objects(sealed case classes and traits) from scala code to java.
 These classes are:
 * PartitionMove
 * LogDirMoveState
 * MissingReplicaMoveState and other LogDi…
- _…2 more comments_

## KAFKA-14596: Move TopicCommand to tools
Sub-task · Resolved (Fixed) · Major · created 2023-01-05 · resolved 2023-10-17


## KAFKA-14597: [Streams] record-e2e-latency-max is not reporting correct metrics 
Bug · Resolved (Fixed) · Major · components: metrics, streams · created 2023-01-05 · resolved 2026-08-10

I was following this KIP documentation ([https://cwiki.apache.org/confluence/display/KAFKA/KIP-613%3A+Add+end-to-end+latency+metrics+to+Streams]) and kafka streams documentation ([https://kafka.apache.org/documentation/#kafka_streams_monitoring:~:text=node%2Did%3D(%5B%2D.%5Cw%5D%2B)-,record%2De2e%2Dlatency%2Dmax,-The%20maximum%20end]) . Based on these documentations , the *record-e2e-latency-max* should monitor the full end to end latencies, which includes both *consumption latencies* and  {*}pr…

- **Bruno Cadonna:** [~talestonini] Thank you for the ticket!
 I noticed that in your screenshot record {{record-e2e-latency-max.jpg}} the metric {{process-total}} is 0 which means that no records were processed when the metric {{record-e2e-latency-max}} got recorded. That would explain why {{record-e2e-latency-max}} is…
- **Tales Tonini:** Hi [~cadonna] , I went through [KIP-613|https://cwiki.apache.org/confluence/display/KAFKA/KIP-613%3A+Add+end-to-end+latency+metrics+to+Streams], its discussion thread, the associated PRs, the trunk code and the related tests. AFAIU:
  # right before starting the source node processing, the processor…
- **Atul Jain:** Hi [~cadonna] , 
 {quote}Could you run your Streams application and ensure that {{process-total}} is 1 or greater when you look at {{{}record-e2e-latency-max{}}}?
 Please, let us know whether the value of the metric makes more sense then.
 {quote}
 In order to report this issue, I started the Stream…
- **Tales Tonini:** Hi [~atuljainiitk] , may I ask what Kafka Streams version you have in your app? Thanks.
- **Atul Jain:** I currently have 2.6.0 version
- _…6 more comments_

## KAFKA-14598: Fix flaky ConnectRestApiTest
Bug · Reopened · Minor · components: connect · labels: flaky-test · created 2023-01-06

ConnectRestApiTest sometimes fails with the message
{{ConnectRestError(404, '<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html;charset=ISO-8859-1"/>\n<title>Error 404 Not Found</title>\n</head>\n<body><h2>HTTP ERROR 404 Not Found</h2>\n<table>\n<tr><th>URI:</th><td>/connector-plugins/</td></tr>\n<tr><th>STATUS:</th><td>404</td></tr>\n<tr><th>MESSAGE:</th><td>Not Found</td></tr>\n<tr><th>SERVLET:</th><td>-</td></tr>\n</table>\n\n</body>\n</html>\n', 'http://172.31.1.75:8083/conn…

- **Ashwin Pankaj:** Did not see this occuring recently - closing this issue.
- **Ashwin Pankaj:** Did not observe this recently
- **Greg Harris:** [~ashwinpankaj] The PR for this is a one line fix, and you already proved that it was fixing a flakey failure. I don't think this should be closed as the problem has not been addressed.
 If you no longer wish to work on this, leave it open and unassigned.

## KAFKA-14599: MirrorMaker pluggable interfaces missing from public API
Bug · Patch Available · Major · components: mirrormaker · created 2023-01-06

MirrorMaker exposes a few pluggable APIs, including:
ConfigPropertyFilter
GroupFilter
TopicFilter
ForwardingAdmin
These are currently missing from our javadoc.

- **Nikolay Izhikov:** Hello, [~mimaison] , [~ChrisEgerton] 
 Can you, please, take a look at my changes?
 https://github.com/apache/kafka/pull/13157

## KAFKA-14600: Flaky test ProducerIdExpirationTest
Test · Resolved (Fixed) · Major · created 2023-01-06 · resolved 2023-02-06

The ProducerIdExpiration test appears to have these flakey failures:
Build / JDK 8 and Scala 2.13 / testTransactionAfterTransactionIdExpiresButProducerIdRemains(String).quorum=zk – kafka.api.ProducerIdExpirationTest: 5 failures
        https://ci-builds.apache.org/blue/organizations/jenkins/Kafka%2Fkafka/detail/trunk/1484/tests/
                org.opentest4j.AssertionFailedError: Producer IDs were not added.
        https://ci-builds.apache.org/blue/organizations/jenkins/Kafka%2Fkafka/detai…


## KAFKA-14601: Improve exception handling in KafkaEventQueue
Bug · Open · Major · created 2023-01-06

If KafkaEventQueue gets an InterruptedException while waiting for a condition variable, it currently exits immediately. Instead, it should complete the remaining events exceptionally and then execute the cleanup event. This will allow us to finish any necessary cleanup steps.
Also, handle cases where Event#handleException itself throws an exception.


## KAFKA-14602: offsetDelta in BatchMetadata is an int but the values are computed as difference of offsets which are longs.
Bug · Open · Major · components: core · created 2023-01-07

This is a followup of the discussion in https://github.com/apache/kafka/pull/13043#discussion_r1063071578
offsetDelta in BatchMetadata is an int. Becasue of which, ProducerAppendInfo may set a value that can overflow. Ideally, this data type should be long instead of int.


## KAFKA-14603: Move KafkaMetricsGroup to server-common module.
Sub-task · Resolved (Fixed) · Major · components: core · created 2023-01-07 · resolved 2023-03-09

- **Satish Duggana:** [~ivanyu] Assigned to you as you are already working on this with https://github.com/apache/kafka/pull/13067/
 Please feel free to reassign if needed.
- **Ivan Yurchenko:** Thank you [~satish.duggana]. I'll move PR out of the draft state soon

## KAFKA-14604: SASL session expiration time will be overflowed when calculation
Bug · Resolved (Fixed) · Major · created 2023-01-07 · resolved 2025-08-03

When sasl server of client set a large expiration time, the timeout value might be overflowed, and cause the session timeout immediately.
[Here|https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/common/security/authenticator/SaslServerAuthenticator.java#L694]'s the sasl server timeout's calculation
[Here|https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/common/security/authenticator/SaslClientAuthenticator.java#L692]'s the sasl cli…

- **PoAn Yang:** PR: [https://github.com/apache/kafka/pull/18526]

## KAFKA-14640: Update AddPartitionsToTxn protocol to batch and handle verifyOnly requests
Sub-task · Resolved (Fixed) · Major · created 2023-01-19 · resolved 2023-03-07

As part of KIP-890 we are making some changes to this protocol.
1. We can send a request to verify a partition is added to a transaction
2. We can batch multiple transactional IDs


## KAFKA-14641: Cleanup CommitNeeded after EOS-V1 is removed
Improvement · Open · Major · components: streams · created 2023-01-19

This is a follow-up of KAFKA-14294.
Today we have several flags to determine if KS need to execute a commit: 1) task-level "commitNeeded" which is set whenever process() or punctuator() is called, 2) if there are input topic offsets to commit, retrieved from the "task.prepareCommit()", 3) the "transactionInFlight" flag from producer as a fix of KAFKA-14294 (this subsumes the first "commitNeeded" functionality).
Given that we are still having EOS-v1, cleanup this would be a bit complex. But aft…


## KAFKA-14642: TopicBased RemoteLogMetadataManager can't support reassign user-partitions
Improvement · Open · Blocker · components: core · created 2023-01-20

{*}Background{*}:
In [KIP-405: Kafka Tiered Storage - Apache Kafka - Apache Software Foundation|https://cwiki.apache.org/confluence/display/KAFKA/KIP-405%3A+Kafka+Tiered+Storage],  kafka introduced the feature of hierarchical storage.
Also, [KAFKA-9555] Topic-based implementation for the RemoteLogMetadataManager - ASF JIRA (apache.org) implements the default RLMM - 'TopicBased-RLMM'.
{*}Problem{*}:
TopicBased-RLMM will only subscribe to the Partitions where the current Broker is Leader or Fo…

- **hzh0425:** Hi, [~satishd] [~junrao] [~Hangleton] , Could you pls help to review this issue?
- **Satish Duggana:** Thanks [~hzh0425@apache] for the JIRA. Our implementation on 2.8.x handles those scenarios, and [~ckamal] is planning to  update RLMM on trunk with these improvements.
- **Alexandre Dupriez:** Thanks [~hzh0425@apache] for the report. Really appreciate you looking at the tier storage feature. Let's keep this rolling. Thanks!
- **hzh0425:** Thanks for your reply! [~satish.duggana] [~Hangleton] 
 So what is your solution? Let RLMM subscribe to all topics? Have you considered using rocksdb to store the full amount of metadata?
 I'm looking forward to having the opportunity to implement Tiered-Stoarge with you, because I am now promoting…
- **hzh0425:** BTW, can I implement a Rocksdb based metadataCache for TopicBased RLMM? [~Hangleton] [~satish.duggana]
- _…2 more comments_

## KAFKA-14643: TopicBased RemoteLogMetadataManager can't support reassign user-partitions
Improvement · Open · Major · components: core · created 2023-01-20

{*}Background{*}:
In [KIP-405: Kafka Tiered Storage - Apache Kafka - Apache Software Foundation|https://cwiki.apache.org/confluence/display/KAFKA/KIP-405%3A+Kafka+Tiered+Storage],  kafka introduced the feature of hierarchical storage.
Also, KAFKA-9555 Topic-based implementation for the RemoteLogMetadataManager - ASF JIRA (apache.org) implements the default RLMM - 'TopicBased-RLMM'.
{*}Problem{*}:
TopicBased-RLMM will only subscribe to the Partitions where the current Broker is Leader or Foll…


## KAFKA-14644: Process should stop after failure in raft IO thread
Bug · Resolved (Fixed) · Major · created 2023-01-20 · resolved 2023-01-25

We have seen a few cases where an unexpected error in the Raft IO thread causes the process to enter a zombie state where it is no longer participating in the raft quorum. In this state, a controller can no longer become leader or help in elections, and brokers can no longer update metadata. It may be better to stop the process in this case since there is no way to recover.


## KAFKA-14645: Plugin classloader not used when retrieving connector plugin config defs via REST API
Bug · Resolved (Fixed) · Major · components: connect · created 2023-01-23 · resolved 2023-01-30

We don't switch to the plugin classloader when servicing requests to the {{GET /connector-plugins/<type>/config}} endpoint, which can result in classloading failures for, e.g., properties that accept the name of a pluggable class to load.
Reported externally in [https://github.com/kcctl/kcctl/issues/266]


## KAFKA-14646: SubscriptionWrapper is of an incompatible version (Kafka Streams 3.2.3 -> 3.3.2)
Bug · Resolved (Fixed) · Major · components: streams · created 2023-01-23 · resolved 2023-01-26

Hey folks,
we've just updated an application from *_Kafka Streams 3.2.3 to 3.3.2_* and started getting the following exceptions:
[code/log omitted]
After swiftly looking through the code, this exception is potentially thrown in two places:
 * [https://github.com/apache/kafka/blob/3.3.2/streams/src/main/java/org/apache/kafka/streams/kstream/internals/foreignkeyjoin/SubscriptionJoinForeignProcessorSupplier.java#L73-L78]
 ** Here the check was changed in Kafka 3.3.x: [https://github.com/apache…

- **Matthias J. Sax:** Did you upgrade with two rolling bounced leveraging `upgrad_from` config?
 I assume is related to https://issues.apache.org/jira/browse/KAFKA-13769
 Of course, K13769 could have introduced some bug, but we actually to test rolling upgrades and would hope it would have caught it (otherwise, we need t…
- **Jochen Schalanda:** {quote}Did you upgrade with two rolling bounced leveraging `upgrad_from` config?
 {quote}
 [~mjsax] Ah, in fact we didn't. I assumed (incorrectly) that this would only be necessary when updating across major versions.
 I found [https://kafka.apache.org/33/documentation/streams/upgrade-guide] which c…
- **Matthias J. Sax:** Thanks for following up – glad to hear that it's in the docs... And I hope it resolved the problem.
- **Jochen Schalanda:** Unfortunately the two rolling updates (with {{upgrade.from="3.2"}} and then removing the setting again) didn't help.
 We still see the same exception:
 [code/log omitted]
 [~mjsax] Do you have any hints how to resolve this issue? We see it in only 2 topologies out of 15 and I'm afraid that downgradi…
- **Jochen Schalanda:** Could it still be that the check in [https://github.com/apache/kafka/blob/3.3.2/streams/src/main/java/org/apache/kafka/streams/kstream/internals/foreignkeyjoin/SubscriptionStoreReceiveProcessorSupplier.java#L94-L99] is too restrictive and should read *{{record.value().getVersion() > SubscriptionWrap…
- _…4 more comments_

## KAFKA-14647: Move TopicFilter shared class
Sub-task · Resolved (Fixed) · Major · created 2023-01-24 · resolved 2023-07-18

- **Sagar Rao:** Move TopicFilter in core/kafka/utils to server-common util since this is also shared by a few commands.

## KAFKA-14648: Do not fail clients if bootstrap servers is not immediately resolvable
Bug · Resolved (Fixed) · Major · components: clients · created 2023-01-24 · resolved 2026-07-29

In dynamic environments, such as system tests, there is sometimes a delay between when a client is initialized and when the configured bootstrap servers become available in DNS. Currently clients will fail immediately if none of the bootstrap servers can resolve. It would be more convenient for these environments to provide a grace period to give more time for initialization.

- **Kirk True:** Would a fix for this cover the case where {{ClientUtils.parseAndValidateAddresses}} can't resolve any of the addresses in the bootstrap servers set? We're seeing a case where there's a blip in DNS resolution during the time of {{KafkaAdminClient}} construction and it is unrecoverable.

## KAFKA-14649: Failures instantiating Connect plugins hides other plugins from REST API, or crash worker
Bug · Resolved (Fixed) · Minor · components: connect · created 2023-01-24 · resolved 2023-03-02

Connect plugin path scanning evaluates the version() method of plugins to determine which version of a plugin to load, and what version to advertise as part of the REST API. This process involves reflectively constructing an instance of the class and calling the version method, which can fail in the following scenarios:
1. If a plugin throws an exception from a static initialization block
2. If a plugin does not have a default constructor (such as a non-static inner class)
3. If a plugin has…


## KAFKA-14650: IQv2 can throw ConcurrentModificationException when accessing Tasks 
Bug · Resolved (Fixed) · Major · components: streams · created 2023-01-24 · resolved 2023-02-09

From failure in *[PositionRestartIntegrationTest.verifyStore[cache=false, log=true, supplier=IN_MEMORY_WINDOW, kind=PAPI]|https://ci-builds.apache.org/job/Kafka/job/kafka/job/3.4/63/testReport/junit/org.apache.kafka.streams.integration/PositionRestartIntegrationTest/Build___JDK_11_and_Scala_2_13___verifyStore_cache_false__log_true__supplier_IN_MEMORY_WINDOW__kind_PAPI_/]*
java.util.ConcurrentModificationException
	at java.base/java.util.TreeMap$PrivateEntryIterator.nextEntry(TreeMap.java:1208)…


## KAFKA-14737: Move kafka.utils.json to server-common
Sub-task · Resolved (Fixed) · Major · created 2023-02-21 · resolved 2023-07-18

The JSON utils are used by a few tools (DeleteRecordsCommand, ReassignPartitionsCommand and LeaderElectionCommand) and also by a few other classes in core.

- **Ismael Juma:** It makes sense to have a similar class in `server-common`, but I don't think it makes sense to move the one in `core` since it's a thin wrapper over `Jackson` anyway.
- **Omnia Ibrahim:** I will add a similar class in `server-common` to unblock the moving these commands out of core. And later we can decide if we need need to switch to this server-common one everywhere or not.

## KAFKA-14738: Topic disappears from kafka_topic.sh --list after modifying it with kafka_acl.sh
Bug · Resolved (Not A Bug) · Major · components: core · created 2023-02-21 · resolved 2023-02-27

Topic is not listed via kafka-topics.sh --list after modifying it with kafka-acls.sh (-add --allow-principal User:CN=test --operation Read):
$ /opt/kafka/bin/kafka-topics.sh --create --bootstrap-server kafka:9092 --topic test2 --replication-factor 1 --partitions 50
Created topic test2.
$ /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server kafka:9092 --topic test2
test2
$ /opt/kafka/bin/kafka-acls.sh --bootstrap-server kafka:9092 --topic test2 --add --allow-principal User:CN=test --oper…

- **Soumyajit Sahu:** This is not a bug. You are listing your topics as ANONYMOUS user and your topic now has an acl for User:test.
 If you try to list the topics as user test, it should list it for you. Try the --command.config parameter to pass a jaas config.
- **Soumyajit Sahu:** This isn't a big. You are listing topics as ANONYMOUS user while your topic has an acl for User:test only.
 Try using the --command.config to pass a jaas config and run the command as User:test.
- **Gabriel Lukacs:** ok, thanks for clarification, my fault, i was not familiar with acl/jaas, but now it is clear.
 sorry for inconveniences, pls close this bug.

## KAFKA-14739: Kafka consumer reading messages out of order after a rebalance
Bug · Open · Major · created 2023-02-21

We are seeing often when our consumers are running and a rebalance is triggered, some partitions do not resume at the correct offset causing a large number of events to be skipped.
Our understanding is that within a partition events should also be read in chronological order.
These consumers run once a day and we see that when they resume again the next day it does return to the missed events.  
An example we investigated: 
{quote}We see for partition 88 starting processing around Offset 140…

- **Luke Chen:** [~colinshaw] , Have you tried to run with the latest version of kafka client? We did some improvement to it before. Please check if this issue still existed. Thanks.

## KAFKA-14740: Missing source tag on MirrorSource metrics
Improvement · Resolved (Fixed) · Major · components: mirrormaker · created 2023-02-22 · resolved 2023-03-21

The metrics defined in MirrorSourceMetrics have the following tags "target", "topic", "partition". It would be good to also have a "source" tag with the source cluster alias.

- **Mickael Maison:** [~ryannedolan] Do you remember if there was a reason not to include the source tag on these metrics? MirrorCheckpointMetrics have the source tag.
- **Ryanne Dolan:** [~mimaison] the topic name usually includes the source cluster already, so I figured it was redundant. With identity replication you don't get that, but you presumably know what the source is in such cases. I don't have any objections to adding it tho.
- **Mickael Maison:** Thanks for the quick reply. I think it would make dealing metrics a little bit easier when you have a bunch of mirroring routes between multiple clusters. I'll draft a small KIP.

## KAFKA-14741: Add description field to connector configs
Improvement · Resolved (Won't Do) · Major · components: connect · created 2023-02-22 · resolved 2023-04-05

Connectors are identified by their name. In many cases it would be useful to attach a description/comment to connectors to provide some context. This would be especially useful on Connect clusters running several connectors and/or shared by multiple teams.


## KAFKA-14742: Flaky ExactlyOnceSourceIntegrationTest.testConnectorBoundary OOMs
Improvement · Resolved (Fixed) · Minor · labels: flaky-test · created 2023-02-22 · resolved 2023-02-28

The ExactlyOnceSourceIntegrationTest appears to occasionally throw the following exception in my local test runs:
[code/log omitted]
It appears that the data produced by the connectors under test is too large to be asserted on with the current assertions' memory overhead. We should try to optimize the assertions' overhead and or reduce the number of records being asserted on.


## KAFKA-14743: MessageConversionsTimeMs for fetch request metric is not updated
Bug · Resolved (Fixed) · Major · components: core · created 2023-02-23 · resolved 2023-02-26

During message conversion, there are 2 metrics we should update as doc written:
!image-2023-02-23-18-09-24-916.png|width=652,height=121!
In KAFKA-14295, it is addressing the issue in FetchMessageConversionsPerSec metric. This ticket will address the issue in *kafka.network:type=RequestMetrics,name=MessageConversionsTimeMs,request=fetch.*

- **Luke Chen:** PR: https://github.com/apache/kafka/pull/13297
