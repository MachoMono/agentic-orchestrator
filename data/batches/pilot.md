## KAFKA-12345: KIP-500: AlterIsrManager crashes on broker idle-state
Task · Resolved (Fixed) · Minor · components: core · labels: kip-500 · created 2021-02-19 · resolved 2021-04-17

Occasionally, a scheduler thread on a broker crashes with this stack
[code/log omitted]
After that the broker is unable to fetch any records from any other broker (and vice versa)
[code/log omitted]

- **Alok Nikhil:** Adding a bit more context. Seems like there was a controller quorum voting event just before this crash. Seems to be related
 [code/log omitted]
- **Deng Ziming:** hello, please provide your specified Kafka version, or the revision number if you are using the dev branch of kafka for convenience.
- **Alok Nikhil:** Hi [~dengziming]. I have updated the Kafka version and the priority. This is part of the KIP-500 merge. So, it's not an active issue (considering KIP-500 is still in development and not the default mode the Broker will operate in).
- **Deng Ziming:** This is weird, I investigated it for some time and found it's impossible for AlteIsrMgr to throw a NEP, do you have other useful information, for example, the revision number of your source code, or do you have changed the source code?

## KAFKA-12567: Flaky Test TransactionsTest.testFencingOnCommit
Test · Open · Critical · components: core, unit tests · labels: flaky-test · created 2021-03-27

{quote}org.opentest4j.AssertionFailedError: Consumed 0 records before timeout instead of the expected 2 records at org.junit.jupiter.api.AssertionUtils.fail(AssertionUtils.java:39) at org.junit.jupiter.api.Assertions.fail(Assertions.java:117) at kafka.utils.TestUtils$.pollUntilAtLeastNumRecords(TestUtils.scala:852) at kafka.utils.TestUtils$.consumeRecords(TestUtils.scala:1476) at kafka.api.TransactionsTest.testFencingOnCommit(TransactionsTest.scala:331){quote}
STDOUT (all of those line appear m…


## KAFKA-12882: Add ActiveBrokerCount and FencedBrokerCount metrics (KIP-748)
Improvement · Resolved (Fixed) · Minor · labels: needs-kip · created 2021-06-02 · resolved 2021-10-25

Adding RegisteredBrokerCount and UnfencedBrokerCount metrics to the QuorumController.

- **Konstantine Karantasis:** The KIP has been published but it's still under discussion. 
 [https://cwiki.apache.org/confluence/display/KAFKA/KIP-748%3A+Add+Broker+Count+Metrics#KIP748:AddBrokerCountMetrics]
 I'm resetting the Fix version since we are past the relevant deadlines. Please make sure to set the appropriate version…
- **David Jacot:** [~rdielhenn] I have split the ticket into two tasks, one for each controller. I will do the ZK one.

## KAFKA-12892: InvalidACLException thrown in tests caused jenkins build unstable
Bug · Open · Major · created 2021-06-04

In KAFKA-12866, we fixed the issue that Kafka required ZK root access even when using a chroot. But after the PR merged (build #183), trunk build keeps failing at least one test group (mostly, JDK 15 and Scala 2.13). The build result will said nothing useful:
[code/log omitted]
After investigation, I found the failed tests is because there are many `InvalidACLException` thrown during the tests, ex:
[code/log omitted]
Log can be found [here|[https://ci-builds.apache.org/blue/rest/organization…

- **Luke Chen:** I tried to set the original root acl back, but it failed. That is:
 [code/log omitted]
 I think we need [~soarez] [~omkreddy]  's help. Thanks.
- **Bruno Cadonna:** Is PR #10821 supposed to solve the issue?
 I still see a lot of 
 [code/log omitted]
 Also on PRs that contain PR #10821. For example https://ci-builds.apache.org/blue/rest/organizations/jenkins/pipelines/Kafka/pipelines/kafka-pr/branches/PR-10856/runs/3/nodes/14/steps/121/log/?start=0
- **Igor Soarez:** Yes it was - by applying the ACL changes to a unique child znode instead of to the root, there shouldn't be any interference with other tests. I'm not sure if this is the new test that's still a problem or if there's any lingering state in zookeeper across builds. It is strange that only some test r…

## KAFKA-13115: Document that doSend can be blocking
Task · Resolved (Fixed) · Minor · components: docs · labels: documentation, pull-request-available · created 2021-07-21 · resolved 2024-05-14

https://github.com/apache/kafka/pull/11023


## KAFKA-13359: Round Robin Kafka Producer Routes to only half the partitions when even number of partitions
Bug · Open · Minor · components: producer  · created 2021-10-07

When you have 1 message per batch, in the round robin Partitioner. The messages go only to half the partitions beacuse it always skips 1 partition. This works out for odd number of partitions because skipping 1 will mean all partitions get a hit eventually, but with an even number half the partitions never get selected.
So if you have partitions 1, 2, 3, 4 
Message 1: Partion 1
Message 2: Partion 3
Message 3: Partion 1 ... so on. [ Here 2 and 4 are never selected]
If you have partitions 1,…

- **Luke Chen:** The root cause of this issue should be KAFKA-9965.

## KAFKA-13527: Add top-level error code field to DescribeLogDirsResponse
Bug · Resolved (Fixed) · Major · created 2021-12-09 · resolved 2022-02-01

Ticket for KIP-784: https://cwiki.apache.org/confluence/display/KAFKA/KIP-784%3A+Add+top-level+error+code+field+to+DescribeLogDirsResponse


## KAFKA-13677: version 3.0.0 Processor implementation uses parameter record (restricted identifier)
Improvement · Open · Minor · components: streams · created 2022-02-21

Since 2.7.0 interface:
{quote}org.apache.kafka.streams.processor.Processor<K, V>
{quote}
became depricated.
It was replaced with interface: 
{quote}org.apache.kafka.streams.processor.api.Processor<KIn, VIn, KOut, VOut>
{quote}
which defines method:
{quote}void process(Record<KIn, VIn> record);
{quote}
There is a sonar lint rule _java:S6213:_
_"Restricted Identifiers should not be used as Identifiers"_ for:
 * var
 * yield
 * record <----
Maybe this parameter could be renamed into…


## KAFKA-13805: Upgrade vulnerable dependencies march 2022
Bug · Resolved (Fixed) · Blocker · labels: secutiry · created 2022-04-07 · resolved 2023-01-12

https://nvd.nist.gov/vuln/detail/CVE-2020-36518
|Packages|Package Version|CVSS|Fix Status|
|com.fasterxml.jackson.core_jackson-databind| 2.10.5.1| 7.5|fixed in 2.13.2.1|
|com.fasterxml.jackson.core_jackson-databind|2.13.1|7.5|fixed in 2.13.2.1|
Our security scan detected the above vulnerabilities
upgrade to correct versions for fixing vulnerabilities

- **Bruno Cadonna:** [~shivakumar] Are you referring to the following CVE?
 https://nvd.nist.gov/vuln/detail/CVE-2020-36518
 This CVE seems to affect 2.8.1, 3.0.1 but not 3.1.1 and 3.2.0 since the latter ones use 2.12.6.1 (see  KAFKA-13658).
- **Kirk True:** According to [https://mvnrepository.com/artifact/com.fasterxml.jackson.core/jackson-databind,] 2.13.0 still has the vulnerability. 2.13.2.1 looks to be the first version in the 2.13.x line that has the fix.
- **Bruno Cadonna:** [~kirktrue] Under "Known Affected Software Configurations" the CVE says "Up to (excluding) 2.12.6.1". We are not using the 2.13.x line.
- **Kirk True:** [~cadonna] - Sorry for the confusion... I was mentioning the 2.13.x line because the description stated that the issue was "fixed in 2.13.0", which I don't believe is accurate.
- **Bruno Cadonna:** [~kirktrue] Ah, got it! You are right! I updated the description.
- _…1 more comments_

## KAFKA-13870: support both Suppressed untilTimeLimit and maxBytes without using emitEarlyWhenFull()
New Feature · Open · Major · labels: needs-kip · created 2022-05-04

My use case is to use  ** *untilTimeLimit* with *maxBytes,* but when the buffer is full, the application is breaking, but with using *{{emitEarlyWhenFull}}* {{{}application is not breaking but{}}}{*}{{}}{*} it sends out the same key record multiple times in a particular window when the buffer exceeds max bytes 
for eg:-
*Suppressed.untilTimeLimit(Duration.ofMinutes(15),Suppressed.BufferConfig.maxBytes(10000).emitEarlyWhenFull())*
messages flow : (A,1) (A,2) (A,3) -> aggregation result : (A,6)…

- **Matthias J. Sax:** I think you mix up two concepts: windowing is about "grouping" records according to their timestamp. Thus, the _window-size_ you define via `TimeWindows.withSizeAndGrace()` (or similar) defines into which window a record falls into.
 On the other hand suppression has nothing to do with the definitio…

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

## KAFKA-14319: Storage tool format command does not work with old metadata versions
Bug · Open · Major · created 2022-10-18

When using the format tool with older metadata versions, we see the following error:
[code/log omitted]
For versions prior to `3.3-IV0`, we should skip creation of the `bootstrap.checkpoint` file instead of failing.


## KAFKA-14436: Initialize KRaft with arbitrary epoch
Sub-task · Resolved (Won't Fix) · Major · created 2022-12-02 · resolved 2023-03-24

For the ZK migration, we need to be able to initialize Raft with an arbitrarily high epoch (within the size limit). This is because during the migration, we want to write the Raft epoch as the controller epoch in ZK. We require that epochs in /controller_epoch are monotonic in order for brokers to behave normally.

- **Colin McCabe:** We decided to preserve and continue to use the ZK epoch instead. Closing.

## KAFKA-14740: Missing source tag on MirrorSource metrics
Improvement · Resolved (Fixed) · Major · components: mirrormaker · created 2023-02-22 · resolved 2023-03-21

The metrics defined in MirrorSourceMetrics have the following tags "target", "topic", "partition". It would be good to also have a "source" tag with the source cluster alias.

- **Mickael Maison:** [~ryannedolan] Do you remember if there was a reason not to include the source tag on these metrics? MirrorCheckpointMetrics have the source tag.
- **Ryanne Dolan:** [~mimaison] the topic name usually includes the source cluster already, so I figured it was redundant. With identity replication you don't get that, but you presumably know what the source is in such cases. I don't have any objections to adding it tho.
- **Mickael Maison:** Thanks for the quick reply. I think it would make dealing metrics a little bit easier when you have a bunch of mirroring routes between multiple clusters. I'll draft a small KIP.

## KAFKA-14853: the serializer/deserialize which extends ClusterResourceListener is not added to Metadata
Bug · Resolved (Fixed) · Minor · created 2023-03-27 · resolved 2023-03-29

I noticed this issue when reviewing  KAFKA-14848


## KAFKA-14906: Extract the coordinator service log from server log
Improvement · Patch Available · Major · components: core · created 2023-04-14

Currently, the coordinator service log and server log are mixed together. When troubleshooting the coordinator problem, it is necessary to filter from the server log, which is not very convenient. Therefore, the coordinator log is separated like the controller log.

- **hudeqi:** This change will be reintroduced in version 4.x.
- **hudeqi:** This change will be reintroduced in version 4.x.
- **David Jacot:** Removed the fix version as this work is not planned in 4.0.

## KAFKA-15184: New consumer internals refactoring and clean up
Sub-task · Resolved (Resolved) · Blocker · components: clients, consumer · labels: consumer-threading-refactor, kip-848-e2e, kip-848-preview · created 2023-07-12 · resolved 2023-10-24

Minor refactoring of the new consumer internals including introduction of the {{RequestManagers}} class to hold references to the {{RequestManager}} instances.

- **Kirk True:** See pull request [#14406|https://github.com/apache/kafka/pull/14406].

## KAFKA-15478: Update connect to use ForwardingAdmin
New Feature · Open · Major · labels: need-kip · created 2023-09-19

Connect uses AdminClients to create topics; while this simplifies the implementation of Connect it has the following problems 
 * It assumes that whoever runs Connect must have admin access to both source and destination clusters. This assumption is not necessarily valid all the time.
 * It creates conflict in use-cases where centralised systems or tools manage Kafka resources. 
It would be easier if customers could provide how they want to manage Kafka topics through admin client or using th…


## KAFKA-15589: Flaky  kafka.server.FetchRequestTest
Task · Resolved (Duplicate) · Major · created 2023-10-11 · resolved 2023-10-11

I've been seeing a lot of test failures recently for  kafka.server.FetchRequestTest
Specifically: !image-2023-10-11-13-19-37-012.png!

- **Justine Olshan:** Duplicate of https://issues.apache.org/jira/browse/KAFKA-15566

## KAFKA-15824: SubscriptionState's maybeValidatePositionForCurrentLeader should handle partition which isn't subscribed yet
Bug · Resolved (Fixed) · Major · components: clients · created 2023-11-14 · resolved 2023-11-15

As can be [maybeValidatePositionForCurrentLeader|https://github.com/msn-tldr/kafka/blob/2e2f32c05008cdd7009e5f76fdd92f98996aab84/clients/src/main/java/org/apache/kafka/clients/consumer/internals/SubscriptionState.java#L459] doesn't check if partition is subscribed. It can be done by checking TopicPartitionState cached is null or not, as done by [maybeCompleteValidation|https://github.com/msn-tldr/kafka/blob/2e2f32c05008cdd7009e5f76fdd92f98996aab84/clients/src/main/java/org/apache/kafka/clients/c…


## KAFKA-16340:  Replication factor: 3 larger than available brokers: 1.
Wish · Open · Major · created 2024-03-05

Setting remote.log.metadata.topic.replication.factor is invalid
[code/log omitted]
!image-2024-03-05-09-31-35-058.png!
[code/log omitted]


## KAFKA-16359: kafka-clients-3.7.0.jar published to Maven Central is defective
Bug · Resolved (Fixed) · Critical · components: clients · created 2024-03-11 · resolved 2024-04-04

The {{kafka-clients-3.7.0.jar}} that has been published to Maven Central is defective: it's {{META-INF/MANIFEST.MF}} bogusly include a {{Class-Path}} element:
[code/log omitted]
This bogus {{Class-Path}} element leads to compiler warnings for projects that utilize it as a dependency:
[code/log omitted]
Either the {{kafka-clients-3.7.0.jar}} needs to be respun and published without the bogus {{Class-Path}} element in it's {{META-INF/MANIFEST.MF}} or a new release should be published that corr…

- **Gaurav Narula:** This is likely because of the shadow jar plugin https://github.com/johnrengelman/shadow/tree/9c5182d2d9c5f7141e4d2a525ec94d6111283cd9/src/docs/configuration#configuring-the-jar-manifest
- **Apoorv Mittal:** Hi [~norrisjeremy] , thanks for reporting the issue. As [~gnarula] mentioned this comes as part of shadow plugin, I will look into the issue and should come back with right resolution.
- **Gaurav Narula:** [~apoorvmittal10] I stumbled upon [https://github.com/johnrengelman/shadow/issues/324] and figured it might be useful when you take this up.
- **Matthias J. Sax:** Just to clarify: we cannot re-publish a 3.7.0 artifact. – We can only fix this with 3.7.1 release. Seems we should push out 3.7.1 rather sooner than later.
- **Jeremy Norris:** Yes, if you cannot publish a fixed version of 3.7.0 artifact, then a new 3.7.1 release should be spun.
 The 3.7.0 artifact is simply broken.
- _…5 more comments_

## KAFKA-16844: ByteArrayConverter can't convert ByteBuffer
Improvement · Resolved (Fixed) · Minor · components: connect · created 2024-05-27 · resolved 2024-05-30

In current Schema design, schema type Bytes correspond to two kinds of classes, byte[] and ByteBuffer. But current ByteArrayConverter can only convert byte[]. My suggestion is to add ByteBuffer support in current ByteArrayConverter.

- **Arnav Dadarya:** Can you assign to this, so I can start working on this
- **Fan Yang:** Already sent PR for it.

## KAFKA-17215: Remove get-prefix for all getters
Improvement · Open · Minor · components: streams, streams-test-utils · labels: needs-kip · created 2024-07-29

Kafka traditionally does not use a `get` prefix for getter methods. However, for multiple public interfaces, we don't follow this common pattern, but actually have a get-prefix.
We might want to clean this up. The upcoming 4.0 release might be a good opportunity to deprecate existing methods and add them back with the "correct" name.
We should maybe also do multiple smaller KIPs instead of just one big KIP. We do know of the following
 * StreamsConfig (getMainConsumerConfigs, getRestoreConsum…

- **Ksolves India Limited:** [~mjsax] I would like to work on creating the necessary KIPs and work on this ticket. However, we need Confluence account which we requested earlier as well. Can you help us to provide the same? 
 Comment where I asked for access - https://issues.apache.org/jira/browse/INFRA-25451?focusedCommentId=1…
- **Matthias J. Sax:** I cannot help with creating a Confluence account, however, your account should have been created according to https://issues.apache.org/jira/browse/INFRA-25451?focusedCommentId=17867582&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-17867582 ?
 If your account was no…
- **Ksolves India Limited:** [~mjsax] For now, we didn't get Confluence access. We'll follow up there.
 In the meantime, we'll review the comments on attached PR & the POC one.

## KAFKA-17444: High memory allocation rate for FetchSession.update 
Improvement · Open · Major · components: core · created 2024-08-30

!image-2024-08-30-10-34-33-011.png|width=757,height=241!
when single node 7w fetch qps, 1000+ consumer fetch connection the touch compare logic will consume a lot memory allocate 8%.


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

## KAFKA-18070: Update kafka-metadata-quorum.sh output in docs to match post-KIP-853 appearance
Bug · Resolved (Fixed) · Major · created 2024-11-22 · resolved 2024-12-02

- **Kuan Po Tseng:** I can assist with this. May I take over?

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

## KAFKA-18969: Rewrite ShareConsumerTest#setup by beforeEach and move ShareConsumerTest to clients-integration-tests module 
Improvement · Resolved (Fixed) · Major · created 2025-03-12 · resolved 2025-03-18

Using BeforeEach can ensure the `setup` is executed for each test case. Also, ShareConsumerTest can be moved from core module to clients-integration-tests module.


## KAFKA-19249: Replace Consumer#close(Duration) with Consumer#close(CloseOptions)
Improvement · Resolved (Fixed) · Major · created 2025-05-07 · resolved 2025-11-25

We have introduced Consumer#close(CloseOptions) in KIP-1092.
We should also replace the deprecated method with the new method.

- **Vinod Baba:** [~frankvicky] I am new to the Kafka project and looking to start with a beginner-level task. Can I take this up ? Thanks
- **Chang-Yu Huang:** [~vinodbaba] are you still looking for this issue? I will take it if you don't have time.

## KAFKA-19466: LogConcurrencyTest should close the log when the test completes
Improvement · Resolved (Fixed) · Major · created 2025-07-02 · resolved 2025-07-09

In 
testUncommittedDataNotConsumedFrequentSegmentRolls() and testUncommittedDataNotConsumed(), we call createLog(), but never close the log when the tests complete.

- **Jhen-Yung Hsu:** I’d like to work on this. Thank you :)
- **Chia-Ping Tsai:** [~yung] thanks for taking over it. This test class is also ready to be migrated. Could you please rewrite the test by Java code and then move it to storage module?
- **Jhen-Yung Hsu:** Sure. I’m happy to do that.
- **Jhen-Yung Hsu:** Here is the fix along with the migration: [https://github.com/apache/kafka/pull/20110]. Thank you

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

## KAFKA-19796: Introduce computations for inFlightTerminalRecords
Sub-task · Resolved (Fixed) · Minor · created 2025-10-16 · resolved 2025-10-29


## KAFKA-20001: Remove deprecated broker-side usage of num.partitions and default.replication.factor for topic auto-creation in 5.0.0
Improvement · Open · Major · components: config · created 2025-12-17

KIP-1211 _“Align the behavior of num.partitions and default.replication.factor for topic creation”_ deprecates the usage of {{num.partitions}} and {{default.replication.factor}} in {{broker.properties}} for normal topic auto creation. In the 4.x line, we kept backward compatibility by:
 * Applying the broker-side values only when they are explicitly present in {{broker.properties}} in {{DefaultAutoTopicCreationManager.}}
 * Emitting warnings in {{KafkaConfig}} when these configs are set in the…


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

## KAFKA-20452: Avoid creating unnecessary empty batches in LogCleaner below the High Watermark
Improvement · Resolved (Fixed) · Minor · created 2026-04-14 · resolved 2026-05-08

see https://github.com/apache/kafka/pull/17193#discussion_r1826381383

- **Kartikay Dubey:** Picking this up
- **Chia-Ping Tsai:** [~dubeykartikay] thanks for picking this up. However, we actually have a draft PR in progress for this issue. Would you be interested in reviewing it for us instead?
- **Kartikay Dubey:** Apologize for jumping the gun *😅 .* 
 Yes, ill be happy to review the PR : )

## KAFKA-20500: Transactional support for VersionedStores
Sub-task · Resolved (Fixed) · Major · components: streams · created 2026-04-20 · resolved 2026-06-30

Versioned state stores also need transactionality. Under the hood, they simply use {{{}RocksDBStore{}}}, so make use of the {{{}RocksDBTransctionBuffer{}}}. However, we need to wire up the various pieces of {{{}VersionedStateStore{}}}s to make it work:
 * {{LogicalKeyValueSegment}}
 * {{VersionedBytesStore}}
 * {{VersionedKeyValueStore}}
 * {{Versioned(Metered|Caching|ChangeLogging)Stores}}


## KAFKA-20797: KIP-1365: Transform Observability and Skipped Record Handling for Kafka Connect
Improvement · Open · Major · components: connect, kip · created 2026-07-11

Kafka Connect's Single Message Transform (SMT) framework allows users to build chains of transformations that process records between the connector and Kafka. Transforms can modify records, route them to different topics, or *drop them entirely* by returning {{null}} (a filter operation). When combined with the error tolerance framework ({{{}errors.tolerance=all{}}}), records can also be diverted to a Dead Letter Queue (DLQ) before reaching the connector.
Today, the transform layer has two sign…


## KAFKA-20901: [KRaft] cordoned.log.dirs is accepted but not enforced when log.dirs uses a relative path
Bug · Open · Major · components: core · created 2026-08-06

h2. Description
When {{log.dirs}} is configured with a relative path, setting {{cordoned.log.dirs}} has inconsistent behavior:
 # Setting {{cordoned.log.dirs}} to the absolute path returned by {{DescribeLogDirs}} is rejected because it does not exactly match the relative value in {{{}log.dirs{}}}.
 # Setting {{cordoned.log.dirs}} to the relative path succeeds and the dynamic configuration is persisted.
 # However, the directory is not actually treated as cordoned, and replicas for newly crea…

- **majialong:** Thanks for reporting this. I reproduced the issue locally on the current trunk. I’d like to work on it, so I’ll assign it to myself and investigate a fix.
- **majialong:** Hi [~mimaison] , I’ve opened PR  [https://github.com/apache/kafka/pull/23241] to address this issue. Could you please review it when you have a chance? Thanks!
