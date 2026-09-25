## KAFKA-12164: ssue when kafka connect worker pod restart, during creation of nested partition directories in hdfs file system.
Bug · Resolved (Invalid) · Critical · components: connect · created 2021-01-08 · resolved 2024-06-17

In our production labs, an issue is observed. Below is the sequence of the same.
 # hdfs connector is added to the connect worker.
 # hdfs connector is creating folders in hdfs /test1=1/test2=2/
Based on the custom partitioner. Here test1 and test2 are two separate nested directories derived from multiple fields in the record using a custom partitioner.
 # Now kafka connect hdfs connector uses below function calls to create the directories in the hdfs file system.
fs.mkdirs(new Path(filenam…

- **kaushik srinivas:** [~ijuma]
 Need your inputs.
- **kaushik srinivas:** [~ijuma]
 This is an issue with lot of impacts. Can you provide some suggestions.
- **Ismael Juma:** cc [~kkonstantine] [~rhauch]
- **Konstantine Karantasis:** Thanks for reporting [~kaushik srinivas] 
 First, I need to note that this issue seems to belong in its entirety to:
 [https://github.com/confluentinc/kafka-connect-hdfs/issues] 
 given that the behavior is not affected by the guarantees that the Kafka Connect framework provides. 
 Briefly, let me s…
- **kaushik srinivas:** Hi [~kkonstantine]
 We have created the ticket even on the hdfs sink connector side as well.
 Below is the ticket 
 [https://github.com/confluentinc/kafka-connect-hdfs/issues/538]
 We have also captured more detailed analysis over there. But there are no responses in that forum as well.
 -Kaushik
- _…4 more comments_

## KAFKA-12562: Remove deprecated-overloaded "KafkaStreams#metadataForKey" and "KafkaStreams#store"
Sub-task · Resolved (Fixed) · Minor · components: streams · created 2021-03-26 · resolved 2021-03-28


## KAFKA-12760: Delete My Account
Wish · Resolved (Invalid) · Minor · created 2021-05-07 · resolved 2021-05-11

I wish to have my account deleted. There doesnt seem to be a way to do it from within my own account, but it should be possible for an admin to do it.
Many thanks.

- **Matthias J. Sax:** [~byusti] – we cannot delete your account either.
 You could try to file a ticket against [https://issues.apache.org/jira/projects/INFRA] – maybe they are able to help with this request.

## KAFKA-13186: Proposal for commented code
Wish · Open · Trivial · created 2021-08-10

Hello! I saw in your [coding guidelines|https://kafka.apache.org/coding-guide.html] that ??Don't check in commented out code. ??
However, I still witness commented code in some files like:
* connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ConnectorConfigTest.java
* streams/src/test/java/org/apache/kafka/streams/state/internals/TimeOrderedKeyValueBufferTest.java
* clients/src/main/java/org/apache/kafka/clients/consumer/internals/AbstractStickyAssignor.java
Would you like to re…


## KAFKA-13271: Error while fetching metadata with correlation id 219783 : LEADER_NOT_AVAILABLE
Bug · Open · Major · components: producer  · created 2021-09-03

Hi dear kafka support
We are getting below error after a new connector creation
[2021-09-02 19:15:23,878] WARN [Producer clientId=producer-178] Error while fetching metadata with correlation id 219783 : \{ tkr_prd2.tkr.glrep_file2=LEADER_NOT_AVAILABLE} (org.apache.kafka.clients.NetworkClient)
[2021-09-02 19:15:23,982] WARN [Producer clientId=producer-178] Error while fetching metadata with correlation id 219784 : \{ tkr_prd2.tkr.glrep_file2=LEADER_NOT_AVAILABLE} (org.apache.kafka.clients.Netw…


## KAFKA-13466: delete unused config batch.size in kafka-console-producer.sh
Bug · Resolved (Fixed) · Minor · components: core · created 2021-11-19 · resolved 2022-03-05

official docs:
!image-2021-11-19-04-05-15-754.png!
shell scripts is:
!image-2021-11-19-04-09-28-299.png!
in fact, the batch-size config is already not used everywhere in the code anymore, so delete this and may not have a misunderstanding in the future


## KAFKA-13470: Test the handling of secure controller ports
Improvement · Open · Major · created 2021-11-22

It should be possible to configure the controller to use secure ports. We need a junit integration test for this

- **Colin McCabe:** We do not include the controller listener in the 'listeners' configuration. I will remove that part of this from the Description.

## KAFKA-13471: Test rolling change of KRaft controller endpoints
Improvement · Open · Major · components: controller, kraft · labels: test · created 2021-11-22

We should have a test of making a rolling change to KRaft controller endpoints. For example, going from PLAINTEXT or SSL. (This would involve going through an intermediate stage where the controllers exposed both endpoints.)


## KAFKA-13676: When processing in ALOS, when one task encounters a task-specific exception we could still commit progress made by other tasks
Improvement · Resolved (Fixed) · Major · components: streams · created 2022-02-18 · resolved 2022-02-23

When processing in ALOS, we might as well commit progress made by other tasks when some task encounters specific exception. If one task has an issue and we have already successfully completed processing on at least one task it would be good to commit those successfully processed tasks. This should prevent limit the duplicated records downstream and also be more efficient.
Also if one task is having lots of issues the other tasks can at least make progress. When we introduced the thread replacem…


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


## KAFKA-13722: Update internal interfaces that use ProcessorContext to use StateStoreContext instead
Improvement · Reopened · Major · components: streams · created 2022-03-09

This is a remainder that when we remove the deprecated public APIs that uses the ProcessorContext, like `StateStore.init`, we should also consider updating the internal interfaces with the ProcessorContext as well. That includes:
1. Segments and related util classes which use ProcessorContext.
2. For state stores that leverage on ProcessorContext.getXXXTime, their logic should be moved out of the state store impl but to the processor node level that calls on these state stores.

- **Matthias J. Sax:** We needed to revet one PR for 4.1 release, as it introduces a regression bug: [https://github.com/apache/kafka/pull/18292]
 Re-opening to make sure we complete this issue with 4.2 release – as we did only revert in 4.1 branch, but not in trunk, also filed https://issues.apache.org/jira/browse/KAFKA-…

## KAFKA-13763: Improve unit testing coverage and flexibility for IncrementalCooperativeAssignor
Improvement · Resolved (Done) · Minor · components: connect · created 2022-03-23 · resolved 2022-05-12

The [tests|https://github.com/apache/kafka/blob/dcd09de1ed84b43f269eb32fc2baf589a791d468/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/distributed/IncrementalCooperativeAssignorTest.java] for the {{IncrementalCooperativeAssignor}} class provide a moderate level of coverage and cover some non-trivial cases, but there are some areas for improvement that will allow us to iterate on the assignment logic for Kafka Connect faster and with greater confidence.
These improvements includ…

- **Chris Egerton:** Discussed earlier during review of https://github.com/apache/kafka/pull/10367

## KAFKA-13803: Refactor Leader API Access
Improvement · Resolved (Fixed) · Major · created 2022-04-06 · resolved 2022-06-03

Currently, AbstractFetcherThread has a series of protected APIs which control access to the Leader. ReplicaFetcherThread and ReplicaAlterLogDirsThread respectively override these protected APIs and handle access to the Leader in a remote broker leader and a local leader context.
We propose to move these protected APIs to a LeaderEndPoint interface, which will serve all fetches from the Leader. We will implement a RemoteLeaderEndPoint and a LocalLeaderEndPoint accordingly. This change will great…

- **Jun Rao:** merged the PR to trunk

## KAFKA-13935: Factor out static IBP usages from broker
Sub-task · Resolved (Fixed) · Major · created 2022-05-24 · resolved 2022-08-22

We pass the IBP down to the log layer for checking things like compression support. Currently, we are still reading this from KafkaConfig. In ZK mode this is fine, but in KRaft mode, reading the IBP from the config is not supported.
Since KRaft only supports IBP/MetadataVersion greater than 3.0 (which supports the compression mode we check for), we may be able to avoid using a dynamic call and/or volatile to get the current version.


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

## KAFKA-14018: Kafka SSL can't support p12 certificate using sha256 on jdk8
Improvement · Open · Minor · components: clients · created 2022-06-24

Our partner changed the encryption algorithm of the p12  certificate from SHA1 to SHA256 for some reason. As a result, Kafka reported a connection error due to the wrong password.But we found the root cause is that the keytool of JDK8 does not support this encryption format.
I would like to open a PR to contribute some code to support this case


## KAFKA-14019: removeMembersFromConsumerGroup can't delete all members when there is no members already
Bug · Open · Minor · created 2022-06-24

The root cause is that the method fetch no member from server, so it fails to construct RemoveMembersFromConsumerGroupOptions (it can't accept empty list)
It seems to me deleting all members from a "empty" list is valid.

- **Kvicii.Yu:** [~chia7712]  hi, your meaning we need change this RemoveMembersFromConsumerGroupOptions#removeAll method? If we do this, what correct things we can do?

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

## KAFKA-14549: Move LogDirFailureChannel to storage module
Sub-task · Resolved (Fixed) · Major · created 2022-12-22 · resolved 2022-12-23


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

## KAFKA-14741: Add description field to connector configs
Improvement · Resolved (Won't Do) · Major · components: connect · created 2023-02-22 · resolved 2023-04-05

Connectors are identified by their name. In many cases it would be useful to attach a description/comment to connectors to provide some context. This would be especially useful on Connect clusters running several connectors and/or shared by multiple teams.


## KAFKA-14851: Move StreamResetterTest to tools
Sub-task · Resolved (Fixed) · Minor · created 2023-03-27 · resolved 2023-07-21

This came up as a suggestion here: https://github.com/apache/kafka/pull/13127#discussion_r1105688687


## KAFKA-14854: Refactor inter broker send thread to handle all interbroker requests on one thread
Sub-task · In Progress · Major · created 2023-03-27

Currently we create a new thread for each interbroker request that implements InterbrokerSendThread. It would be better to implement a single thread that multiple request types can use with their custom logic. 
I propose creating a single thread that takes a collection of "managers" for each request and sends the requests generated.


## KAFKA-14899: Revisit Action Queue
Sub-task · Open · Major · created 2023-04-12

With Kafka-14561 we introduced a notion for callback requests. It would be nice to standardize and combine action queue usage here. However, the current implementation of the callback request assumes local time is computed upon response send. 
This same paradigm may not be the case with the action queue. We should follow up and see what changes need to be made to combine the two.


## KAFKA-14907: Add the traffic metric of the partition dimension in BrokerTopicStats
Improvement · Patch Available · Major · components: core · labels: KIP-922 · created 2023-04-14

{color:#172b4d}Currently, there are two metrics for measuring the traffic in topic dimensions: MessagesInPerSec, BytesInPerSec, but there are two problems:{color}
{color:#172b4d}1. It is difficult to intuitively reflect the problem of topic partition traffic inclination through these indicators, and it is impossible to clearly see which partition has the largest traffic and the traffic situation of each partition. But the partition dimension can solve this.{color}
{color:#172b4d}2. For the sud…


## KAFKA-14978: ExactlyOnceWorkerSourceTask does not remove parent metrics
Bug · Resolved (Fixed) · Major · components: connect · created 2023-05-09 · resolved 2023-05-11

ExactlyOnceWorkerSourceTask removeMetrics does not invoke super.removeMetrics, meaning that only the transactional metrics are removed, and common source task metrics are not.


## KAFKA-14987: Implement Group/Offset expiration
Sub-task · Resolved (Fixed) · Major · created 2023-05-11 · resolved 2023-10-12


## KAFKA-15179: Add integration tests for the FileStream Sink and Source connectors
Test · Resolved (Done) · Minor · created 2023-07-11 · resolved 2023-09-07

Add integration tests for the FileStream Sink and Source connectors covering various different common scenarios.


## KAFKA-15598: Add integration tests for DescribeGroups API, DeleteGroups API and OffsetDelete API
Sub-task · Resolved (Fixed) · Major · created 2023-10-12 · resolved 2023-11-02


## KAFKA-15828: Protect clients from broker hostname reuse
Bug · Resolved (Fixed) · Major · components: clients, consumer, producer  · labels: needs-kip · created 2023-11-14 · resolved 2026-07-06

In some environments such as k8s, brokers may be assigned to nodes dynamically from an available pool. When a cluster is rolling, it is possible for the client to see the same node advertised for different broker IDs in a short period of time. For example, kafka-1 might be initially assigned to node1. Before the client is able to establish a connection, it could be that kafka-3 is now on node1 instead. Currently there is no protection in the client or in the protocol for this scenario. If the co…


## KAFKA-15829: How to build Kafka 2.7 with maven instead of gradle?
Wish · Open · Minor · created 2023-11-15

It's difficult to upgrade the version of gradle in kafka building. Is there a solution to build kafka 2.7 with maven?


## KAFKA-15830: Add request/response handling in KafkaApis and update metrics plugin
Sub-task · Resolved (Fixed) · Major · created 2023-11-15 · resolved 2023-12-05

- **Jun Rao:** Merged the PR to trunk.

## KAFKA-16016: Migrate utility scripts to kafka codebase
Sub-task · Resolved (Fixed) · Blocker · components: core · created 2023-12-15 · resolved 2024-01-08

Migrate the logic implemented in golang to kafka codebase by creating a new entrypoint for docker images

- **Stanislav Kozlovski:** We are discussing in the mailing list thread for [DISCUSS] KIP-975 Docker Image for Apache Kafka about whether this should be considered a blocker for 3.7. I am leaning toward no
- **Stanislav Kozlovski:** Changing the Fix Version here to unblock RC creation for 3.7

## KAFKA-16020: Time#waitForFuture should tolerate nanosecond overflow
Bug · Open · Major · created 2023-12-15

Reported by [~jsancio] here https://github.com/apache/kafka/pull/15007#discussion_r1428359211
Time#waitForFuture should follow the JDK recommendation for comparing elapsed nanoseconds to a duration.
https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/System.html#nanoTime()
{quote}
For example, to measure how long some code takes to execute:
 long startTime = System.nanoTime();
 // ... the code being measured ...
 long elapsedNanos = System.nanoTime() - startTime;
To co…


## KAFKA-16021: Eagerly load Charset for StringSerializer/StringDeserializer
Improvement · Resolved (Fixed) · Minor · components: clients · created 2023-12-15 · resolved 2023-12-24

StringSerializer and StringDeserializer currently use the String constructor and getBytes methods that take the encoding as a String, necessitating a Charset lookup every time those methods are called.
We could save that lookup by performing it once during the serializer configure call instead.


## KAFKA-16109: Write system tests cover the "simple consumer + commit" use case
Test · Open · Minor · components: clients, consumer, system tests · labels: consumer-threading-refactor, system-tests · created 2024-01-10

- **PoAn Yang:** Hi [~kirktrue], if you're not working on this, may I take it? Thank you.
- **Kirk True:** [~yangpoan]—it's all yours :)
- **Lianet Magrans:** [~kirktrue] do you think this should be Major for 4.0 given that we do have coverage for this path at the integration test level, ex. PlaintextConsumerCommitTest#testCommitMetadata)?
- **Kirk True:** I think we can push it to post-4.0 and/or lower the priority. Thanks!

## KAFKA-16110: Document and publicize performance test results for AsyncKafkaConsumer
Task · Open · Major · components: clients, consumer · labels: consumer-threading-refactor, performance-benchmark · created 2024-01-10

- **Philip Nee:** Hi [~kirktrue] - Thanks for filing this JIRA.  There are two paths forward for the performance testing.  One is using trogdor - which does more than performance testing but also allow us to test different fault scenarios.  Second is implementing our own benchmarking test, I started working on it som…
- **Philip Nee:** My proposal here is
 - Let's run trogdor to see what can we get out of it. If the current settings is not satisfied then we can add more "specs" to the repo and see if we can get to the point we want.
 - We also might want to monitor the performance of the head of trunk as we are putting code in.  I…
- **Kirk True:** Yes, we can use Trogdor for some _basic_ performance numbers. Nothing too granular or detailed.
- **Colin McCabe:** Changing target fix version to 4.0 since this is not a blocker and we are past code freeze

## KAFKA-16111: Implement tests for tricky rebalance callback scenarios
Test · Open · Minor · components: clients, consumer · labels: callback, consumer-threading-refactor, integration-tests · created 2024-01-10

There is justified concern that the new threading model may not play well with "tricky" {{ConsumerRebalanceListener}} callbacks. We need to provide some assurance that it will support complicated patterns.
 # Design and implement test scenarios
 # Update and document any design changes with the callback sub-system where needed
 # Provide fix(es) to the {{AsyncKafkaConsumer}} implementation to abide by said design

- **Lucas Brutschy:** https://github.com/apache/kafka/pull/15408 Example test
- **Colin McCabe:** Changing target fix version to 4.0 since this is not a blocker and we are past code freeze
- **Lianet Magrans:** I downgraded the priority here given that multiple test have been added to the PlaintextConsumerCallbackTest, so even though we could add more, I don't think is task should be Major for 4.0.

## KAFKA-16181: Use incrementalAlterConfigs when updating broker configs by kafka-configs.sh
Improvement · Resolved (Resolved) · Major · created 2024-01-22 · resolved 2024-12-02


## KAFKA-16340:  Replication factor: 3 larger than available brokers: 1.
Wish · Open · Major · created 2024-03-05

Setting remote.log.metadata.topic.replication.factor is invalid
[code/log omitted]
!image-2024-03-05-09-31-35-058.png!
[code/log omitted]


## KAFKA-16341: Fix un-compressed records
Sub-task · Resolved (Fixed) · Major · created 2024-03-05 · resolved 2024-03-23

- **Chia-Ping Tsai:** pending for backporting to 3.6
- **Johnny Hsu:** on it now, thanks for the reminder

## KAFKA-16342: Fix compressed records
Sub-task · Resolved (Fixed) · Major · created 2024-03-05 · resolved 2024-03-16


## KAFKA-16343: Improve tests of streams foreignkeyjoin package
Improvement · Resolved (Fixed) · Major · components: streams, unit tests · created 2024-03-05 · resolved 2024-06-09

Some classes are not tested in streams foreignkeyjoin package, such as SubscriptionSendProcessorSupplier and ForeignTableJoinProcessorSupplier. Corresponding tests should be added.
The class ForeignTableJoinProcessorSupplierTest should be renamed as it is not testing ForeignTableJoinProcessor, but rather SubscriptionJoinProcessorSupplier.


## KAFKA-16367: Full ConsumerGroupHeartbeat response must be sent when full request is received
Sub-task · Resolved (Fixed) · Major · created 2024-03-12 · resolved 2024-03-19


## KAFKA-16517: Do not decode metadata records in the internal kraft partition listener
Sub-task · Resolved (Fixed) · Major · components: kraft · created 2024-04-11 · resolved 2026-08-12

The implementation for the internal partition listener for kraft reads and decodes the data record. This is not required and it is only done because it is easier to implement with the current code.


## KAFKA-16519: Expose the supported and finalized kraft.version in ApiVersions response
Sub-task · Resolved (Duplicate) · Major · components: core · created 2024-04-11 · resolved 2024-07-22

- **Josep Prat:** Changing target fix version to 3.9 since this is not a blocker and we are past code freeze
- **José Armando García Sancio:** This was resolved as part of another issue and pr.
- **Colin McCabe:** Removing fix version 3.9 for this duplicate JIRA since it is confusing release.py

## KAFKA-16677: Replace ClusterType#ALL and ClusterType#DEFAULT by Array
Improvement · Resolved (Fixed) · Minor · created 2024-05-07 · resolved 2024-05-13

Both ClusterType#ALL and ClusterType#DEFAULT are a kind of "tag" instead of true "type". It seems to me they can be removed by using Array. For example:
ClusterType#ALL -> {Type.ZK, Type.KRAFT, Type.CO_KRAFT}
ClusterType#DEFAULT -> {}
There are two benefits
1. That is more readable for "ALL type". 
2. We don't throw the awkward "exception" when seeing "DEFAULT".

- **Chia-Ping Tsai:** For another, we can simplify the code (https://github.com/apache/kafka/blob/trunk/tools/src/test/java/org/apache/kafka/tools/consumer/group/ConsumerGroupCommandTestUtils.java#L77)
 [code/log omitted]
- **PoAn Yang:** Hi [~chia7712], I think the feature is good. Most of time, we use same config to run KRAFT and CO_KRAFT. If we can use `setTypes`, we don't need to create another builder.
- **PoAn Yang:** Hi [~chia7712], I'm interested in this feature. If you're not working on it, may I assign to myself? Thank you.

## KAFKA-16678: Remove unimplementedquorum from EndToEndAuthorizationTest
Test · Resolved (Fixed) · Minor · created 2024-05-07 · resolved 2024-05-08

`unimplementedquorum`[0] is used to skip test cases if they don't support to run by kraft. However, KAFKA-15219 , KAFKA-14765 and KAFKA-14776 make related tests support to run by kraft.
In short, it is time to remove the unused variable :)
[0] [https://github.com/apache/kafka/blob/d76352e2151178521dc447e3406dabb8fcd4c57c/core/src/test/scala/integration/kafka/api/EndToEndAuthorizationTest.scala#L146]

- **TengYao Chi:** I am able to handle this issue.

## KAFKA-16679: Merge unit test down to the class of integration test
Test · Resolved (Fixed) · Minor · created 2024-05-07 · resolved 2024-05-11

Normally, we don't put multi test classes into single file. Those test classes can be extracted into a new class file. Or we can merge them into single class by using "@Test" annotation. That can make those test cases run without embedded cluster.

- **Cheng-Kai, Zhang:** Hi [~chia7712] , could I work on this one? :D

## KAFKA-16680: Make ClusterTestExtensions support SASL
New Feature · Resolved (Fixed) · Major · created 2024-05-07 · resolved 2026-07-19

This is a umbrella issue.
In order to migrate more tests to new test infra, we ought to make it support SASL at least.
*phase1: reuse/rewrite existent SASL utils by Java*
 # MiniKdc
 # JaasTestUtils
 # Move security-related helpers from scala.TestUtils
 # extract/rewrite non-zk code from SaslSetup to new java class
*phase2: make `ClusterTest#securityProtocol` works. It does not work for kraft mode :(*
 # add client-related helper to generate consumer/producer/admin class with security co…


## KAFKA-16681: Rewrite MiniKDC by Java
Sub-task · Resolved (Fixed) · Major · created 2024-05-07 · resolved 2024-09-13

Noted:
 # we need to move it from scala folder to java folder
 # don't change the package name since system tests requires it

- **PoAn Yang:** Hi [~chia7712], I'm interested in this. If you are not working on it, may I assign to myself? Thank you.

## KAFKA-16682: Rewrite JassTestUtils by Java
Sub-task · Resolved (Fixed) · Minor · created 2024-05-07 · resolved 2024-08-13

as title
one more thing is that we should change the package name from kafka.utils to kafka.security

- **TengYao Chi:** I am able to handle this issue.

## KAFKA-16683: Extract security-related helpers from scala.TestUtils to java class
Sub-task · Resolved (Fixed) · Minor · created 2024-05-07 · resolved 2024-09-26

We can merge them into `JaasTestUtils and then rename `JaasTestUtils` to `SecurityTestUtils.

- **PoAn Yang:** Hi [~chia7712], I'm interested in this. May I take it? Thank you.
- **PoAn Yang:** PR: [https://github.com/apache/kafka/pull/16912]

## KAFKA-16839: Replace KafkaRaftClient's voterNode with leadeNode
Sub-task · Open · Major · created 2024-05-24

The id passed to KafkaRaftClient.voterNode is always the leader id.


## KAFKA-16840: Add a --timeout option to ConfigCommand
Improvement · Open · Minor · components: admin · created 2024-05-25


## KAFKA-16843: Remove preAppendErrors from createPutCacheCallback
Improvement · Resolved (Fixed) · Minor · created 2024-05-26 · resolved 2024-06-05

origin discussion: [https://github.com/apache/kafka/pull/16072#pullrequestreview-2077368462]
The method `createPutCacheCallback` has a input argument `preAppendErrors` [0]. It is used to keep the "error" happens before appending. However, the pre-append error is handled before by calling `responseCallback` [1]. Hence, we can remove `preAppendErrors`.
[0] https://github.com/apache/kafka/blob/trunk/core/src/main/scala/kafka/coordinator/group/GroupMetadataManager.scala#L387
[1] https://github.co…

- **PoAn Yang:** Hi [~chia7712], thanks for filing the ticket. If you're not working on this, I would like to help to remove unused parameter. Thanks.
- **PoAn Yang:** The PR [https://github.com/apache/kafka/pull/16105] is merged. Resolved the issue.

## KAFKA-16845: Migrate ReplicationQuotasTestRig to new test infra
Sub-task · Resolved (Fixed) · Minor · created 2024-05-27 · resolved 2024-10-24

as title

- **Ken Huang:** I'm interesting in this ticket
- **Dmitry Werner:** [~m1a2st] Hello, are you working on this task?
 I can grab issue if you have no time.
- **Ken Huang:** [~javakillah], sure you can take it.

## KAFKA-16847: Revise the README for recent CI changes 
Improvement · Resolved (Invalid) · Minor · created 2024-05-28 · resolved 2024-05-29

The recent changes [0] removes the test of 11 and 17, and that is good to our CI resources. However, in the root readme we still declaim "We build and test Apache Kafka with Java 8, 11, 17 and 21" 
[0] https://github.com/apache/kafka/commit/adab48df6830259d33bd9705b91885c4f384f267
[1] https://github.com/apache/kafka/blob/trunk/README.md?plain=1#L7

- **Cheng-Kai, Zhang:** hi [~chia7712]  may I take this easy fix? :)
- **Chia-Ping Tsai:** sure, btw please follow the mail https://lists.apache.org/thread/jvz1g2mkjrnqskk52n28sxhwdjo74m34 for possible changes about CI
- **Greg Harris:** Hey FYI the trunk builds still run the full suite, so this isn't inaccurate right now. If the 11 and 17 builds are disabled completely then it will be accurate.
- **Justine Olshan:** +1 to what [~gharris1727] said, I was just coming here to say the same.
- **Chia-Ping Tsai:** {quote}
 the trunk builds still run the full suite
 {quote}
 The README says that we run both "build" and "test" for 11 and 17, but we don't run "test" for 11 and 17, right?
- _…2 more comments_

## KAFKA-17045: Move MetadataLogConfig from kafka to kafka.raft
Improvement · Resolved (Duplicate) · Minor · created 2024-06-27 · resolved 2025-03-20

The MetadataLogConfig belongs to raft, move file to raft to mach the package name.

- **Ksolves India Limited:** The file named MetadataLogConfig is written in Scala which is in location kafka/core/src/main/scala/kafka/MetadataLogConfig.scala 
 and the separate raft package contains the files written in Java.
 If you are referring this, then we have to create MetadataLogConfig or create a scala package into ra…
- **Lin Siyuan:** If your intention is just to "kafka\core\src\main\scala\kafka\raft", I enclose the PR "https://github.com/apache/kafka/pull/16484/"
- **PoAn Yang:** This will be covered by https://issues.apache.org/jira/browse/KAFKA-15599 with PR https://github.com/apache/kafka/pull/19246.

## KAFKA-17106: Enable KafkaConsumerTest#testFetchProgressWithMissingPartitionPosition for AsyncConsumer
Sub-task · Resolved (Fixed) · Minor · components: clients, consumer, unit tests · created 2024-07-10 · resolved 2024-07-14

That test can be fixed by this approach (https://github.com/apache/kafka/pull/16541#discussion_r1671273572)


## KAFKA-17110: Enable valid test case in KafkaConsumerTest for AsyncKafkaConsumer
Sub-task · Resolved (Fixed) · Minor · created 2024-07-10 · resolved 2024-07-14

Enable testResetUsingAutoResetPolicy, verifyPollTimesOutDuringMetadataUpdate, testPollThrowsInterruptExceptionIfInterrupted, fetchResponseWithUnexpectedPartitionIsIgnored, testManualAssignmentChangeWithAutoCommitEnabled, testManualAssignmentChangeWithAutoCommitDisabled, testOffsetOfPausedPartitions, and testCloseShouldBeIdempotent for AsyncKafkaConsumer

- **Lianet Magrans:** Hey [~yangpoan] , thanks for taking on this one! Heads-up in case it helps, we've dealt with some KafkaConsumerTests that cannot be applied to the AsyncConsumer just because of the way the are written. In those cases, it's fair to leave them running for the CLASSIC only, and write a separate test on…
- **PoAn Yang:** Hi [~lianetm], thanks for the comment. I will check again all test cases which are only marked with `CLASSIC`. If the case needs to rewrite in AsyncKafkaConsumerTest, I will add new tests to AsyncKafkaConsumerTest and move CLASSIC only test cases to LegacyKafkaConsumerTest. I think this is goal of K…

## KAFKA-17213: Change exceptions like ControllerMovedException to be retriable
Improvement · Open · Minor · components: clients · created 2024-07-29

After the Kafka client fails to send, it will update the metadata. The {{InvalidMetadataException}} is retryable. I think the Controller information also belongs to Kafka's metadata, so {{ControllerMovedException}} should be {{{}InvalidMetadataException{}}}.


## KAFKA-17214: Add 3.8.0 Streams and Core to system tests
Bug · Closed (Fixed) · Major · components: clients, consumer, core, producer , streams, system tests · created 2024-07-29 · resolved 2024-07-30

As per Release Instructions we should add 3.8.0 version to system tests. Example PRs:
 * Broker and clients: [https://github.com/apache/kafka/pull/12210]
 * Streams: [https://github.com/apache/kafka/pull/12209]

- **Matthias J. Sax:** As we already have a 3.9 branch, PR for this ticket should also be cherry-picked to 3.9 branch.
- **Josep Prat:** Note 2 PRs will be created, one for Core and Client and another one for Streams
- **Josep Prat:** Merged the 2 PRs to trunk and 3.9
- **Matthias J. Sax:** Thanks a ton [~jlprat]!

## KAFKA-17217: Clients : Optimise batching of requests per node in ShareConsumeRequestManager
Sub-task · Resolved (Fixed) · Major · created 2024-07-30 · resolved 2024-08-09

In ShareConsumeRequestManager, currently every time we perform a commitSync or commitAsync, we create one ShareAcknowledge RPC for the same. Here, we can optimise the number of RPC calls by batching the acknowledgements before the next poll is invoked per node. 
This will ensure that between 2 calls, the acknowledgements are accumulated in one request per node and then sent during poll, resulting in lesser RPC calls.


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


## KAFKA-17585: `offsetResetStrategyTimestamp` should return `long` instead of `Long`
Improvement · Resolved (Fixed) · Trivial · created 2024-09-20 · resolved 2024-09-24

the null behavior was removed by [https://github.com/apache/kafka/commit/2b233bfa5f35bf237effe8c5202fd2b80c601943,] so we can return long and then remove the null check to simplify the code.

- **kangning.li:** [~chia7712]  I am interested in this issue.Cloud you assign it to me?

## KAFKA-17988: Fix flaky ReconfigurableQuorumIntegrationTest.testRemoveAndAddSameController
Bug · Resolved (Fixed) · Major · created 2024-11-12 · resolved 2024-11-24

https://ge.apache.org/scans/tests?search.rootProjectNames=kafka&search.timeZoneId=Asia%2FTaipei&tests.container=kafka.server.ReconfigurableQuorumIntegrationTest&tests.test=testRemoveAndAddSameController()

- **Kevin Wu:** Submitted a PR that fixes this.

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

## KAFKA-18068: Fixing typo in ProducerConfig
Bug · Resolved (Fixed) · Minor · labels: kip · created 2024-11-22 · resolved 2025-08-07

Fix typos:
{{PARTITIONER_ADPATIVE_PARTITIONING_ENABLE_CONFIG}}
{{PARTITIONER_ADPATIVE_PARTITIONING_ENABLE_DOC}}
Also end of line whitespaces needs removing in descriptions.

- **João Pedro Fonseca:** I have labeled it as need-kip based on [~chia7712]'s comment in PR. :)
- **Chia-Ping Tsai:** [~mingyen066] it would be useful if we can check other typo in this KIP.
- **Ming-Yen Chung:** [~chia7712] I’ve checked the other config variables and didn’t find any with typos.

## KAFKA-18273: Implement kafka-share-groups.sh --describe --verbose
Sub-task · Resolved (Fixed) · Major · created 2024-12-16 · resolved 2025-01-02

This is the share groups part of KIP-1099.


## KAFKA-18390: Use LinkedHashMap instead of Map in creating MetricName and SensorBuilder
Improvement · Open · Major · created 2025-01-02

see https://github.com/apache/kafka/pull/18232#discussion_r1900425014

- **Mickael Maison:** Moving to the next release as we're now in code freeze for 4.1.0.
- **Christo Lolov:** Moving to 4.3 since we are past the code freeze for 4.2! Let me know if I have misunderstood something!
- **Mickael Maison:** Moving to the next release as we're now in code freeze for 4.3.0.
- **Omnia Ibrahim:** Moving to 4.5 as we are now in 4.4.0 code freeze
- **Omnia Ibrahim:** I can see one PR merged and 2 closed so if this still no done I will move it to 4.5 feel free to change it back to 4.4 if you believe it is done and merged

## KAFKA-18392: Require client-generated member IDs for ShareGroupHeartbeat
Sub-task · Resolved (Fixed) · Major · created 2025-01-02 · resolved 2025-01-22

This implements KIP-1082 for share groups.


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

## KAFKA-19130: Do not add fenced brokers to BrokerRegistrationTracker on startup
Bug · Resolved (Fixed) · Minor · created 2025-04-11 · resolved 2025-07-01

When the controller starts up (or becomes active after being inactive), we add all of the
registered brokers to BrokerRegistrationTracker so that they will not be accidentally fenced the
next time we are looking for a broker to fence. We do this because the state in
BrokerRegistrationTracker is "soft state" (it doesn't appear in the metadata log), and the newly
active controller starts off with no soft state. (Its soft state will be populated by the brokers
sending heartbeat requests to it…

- **Mickael Maison:** The PR has been merged, marking as resolved.

## KAFKA-19137: Use `StandardCharsets.UTF_8` instead of `StandardCharsets.UTF_8.name()`
Improvement · Resolved (Fixed) · Minor · created 2025-04-14 · resolved 2025-04-15

The checked exception {{UnsupportedEncodingException}} for {{StandardCharsets.UTF_8.name()}} can be avoided by using {{StandardCharsets.UTF_8}} directly.

- **kangning.li:** [~chia7712]    If you have not started on this issue, cloud you assign it to me ?

## KAFKA-19250: abortTransactions should not return abortable exception
Sub-task · Resolved (Fixed) · Major · created 2025-05-07 · resolved 2025-06-04


## KAFKA-19252: Support broker and controller restarts in testkit
Improvement · Open · Major · components: unit tests · created 2025-05-07

We should support broker and controller restarts in ClusterTest (and testkit). Since these components are not designed to be reused, we will need to create them on-demand when a node is restarted.
Not having this feature makes it difficult for many tests to be converted from IntegrationTestHarness. Some tests have done so, but by reaching down into the broker implementation classes like [https://github.com/apache/kafka/commit/c527530e806c7d9f79348656d801b1b78e8f2bec#diff-9003994ba58aae31e74ea55…

- **PoAn Yang:** It looks like we have a similar ticket https://issues.apache.org/jira/browse/KAFKA-17259. I will keep working on it. Thanks.

## KAFKA-19253: Improve metadata handling for share version using feature listeners
Sub-task · Resolved (Fixed) · Major · created 2025-05-07 · resolved 2025-05-15

Reference comment - [https://github.com/apache/kafka/pull/19542/files#r2064029087]


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

## KAFKA-19270: Remove optional from ClusterInstance#controllerListenerName
Improvement · Resolved (Fixed) · Minor · created 2025-05-12 · resolved 2025-05-15

in kraft mode, the listener name should be always exist.


## KAFKA-19271: Private interface for injecting test wrappers for KIP-1071 enabled consumers
Sub-task · Resolved (Fixed) · Major · components: streams · created 2025-05-12 · resolved 2025-06-03

The new rebalance protocol cannot be supported by the existing KafkaClientSupplier and KIP-1088 is on hold.
For now, to support current internal testing cases that use KafkaClientSupplier for injecting test behavior, we need a private interface that can fulfil this functionality for KIP-1071.


## KAFKA-19431: Stronger assignment consistency with subscription for consumer groups 
Improvement · Resolved (Fixed) · Major · components: group-coordinator · created 2025-06-24 · resolved 2025-10-06

Currently, consumer group assignments are eventually consistent with subscriptions: when a member has unrevoked partitions, it is not allowed to reconcile with the latest target assignment. If a member with unrevoked partitions shrinks its subscription, it may observe assignments from the broker containing topics it is no longer subscribed to.
If we wanted to, we could tighten this up at the cost of extra CPU time. Note that it's not feasible to close the gap for regex subscriptions, since ther…


## KAFKA-19433: Unify broker heartbeat RPC timeout and periodic resend timeout
Improvement · Open · Minor · created 2025-06-24

We should unify the broker heartbeat RPC timeout and the periodic resend timeout so that RPC timeouts don't result in us sending broker heartbeats less frequently than usual.

- **Jimmy Wang:** Hi [~cmccabe] ,
 I think I could help with this issue :)
- **Jimmy Wang:** Hi [~cmccabe] , sorry for the late response. I'm a bit confused because currently, for the broker, both the periodic resend timeout and the RPC timeout are set to {{{}broker.heartbeat.interval.ms{}}}. I wonder if I've missed something or if I didn't understand your point correctly. Could you help to…

## KAFKA-19476: Improve state transition handling in SharePartition
Sub-task · Resolved (Fixed) · Major · created 2025-07-06 · resolved 2025-08-02


## KAFKA-19580: Upgrade spotbug to 4.9.4
Improvement · Resolved (Fixed) · Minor · created 2025-08-05 · resolved 2025-08-10

see discussion https://github.com/apache/kafka/pull/20295#issuecomment-3146551515

- **xuanzhang gong:** hello,I will fix it
- **Stig Rohde Døssing:** I've raised https://github.com/apache/kafka/pull/20333 to fix this.
 [~gongxuanzhang] Sorry, I didn't notice your comment until now, I didn't mean to steal this issue, it just kind of happened since I did the previous spotbugs-related work too. Feel free to let me know if you have a better fix than…

## KAFKA-19587: Unify kraft shutdown logic in poll methods
Task · Open · Major · created 2025-08-07

Currently, different KRaft replica states handle polling during graceful shutdown differently. This Jira aims to unify their logic.


## KAFKA-19660: JoinWithIncompleteMetadataIntegrationTest fails in isolated run of one parameter
Sub-task · Resolved (Fixed) · Major · components: streams, unit tests · created 2025-09-01 · resolved 2025-09-10

When I run JoinWithIncompleteMetadataIntegrationTest, with only the new protocol enabled, it fails (since it does not run long enough for the exception to be triggered by the timer).
When the test is run for both protocols, the second run passes because it uses an existing group ID and that is why it why streams is shutting down.


## KAFKA-19666: Clean up integration tests related to state-updater
Sub-task · Resolved (Resolved) · Blocker · components: streams, unit tests · created 2025-09-02 · resolved 2025-09-12

This is the first step in the parent task: To clean up all the integration tests related to state-updater flag
See [https://github.com/apache/kafka/pull/20392#issuecomment-3240659815] for more details


## KAFKA-19683: Clean up TaskManagerTest
Sub-task · Resolved (Resolved) · Blocker · components: streams, unit tests · created 2025-09-07 · resolved 2025-12-02

See https://github.com/apache/kafka/pull/20392#issuecomment-3241457533

- **Shashank:** Hi [~lucasbru], since the tests in the cleanup of this file are many, I would like to propose to make incremental changes to this cleanup.
 - Removal of dead tests and address these 3 comments - [#1|https://github.com/apache/kafka/pull/19275#discussion_r2107811068], [#2|https://github.com/apache/kaf…
- **sanghyeok An:** I think, after this tickets are resolved, https://issues.apache.org/jira/browse/KAFKA-12569 can be resolved as well.
- **Shashank:** You're right! Thank you [~chickenchickenlove]

## KAFKA-19687: MetaDataShell log error message for SNAPSHOT_HEADER and SNAPSHOT_FOOTER
Improvement · Open · Minor · created 2025-09-08

```
./bin/kafka-metadata-shell.sh -s /tmp/kafka-meta/bootstrap.checkpoint
17:31:43 Loading...
[2025-09-08 17:32:19,271] ERROR Ignoring control record with type SNAPSHOT_HEADER at offset 0 (org.apache.kafka.metadata.util.SnapshotFileReader)
[2025-09-08 17:32:19,274] ERROR Ignoring control record with type SNAPSHOT_FOOTER at offset 5 (org.apache.kafka.metadata.util.SnapshotFileReader) Starting...
```


## KAFKA-19693: Introduce PersisterBatch in SharePartition
Sub-task · Resolved (Fixed) · Major · created 2025-09-09 · resolved 2025-09-10


## KAFKA-19795: Mark the minOneMessage as false when delayedRemoteFetch is present in the first partition
Task · Resolved (Fixed) · Major · created 2025-10-16 · resolved 2025-10-16


## KAFKA-19796: Introduce computations for inFlightTerminalRecords
Sub-task · Resolved (Fixed) · Minor · created 2025-10-16 · resolved 2025-10-29


## KAFKA-19798: Persist deliveryCompleteCount in ShareSnapshot and ShareUpdate records
Sub-task · Resolved (Fixed) · Minor · created 2025-10-16 · resolved 2025-11-03


## KAFKA-19800: Compute share partition lag in GroupCoordinatorService
Sub-task · Resolved (Fixed) · Minor · created 2025-10-16 · resolved 2025-11-17


## KAFKA-19822: Remove all static classes in Field except TaggedFieldsSection
Improvement · Resolved (Fixed) · Major · components: clients · created 2025-10-22 · resolved 2025-11-05

All static classes in Field except TaggedFieldsSection are not really being used. We should remove them.


## KAFKA-19830: Refactor KafkaRaftClient to use event scheduler framework
Improvement · Open · Major · created 2025-10-23


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

## KAFKA-19942: Clean up StreamThread and StoreChangelogReader Test
Sub-task · Resolved (Resolved) · Blocker · components: streams, unit tests · created 2025-11-30 · resolved 2025-12-02

Clean up StreamThreadTest.java and StoreChangelogReaderTest.java to always use StateUpdater.
We also update the config to always have stateupdater enabled.


## KAFKA-20105: Move FetchSessionTest to server module
Sub-task · Resolved (Fixed) · Minor · created 2026-01-30 · resolved 2026-02-04


## KAFKA-20146: Add CI job to detect dependency conflicts in setup.py
Improvement · Resolved (Fixed) · Minor · created 2026-02-07 · resolved 2026-02-22

from: [https://github.com/apache/kafka/pull/21415]


## KAFKA-20147: Add CI job to detect dependency conflicts in setup.py
Improvement · Resolved (Duplicate) · Minor · created 2026-02-07 · resolved 2026-02-07

from: [https://github.com/apache/kafka/pull/21415]


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

## KAFKA-20326: WindowStoreMaterializerTests needs to get updated
Sub-task · Resolved (Fixed) · Blocker · components: streams · created 2026-03-17 · resolved 2026-03-20

`shouldCreateHeadersStoreWithOnWindowCloseAndCachingEnabled` is incorrect – we removed a check to make it pass for now, but need to add back the correct assertion after the root cause was fixed.
ref: [https://github.com/apache/kafka/pull/21580/changes#r2921529513]


## KAFKA-20331: Update upgrade.md to mention new assignment offload configs
Sub-task · Resolved (Fixed) · Major · created 2026-03-18 · resolved 2026-04-07


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

## KAFKA-20454: Verify that `bin/kafka-consumer-groups.sh --reset-offsets` fails for "streams" group
Test · Open · Minor · components: streams, unit tests · created 2026-04-15

With KIP-848/1071 we now have three types of groups, "classic", "consumer", and "streams". (And with KIP-932, actually also "share" groups, but they are orthogonal to this ticket).
When users reset group offset, they can use `bin/kafka-consumer-groups.sh` tool, which always uses group-type "classic".
For a "consumer" group, this is not a problem, because mixed groups are supported.
However, for a "streams" group, mixed mode (with "classic") is not supported atm. We should add a test that veri…


## KAFKA-20639: Move EnvelopeUtils to server module
Sub-task · Resolved (Fixed) · Minor · created 2026-05-29 · resolved 2026-06-01


## KAFKA-20645: Move LogLoaderTest to storage module
Sub-task · Resolved (Fixed) · Major · created 2026-05-30 · resolved 2026-06-25


## KAFKA-20648: Move Processor to server module
Sub-task · Open · Major · created 2026-06-01


## KAFKA-20793: Mark share.version=2 stable
Sub-task · Resolved (Fixed) · Major · created 2026-07-10 · resolved 2026-07-23


## KAFKA-20795: RequestConvertToJson#request and RequestConvertToJson#response could be implemented by generator
Improvement · Open · Minor · created 2026-07-10

These methods are currently hardcoded to convert requests/responses to JSON. This is a perfect use case for the generator module, so we should delegate the implementation to it.

- **dino2895:** {{Hi, I will take this up.}}

## KAFKA-21053: Rewrite shouldThrowIllegalStateExceptionOnOffsetIfNoRecordContext
Test · Resolved (Fixed) · Minor · created 2026-09-09 · resolved 2026-09-11

It stays on the very old logic. We should rewrite it to match the current implementation.


## KAFKA-21054: Use assertThrows in InternalTopicManagerTest timeout tests
Test · Open · Minor · components: streams, unit tests · created 2026-09-09

[code/log omitted]
[code/log omitted]
It should leverage assertThrows to ensure it does throw exception.


## KAFKA-21056: migrate to gradle version catalog
Improvement · Open · Minor · created 2026-09-09

the kafka project currently has its own custom [{{dependencies.gradle}}|https://github.com/apache/kafka/blob/trunk/gradle/dependencies.gradle] mechanism to manage dependency versions.
gradle nowadays has a standard way of dealing with this, the [version catalog|https://docs.gradle.org/current/userguide/version_catalogs.html], which is also clearly listed as part of their [best practices|https://docs.gradle.org/current/userguide/best_practices_dependencies.html#use_version_catalogs].
i'd sugges…


## KAFKA-21145: Reenable tests once compression is supported 
Sub-task · Open · Minor · created 2026-09-22

See the comment: https://github.com/apache/kafka/pull/23135#discussion_r3769371194


## KAFKA-21148: speed up JoinStoreIntegrationTest
Improvement · Open · Minor · created 2026-09-23

similar to KAFKA-21133


## KAFKA-21150: Refactor AbstractKafkaConfig#processRoles
Improvement · Open · Minor · created 2026-09-23

[code/log omitted]
We could add a helper method to {{ProcessRole}} that converts a string to a {{{}ProcessRole{}}}, and then rewrite {{processRoles()}} in a fluent style.

