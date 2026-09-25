## KAFKA-12157: test Upgrade 2.7.0 from 2.0.0 occur a question
Bug · Open · Blocker · components: log · created 2021-01-07

I was in a test environment, rolling upgrade from version 2.0.0 to version 2.7.0, and encountered the following problems. When the rolling upgrade progressed to the second round, I stopped the first broker(1001) in the second round and the following error occurred. When an agent processes the client producer request, the starting offset of the leader epoch of the partition leader suddenly becomes 0, and then continues to process write requests for the same partition, and an error log will appear…


## KAFKA-12158: Consider better return type of RaftClient.scheduleAppend
Sub-task · Resolved (Fixed) · Major · created 2021-01-07 · resolved 2021-08-02

Currently `RaftClient` has the following Append API:
[code/log omitted]
There are a few possible cases that the single return value is trying to handle:
1. The epoch doesn't match or we are not the current leader => return Long.MaxValue
2. We failed to allocate memory to write the the batch (backpressure case) => return null
3. We successfully scheduled the append => return the expected offset
It might be better to define a richer type so that the cases that must be handled are clearer. At…

- **Sagar Rao:** hey [~hachikuji], can I take this one up?
- **José Armando García Sancio:** Yes [~sagarrao] . Feel free to pick this up.

## KAFKA-12159: kafka-console-producer prompt should redisplay after an error output
Bug · Open · Minor · components: producer , tools · created 2021-01-07

*BLUF:* The kafka-console-producer should return its prompt after outputting an error message (if it is still running, which in most cases, it is). Current behaviour is it doesn't return a prompt, and hitting return at that point shuts it down.
This started with a ticket logged against Confluent Platform feature documentation.
*DETAIL AND EXAMPLE:* The console producer utility behaves in a less than optimal way when you get an error. It doesn’t return the producer prompt even though the produc…


## KAFKA-12160: KafkaStreams configs are documented incorrectly
Bug · Resolved (Fixed) · Minor · components: docs, streams · created 2021-01-08 · resolved 2021-02-23

In version 2.3, we removed the KafkaStreams default of `max.poll.interval.ms` and fall-back to the consumer default. However, the docs still contain `Integer.MAX_VALUE` as default.
Because we rely on the consumer default, we should actually remove `max.poll.interval.ms` from the Kafka Streams docs completely. We might want to fix this is some older versions, too. Not sure how far back we want to go.
Furhtermore, in 2.7 docs, the section of "Default Values" and "Parameters controlled by Kafka S…


## KAFKA-12161: Raft observers should not require an id to fetch
Sub-task · Resolved (Fixed) · Major · created 2021-01-08 · resolved 2021-01-15

It is useful to allow observers to replay the metadata log without requiring a replica id. For example, this can be used by tools in order to inspect the current metadata state. In order to support this, we should modify `KafkaRaftClient` so that the broker id is not required.

- **Boyang Chen:** I was wondering whether we could just get a random UUID for observer when we do the tooling?
- **Jason Gustafson:** [~bchen225242] That's not a bad idea. However, we are constrained a little bit since Fetch requires an int32 replicaId. I think it might be simpler for the moment to make the field optional and treat non-participating observers more like consumers.

## KAFKA-12162: Kafka broker continued to run after failing to create "/brokers/ids/X" znode.
Bug · Open · Major · created 2021-01-08

We found that Kafka broker continued to run after it failed to create "/brokers/ids/X" znode and still acted as a partition leader. This should've been fixed in https://issues.apache.org/jira/browse/KAFKA-7165 but there might be a corner case that was not handled here.
Here's the log snippet.
[code/log omitted]


## KAFKA-12163: Controller should ensure zkVersion is monotonically increasing when sending UpdateMetadata requests.
Bug · Open · Major · created 2021-01-08

When sending UpdateMetadata requests, controller does not currently perform any check to ensure zkVersion is monotonically increasing. If Zookeeper gets into a bad state, this can cause Kafka cluster to get into a bad state and possible data loss as well.
Controller should perform a check to protect the Kafka clusters from getting into a bad state.
Following shows an example of zkVersion going backward at 2020-12-08 14:10:46,420.
[code/log omitted]


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

## KAFKA-12165: org.apache.kafka.common.quota classes omitted from Javadoc
Bug · Resolved (Fixed) · Minor · components: clients · created 2021-01-08 · resolved 2021-01-08

The public API classes in `org.apache.kafka.common.quota` should be included in the javadoc, but are currently omitted. E.g. see https://kafka.apache.org/27/javadoc/org/apache/kafka/clients/admin/Admin.html#alterClientQuotas-java.util.Collection-


## KAFKA-12166: Add a metric for reporting idle connections closed
Improvement · Open · Minor · components: core, metrics · created 2021-01-08

The Kafka Broker has a logic for closing connections when they have been idle for a configurable amount of time.
Currently the only way the broker report this is via the TRACE level logs, however, it would amazing to have a new metric to track it via the monitoring tack of choice.


## KAFKA-12167: Consumer group does not rebalance properly when joining more than one node
Bug · Open · Major · components: consumer · created 2021-01-08

Hi
We have spotted strange issue:
Joining more than one consumer to consumer group fails not leaving absolutely any information in broker logs.
We though that this may have been https://issues.apache.org/jira/browse/KAFKA-9752 but after upgrading client libs to 2.5 we still faced same issue(brokers are 2.6).
We reviewed logs and could not find anything.
After investigating the only thing that is bad about this cluster is huge amount of dead consumer(no longer used) groups which we will be c…


## KAFKA-12342: Get rid of raft/meta log shim layer
Improvement · Resolved (Fixed) · Major · labels: kip-500 · created 2021-02-18 · resolved 2021-05-21

We currently use a shim to bridge the interface differences between `RaftClient` and `MetaLogManager`. We need to converge the two interfaces and get rid of the shim.


## KAFKA-12343: Recent change to use SharedTopicAdmin in KakfkaBasedLog fails with AK 0.10.x brokers
Bug · Resolved (Fixed) · Blocker · components: connect · created 2021-02-18 · resolved 2021-02-20

System test failure ([sample|http://confluent-kafka-2-7-system-test-results.s3-us-west-2.amazonaws.com/2021-02-18--001.1613655226--confluentinc--2.7--54952635e5/report.html]):
[code/log omitted]


## KAFKA-12344: Support SlidingWindows in the Scala API
Improvement · Resolved (Fixed) · Major · components: streams · labels: newbie, scala · created 2021-02-18 · resolved 2021-04-26

in KIP-450 we implemented sliding windows for the Java API but left out a few crucial methods to allow sliding windows to work through the Scala API. We need to add those methods to make the Scala API fully leverage sliding windows

- **Ketul Gupta:** Hi [~lct45],
 I would like to work on this.
 I am going through [KIP-450|https://cwiki.apache.org/confluence/display/KAFKA/KIP-450%3A+Sliding+Window+Aggregations+in+the+DSL] , and would later look into implementation in java for doing it in scala.
 Would you guide me in this by giving some pointers…
- **Leah Thomas:** Hi [~ketulgupta], thanks for picking this up! It should be a relatively easy fix. If you look at [KGroupedStream.scala|https://github.com/apache/kafka/blob/trunk/streams/streams-scala/src/main/scala/org/apache/kafka/streams/scala/kstream/KGroupedStream.scala#L155] you can see that there's a `windowe…
- **Matthias J. Sax:** Sound about right – in the Java code, `windowedBy(SlidingWindows)` returns a `TimeWindowedKStream` and thus the Scala code should do a similar thing.
- **Ketul Gupta:** Hi [~lct45]  [~mjsax] , I have made the method additions in KGroupedStream and Cogrouped stream as windowedBy(SlidingWindows)
 method was there in both the classes, also added test in KtableTests. Please review the changes.

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

## KAFKA-12346: punctuate is called at twice the duration passed as the first argument to Processor.Schedule (with PunctuationType.WALL_CLOCK_TIME)
Bug · Open · Major · components: streams · created 2021-02-19

A stream transform called with the idiom below causes punctuate to be called at twice the duration of the argument passed
[code/log omitted]
If the interval is specified as 1 second, the callback fires every 2 seconds. If the interval is specified as 5 seconds, the callback fires every 10 seconds.


## KAFKA-12347: Improve Kafka Streams ability to track progress
Improvement · Resolved (Done) · Major · components: streams · labels: kip · created 2021-02-19 · resolved 2021-03-05

Add methods to track records being consumed fully and to tell if tasks are idling. This will allow users of streams to build uptime metrics around streams with less difficulty.
KIP-715: [https://cwiki.apache.org/confluence/display/KAFKA/KIP-715%3A+Expose+Committed+offset+in+streams]

- **Walker Carlson:** KIP: https://cwiki.apache.org/confluence/x/aRRRCg

## KAFKA-12348: The metadata module currently uses Yammer metrics.  Should it uses Kafka metrics instead?
Task · Open · Minor · components: metrics · created 2021-02-19


## KAFKA-12349: Follow up on PartitionEpoch in KIP-500
Improvement · Resolved (Fixed) · Major · created 2021-02-20 · resolved 2021-06-15

* Remove the compatibility shim between raft and the kip-500 controller
* standardize on the epoch data type (probably int)
* review partition epoch, leader epoch

- **Colin McCabe:** [~hachikuji] has a PR for removing the compatibility shim here
- **Colin McCabe:** We removed the shim.

## KAFKA-12350: document  about refresh.topics.interval.seconds default value is not right 
Bug · Resolved (Fixed) · Minor · components: website · created 2021-02-20 · resolved 2021-02-24

The config, refresh.topics.interval.seconds, described in document  give the defalut value 6000, ten minutes. 600 seconds or 100 minutes?

- **Luke Chen:** The default values are set to 10 * 60 seconds, which is 10 minutes. I'll update the document. Thanks for reporting [~superheizai]
- **ASF GitHub Bot:** showuon opened a new pull request #332: URL: https://github.com/apache/kafka-site/pull/332    Correct the wrong default value. ref: https://github.com/apache/kafka/pull/10165 ---------------------------------------------------------------- This is an automated message from the Apache Git Service. To…
- **ASF GitHub Bot:** showuon commented on pull request #332: URL: https://github.com/apache/kafka-site/pull/332#issuecomment-786370398    @chia7712 , could you also review this PR? Same as this one: apache/kafka#10165, Just in kafka-site repo. Thanks. ---------------------------------------------------------------- This…
- **ASF GitHub Bot:** chia7712 merged pull request #332: URL: https://github.com/apache/kafka-site/pull/332 ---------------------------------------------------------------- This is an automated message from the Apache Git Service. To respond to the message, please log on to GitHub and use the URL above to go to the speci…
- **ASF GitHub Bot:** chia7712 commented on pull request #332: URL: https://github.com/apache/kafka-site/pull/332#issuecomment-786457377    @showuon Thanks for this patch :) ---------------------------------------------------------------- This is an automated message from the Apache Git Service. To respond to the message…

## KAFKA-12351: Fix misleading max.request.size behavior
Improvement · Resolved (Duplicate) · Major · created 2021-02-20 · resolved 2021-02-20

The producer has a configuration called `max.request.size`. It is documented as follows:
[code/log omitted]
So basically the intent is to limit the overall size of the request, but the documentation says that it also serves as a maximum cap on the uncompressed batch size.
In the implementation, however, we use it as a maximum cap on uncompressed record sizes, not batches. Additionally, we treat this as a soft limit when applied to requests. Both of these differences are worth pointing out in…

- **Ismael Juma:** I think we have an existing JIRA about this btw.

## KAFKA-12352: Improve debuggability with continuous consumer rebalances
Improvement · Open · Major · components: consumer, streams · created 2021-02-21

There are several scenarios where a consumer/streams client can fall into continuous rebalances and hence does not make any progress. Today when this happens, developers usually need to do a lot digging in order to get insights on what happens. Here's short summary of different scenarios where we (re-)trigger rebalances: 
1. Group member kicked out of the group: when the coordinator kicked out the member, later on when the member issues a join / sync / heartbeat / offset-commit, it will fail an…


## KAFKA-12457: Implications of KIP-516 for quorum controller
Improvement · Resolved (Fixed) · Major · labels: kip-500 · created 2021-03-11 · resolved 2021-04-08

KIP-516 introduces topic IDs to Kafka. We are in the process of updating many of the protocols to support them. In most cases, we are dropping the topic name entirely from new API versions. I think there are two open questions for KIP-500 in regard to this:
1. Can we assume topic ID existence in KIP-500? 
I think the answer here is yes, and the existing code already assumes it. The nice thing is that KIP-516 brings with it the logic to create topic IDs for existing topics. We can rely on this…

- **Justine Olshan:** Thanks for creating this JIRA. There is some discussion on sentinel topic IDs in KIP-516 as well, but it has been a while. I think the original plan was to use the sentinel ID as a sort of bootstrap for Vote requests and then to generate a unique topic ID for the metadata topic. Very much open to di…
- **Justine Olshan:** FYI, there is already work in progress to support FETCH using topic ID rather than name. https://github.com/apache/kafka/pull/9944
- **Guozhang Wang:** [~jolshan] [~hachikuji] Just curious, are we going to generate uuid for other internal topics (offset, txn) as well or use hard-coded sentinels, meaning different clusters would have different ids for them?
- **Jason Gustafson:** [~guozhang] My understanding is that the current logic in KafkaController will generate topic IDs for all existing topics including internal ones. The `@metadata` topic poses a different challenge because there is a bootstrapping problem when a cluster is first created (you have to be able to fetch…
- **Justine Olshan:** I'm going to start with the sentinel ID for now. I'll be using  Uuid(0L, 1L) as designated in the Uuid class.

## KAFKA-12458: Implementation of Tiered Storage Integration with Azure Storage (ADLS + Blob Storage)
Sub-task · Resolved (Won't Do) · Major · created 2021-03-12 · resolved 2023-08-31

Task to cover integration support for Azure Storage
 * Azure Blob Storage
 * Azure Data Lake Store
Will split task up later into distinct tracks and components

- **Israel Ekpo:** This issue is not tied to any release since the code will be hosted outside of the Kafka Repo
- **Ivan Yurchenko:** FYI: I've been working on a {{RemoteStorageManager}} implementation that currently supports only AWS S3, but it's planned to add Azure in near future. [https://github.com/aiven/tiered-storage-for-apache-kafka]
- **Satish Duggana:** We are not planning to add RSM implementations as part of Apache Kafka. We can refer these RSM plugin implementations in Apache Kafka documentation.

## KAFKA-12459: Improve raft simulation tests
Sub-task · Resolved (Fixed) · Major · created 2021-03-12 · resolved 2021-03-18

A couple small suggestions to improve the event simulation tests (courtesy of [~enether]):
1. When a test fails, ensure that the random number seed is displayed in the output so that it can be reproduced.
2. Once we have done the first one, then using non-deterministic seeds would be a good idea since we can get a bigger benefit out of repeated builds.
3. It is a bit painful today to reproduce failures since each test case runs multiple random seeds. It would be helpful to have a convenient w…

- **Lucas Bradstreet:** It might be worth considering looking at how much work it'd be to switch these tests over to a property testing library as that will give you the seed behavior you want, and will give you the additional benefit of shrinking the inputs when there's a failure.

## KAFKA-12460: Raft should prevent truncation below high watermark
Sub-task · Resolved (Fixed) · Major · created 2021-03-12 · resolved 2021-03-13

Eventually we will have to come up with some approach to recover from committed data loss in the raft quorum (something akin to unclean leader election for normal partitions).  For now, we would rather be stricter and fail fast rather than allowing committed data to be silently lost. Specifically, we can prevent any attempt to truncate below the high watermark since this is a clear indication of data loss. The long term thought I have in mind is to give users an --unsafe flag or something like t…


## KAFKA-12461: Extend LogManager to cover the metadata topic
Sub-task · Open · Major · created 2021-03-12

The `@metadata` topic is not managed by `LogManager` since it uses a new snapshot-based retention policy. This means that it is not covered by the recovery and high watermark checkpoints. It would be useful to fix this. We can either extend `LogManager` so that it is aware of the snapshotting semantics implemented by the `@metadata` topic, or we can create something like a `RaftLogManager`.


## KAFKA-12462: Threads in PENDING_SHUTDOWN entering a rebalance can cause an illegal state exception 
Bug · Resolved (Fixed) · Blocker · components: streams · labels: streams · created 2021-03-12 · resolved 2021-03-13

A thread was removed, sending it to the PENDING_SHUTDOWN state, but went through a rebalance before completing the shutdown.
[code/log omitted]
Inside StreamsRebalanceListener#onPartitionsRevoked, we have
[code/log omitted]
Since PENDING_SHUTDOWN → PARTITIONS_REVOKED is a disallowed transition, we never invoke TaskManager#handleRevocation. Currently handleRevocation is responsible for preparing any active tasks for close, including committing offsets and writing the checkpoint as well as sus…

- **A. Sophie Blee-Goldman:** Thanks Walker! This actually seems like a long-lurking bug that was just surfaced by the removeStreamThread() feature, not caused by it. Before we could remove threads this was only possible when shutting down the client, which we don’t test as frequently as we now do removeStreamThread(). It’s also…
- **Walker Carlson:** If we were shutting down the whole client the thread would become dead either way. In 2.7 I think the only impact it would have is that the handler would get called after the close call when it shouldn’t. But otherwise it might not have an effect. I suppose there is no harm to back-porting though.…
- **A. Sophie Blee-Goldman:** The only real downside in 2.7 is that we won't properly clean up the task, ie we'll skip committing the offsets and writing the checkpoint. So we'd lose any work we did since the last commit – for EOS this would be a perf hit since we'd probably need to restore the state stores from scratch after st…
- **Walker Carlson:** This also affects 2.6

## KAFKA-12463: Update default consumer partition assignor for sink tasks
Improvement · Open · Major · components: connect · labels: needs-kip · created 2021-03-14

Kafka consumers have a pluggable [partition assignment interface|https://kafka.apache.org/27/javadoc/org/apache/kafka/clients/consumer/ConsumerPartitionAssignor.html] that comes with several out-of-the-box implementations including the [RangeAssignor|https://kafka.apache.org/27/javadoc/org/apache/kafka/clients/consumer/RangeAssignor.html], [RoundRobinAssignor|https://kafka.apache.org/27/javadoc/org/apache/kafka/clients/consumer/RoundRobinAssignor.html], [StickyAssignor|https://kafka.apache.org/2…

- **Chris Egerton:** [~bchen225242] can you confirm the upgrade semantics outlined here? I think the Kafka group coordinator should force every consumer in the group to use range assignment until every consumer in the group is configured to use both the cooperative sticky assignor and the range assignor (in that order),…
- **A. Sophie Blee-Goldman:** [~ChrisEgerton] just fyi, the CooperativeStickyAssignor was introduced in 2.4, not 2.3. Also, that upgrade protocol sounds correct but it should be covered in the KIP-429 document – did you check out the steps listed for Consumer upgrades in the section called "Compatibility and Upgrade Path"? [Link…
- **Chris Egerton:** Ah, thanks [~ableegoldman], I'd misread the javadocs for the cooperative sticky assignor. Updated the description to point to 2.4 instead of 2.3.
 RE clearness on the upgrade section in KIP-429–I didn't see a specific section for Connect, and both of the sections that were there ("Consumer" and "Str…
- **Chris Egerton:** cc [~rhauch] what do you think about this?
- **A. Sophie Blee-Goldman:** Isn't the upgrade path for Connect identical to the one for the Consumer? There's no mention of Connect in KIP-429 because that KIP focuses on cooperative rebalancing for the plain Consumer and Kafka Streams, while Connect had its own separate KIP and protocol for incremental cooperative rebalancing…
- _…15 more comments_

## KAFKA-12464: Enhance constrained sticky Assign algorithm
Improvement · Resolved (Fixed) · Major · components: consumer · labels: perfomance · created 2021-03-15 · resolved 2021-05-06

In KAFKA-9987, we did a great improvement for the case when all consumers were subscribed to same set of topics. The algorithm contains 4 phases:
 # Reassign as many previously owned partitions as possible, up to the maxQuota
 # Fill remaining members up to minQuota
 # If we ran out of unassigned partitions before filling all consumers, we need to start stealing partitions from the over-full consumers at max capacity
 # Otherwise we may have run out of unfilled consumers before assigning all…

- **Luke Chen:** [~ableegoldman] [~guozhang], could you help review this enhancement and have some comments? Thank you.
- **A. Sophie Blee-Goldman:** Thanks for the proposal – I think the basic idea makes sense. There is an existing scale test in AbstractStickyAssignorTest called  testLargeAssignmentAndGroupWithUniformSubscription() which you can use to measure the improvement. It already has pretty good performance but further optimizations are…
- **Luke Chen:** [~ableegoldman], good news, after my enhancement, the _testLargeAssignmentAndGroupWithUniformSubscription_ test time down from 28xx ms, to 18xx ms. Improved 33% of performance. PR is submitted. Thank you.
- **Luke Chen:** OK, I was wrong. The final version of PR doesn't make any difference for the performance. I didn't do round-robin assign in previous change, but I found it's required for the assignor. After doing round-robin, the performance is pretty much the same as before (since loop many times), but at least, t…
- **Luke Chen:** Another improvement is implemented (check https://github.com/apache/kafka/pull/10509#issuecomment-822975764)
 After the change: the {{testLargeAssignmentAndGroupWithUniformSubscription}} (1 million partitions) will run from *~2600 ms*
  *down to ~1400 ms*, improves *46%* of performance, almost *2x f…

## KAFKA-12465: Decide whether inconsistent cluster id error are fatal
Sub-task · Open · Major · created 2021-03-15

Currently, we just log an error when an inconsistent cluster-id occurred. We should set a window during startup when these errors are fatal but after that window, we no longer treat them to be fatal. see https://github.com/apache/kafka/pull/10289#discussion_r592853088

- **Jose Armando Garcia Sancio:** One solution is to implement it when handling a response, invalid cluster id are fatal unless a previous response contained a valid cluster id.
- **Omnia Ibrahim:** I have been testing KRAFT and I tried this scenario where I setup a cluster with 3 combined nodes (broker, controller) and 3 nodes as brokers then later at some point I add an extra 2 nodes to the KRAFT with different cluster id. I would expect if this is a really deployment on production then these…
- **Deng Ziming:** [~omnia_h_ibrahim] Thank you for the feedback, we are now trying to design an algorithm to decide when to treat `INCONSISTENT_CLUSTER_ID`, some discussions are listed here: [https://github.com/apache/kafka/pull/10289#discussion_r592853088]
 I think [~jagsancio]'s suggestion is a good one, WDYT?

## KAFKA-12466: Controller and Broker Metadata Snapshots
New Feature · In Progress · Major · labels: kip-500 · created 2021-03-15


## KAFKA-12467: Implement QuorumController metadata snapshots
Sub-task · Resolved (Fixed) · Major · labels: kip-500 · created 2021-03-15 · resolved 2021-07-01

Implement QuorumController metadata snapshots.


## KAFKA-12557: org.apache.kafka.clients.admin.KafkaAdminClientTest#testClientSideTimeoutAfterFailureToReceiveResponse intermittently hangs indefinitely
Bug · Resolved (Fixed) · Major · components: clients, core · created 2021-03-25 · resolved 2021-03-30

While running tests for [https://github.com/apache/kafka/pull/10397,] I got a test timeout under Java 8.
I ran it locally via `./gradlew clean -PscalaVersion=2.12 :clients:unitTest --profile --no-daemon --continue -PtestLoggingEvents=started,passed,skipped,failed -PignoreFailures=true -PmaxTestRetries=1 -PmaxTestRetryFailures=5` (copied from the Jenkins log) and was able to determine that the hanging test is:
org.apache.kafka.clients.admin.KafkaAdminClientTest#testClientSideTimeoutAfterFailure…


## KAFKA-12558: MM2 may not sync partition offsets correctly
Bug · Resolved (Fixed) · Major · components: mirrormaker · created 2021-03-25 · resolved 2023-01-10

There is a race condition in {{MirrorSourceTask}} where certain partition offsets may never be sent. The bug occurs when the [outstandingOffsetSync semaphore is full|https://github.com/apache/kafka/blob/trunk/connect/mirror/src/main/java/org/apache/kafka/connect/mirror/MirrorSourceTask.java#L207]. In this case, the sendOffsetSync [will silently fail|https://github.com/apache/kafka/blob/trunk/connect/mirror/src/main/java/org/apache/kafka/connect/mirror/MirrorSourceTask.java#L207].
This failure i…

- **Ryanne Dolan:** This sounds right. Updating the partition store without sending an offset sync means additional offset syncs are unlikely to arrive for a long time, if ever. I'm happy to fix but will leave this unassigned for a bit in case someone else wants to take this on.
- **Angelos Kaltsikis:** Just one clarification:
  The number of *LEADER* partitions / The number of tasks <= 10
 Correct?
 [~askldjd]

## KAFKA-12559: Add a top-level Streams config for bounding off-heap memory
Improvement · Open · Major · components: streams · labels: needs-kip, newbie, newbie++ · created 2021-03-25

At the moment we provide an example of how to bound the memory usage of rocskdb in the [Memory Management|https://kafka.apache.org/27/documentation/streams/developer-guide/memory-mgmt.html#rocksdb] section of the docs. This requires implementing a custom RocksDBConfigSetter class and setting a number of rocksdb options for relatively advanced concepts and configurations. It seems a fair number of users either fail to find this or consider it to be for more advanced use cases/users. But RocksDB c…

- **A. Sophie Blee-Goldman:** We can also consider whether to apply this bounded memory configuration by default. Picking a reasonable default value is rather challenging: if we make it something very low like 1GB then this could cause a drastic perf hit for users upgrading without setting this config. I would personally advocat…
- **amuthan Ganeshan:** Hi [~ableegoldman] and [~mjsax]
 I would like to work on this.
 Would you guide me in this by giving some pointers to start with...
- **A. Sophie Blee-Goldman:** Sure thing -- I recommend checking out the example implementation in the Memory Management section (linked to in the ticket description) and read up on the KIP process if you're not familiar with it yet: https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Improvement+Proposals
 The idea here is…
- **amuthan Ganeshan:** Thanks, [~ableegoldman], for the explanation; yep, it makes sense now. Let me give it a try and get back to you if I have further questions.
- **Martin Sundeqvist:** [~ableegoldman] [~simplyamuthan] Hi, I can see it's been a while since the last update. I'm new at this, and would like to take a crack at it, unless things are already moving forward?
- _…10 more comments_

## KAFKA-12560: Accidental delete of some log files kafka-authorizer.log and kafka-request.log can break topics in cluster
Bug · Open · Minor · components: log · created 2021-03-26

These two log files have 0 byte size and last created modified or updated  along time ago and these files seem to be created on startup.
When disks fill up, sometimes admins go through old log files and delete them. In this case, these two .log were also picked up. Note that I acknowledge this is a mistake as it should be filtered by extension but nevertheless anything in /var/log should not cause process to have issues and if the file doesn't exist, the process should simply recreate it.
The…


## KAFKA-12561: Fix flaky kafka.server.RaftClusterTest.testCreateClusterAndCreateListDeleteTopic()
Test · Resolved (Fixed) · Major · created 2021-03-26 · resolved 2021-03-31

[code/log omitted]
Also the same error as in testCreateClusterAndCreateAndManyTopics
https://ci-builds.apache.org/job/Kafka/job/kafka-trunk-jdk11/634/testReport/junit/kafka.server/RaftClusterTest/testCreateClusterAndCreateListDeleteTopic__/
https://ci-builds.apache.org/job/Kafka/job/kafka-trunk-jdk8/602/testReport/junit/kafka.server/RaftClusterTest/testCreateClusterAndCreateListDeleteTopic__/
https://ci-builds.apache.org/job/Kafka/job/kafka-trunk-jdk15/667/testReport/junit/kafka.server/RaftC…


## KAFKA-12562: Remove deprecated-overloaded "KafkaStreams#metadataForKey" and "KafkaStreams#store"
Sub-task · Resolved (Fixed) · Minor · components: streams · created 2021-03-26 · resolved 2021-03-28


## KAFKA-12563: Something wrong with MM2 metrics
Bug · Resolved (Fixed) · Major · components: mirrormaker · created 2021-03-26 · resolved 2023-02-24

The metric _*`adt_2dc_c1_kafka_connect_mirror_source_connector_replication_latency_ms_avg`*_ shows that value of latency is a very large number but the amount of messages in two DC are the same.
View details in the attachment.

- **Ryanne Dolan:** The metric is calculated based on the timestamp of each replicated record, which can be set by client code. e.g. a producer can set a timestamp of zero, which would yield the replication latency you observe.
- **Bui Thanh MInh:** Thanks, but as I understand the meaning of this metric, two clusters are in sync if the value is zero. So, my question in this case is how to identify the replication lag betwen 2 clusters correctly?
- **Ryanne Dolan:** You can look at the lag of the internal consumers to get an idea of how far behind the connectors are from real time. But I agree that a metric like you describe would be useful. Are you interested in proposing a KIP? Can you close this ticket?
- **Bui Thanh MInh:** It seems helpful, I will try, thanks.

## KAFKA-12564: KTable#filter-method called twice after aggregation
Bug · Resolved (Not A Bug) · Major · components: streams · created 2021-03-26 · resolved 2021-03-27

Libraries from build.sbt:
{{"org.apache.kafka" % "kafka_2.13" % "2.7.0",}}
{{"org.apache.kafka" % "kafka-streams" % "2.7.0",}}
{{"org.apache.kafka" % "kafka-clients" % "2.7.0",}}
{{"org.apache.kafka" % "kafka-streams-scala_2.13" % "2.7.0",}}
h4.  
h4. Feed the Stream "issue_stream" with:
{{(1->"A")}}
 {{(1->"B")}}
h4.  
h4. Topology:
{{// #1}}
 {{val issueStream:KStream[Int,String] = builder.stream[Int,String]("issue_stream")}}
{{// #2}}
 {{val aggTable:KTable[Int,String] =}}
 {{i…

- **Matthias J. Sax:** The observed behavior is expected. For `KTable` filter, the predicate needs to be evaluated twice, once for the _previous_ result, and once for the _new_ result. I can go into more technical details if you want to understand the details.
 Why do you think there is a bug? As you mentioned in the tick…
- **Jess J.:** [~mjsax] Thanks for your feedback. Would you mind taking a deeper look at the following?
 If the filter method is called twice per input tuple it leaves me with the following possible output combinations:
 ||filter-method return value for 1st call||filter-method return value for 2nd call||emits||
 |…
- **Matthias J. Sax:** {quote}In the (stateless) filter-method I cannot determine which of the two records is the current and which the previous. Or do I miss something crucial?
 Neither can I find anything in the documentation about the three different possible outcomes described above, nor the need to combine two calls…
- **Jess J.:** [~mjsax] Thanks for your explanation and time. (y)

## KAFKA-12565: Global thread only topologies should be able to shutdown applications via the uncaught exception handler
Improvement · Open · Major · components: streams · created 2021-03-26

Global thread only topologies should be able to shutdown applications via the uncaught exception handler.
Currently because there is no stream thread in this case, there is nothing to participate in a rebalance to communicate the request. If we add a stream thread to do this it will result in an `IllegalStateException` because "Consumer is not subscribed to any topics or assigned any partitions".


## KAFKA-12566: Flaky Test MirrorConnectorsIntegrationSSLTest#testReplication
Test · Resolved (Fixed) · Critical · components: mirrormaker, unit tests · labels: flaky-test · created 2021-03-27 · resolved 2023-02-17

[code/log omitted]
{{LOGs}}
{quote}[2021-03-26 03:28:06,157] ERROR Could not check connector state info. (org.apache.kafka.connect.util.clusters.EmbeddedConnectClusterAssertions:420) org.apache.kafka.connect.runtime.rest.errors.ConnectRestException: Could not read connector state. Error response: \{"error_code":404,"message":"No status found for connector MirrorSourceConnector"} at org.apache.kafka.connect.util.clusters.EmbeddedConnectCluster.connectorStatus(EmbeddedConnectCluster.java:479) at…

- **Matthias J. Sax:** Different method: \{{testReplicationWithEmptyPartition}} failed with timeout
 {quote} {{java.lang.RuntimeException: java.util.concurrent.ExecutionException: org.apache.kafka.common.errors.TimeoutException: The request timed out.
  at org.apache.kafka.connect.mirror.integration.MirrorConnectorsIntegr…
- **Matthias J. Sax:** Another timeout:
 {quote} {{java.lang.RuntimeException: java.util.concurrent.ExecutionException: org.apache.kafka.common.errors.TimeoutException: The request timed out.
 	at org.apache.kafka.connect.mirror.integration.MirrorConnectorsIntegrationSSLTest.startClusters(MirrorConnectorsIntegrationSSLTes…
- **Matthias J. Sax:** [https://github.com/apache/kafka/pull/10495/checks?check_run_id=2291819321]
- **Matthias J. Sax:** [https://github.com/apache/kafka/pull/10301/checks?check_run_id=2284331932]
- **Matthias J. Sax:** [https://github.com/apache/kafka/pull/10506/checks?check_run_id=2327349920]
 [https://github.com/apache/kafka/pull/10506/checks?check_run_id=2327310946] 
 {quote} {{java.lang.RuntimeException: java.util.concurrent.ExecutionException: org.apache.kafka.common.errors.TimeoutException: The request timed…
- _…6 more comments_

## KAFKA-12567: Flaky Test TransactionsTest.testFencingOnCommit
Test · Open · Critical · components: core, unit tests · labels: flaky-test · created 2021-03-27

{quote}org.opentest4j.AssertionFailedError: Consumed 0 records before timeout instead of the expected 2 records at org.junit.jupiter.api.AssertionUtils.fail(AssertionUtils.java:39) at org.junit.jupiter.api.Assertions.fail(Assertions.java:117) at kafka.utils.TestUtils$.pollUntilAtLeastNumRecords(TestUtils.scala:852) at kafka.utils.TestUtils$.consumeRecords(TestUtils.scala:1476) at kafka.api.TransactionsTest.testFencingOnCommit(TransactionsTest.scala:331){quote}
STDOUT (all of those line appear m…


## KAFKA-12637: Remove deprecated PartitionAssignor interface
Improvement · Resolved (Fixed) · Blocker · components: consumer · labels: newbie, newbie++ · created 2021-04-09 · resolved 2021-04-13

In KIP-429, we deprecated the existing PartitionAssignor interface in order to move it out of the internals package and better align the name with other pluggable Consumer interfaces. We added an adapter to convert from existing o.a.k.clients.consumer.internals.PartitionAssignor to the new o.a.k.clients.consumer.ConsumerPartitionAssignor and support the deprecated interface. This was deprecated in 2.4, so we should be ok to remove it and the PartitionAssignorAdaptor in 3.0


## KAFKA-12638: Remove default implementation of ConsumerRebalanceListener#onPartitionsLost
Improvement · Open · Major · components: consumer · created 2021-04-09

When we added the #onPartitionsLost callback to the ConsumerRebalanceListener in KIP-429, we gave it a default implementation that just invoked the existing #onPartitionsRevoked method for backwards compatibility. This is somewhat inconvenient, since we generally want to invoke #onPartitionsLost in order to skip the committing of offsets on revoked partitions, which is exactly what #onPartitionsRevoked does.
I don't think we can just remove it in 3.0 since we haven't indicated that we "deprecat…

- **Ben Chen:** Just curious. For such issue tagged with Majority, who can work on it? Especially there's some time constraints. Also do we have some mechanism to earn credits so that someone with enough "credits" can work on certain things?
- **A. Sophie Blee-Goldman:** Nope, no such things as credits in Kafka -- technically anyone can pick up anything, and the major deciding factor is just your own confidence and familiarity with Kafka. If you're relatively new to Kafka and pick up something large that you need a lot of help with, you might struggle to get it done…
- **A. Sophie Blee-Goldman:** If you're interested in this ticket, we can't do the whole thing because of the compatibility concerns I mentioned but feel free to pick up the first part, and just log a warning if the user has not implemented the #onPartitionsLost callback. Something like this: https://github.com/apache/kafka/blob…
- **Ben Chen:** Really appreciate it!
- **Deng Ziming:** [~ben.c] Feel free to take as many issues as you can as long as you have enough time.

## KAFKA-12639: AbstractCoordinator ignores backoff timeout when joining the consumer group
Bug · Resolved (Fixed) · Major · components: clients, consumer · created 2021-04-09 · resolved 2023-03-01

We observed heavy logging while trying to join consumer group during partial unavailability of Kafka cluster (it's part of our testing process). Seems that {{rebalanceConfig.retryBackoffMs}} used in  {{ org.apache.kafka.clients.consumer.internals.AbstractCoordinator#joinGroupIfNeeded}} is not respected. Debugging revealed that {{Timer}} instance technically is expired thus using sleep of 0 milliseconds which defeats the purpose of backoff timeout.
Minimal backoff timeout should be respected.
[…

- **Ismael Juma:** Is this related to [https://github.com/apache/kafka/commit/f8f57960c69fe677b9192b841fb7a0361ef2cc83] ?
- **Guozhang Wang:** This is a separate issue, as `joinGroupIfNeeded` is not called by the heartbeat thread at all.
 I checked the code in trunk and compared with 2.7, I can confirm the situation still persists there. But this may not be a real issue, just in [~matiss.gutmanis]'s testing environment.
 The key is that in…
- **Philip Nee:** Hey [~matiss.gutmanis] - I'm arriving at the same conclusion as what Guozhang previous mentioned, would you mind sharing/briefly describe your test environment?
 [~guozhang] - should we could exit upon expired timer? maybe something like
 ```
 if (timer.isExpired())
 {   return false; }
 timer.sleep…
- **Guozhang Wang:** Yeah that would work better I think.

## KAFKA-12640: AbstractCoordinator ignores backoff timeout when joining the consumer group
Bug · Resolved (Duplicate) · Major · components: consumer · created 2021-04-09 · resolved 2022-02-24

We observed heavy logging while trying to join consumer group during partial unavailability of Kafka cluster (it's part of our testing process). Seems that {{rebalanceConfig.retryBackoffMs}} used in  {{ org.apache.kafka.clients.consumer.internals.AbstractCoordinator#joinGroupIfNeeded}} is not respected. Debugging revealed that {{Timer}} instance technically is expired thus using sleep of 0 milliseconds which defeats the purpose of backoff timeout.
Minimal backoff timeout should be respected.
[…


## KAFKA-12641: Clear RemoteLogLeaderEpochState entry when it become empty. 
Bug · Open · Major · created 2021-04-09

https://github.com/apache/kafka/pull/10218#discussion_r609895193

- **Konstantine Karantasis:** Feature freeze for AK 3.0 has passed. Pushing to the next AK release
- **David Jacot:** Feature freeze for AK 3.1 has passed. Pushing to the next AK release.
- **Bruno Cadonna:** Removing from the 3.2.0 release since code freeze has passed.
- **hudeqi:** Hi, [~abhijeetkumar] Are you still following this issue? If you don't have time, I can take over. Thanks.

## KAFKA-12642: Improve Rebalance reason upon metadata change
Improvement · Open · Minor · components: core · created 2021-04-09

Whenever the known member metadata does not match anymore the one from a JoinGroupRequest, the GroupCoordinator triggers a rebalance with the following reason  "Updating metadata for member ${member.memberId}"  but  there 2 underlying reasons from that part of the code in MemberMetadata.scala : 
[code/log omitted]
Could we improve the Rebalance Reason with a bit more detail maybe ? 
Thank you

- **Guozhang Wang:** Hi [~nicolas.guyomar] Maybe in the existing log message, we can print the `protocols` and `supportedProtocols` of the member, in the form of <string, number-of-bytes>? If you agree, please feel free to submit a PR.

## KAFKA-12643: Kafka Streams 2.7 with Kafka Broker 2.6.x regression: bad timestamp in transform/process (this.context.schedule function)
Bug · Resolved (Duplicate) · Major · components: streams · created 2021-04-09 · resolved 2021-04-12

During a tranform() or a process() method:
Define a schedule tyask:
this.context.schedule(Duration.ofSeconds(1), PunctuationType.WALL_CLOCK_TIME, timestamp -> \{...}
store.put(...) or context.forward(...) produce a record with an invalid timestamp.
For the forward, a workaround is define the timestamp:
context.forward(entry.key, entry.value.toString(), To.all().withTimestamp(timestamp));
But for state.put(...) or state.delete(...) functions there is no workaround.
Is it mandatory to have…

- **Guozhang Wang:** Hello [~devano], thanks for reporting this issue, could you check if what you observed is similar to this scenario? https://issues.apache.org/jira/browse/KAFKA-12323
- **David EVANO:** Hello, Yes, this seems to be a duplicate of the mentioned issue . Thanks David Evano Le ven. 9 avr. 2021 à 18:21, Guozhang Wang (Jira) <jira@apache.org> a
- **Guozhang Wang:** Thanks for confirming!

## KAFKA-12644: Add Missing Class-Level Javadoc to Descendants of org.apache.kafka.common.errors.ApiException
Improvement · In Progress · Major · components: clients, documentation · labels: documentation · created 2021-04-09

I noticed that class-level Javadocs are missing from some classes in the org.apache.kafka.common.errors package. This issue is for tracking the work of adding the missing class-level javadocs for those Exception classes.
https://kafka.apache.org/27/javadoc/org/apache/kafka/common/errors/package-summary.html
https://github.com/apache/kafka/tree/trunk/clients/src/main/java/org/apache/kafka/common/errors
Basic class-level documentation could be derived by mapping the error conditions documented…

- **Jason Gustafson:** Downgrading priority since this is not a blocker. We can nevertheless aim for 3.0.
- **Konstantine Karantasis:** Given that at this point in time for 3.0 we are focusing exclusively on blocker issues and stabilization fixes (e.g. tests), I'll go ahead and push the target fix version for this issue to 3.0.1 and 3.1.0.
- **David Jacot:** Moving to the next release as we are past the 3.1 release code freeze.
- **Bruno Cadonna:** Removing from the 3.2.0 release since code freeze has passed.

## KAFKA-12645: KIP-731: Record Rate Limiting for Kafka Connect
Improvement · Open · Minor · created 2021-04-09

https://cwiki.apache.org/confluence/display/KAFKA/KIP-731%3A+Record+Rate+Limiting+for+Kafka+Connect


## KAFKA-12646: Implement snapshot generation on brokers
Sub-task · Resolved (Fixed) · Major · components: controller · labels: kip-500 · created 2021-04-09 · resolved 2021-08-03


## KAFKA-12647: Implement loading snapshot in the broker
Sub-task · Resolved (Fixed) · Major · labels: kip-500 · created 2021-04-09 · resolved 2021-08-03


## KAFKA-12759: Kafka consumers with static group membership won't consume from newly subscribed topics
Bug · Open · Minor · components: clients, consumer · created 2021-05-06

We've recently started using static group membership and noticed that when adding a new topic to the subscription, it's not consumed from, regardless of how long the consumer is left to run. A workaround we have is shutting down all consumers in the group for longer than session.timeout.ms, then starting them back up. Is this expected behaviour or a bug?
Sample application:
[code/log omitted]
Steps to reproduce:
 0. update bootstrap server config in example code
 1. run above application, w…

- **David Jacot:** [~apolyakov] Thanks for raising this. It is actually a limitation of the classic rebalance protocol used with static members. The issue is that when a consumer rejoins, the server only sees the subscription as a byte array so it does not really know whether the subscription has changed or not. Doing…
- **Dan O'Reilly:** Thanks for the reply, [~dajac]! Agreed that KIP-848 is the long-term answer, and we're working toward it, but the migration is gradual, and while the classic protocol is still active I think it's worth supporting this case. I'm aware of a few teams where this still bites them in production today.
 O…

## KAFKA-12760: Delete My Account
Wish · Resolved (Invalid) · Minor · created 2021-05-07 · resolved 2021-05-11

I wish to have my account deleted. There doesnt seem to be a way to do it from within my own account, but it should be possible for an admin to do it.
Many thanks.

- **Matthias J. Sax:** [~byusti] – we cannot delete your account either.
 You could try to file a ticket against [https://issues.apache.org/jira/projects/INFRA] – maybe they are able to help with this request.

## KAFKA-12761: Consumer offsets are deleted 7 days after last offset commit instead of EMPTY status
Bug · Open · Major · components: core · created 2021-05-07

If I understand correctly the following [KIP-211|https://cwiki.apache.org/confluence/display/KAFKA/KIP-211%3A+Revise+Expiration+Semantics+of+Consumer+Group+Offsets] consumer offsets should only be cleared based on having an Empty status: 
{{Empty}}: The field {{current_state_timestamp}} is set to when group last transitioned to this state. If the group stays in this for {{offsets.retention.minutes}}, the following offset cleanup scheduled task will remove all offsets in the group (as explained…


## KAFKA-12762: Use connection timeout when polling the network for new connections
Bug · Resolved (Fixed) · Major · created 2021-05-07 · resolved 2021-09-17

In some cases, when connecting to brokers, we end up calling selector.select() with the wrong timeout. Since 2.7, we should use a timeout computed from socket.connection.setup.timeout.ms to ensure we detect bad hosts quickly.
This is especially relevant now that client.dns.lookup defaults to use_all_dns_ips. In case, one of the IPs returned in currently unavailable, we want the client to quickly discover it and avoid timing out user calls.
h4.


## KAFKA-12763: NoSuchElementException during kafka-log-start-offset-checkpoint
Bug · Open · Minor · components: log · created 2021-05-07

The following exception was observed in a cluster running Kafka version 2.6.2.
[code/log omitted]


## KAFKA-12764: Expand Gradle build for Scala 3.0 ?
Wish · Resolved (Duplicate) · Minor · components: build · labels: backlog · created 2021-05-08 · resolved 2025-10-17

[~ijuma] *Question:* do you have a plan to build with Scala 3 at some point ? I can offer some assistance for Gradle build part... Please let me know in a comment.
 *_Details about Scala 3:_*
*Scala 3.0.0-RC3 is released recently:*
 * [https://github.com/lampepfl/dotty/releases/tag/3.0.0-RC3]
 * [https://search.maven.org/artifact/org.scala-lang/scala3-compiler_3.0.0-RC3/3.0.0-RC3/jar]
*According to a Scala team version 3 is backward binary compatible version with Scala 2.13*:
 * [https://w…

- **Ismael Juma:** I think we should wait a while before attempting this. It's too soon to drop support for Scala 2.12 and it's costly to support 3 concurrent Scala versions. I would give it 6 months to allow the ecosystem for 3.0 to stabilize and we can then look into our options (including the possibility of droppin…
- **Dejan Stojadinović:** [~ijuma] makes sense. 
 I will assign this ticket to my self and return to it in a few months.
- **Dejan Stojadinović:** {color:blue}*+Related links/resources+:*{color}
  * _*What's New in Apache Kafka 3.0.0*_ [https://blogs.apache.org/kafka/entry/what-s-new-in-apache6]
  * _*KIP-750: Drop support for Java 8 in Kafka 4.0 (deprecate in 3.0)*_ [https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=181308223]…
- **Dejan Stojadinović:** [~ijuma] Is it safe to say that Scala 3 will have to wait for Kafka 4 ?
 I tried to search for some related *_KIP-_* (but could not find any).
 _{{Edit: I see that there is some progress here:}}_ KAFKA-12954
- **Dejan Stojadinović:** Unassigned my self from this ticket :)
 Rationale: ticket is quite old and on top of that - now it seems unlikely that Kafka will switch to Scala 3.x :D
 I'll also solve this as a duplicate of KAFKA-12954

## KAFKA-12765: NPE using SASL when following JavaSpec
Bug · Open · Minor · components: clients · created 2021-05-08

The Class "SaslChannelBuilder", the method "buildTransportLayer" is defined as follows (2.6.0):
[code/log omitted]
When calling "getInetAddress()", the address is always available, because the Oracle Implementation of the "SocketChannel" class sets quite early the "remoteAddress" internally, even when the "isConnected" would return "false".
Oracle seems to have created a bug, because following the specification of Java class "SocketChannel", the "remoteAddress" should be set internally only a…


## KAFKA-12766: Consider Disabling WAL-related Options in RocksDB
Improvement · Resolved (Fixed) · Minor · components: streams · labels: newbie, newbie++ · created 2021-05-10 · resolved 2021-09-08

Streams disables the write-ahead log (WAL) provided by RocksDB since it replicates the data in changelog topics. Hence, it does not make much sense to set WAL-related configs for RocksDB instances within Streams.
Streams could:
- disable WAL-related options
- ignore WAL-related options
- throw an exception when a WAL-related option is set.

- **Bruno Cadonna:** I think throwing an exception is too harsh. Additionally, I do not understand how we should disable the option since we do not have control over the `Options` object. I think, if we want to do something about it, ignoring is the best solution. But I am also fine with not doing anything, because Stre…
- **A. Sophie Blee-Goldman:** Personally I agree that throwing an exception may be too harsh, it's not my impression that any of the wal-related options are "critical" enough that a user would want or need to be informed if they were going to be ignored. We should definitely log a warning at the least.
 Can you clarify a bit mor…
- **Bruno Cadonna:** I have to admit that I blindly followed your comment here: https://github.com/apache/kafka/pull/10568#discussion_r626058786
 I interpreted "disable" as to not offer methods to read and write this option to users which seems hard to achieve. Now I see, that I misinterpreted.
 I am fine with ignoring.…
- **Konstantine Karantasis:** We are past feature freeze for 3.0 and this issue doesn't seem to be a bug. Postponing to the subsequent release.
- **Tomer Wizman:** Hi Bruno, Sophie, Konstantine, nice e-meeting you :)
 According to the discussion here, the link Bruno attached and from what I saw in the code is that we explicitly disable WAL, so it doesn't really matter in terms of correctness whether we set the underlying Options object inside the adapter class…
- _…2 more comments_

## KAFKA-12767: Properly set Streams system test runtime classpath
Task · Open · Minor · components: streams, system tests · labels: newbie++ · created 2021-05-10

Some of the streams system tests started to fail recently when we stopped exporting our transitive dependencies in the test jar.
[~lct45] was kind enough to submit [https://github.com/apache/kafka/pull/10631] to get the system tests running again, but that PR is only a stop-gap.
The real solution is to properly package the transitive dependencies and make them available to the system test runtime.
Here is the reason: PR#10631 gets past the issue by removing runtime usages on Hamcrest, but Ham…

- **John Roesler:** Marked "affects version" to 3.0.0, since this problem was first introduced in trunk during the 3.0 development cycle. All it means is that we don't want or need to try cherry-picking the fixes to older branches.

## KAFKA-12768: Mirrormaker2 consumer config not using newly assigned client id
Bug · Open · Major · components: mirrormaker · created 2021-05-10

Component: MirrorMaker2 from the 2.6.0 distribution.
We tried to set quotas based client.id in mirrormaker2. We tried the setting source.consumer.client.id and source.client.id properties with no luck.
I was able to update the consumer client id using the US->EUROPE.consumer.client.id config (from the customer) with a single instance of MM2. With a single instance, everything works fine without any issue. However, we are running 2 instances of MirrorMaker 2 with tasks.max set to 2 and it doesn…

- **Dongjin Lee:** I reviewed this problem and found the following:
 The MirrorMaker 1 as a standalone application had been included in the Kafka distribution for a long time ago and MirrorMaker 2 was added with [KIP-382|https://cwiki.apache.org/confluence/display/KAFKA/KIP-382%3A+MirrorMaker+2.0] by [~ryannedolan] in…

## KAFKA-12769: Backport of KAFKA-8562
Task · Resolved (Duplicate) · Major · components: network · created 2021-05-10 · resolved 2021-05-11

Kafka-8562 solved the issue of SASL performing a reverse DNS lookup to resolve the IP.
This bug fix should be backported so it's present on 2.7.x and 2.8.x versions.

- **Josep Prat:** I'll work on this
- **Josep Prat:** Submitted patches to branches 2.7 and 2.8

## KAFKA-12882: Add ActiveBrokerCount and FencedBrokerCount metrics (KIP-748)
Improvement · Resolved (Fixed) · Minor · labels: needs-kip · created 2021-06-02 · resolved 2021-10-25

Adding RegisteredBrokerCount and UnfencedBrokerCount metrics to the QuorumController.

- **Konstantine Karantasis:** The KIP has been published but it's still under discussion. 
 [https://cwiki.apache.org/confluence/display/KAFKA/KIP-748%3A+Add+Broker+Count+Metrics#KIP748:AddBrokerCountMetrics]
 I'm resetting the Fix version since we are past the relevant deadlines. Please make sure to set the appropriate version…
- **David Jacot:** [~rdielhenn] I have split the ticket into two tasks, one for each controller. I will do the ZK one.

## KAFKA-12883: Adress KIP-100 type constraints now that Java 7 support is dropped
Improvement · Open · Minor · components: streams · labels: StarterProject, newbie++ · created 2021-06-03

As part of [KIP-100 rejected alternatives|https://cwiki.apache.org/confluence/display/KAFKA/KIP-100+-+Relax+Type+constraints+in+Kafka+Streams+API#KIP100RelaxTypeconstraintsinKafkaStreamsAPI-RejectedAlternatives], we suggested a more correct alternative to the type constraints for some of the {{KStream}} methods.
Unfortunately at the time, there was a Java 7 compiler behavior that prevented us from using those type constraints, so we had to relax them in order to preserve backwards compatibility…


## KAFKA-12884: Remove "--zookeeper" in system tests
Sub-task · Resolved (Done) · Blocker · created 2021-06-03 · resolved 2021-07-09

Have a quick scan, found currently, we did use "–zookeeper" option for some cases. Need to re-visit them to see if they need to removed.

- **Konstantine Karantasis:** [~showuon] will this make it for 3.0 ? The parent issue targets 3.0. If not I'd like to postpone this fix
- **Luke Chen:** [~kkonstantine], thanks to [~rndgstn] , this is fixed in this PR: [https://github.com/apache/kafka/pull/10918.] So we can close this ticket now.

## KAFKA-12885: Add the --timeout property to kafka-leader-election.sh
Improvement · Open · Minor · components: admin · created 2021-06-03

https://issues.apache.org/jira/browse/KAFKA-9220 mentions kafka-preferred-replica-election.sh script hard-coded timeout problems. I see a similar problem with kafka-leader-election.sh.
I would like to add a --timeout parameter to kafka-leader-election.sh to control the request timeout. To solve similar problems.
||parameter||instructions||
|--timeout <String: timeout ms>|The configuration controls the maximum
 amount of time the client will wait 
 for the response of a request. If 
 the re…

- **loboxu:** [~showuon]  [~jagsancio] Can you help me check it? Is it necessary to do this?

## KAFKA-12886: Enable request forwarding by default
Improvement · Resolved (Won't Fix) · Blocker · created 2021-06-03 · resolved 2024-11-12

KIP-590 documents that request forwarding will be enabled in 3.0 by default: https://cwiki.apache.org/confluence/display/KAFKA/KIP-590%3A+Redirect+Zookeeper+Mutation+Protocols+to+The+Controller. This makes it a requirement for users with custom principal implementations to provide a `KafkaPrincipalSerde` implementation. We waited until 3.0 because we saw this as a compatibility break. 
The KIP documents that use of forwarding will be controlled by the IBP. So once the IBP has been configured to…

- **Konstantine Karantasis:** [~rdielhenn] is this improvement still targeting 3.0? Code freeze is approaching, please consider updating the status or the target version accordingly.
- **Ryan Dielhenn:** [~kkonstantine] targeting 3.1 now
- **David Jacot:** Moved it to 3.2.0.
- **Jose Armando Garcia Sancio:** Discussed this with [~DavidA] . This is not needed for 3.3.0 but it is needed for 3.4.0. Marking it as a blocker for that release.
- **Deng Ziming:** KAFKA-14446 will enable forwarding for migration, but still keep forwarding disabled for non-migration usage.
- _…7 more comments_

## KAFKA-12887: Do not trigger user-customized ExceptionalHandler for RTE
Improvement · Reopened · Major · components: streams · created 2021-06-03

Today in StreamThread we have a try-catch block that captures all {{Throwable e}} and then triggers {{this.streamsUncaughtExceptionHandler.accept(e)}}. However, there are possible RTEs such as IllegalState/IllegalArgument exceptions which are usually caused by bugs, etc. In such cases we should not let users to decide what to do with these exceptions, but should let Streams itself to enforce the decision, e.g. in the IllegalState/IllegalArgument we should fail fast to notify the potential error.

- **Josep Prat:** I'll take a stab at this task.
 If I understand it correctly, we want to skip the user defined handler and directly re-throw those up the chain, right?
- **Josep Prat:** Submitted PR https://github.com/apache/kafka/pull/11228
- **Matthias J. Sax:** This feature broke some stuff, and we revert it: [https://github.com/apache/kafka/pull/12421] 
 Reverted in 3.3.0, 3.2.1.
- **Ismael Juma:** Reopened the Jira since the PR was reverted.
- **Ian Corne:** Why wouldn't you allow the user to handle this?
 This is currently in 3.1.1 which is the version in the latest spring boot 2.7 and it disables handling errors in business logic. IllegalArgumentException is not only used for fatal errors..
- _…2 more comments_

## KAFKA-12888: Add transaction tool
Sub-task · Resolved (Fixed) · Major · created 2021-06-04 · resolved 2021-06-22

Implement the transaction tool described in KIP-664: https://cwiki.apache.org/confluence/display/KAFKA/KIP-664%3A+Provide+tooling+to+detect+and+abort+hanging+transactions.


## KAFKA-12889: log clean group consider empty log segment to avoid empty log left
Bug · Resolved (Fixed) · Trivial · components: log cleaner · created 2021-06-04 · resolved 2021-06-19

to avoid log index 4 byte relative offset overflow, log cleaner group check log segments offset to make sure group offset range not exceed Int.MaxValue.
this offset check currentlly not cosider next is next log segment is empty, so there will left empty log files every about 2^31 messages.
the left empty logs will be reprocessed every clean cycle, which will rewrite it with same empty content, witch cause little no need io.
for __consumer_offsets topic, normally we can set cleanup.policy to c…

- **qiang Liu:** create a pull request on github
- **Guozhang Wang:** Thanks [~iamgd67] for reporting the issue and for the fix too!
- **Luke Chen:** Nice find! Thanks for the fix! [~iamgd67]

## KAFKA-12890: Consumer group stuck in `CompletingRebalance`
Bug · Resolved (Fixed) · Blocker · created 2021-06-04 · resolved 2021-06-17

We have seen recently multiple consumer groups stuck in `CompletingRebalance`. It appears that those group never receives the assignment from the leader of the group and remains stuck in this state forever.
When a group transitions to the `CompletingRebalance` state, the group coordinator sets up `DelayedHeartbeat` for each member of the group. It does so to ensure that the member sends a sync request within the session timeout. If it does not, the group coordinator rebalances the group. Note t…

- **David Jacot:** I will backport the patch to 2.8 branch as well.
- **Yang:** Hi [~dajac]   I know this issue and PR have been closed for a while, just wonder if you have any broker-side log for this issue that you can share. Thanks!

## KAFKA-12891: Add --files and --file-separator options to the ConsoleProducer
New Feature · Open · Minor · components: tools · created 2021-06-04

Introduce *--files* to the producer command line tool to support reading data from a given *multi-file*,
Multiple files are separated by *--files-separator*, the default *comma* is the separator.


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

## KAFKA-12991: Fix unsafe access to `AbstractCoordinator.state`
Bug · Resolved (Fixed) · Major · created 2021-06-24 · resolved 2021-06-24


## KAFKA-12992: Make kraft configuration properties public
Sub-task · Resolved (Fixed) · Blocker · components: core · labels: kip-500 · created 2021-06-24 · resolved 2021-07-06

All of the Kraft configurations should be made public:
[code/log omitted]
https://github.com/apache/kafka/blob/2beaf9a720330615bc5474ec079f8b4b105eff91/core/src/main/scala/kafka/server/KafkaConfig.scala#L1043-L1053

- **David Arthur:** Some additional properties were added as part of KAFKA-12155, I also marked them as public for the 3.0 release. https://github.com/apache/kafka/commit/284ec262c6c84063d90271c965e4cbc1eda111fe#diff-cbe6a8b71b05ed22cf09d97591225b588e9fca6caaf95d3b34a43262cfd23aa6

## KAFKA-12993: Formatting of Streams 'Memory Management' docs is messed up 
Bug · Resolved (Fixed) · Blocker · components: docs, streams · created 2021-06-24 · resolved 2021-07-13

The formatting of this page is all messed up, starting in the RocksDB section. It looks like there's a missing closing tag after the example BoundedMemoryRocksDBConfig class

- **Luke Chen:** on it~
- **ASF GitHub Bot:** showuon opened a new pull request #361: URL: https://github.com/apache/kafka-site/pull/361    1. add missing closing tag
    2. remove a redundant `span` tag --  This is an automated message from the Apache Git Service. To respond to the message, please log on to GitHub and use the URL above to go t…
- **ASF GitHub Bot:** showuon commented on a change in pull request #361: URL: https://github.com/apache/kafka-site/pull/361#discussion_r658532684 ########## File path: 27/streams/developer-guide/memory-mgmt.html ########## @@ -179,7 +179,7 @@ <h2><a class="toc-backref" href="#id3">RocksDB</a><a class="headerlink" href="…
- **ASF GitHub Bot:** showuon commented on pull request #361: URL: https://github.com/apache/kafka-site/pull/361#issuecomment-868286033    @ableegoldman , please take a look. Thanks. --  This is an automated message from the Apache Git Service. To respond to the message, please log on to GitHub and use the URL above to g…
- **ASF GitHub Bot:** cadonna commented on pull request #361: URL: https://github.com/apache/kafka-site/pull/361#issuecomment-868481708    @showuon I think this has been already done in PR #10651. --  This is an automated message from the Apache Git Service. To respond to the message, please log on to GitHub and use the…
- _…13 more comments_

## KAFKA-12994: Migrate all Tests to New API and Remove Suppression for Deprecation Warnings related to KIP-633
Improvement · Resolved (Fixed) · Major · components: streams, unit tests · labels: kip-633, newbie, newbie++ · created 2021-06-25 · resolved 2021-10-21

Due to the API changes for KIP-633 a lot of deprecation warnings have been generated in tests that are using the old deprecated APIs. There are a lot of tests using the deprecated methods. We should absolutely migrate them all to the new APIs and then get rid of all the applicable annotations for suppressing the deprecation warnings.
The applies to all Java and Scala examples and tests using the deprecated APIs in the JoinWindows, SessionWindows, TimeWindows and SlidingWindows classes.
This is…

- **Konstantine Karantasis:** Hi [~iekpo]. You mentioned on the dev mailing list that a PR was in the works for this issue.
 https://lists.apache.org/thread.html/r25f41514ae9751f260b5773abc039dfc828b00154297f20b4a14a151%40%3Cdev.kafka.apache.org%3E
 However, I don't see a link on this issue here yet. 
 We are now past code freez…
- **Konstantine Karantasis:** Downgraded the priority to Major since this is not a blocker. If we get a PR soon we could consider inclusion to 3.0 if the changes don't have any risk.
- **A. Sophie Blee-Goldman:** Hey [~iekpo], I'm unassigning this in case someone else wants to pick it up. If you already started working on this and have a partial PR ready with some subset of the tests migrated over, you can just open that PR and we can merge this in pieces. It seems like a lot of tests so splitting it up into…
- **Andrew patterson:** Hello,
 I'd be happy to take this issue on, although I'm not on the contributor list, would it be possible to get added to it so i can assign this issue to myself?
- **Christo Lolov:** Hello, I believe I managed to get some of the tests changed and am happy to pair on this issue with [~officialandyp] :). I have created a sample pull request for preliminary comments at https://github.com/apache/kafka/pull/11214
- _…8 more comments_

## KAFKA-12995: AdminClient listOffsets fail with old Kafka Broker
Bug · Open · Major · components: clients · created 2021-06-25

The implementation of KAFKA-5291 introduced a check for old Brokers compatibility falling back to _*true*_ in *MetadataRequest allowAutoTopicCreation* field for some operations like *describeTopics*.
Then, after that backward-compatibility changes, more methods were added to *AdminClient* like *listOffsets* [KIP-396|https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=97551484] which unfortunately don't have compatibility with old Brokers into account. One might argue that, given th…

- **Alan Artigao Carreño:** I've created a PR [#10929|https://github.com/apache/kafka/pull/10929] but I can't assign to me the ticket.

## KAFKA-12996: OffsetOutOfRange not handled correctly for diverging epochs when fetch offset less than leader start offset
Bug · Resolved (Fixed) · Major · components: core · created 2021-06-25 · resolved 2021-06-29

{color:#24292e}If fetchOffset < startOffset, we currently throw OffsetOutOfRangeException when attempting to read from the log in the regular case. But for diverging epochs, we return Errors.NONE with the new leader start offset, hwm etc.. ReplicaFetcherThread throws OffsetOutOfRangeException when processing responses with Errors.NONE if the leader's offsets in the response are out of range and this moves the partition to failed state. We should add a check for this case when processing fetch re…


## KAFKA-12997: Expose log record append time to the controller/broker
Sub-task · Resolved (Fixed) · Minor · labels: kip-500 · created 2021-06-25 · resolved 2021-08-03

The snapshot records are generated by each individual quorum participant which also stamps the append time in the records. These appends times are generated from a different clock (except in the case of the quorum leader) as compared to the metadata log records (where timestamps are stamped by the leader).
To enable having a single clock to compare timestamps, https://issues.apache.org/jira/browse/KAFKA-12952 adds a timestamp field to the snapshot header which should contain the append time of…


## KAFKA-12998: Implement broker snapshots
Improvement · Open · Major · created 2021-06-26

Implement broker snapshots


## KAFKA-12999: NPE when accessing RecordHeader.key() concurrently
Bug · Resolved (Fixed) · Minor · components: clients · created 2021-06-27 · resolved 2025-11-02

h2. Summary
After upgrading clients to {{2.8.0}}, reading {{ConsumerRecord}}'s header keys started resulting in occasional {{java.lang.NullPointerException}} in case of concurrent access from multiple(2) threads.
h2. Where
NPE happens here [RecordHeader.java:45|https://github.com/apache/kafka/blob/2.8.0/clients/src/main/java/org/apache/kafka/common/header/internals/RecordHeader.java#L45]:
[code/log omitted]
h2. When/why
Cause of issue is introduced by changes of KAFKA-10438 to avoid unnece…

- **Ismael Juma:** Thanks for the ticket. This class was never meant to be thread safe, the value was initialized lazily previously and it just so happened the key was not. Since the consumer is single threaded, this was deemed ok.
 For now, the easiest path is for you to copy the data you care about to your own threa…
- **Ismael Juma:** cc [~chia7712]
- **Antonio Tomac:** {quote}but it would require a KIP and it would probably only be done in a feature release.{quote}
 [~ijuma] What do you suggest for me to do? Should I then write a KIP? Cancel my [PR|https://github.com/apache/kafka/pull/10933]?
 {quote}For now, the easiest path is for you to copy the data you care a…
- **Ismael Juma:** A KIP seems reasonable. The class could be made thread safe at low cost by using a volatile field and synchronization during initialization only.
- **Chia-Ping Tsai:** Thanks for this ticket. As juma explained, the class is not designed for thread-safe. As modern Java make optimization for single thread in sync block, adding sync to make it thread-safe seems to be fine to me. Of course, it needs KIP :)
- _…1 more comments_

## KAFKA-13000: Improve handling of UnsupportedVersionException in MockClient
Improvement · Resolved (Fixed) · Major · created 2021-06-28 · resolved 2021-07-07

MockClient handles UnsupportedVersionException slightly differently than NetworkClient. In some cases, it may throw this exception while instead it should return always return a ClientResponse.
Background: https://github.com/apache/kafka/pull/10743#discussion_r655922760

- **Kirk True:** [~mimaison] - is this ticket still valid? Looking at the code in {{trunk}}, I don't see anywhere in {{MockClient}} where an {{UnsupportedVersionException}} is thrown. I've done some related work in [KAFKA-12989|https://issues.apache.org/jira/browse/KAFKA-12989], so I'm hoping to work on this too, if…
- **Mickael Maison:** [~kirktrue] Sorry it looks like this has already been addressed. Marking as resolved

## KAFKA-13001: UnitTest Failing in Kafka master branch
Bug · Open · Major · components: unit tests · created 2021-06-28

Hi Team, 
The .{color:#FF0000}/gradlew unitTest{color} command is failing in the Kafka 2.7 branch and master branch. The unit test is failing at core:unitTest.  Attached are the test results for the build.


## KAFKA-13089: Revisit the usage of BufferSuppliers in Kraft
Sub-task · Open · Major · components: kraft · labels: kip-500 · created 2021-07-14

The latest KafkaRaftClient creates a new BufferSupplier every time it is needed. A buffer supplier is needed when reading from the log and when reading from a snapshot.
It would be good to investigate if there is a performance and memory usage advantage of sharing the buffer supplier between those use cases and every time the log or snapshot are read.
If BufferSupplier is share, it is very likely that the implementation will have to be thread-safe because we need support multiple Listeners and…

- **Ismael Juma:** The BufferSupplier implementations we have are not thread-safe and work best in a thread-confined way. Can each listener hold a thread confined buffer supplier?
- **Jose Armando Garcia Sancio:** {quote}Can each listener hold a thread confined buffer supplier?
 {quote}
 Yeah. That is one possible solution to this problem. Have the {{RaftClient.Listener}} provide a {{BufferSupplier}} during registration.

## KAFKA-13090: Improve cluster snapshot integration test
Sub-task · Resolved (Fixed) · Major · labels: kip-500 · created 2021-07-14 · resolved 2021-07-19

Extends the test in RaftClusterSnapshotTest to verify that both the controllers and brokers are generating snapshots.

- **Konstantine Karantasis:** Resolving given that the PR got merged and cherry-picked to 3.0: 
 https://github.com/apache/kafka/pull/11054

## KAFKA-13091: Increment HW after shrinking ISR through AlterIsr
Bug · Resolved (Fixed) · Major · created 2021-07-15 · resolved 2021-08-23

After we have shrunk the ISR, we have an opportunity to advance the high watermark. We do this currently in `maybeShrinkIsr` after the synchronous update through ZK. For the AlterIsr path, however, we cannot rely on this call since the request is sent asynchronously. Instead we should attempt to advance the high watermark in the callback when the AlterIsr response returns successfully.


## KAFKA-13092: Perf regression in LISR requests
Bug · Resolved (Fixed) · Critical · created 2021-07-15 · resolved 2021-07-15

With the addition of partition metadata files, we have an extra operation to do when handling LISR requests. This really slows down the processing, so we should flush asynchronously to fix this regression.

- **Jun Rao:** merged the PR to 3.0 and trunk.

## KAFKA-13093: Log compaction should write new segments with record version v2 (KIP-724)
Sub-task · Resolved (Fixed) · Major · created 2021-07-15 · resolved 2025-01-09

If IBP is 3.0 or higher. Currently, log compaction retains the record format of the record batch that was retained.

- **Bruno Cadonna:** Removing from the 3.2.0 release since code freeze has passed.

## KAFKA-13094: Session windows do not consider user-specified grace when computing retention time for changelog
Bug · Open · Major · components: streams · created 2021-07-15

Session windows use internally method {{maintainMs()}} to compute the retention time for their changelog topic if users do not provide a retention time explicitly with {{Materilaized}}. However, {{maintainMs()}} does not consider user-specified grace period when computing the retention time.
The bug can be verified with the following test method:
[code/log omitted]   
The test should pass since the retention time of the changelog topic should be gap + grace. However, the test fails.


## KAFKA-13095: TransactionsTest is failing in kraft mode
Bug · Resolved (Cannot Reproduce) · Blocker · created 2021-07-15 · resolved 2021-08-02

TransactionsTest#testSendOffsetsToTransactionTimeout keeps flaking on Jenkins.

- **Jason Gustafson:** I am closing this since `TransactionsTest` has not yet been converted to KRaft. There was some instability introduced when the topicId fetch changes were introduced, so I think this caused some confusion.

## KAFKA-13096: QueryableStoreProvider is not updated when threads are added/removed/replaced rendering IQ impossible
Bug · Resolved (Fixed) · Blocker · components: streams · created 2021-07-16 · resolved 2021-07-21

The QueryableStoreProviders class is used to route queries to the correct state store on the owning StreamThread, making it a critical piece of IQ. It gets instantiated when you create a new KafkaStreams, and is passed in a list of StreamThreadStateStoreProviders which it then copies and stores. Because it only stores a copy it only ever contains a provider for the StreamThreads that were created during the app's startup, and unfortunately is never updated during an add/remove/replace thread eve…


## KAFKA-13097: Handle the requests gracefully to publish the events in TopicBasedRemoteLogMetadataManager when it is not yet initialized.
Sub-task · Resolved (Invalid) · Major · created 2021-07-16 · resolved 2023-08-31


## KAFKA-13098: No such file exception when recovering snapshots in metadata log dir
Bug · Resolved (Fixed) · Blocker · labels: kip-500 · created 2021-07-16 · resolved 2021-07-17

[code/log omitted]


## KAFKA-13099: Message too large error when expiring transactionalIds
Bug · Resolved (Fixed) · Major · created 2021-07-16 · resolved 2021-07-28

We have seen a couple reports of MESSAGE_TOO_LARGE errors when writing tombstones for expired transactionalIds. This is possible because we collect all expired IDs into a single batch. We should ensure that the created batches are smaller than the max message size. Any expired IDs that cannot fit can be expired later.


## KAFKA-13106: Offsets deletion error
Bug · Resolved (Fixed) · Major · components: admin · created 2021-07-20 · resolved 2021-07-20

When I use:
kafka-consumer-groups.sh --bootstrap-server broker:9092 --delete-offsets --group myGroup --topic myTopic
I have a error:
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/kafka/libs/slf4j-log4j12-1.7.26.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/kafka/libs/slf4j-log4j12-1.7.30.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See [http://www.slf4j.org/codes.html#multiple_bindings] for an explanation.…

- **Robert Janda:** version 2.3.1 does not suport it

## KAFKA-13107: KafkaServer.startup leaves server socket open if zk error is throws (ex. NodeExists)
Bug · Open · Major · created 2021-07-20

kafka.network.Acceptor#serverChannel is not closed if KafkaServer.startup is failed with zk error.
Because the single point where serverChannel.close() is kafka/network/SocketServer.scala:640 but it requires Acceptor to be scheduled.
It is regression: in 2.5 server channel was closed as expected.
Reproduced in 2.8

- **Nikolay Izhikov:** Hello, [~Fuud] 
 Do you have logs? stack trace for described issue?
 Can you attach them to the ticket.

## KAFKA-13108: Improve the test coverage for ConfigCommandTest
Test · Patch Available · Major · components: tools · created 2021-07-20

Follow up for the PR comment: https://github.com/apache/kafka/pull/10811#pullrequestreview-709981356


## KAFKA-13109: WorkerSourceTask is not enforcing the errors.retry.timeout and errors.retry.delay.max.ms parameters in case of a RetriableException during task.poll()
Bug · Open · Major · components: connect · created 2021-07-20

It seems that the {{errors.retry.timeout}} timeout is not enforced if {{RetriableException}} is thrown in the {{poll()}} of a SourceTask.
Looking at Kafka Connect source code:
 * If a task throws a {{RetriableException}} during a {{poll()}}, the connect runtime catch it and returns null: [https://github.com/apache/kafka/blob/2.8.0/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSourceTask.java#L273-L277]
 * Then, {{toSend}} is set to null, and the runtime continues the lo…


## KAFKA-13110: Review and Optimize KIP-500 related Settings
Improvement · Open · Minor · components: kraft · created 2021-07-20

Some configurations/settings for Kraft have been inherited from the ZK era and have not necessarily been thought about again.
This JIRA tracks reviewing configuration settings related to KIP-500 and optimizing them where possible.
An example of settings that need an overhaul:
val BrokerHeartbeatIntervalMs = 2000
val BrokerSessionTimeoutMs = 9000
A 2 second heartbeat interval and consequently a 9 second session timeout are pretty high values and can be optimized to shorter durations.


## KAFKA-13111: Re-evaluate Fetch Sessions when using topic IDs
Improvement · Resolved (Fixed) · Blocker · created 2021-07-20 · resolved 2021-11-15

For fetch request version 13 we have the current method of handling unknown topic IDs.
 * When the receiving broker sees an unknown topic ID in a request or encounters an inconsistent (mismatched) ID in the logs, it sends a top-level error back, delays *all* partitions (in fetcher thread), and closes the session
Ideally, we want to handle the same way as unknown topic names. We hold the topic partition in the session and try to resolve on a future fetch request. 
However, there are a few comp…

- **Jason Gustafson:** Thanks, this makes sense to me. At a high level, we want to keep the protocol simple even if it costs a little more complexity in the implementation. I think it is indeed simpler if topic IDs are handled similarly to topic names. When a topic ID is unknown, we nevertheless store it in the session an…

## KAFKA-13112: Controller's committed offset get out of sync with raft client listener context
Bug · Resolved (Fixed) · Blocker · components: controller, kraft · labels: kip-500 · created 2021-07-21 · resolved 2021-08-02

The active controller creates an in-memory snapshot for every offset returned by RaftClient::scheduleAppend and RaftClient::scheduleAtomicAppend. For RaftClient::scheduleAppend, the RaftClient is free to split those records into multiple batches. Because of this when scheduleAppend is use there is no guarantee that the active leader will always have an in-memory snapshot for every "last committed offset".
To get around this problem, when the active controller renounces from leader if there is n…

- **Konstantine Karantasis:** [~jagsancio] the two subtasks of this issue have been resolved. Does this make this blocker issue resolved as well?
- **Jose Armando Garcia Sancio:** Yes.

## KAFKA-13113: Add unregister support to the RaftClient.
Sub-task · Resolved (Fixed) · Blocker · components: kraft · labels: kip-500 · created 2021-07-21 · resolved 2021-07-24

Implement the following API:
[code/log omitted]


## KAFKA-13114: Unregsiter listener during renounce when the in-memory snapshot is missing
Sub-task · Resolved (Fixed) · Blocker · components: controller · labels: kip-500 · created 2021-07-21 · resolved 2021-08-01

Need to improve the renounce logic to do the following when the last committer offset in-memory snapshot is missing:
 # Reset the snapshot registry
 # Unregister the listener from the RaftClient
 # Register the listener from the RaftClient


## KAFKA-13115: Document that doSend can be blocking
Task · Resolved (Fixed) · Minor · components: docs · labels: documentation, pull-request-available · created 2021-07-21 · resolved 2024-05-14

https://github.com/apache/kafka/pull/11023


## KAFKA-13116: KIP-724: Adjust system tests due to KAFKA-12944
Sub-task · Resolved (Fixed) · Blocker · created 2021-07-21 · resolved 2021-07-23

Several system tests involving legacy message formats are failing due to KAFKA-12944:
http://confluent-kafka-system-test-results.s3-us-west-2.amazonaws.com/2021-07-21--001.system-test-kafka-trunk--1626872410--confluentinc--master–038bdaa4df/report.html
All system tests that write data with legacy message formats need to use IBP 2.8 or lower.


## KAFKA-13184: KafkaProducerException
Bug · Open · Major · components: config · created 2021-08-10

we are receiving timeout error. please help me on this issue
Producer configuation
acks = all
 batch.size = 16384
 bootstrap.servers = [127.0.0.1:9091]
 buffer.memory = 33554432
 client.dns.lookup = default
 client.id =
 compression.type = snappy
 connections.max.idle.ms = 540000
 delivery.timeout.ms = 120000
 enable.idempotence = true
 interceptor.classes = []
 key.serializer = class org.apache.kafka.common.serialization.StringSerializer
 linger.ms = 5
 max.block.ms = 60000
 max…


## KAFKA-13185: Kafka Connect should clear messageBatch after rewind
Bug · Patch Available · Critical · components: connect · created 2021-08-10

WorkerSinkTask contains logic to handle RetriableException that happened in either put or flush. If the same Exception happens for longer than poll or timeout interval and it's thrown as well in preCommit/flush it causes offset to rewind back to the last committed position. Meanwhile messageBatch (message buffer) is not cleared and during the next poll it's used passed to the put method. 
During the next poll the same message is read from the broker and again passed to the put method. 
This re…

- **Yunseop Eom:** PR opened: https://github.com/apache/kafka/pull/23048 for KAFKA-13185. Fixed the Kafka Connect sink-task recovery path so a failed preCommit rewind clears both the pending messageBatch and its associated origOffsets before the next poll, preventing stale records and rewound offsets from being delive…
- **Yunseop Eom:** PR #23048 is open and ready for maintainer review: https://github.com/apache/kafka/pull/23048

## KAFKA-13186: Proposal for commented code
Wish · Open · Trivial · created 2021-08-10

Hello! I saw in your [coding guidelines|https://kafka.apache.org/coding-guide.html] that ??Don't check in commented out code. ??
However, I still witness commented code in some files like:
* connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ConnectorConfigTest.java
* streams/src/test/java/org/apache/kafka/streams/state/internals/TimeOrderedKeyValueBufferTest.java
* clients/src/main/java/org/apache/kafka/clients/consumer/internals/AbstractStickyAssignor.java
Would you like to re…


## KAFKA-13187: Replace EasyMock and PowerMock with Mockito for DistributedHerderTest
Sub-task · Resolved (Done) · Major · created 2021-08-10 · resolved 2023-08-10

- **Jeff Evans:** I'll take a crack at this one.
- **Jeff Evans:** Would be great to get a sanity check here, before proceeding with more work on this test:  https://github.com/apache/kafka/pull/11792

## KAFKA-13188: Release the memory back into MemoryPool
Improvement · Patch Available · Major · created 2021-08-10

Tushar made a [hotfix change|https://github.com/linkedin/kafka/pull/186] to the linkedin/kafka repo hosting apache kafka 2.4.
The change is about releasing memory back to the MemoryPool for the kafka consumer, and his benchmark showed significant improvement in terms of the memory graduating from Young Gen and promoted to Old Gen.
Given the benefit, the change should also be added trunk.

- **Alok Nikhil:** [~luwang] I see that the consumer side memory pool management KIP was never implemented - [https://cwiki.apache.org/confluence/display/KAFKA/KIP-81:+Bound+Fetch+memory+usage+in+the+consumer]
 The default is `MemoryPool.NONE`. How did LinkedIn measure the performance here? Is there a customization /…
- **Tushar Goyal:** [~aloknnikhil] I am the original author for the code change. We measured the performance by adding some custom code to measure the performance in KafkaConsumer. The customization is a follow up PR which was recently merged here [https://github.com/linkedin/kafka/pull/196]
 I can send out a forward p…

## KAFKA-13189: Revisit the CreateTopic API behavior when number of Unfenced Brokers available for placement is less than min_isr
Task · Resolved (Fixed) · Critical · components: controller, kraft · created 2021-08-11 · resolved 2021-08-11

Today when a CreateTopic call is made while the number of brokers available to create the topic is non-zero, the creation of the topic succeeds (under certain conditions). The behavior remains the same even if the min_isr and replication factor for the topic are greater than 1. This would lead to the create succeeding, however a subsequent on the topic immediately failing. This behavior might not be the most intuitive or expected by some users.
This Jira is cut to ensure that this behavior is r…


## KAFKA-13190: Revisit the CreateTopic API behavior when number of Unfenced Brokers available for placement is less than min_isr
Task · Open · Critical · components: controller, kraft · created 2021-08-11

Today when a CreateTopic call is made while the number of brokers available to create the topic is non-zero, the creation of the topic succeeds (under certain conditions). The behavior remains the same even if the min_isr and replication factor for the topic are greater than 1. This would lead to the create succeeding, however a subsequent on the topic immediately failing. This behavior might not be the most intuitive or expected by some users.
This Jira is cut to ensure that this behavior is r…


## KAFKA-13191: Kafka 2.8 - simultaneous restarts of Kafka and zookeeper result in broken cluster
Bug · Open · Major · components: protocol · created 2021-08-11

We're using confluent platform 6.2, running in a Kubernetes environment. The cluster has been running for a couple of years with zero issues, starting from version 1.1, 2.5 and now 2.8. 
We've very recently upgraded to kafka 2.8 from kafka 2.5. 
Since upgrading, we have seen issues when kafka and zookeeper pods restart concurrently. 
We can replicate the issue by restarting either the zookeeper statefulset first or the kafka statefulset first, either way appears to result with the same failur…

- **CS User:** I have been able to replicate this issue using the confluent 6.2 images, please see:
 [https://github.com/csghuser/kafka-fault-test]
 This appears to happen when the Zookeeper leader is shutdown uncleanly. The only changes to the official images are:
  # Add secrets file to the image
  # Modify Zook…
- **Chris Borckholder:** We are seeing similar issues after upgrading to version 2.8.0 (similarly the cluster ran reliably for > 1 year in the current setup with former 2.x versions).
 We are hosting kafka in EC2 (6 broker, 3 zookeeper). In a test environment, we are performing ec2 terminations of broker/zookeeper instances…
- **Loïc Monney:** We were able to reproduce similar scenario in a test environment with 2.8.0, leading also to an inconsistent cluster state, but we were not able to reproduce the issue with 2.6.1.
 Would propose as well to increase the severity of this ticket.
 [~mumrah], [~cmccabe], [~hachikuji] is this something c…
- **Edoardo Comar:** We were also able to reproduce this with 3.0.0 - and corresponding zookeeper 3.6.3
 The easiest way to reproduce for us (in Kubernetes) is :
 Initiate a kafka rollout, and while that is running, delete the zookeeper pod that is the current zookeeper leader.
 it may take a different number of attempt…
- **Edoardo Comar:** [~acldstkusr] can you take a look at https://issues.apache.org/jira/browse/KAFKA-13407 ?
 It might be symptoms of the same underlying issue.
 Would you be able to try reproduce this issue with the fix we propose in https://issues.apache.org/jira/browse/KAFKA-13407 ?
- _…1 more comments_

## KAFKA-13192: broker.id and node.id can be specified inconsistently
Bug · Resolved (Won't Fix) · Major · created 2021-08-11 · resolved 2025-05-13

If both broker.id and node.id are set, and they are set inconsistently (e.g.broker.id=0, node.id=1) then the value of node.id is used and the broker.id value is left at the original value.  The server should detect this inconsistency, throw a ConfigException, and fail to start.

- **Chia-Ping Tsai:** see KAFKA-13224

## KAFKA-13193: Replica manager doesn't update partition state when transitioning from leader to follower with unknown leader
Bug · Resolved (Fixed) · Major · components: kraft, replication · labels: kip-500 · created 2021-08-11 · resolved 2022-02-04

This issue applies to both the ZK and KRaft implementation of the replica manager. In the rare case when a replica transition from leader to follower with no leader the partition state is not updated.
This is because when handling makeFollowers the ReplicaManager only updates the partition state if the leader is alive. The solution is to always transition to follower but not start the fetcher thread if the leader is unknown or not alive.


## KAFKA-13194: LogCleaner may clean past highwatermark
Bug · Resolved (Fixed) · Minor · created 2021-08-11 · resolved 2021-08-13

Here we have the cleaning point being bounded to the active segment base offset and the first unstable offset. Which makes sense:
[code/log omitted]
But LSO starts out as None.
[code/log omitted]
For most code depending on the LSO, fetchLastStableOffsetMetadata is used to default it to the hwm if it's not set.
[code/log omitted]
This means that in the case where the hwm is prior to the active segment base, the log cleaner may clean past the hwm. This is most likely to occur after a broker…

- **Justine Olshan:** There was code to change this in [https://github.com/apache/kafka/pull/9590,] but if we want to fix faster, we should just make a new PR. 
 Replacing
  // we do not clean beyond the first unstable offset
  log.firstUnstableOffset,
 with
  // we do not clean beyond the lastStableOffset (and therefore…
- **Jun Rao:** Merged the PR to trunk.

## KAFKA-13264: backwardFetch in InMemoryWindowStore doesn't return in reverse order
Bug · Resolved (Fixed) · Major · components: streams · created 2021-09-02 · resolved 2021-09-13

When working on another PR, I found currently, the backwardFetch in InMemoryWindowStore doesn't return in reverse order when there are records in the same window.
ex: window size = 500,
input records:
key: "a", value: "aa", timestamp: 0 ==> will be in [0, 500] window
key: "b", value: "bb", timestamp: 10 ==> will be in [0, 500] window
So, internally, the "a" and "b" will be in the same segment.
when fetch in forward order:
"a" -> "b", which is expected
when fetch in backward order:
"a" -…


## KAFKA-13265: Kafka consumers disappearing after certain point of time 
Test · Open · Blocker · components: consumer · created 2021-09-02

Dear Kafka Team,
We are facing one issue for past few days in our development environment. We have topic called 'search-service-topic-dev' and consumer group 'search-service-group' with 10 partitions, and concurrency also 10 at  consumer side. 
When we publish more messages( each message is 115kb) into the topic after some certain point of the time consumers disappeared from the consumer group (note : consumer service are running). Have attached screenshot for reference (filename : Consumer_Di…

- **Ayyandurai Mani:** We are blocked with this behavior, expecting some action from the experts.
- **tangzhongham:** it seems that the problem came from the consumer side, you might need to check the client code and do some threaddump to see consumer's behavior

## KAFKA-13266: `InitialFetchState` should be created after partition is removed from the fetchers
Bug · Resolved (Fixed) · Blocker · created 2021-09-02 · resolved 2021-09-08

`ReplicationTest.test_replication_with_broker_failure` in KRaft mode sometimes fails with the following error in the log:
[code/log omitted]
 The issue is due to a race condition in `ReplicaManager#applyLocalFollowersDelta`. The `InitialFetchState` is created and populated before the partition is removed from the fetcher threads. This means that the fetch offset of the `InitialFetchState` could be outdated when the fetcher threads are re-started because the fetcher threads could have increment…


## KAFKA-13267: InvalidPidMappingException: The producer attempted to use a producer id which is not currently assigned to its transactional id
Bug · Open · Major · components: streams · created 2021-09-02

We're using Confluent Cloud and Kafka Streams 2.8.0 and we've seen these errors pop up in apps using EOS:
[code/log omitted]
Full stack trace:
[code/log omitted]
I've seen that KAFKA-6821 described the same problem on an earlier version of Kafka and was closed due to the subsequent works on EOS.
Another ticket raised recently shows that the exception is still occurring (but the ticket wasn't raised for that specific error): KAFKA-12774

- **Matthias J. Sax:** [~guozhang] [~hachikuji] – Given the error message, this might actually be a broker or producer bug, rather than a Stream issue?
- **Matthias J. Sax:** According to [KIP-691|https://cwiki.apache.org/confluence/display/KAFKA/KIP-691%3A+Enhance+Transactional+Producer+Exception+Handling], {{InvalidPidMappingException}} should actually be considered non-fatal, and we might want to try to handle it within Kafka Streams.
- **Guozhang Wang:** I agree, and as you mentioned in the other PR it seems more related to https://issues.apache.org/jira/browse/KAFKA-10733 (KIP-691)

## KAFKA-13268: Add more integration tests for Table Table FK joins with repartitioning
Improvement · Resolved (Duplicate) · Major · components: streams, unit tests · created 2021-09-02 · resolved 2021-10-08

We should add to the FK join multipartition integration test with a Repartitioned for:
1) just the new partition count
2) a custom partitioner
This is to test if there's a bug where the internal topics don't pick up a partitioner provided that way.

- **A. Sophie Blee-Goldman:** What's the name of that testing framework where you just define the parameter space and then it runs all the permutations of those? We should start using that in Streams, especially for new operators and configurations since we've been bitten a few times by a specific topology we don't have test cov…
- **Guozhang Wang:** I just did that in a recent PR: https://github.com/apache/kafka/pull/11252/files#diff-1060876874aba52f23e63e730ca6d26aac41e9be5f43fde4e5dcfaad5f76f927R65
 I do not have a concrete framework in mind for how to extend that for new operators / configuration permutations though, do you have something in…
- **Victoria Xia:** Hey [~guozhang] we've already got KTableKTableForeignKeyInnerJoinMultiIntegrationTest.java for testing foreign key joins with differing number of partitions on the source tables, and [https://github.com/apache/kafka/pull/11368] is adding coverage for source tables with custom partitioners. Is this t…
- **Guozhang Wang:** Yup, I think KAFKA-13261 would be fully covering it. I'm going to close this one.

## KAFKA-13269: Kafka Streams Aggregation data loss between instance restarts and rebalances
Bug · Open · Major · components: streams · created 2021-09-03

Using Kafka Streams 2.6.2 and doing count based aggregation of messages. Also setting Processing Guarantee - EXACTLY_ONCE_BETA and NUM_STANDBY_REPLICAS_CONFIG = 1. Sending some messages and restarting instances in middle while processing to test fault tolerance. The output count is incorrect because of data loss while restoring state.
It looks like the streams task becomes active and starts processing even when the state is not fully restored but is within the acceptable recovery lag (default i…

- **A. Sophie Blee-Goldman:** Hey [~rohitbobade], thanks for the report. Unfortunately I don't think the acceptable recovery lag is directly responsible, as that config is only used within the assignor to figure out the placement of tasks. Assigning a task as "Active" just means that the instance should try to process it, the ta…
- **Rohit Bobade:** Thanks [~ableegoldman], will check this and also debug further. Just to add details - I noticed the same behavior (data loss between instance restarts and rebalances) even without EOS
