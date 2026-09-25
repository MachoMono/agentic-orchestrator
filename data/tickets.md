# KAFKA ticket digest (1012 issues)

Trimmed for reading: descriptions ≤500 chars, first 5 comments ≤300 chars each, code blocks and stack traces removed. Full data: `data/raw/kafka_issues.jsonl`.

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

- **kaushik srinivas:** [~ijuma] Need your inputs.
- **kaushik srinivas:** [~ijuma] This is an issue with lot of impacts. Can you provide some suggestions.
- **Ismael Juma:** cc [~kkonstantine] [~rhauch]
- **Konstantine Karantasis:** Thanks for reporting [~kaushik srinivas]  First, I need to note that this issue seems to belong in its entirety to: [https://github.com/confluentinc/kafka-connect-hdfs/issues]  given that the behavior is not affected by the guarantees that the Kafka Connect framework provides.  Briefly, let me s…
- **kaushik srinivas:** Hi [~kkonstantine] We have created the ticket even on the hdfs sink connector side as well. Below is the ticket  [https://github.com/confluentinc/kafka-connect-hdfs/issues/538] We have also captured more detailed analysis over there. But there are no responses in that forum as well. -Kaushik
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

- **Ketul Gupta:** Hi [~lct45], I would like to work on this. I am going through [KIP-450|https://cwiki.apache.org/confluence/display/KAFKA/KIP-450%3A+Sliding+Window+Aggregations+in+the+DSL] , and would later look into implementation in java for doing it in scala. Would you guide me in this by giving some pointers…
- **Leah Thomas:** Hi [~ketulgupta], thanks for picking this up! It should be a relatively easy fix. If you look at [KGroupedStream.scala|https://github.com/apache/kafka/blob/trunk/streams/streams-scala/src/main/scala/org/apache/kafka/streams/scala/kstream/KGroupedStream.scala#L155] you can see that there's a `windowe…
- **Matthias J. Sax:** Sound about right – in the Java code, `windowedBy(SlidingWindows)` returns a `TimeWindowedKStream` and thus the Scala code should do a similar thing.
- **Ketul Gupta:** Hi [~lct45]  [~mjsax] , I have made the method additions in KGroupedStream and Cogrouped stream as windowedBy(SlidingWindows) method was there in both the classes, also added test in KtableTests. Please review the changes.

## KAFKA-12345: KIP-500: AlterIsrManager crashes on broker idle-state
Task · Resolved (Fixed) · Minor · components: core · labels: kip-500 · created 2021-02-19 · resolved 2021-04-17

Occasionally, a scheduler thread on a broker crashes with this stack
[code/log omitted]
After that the broker is unable to fetch any records from any other broker (and vice versa)
[code/log omitted]

- **Alok Nikhil:** Adding a bit more context. Seems like there was a controller quorum voting event just before this crash. Seems to be related [code/log omitted]
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
- **Chris Egerton:** Ah, thanks [~ableegoldman], I'd misread the javadocs for the cooperative sticky assignor. Updated the description to point to 2.4 instead of 2.3. RE clearness on the upgrade section in KIP-429–I didn't see a specific section for Connect, and both of the sections that were there ("Consumer" and "Str…
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
- **Luke Chen:** Another improvement is implemented (check https://github.com/apache/kafka/pull/10509#issuecomment-822975764) After the change: the {{testLargeAssignmentAndGroupWithUniformSubscription}} (1 million partitions) will run from *~2600 ms*  *down to ~1400 ms*, improves *46%* of performance, almost *2x f…

## KAFKA-12465: Decide whether inconsistent cluster id error are fatal
Sub-task · Open · Major · created 2021-03-15

Currently, we just log an error when an inconsistent cluster-id occurred. We should set a window during startup when these errors are fatal but after that window, we no longer treat them to be fatal. see https://github.com/apache/kafka/pull/10289#discussion_r592853088

- **Jose Armando Garcia Sancio:** One solution is to implement it when handling a response, invalid cluster id are fatal unless a previous response contained a valid cluster id.
- **Omnia Ibrahim:** I have been testing KRAFT and I tried this scenario where I setup a cluster with 3 combined nodes (broker, controller) and 3 nodes as brokers then later at some point I add an extra 2 nodes to the KRAFT with different cluster id. I would expect if this is a really deployment on production then these…
- **Deng Ziming:** [~omnia_h_ibrahim] Thank you for the feedback, we are now trying to design an algorithm to decide when to treat `INCONSISTENT_CLUSTER_ID`, some discussions are listed here: [https://github.com/apache/kafka/pull/10289#discussion_r592853088] I think [~jagsancio]'s suggestion is a good one, WDYT?

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
- **Angelos Kaltsikis:** Just one clarification:  The number of *LEADER* partitions / The number of tasks <= 10 Correct? [~askldjd]

## KAFKA-12559: Add a top-level Streams config for bounding off-heap memory
Improvement · Open · Major · components: streams · labels: needs-kip, newbie, newbie++ · created 2021-03-25

At the moment we provide an example of how to bound the memory usage of rocskdb in the [Memory Management|https://kafka.apache.org/27/documentation/streams/developer-guide/memory-mgmt.html#rocksdb] section of the docs. This requires implementing a custom RocksDBConfigSetter class and setting a number of rocksdb options for relatively advanced concepts and configurations. It seems a fair number of users either fail to find this or consider it to be for more advanced use cases/users. But RocksDB c…

- **A. Sophie Blee-Goldman:** We can also consider whether to apply this bounded memory configuration by default. Picking a reasonable default value is rather challenging: if we make it something very low like 1GB then this could cause a drastic perf hit for users upgrading without setting this config. I would personally advocat…
- **amuthan Ganeshan:** Hi [~ableegoldman] and [~mjsax] I would like to work on this. Would you guide me in this by giving some pointers to start with...
- **A. Sophie Blee-Goldman:** Sure thing -- I recommend checking out the example implementation in the Memory Management section (linked to in the ticket description) and read up on the KIP process if you're not familiar with it yet: https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Improvement+Proposals The idea here is…
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

- **Matthias J. Sax:** The observed behavior is expected. For `KTable` filter, the predicate needs to be evaluated twice, once for the _previous_ result, and once for the _new_ result. I can go into more technical details if you want to understand the details. Why do you think there is a bug? As you mentioned in the tick…
- **Jess J.:** [~mjsax] Thanks for your feedback. Would you mind taking a deeper look at the following? If the filter method is called twice per input tuple it leaves me with the following possible output combinations: ||filter-method return value for 1st call||filter-method return value for 2nd call||emits|| |…
- **Matthias J. Sax:** {quote}In the (stateless) filter-method I cannot determine which of the two records is the current and which the previous. Or do I miss something crucial? Neither can I find anything in the documentation about the three different possible outcomes described above, nor the need to combine two calls…
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

- **Matthias J. Sax:** Different method: \{{testReplicationWithEmptyPartition}} failed with timeout {quote} {{java.lang.RuntimeException: java.util.concurrent.ExecutionException: org.apache.kafka.common.errors.TimeoutException: The request timed out.  at org.apache.kafka.connect.mirror.integration.MirrorConnectorsIntegr…
- **Matthias J. Sax:** Another timeout: {quote} {{java.lang.RuntimeException: java.util.concurrent.ExecutionException: org.apache.kafka.common.errors.TimeoutException: The request timed out. 	at org.apache.kafka.connect.mirror.integration.MirrorConnectorsIntegrationSSLTest.startClusters(MirrorConnectorsIntegrationSSLTes…
- **Matthias J. Sax:** [https://github.com/apache/kafka/pull/10495/checks?check_run_id=2291819321]
- **Matthias J. Sax:** [https://github.com/apache/kafka/pull/10301/checks?check_run_id=2284331932]
- **Matthias J. Sax:** [https://github.com/apache/kafka/pull/10506/checks?check_run_id=2327349920] [https://github.com/apache/kafka/pull/10506/checks?check_run_id=2327310946]  {quote} {{java.lang.RuntimeException: java.util.concurrent.ExecutionException: org.apache.kafka.common.errors.TimeoutException: The request timed…
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
- **Guozhang Wang:** This is a separate issue, as `joinGroupIfNeeded` is not called by the heartbeat thread at all. I checked the code in trunk and compared with 2.7, I can confirm the situation still persists there. But this may not be a real issue, just in [~matiss.gutmanis]'s testing environment. The key is that in…
- **Philip Nee:** Hey [~matiss.gutmanis] - I'm arriving at the same conclusion as what Guozhang previous mentioned, would you mind sharing/briefly describe your test environment? [~guozhang] - should we could exit upon expired timer? maybe something like ``` if (timer.isExpired()) {   return false; } timer.sleep…
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
- **Dan O'Reilly:** Thanks for the reply, [~dajac]! Agreed that KIP-848 is the long-term answer, and we're working toward it, but the migration is gradual, and while the classic protocol is still active I think it's worth supporting this case. I'm aware of a few teams where this still bites them in production today. O…

## KAFKA-12760: Delete My Account
Wish · Resolved (Invalid) · Minor · created 2021-05-07 · resolved 2021-05-11

I wish to have my account deleted. There doesnt seem to be a way to do it from within my own account, but it should be possible for an admin to do it.
Many thanks.

- **Matthias J. Sax:** [~byusti] – we cannot delete your account either. You could try to file a ticket against [https://issues.apache.org/jira/projects/INFRA] – maybe they are able to help with this request.

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
- **Dejan Stojadinović:** [~ijuma] makes sense.  I will assign this ticket to my self and return to it in a few months.
- **Dejan Stojadinović:** {color:blue}*+Related links/resources+:*{color}  * _*What's New in Apache Kafka 3.0.0*_ [https://blogs.apache.org/kafka/entry/what-s-new-in-apache6]  * _*KIP-750: Drop support for Java 8 in Kafka 4.0 (deprecate in 3.0)*_ [https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=181308223]…
- **Dejan Stojadinović:** [~ijuma] Is it safe to say that Scala 3 will have to wait for Kafka 4 ? I tried to search for some related *_KIP-_* (but could not find any). _{{Edit: I see that there is some progress here:}}_ KAFKA-12954
- **Dejan Stojadinović:** Unassigned my self from this ticket :) Rationale: ticket is quite old and on top of that - now it seems unlikely that Kafka will switch to Scala 3.x :D I'll also solve this as a duplicate of KAFKA-12954

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
- **A. Sophie Blee-Goldman:** Personally I agree that throwing an exception may be too harsh, it's not my impression that any of the wal-related options are "critical" enough that a user would want or need to be informed if they were going to be ignored. We should definitely log a warning at the least. Can you clarify a bit mor…
- **Bruno Cadonna:** I have to admit that I blindly followed your comment here: https://github.com/apache/kafka/pull/10568#discussion_r626058786 I interpreted "disable" as to not offer methods to read and write this option to users which seems hard to achieve. Now I see, that I misinterpreted. I am fine with ignoring.…
- **Konstantine Karantasis:** We are past feature freeze for 3.0 and this issue doesn't seem to be a bug. Postponing to the subsequent release.
- **Tomer Wizman:** Hi Bruno, Sophie, Konstantine, nice e-meeting you :) According to the discussion here, the link Bruno attached and from what I saw in the code is that we explicitly disable WAL, so it doesn't really matter in terms of correctness whether we set the underlying Options object inside the adapter class…
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

- **Dongjin Lee:** I reviewed this problem and found the following: The MirrorMaker 1 as a standalone application had been included in the Kafka distribution for a long time ago and MirrorMaker 2 was added with [KIP-382|https://cwiki.apache.org/confluence/display/KAFKA/KIP-382%3A+MirrorMaker+2.0] by [~ryannedolan] in…

## KAFKA-12769: Backport of KAFKA-8562
Task · Resolved (Duplicate) · Major · components: network · created 2021-05-10 · resolved 2021-05-11

Kafka-8562 solved the issue of SASL performing a reverse DNS lookup to resolve the IP.
This bug fix should be backported so it's present on 2.7.x and 2.8.x versions.

- **Josep Prat:** I'll work on this
- **Josep Prat:** Submitted patches to branches 2.7 and 2.8

## KAFKA-12882: Add ActiveBrokerCount and FencedBrokerCount metrics (KIP-748)
Improvement · Resolved (Fixed) · Minor · labels: needs-kip · created 2021-06-02 · resolved 2021-10-25

Adding RegisteredBrokerCount and UnfencedBrokerCount metrics to the QuorumController.

- **Konstantine Karantasis:** The KIP has been published but it's still under discussion.  [https://cwiki.apache.org/confluence/display/KAFKA/KIP-748%3A+Add+Broker+Count+Metrics#KIP748:AddBrokerCountMetrics] I'm resetting the Fix version since we are past the relevant deadlines. Please make sure to set the appropriate version…
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

- **Josep Prat:** I'll take a stab at this task. If I understand it correctly, we want to skip the user defined handler and directly re-throw those up the chain, right?
- **Josep Prat:** Submitted PR https://github.com/apache/kafka/pull/11228
- **Matthias J. Sax:** This feature broke some stuff, and we revert it: [https://github.com/apache/kafka/pull/12421]  Reverted in 3.3.0, 3.2.1.
- **Ismael Juma:** Reopened the Jira since the PR was reverted.
- **Ian Corne:** Why wouldn't you allow the user to handle this? This is currently in 3.1.1 which is the version in the latest spring boot 2.7 and it disables handling errors in business logic. IllegalArgumentException is not only used for fatal errors..
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

- **Luke Chen:** I tried to set the original root acl back, but it failed. That is: [code/log omitted] I think we need [~soarez] [~omkreddy]  's help. Thanks.
- **Bruno Cadonna:** Is PR #10821 supposed to solve the issue? I still see a lot of  [code/log omitted] Also on PRs that contain PR #10821. For example https://ci-builds.apache.org/blue/rest/organizations/jenkins/pipelines/Kafka/pipelines/kafka-pr/branches/PR-10856/runs/3/nodes/14/steps/121/log/?start=0
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
- **ASF GitHub Bot:** showuon opened a new pull request #361: URL: https://github.com/apache/kafka-site/pull/361    1. add missing closing tag    2. remove a redundant `span` tag --  This is an automated message from the Apache Git Service. To respond to the message, please log on to GitHub and use the URL above to go t…
- **ASF GitHub Bot:** showuon commented on a change in pull request #361: URL: https://github.com/apache/kafka-site/pull/361#discussion_r658532684 ########## File path: 27/streams/developer-guide/memory-mgmt.html ########## @@ -179,7 +179,7 @@ <h2><a class="toc-backref" href="#id3">RocksDB</a><a class="headerlink" href="…
- **ASF GitHub Bot:** showuon commented on pull request #361: URL: https://github.com/apache/kafka-site/pull/361#issuecomment-868286033    @ableegoldman , please take a look. Thanks. --  This is an automated message from the Apache Git Service. To respond to the message, please log on to GitHub and use the URL above to g…
- **ASF GitHub Bot:** cadonna commented on pull request #361: URL: https://github.com/apache/kafka-site/pull/361#issuecomment-868481708    @showuon I think this has been already done in PR #10651. --  This is an automated message from the Apache Git Service. To respond to the message, please log on to GitHub and use the…
- _…13 more comments_

## KAFKA-12994: Migrate all Tests to New API and Remove Suppression for Deprecation Warnings related to KIP-633
Improvement · Resolved (Fixed) · Major · components: streams, unit tests · labels: kip-633, newbie, newbie++ · created 2021-06-25 · resolved 2021-10-21

Due to the API changes for KIP-633 a lot of deprecation warnings have been generated in tests that are using the old deprecated APIs. There are a lot of tests using the deprecated methods. We should absolutely migrate them all to the new APIs and then get rid of all the applicable annotations for suppressing the deprecation warnings.
The applies to all Java and Scala examples and tests using the deprecated APIs in the JoinWindows, SessionWindows, TimeWindows and SlidingWindows classes.
This is…

- **Konstantine Karantasis:** Hi [~iekpo]. You mentioned on the dev mailing list that a PR was in the works for this issue. https://lists.apache.org/thread.html/r25f41514ae9751f260b5773abc039dfc828b00154297f20b4a14a151%40%3Cdev.kafka.apache.org%3E However, I don't see a link on this issue here yet.  We are now past code freez…
- **Konstantine Karantasis:** Downgraded the priority to Major since this is not a blocker. If we get a PR soon we could consider inclusion to 3.0 if the changes don't have any risk.
- **A. Sophie Blee-Goldman:** Hey [~iekpo], I'm unassigning this in case someone else wants to pick it up. If you already started working on this and have a partial PR ready with some subset of the tests migrated over, you can just open that PR and we can merge this in pieces. It seems like a lot of tests so splitting it up into…
- **Andrew patterson:** Hello, I'd be happy to take this issue on, although I'm not on the contributor list, would it be possible to get added to it so i can assign this issue to myself?
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

- **Ismael Juma:** Thanks for the ticket. This class was never meant to be thread safe, the value was initialized lazily previously and it just so happened the key was not. Since the consumer is single threaded, this was deemed ok. For now, the easiest path is for you to copy the data you care about to your own threa…
- **Ismael Juma:** cc [~chia7712]
- **Antonio Tomac:** {quote}but it would require a KIP and it would probably only be done in a feature release.{quote} [~ijuma] What do you suggest for me to do? Should I then write a KIP? Cancel my [PR|https://github.com/apache/kafka/pull/10933]? {quote}For now, the easiest path is for you to copy the data you care a…
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
- **Jose Armando Garcia Sancio:** {quote}Can each listener hold a thread confined buffer supplier? {quote} Yeah. That is one possible solution to this problem. Have the {{RaftClient.Listener}} provide a {{BufferSupplier}} during registration.

## KAFKA-13090: Improve cluster snapshot integration test
Sub-task · Resolved (Fixed) · Major · labels: kip-500 · created 2021-07-14 · resolved 2021-07-19

Extends the test in RaftClusterSnapshotTest to verify that both the controllers and brokers are generating snapshots.

- **Konstantine Karantasis:** Resolving given that the PR got merged and cherry-picked to 3.0:  https://github.com/apache/kafka/pull/11054

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

- **Nikolay Izhikov:** Hello, [~Fuud]  Do you have logs? stack trace for described issue? Can you attach them to the ticket.

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

- **Alok Nikhil:** [~luwang] I see that the consumer side memory pool management KIP was never implemented - [https://cwiki.apache.org/confluence/display/KAFKA/KIP-81:+Bound+Fetch+memory+usage+in+the+consumer] The default is `MemoryPool.NONE`. How did LinkedIn measure the performance here? Is there a customization /…
- **Tushar Goyal:** [~aloknnikhil] I am the original author for the code change. We measured the performance by adding some custom code to measure the performance in KafkaConsumer. The customization is a follow up PR which was recently merged here [https://github.com/linkedin/kafka/pull/196] I can send out a forward p…

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

- **CS User:** I have been able to replicate this issue using the confluent 6.2 images, please see: [https://github.com/csghuser/kafka-fault-test] This appears to happen when the Zookeeper leader is shutdown uncleanly. The only changes to the official images are:  # Add secrets file to the image  # Modify Zook…
- **Chris Borckholder:** We are seeing similar issues after upgrading to version 2.8.0 (similarly the cluster ran reliably for > 1 year in the current setup with former 2.x versions). We are hosting kafka in EC2 (6 broker, 3 zookeeper). In a test environment, we are performing ec2 terminations of broker/zookeeper instances…
- **Loïc Monney:** We were able to reproduce similar scenario in a test environment with 2.8.0, leading also to an inconsistent cluster state, but we were not able to reproduce the issue with 2.6.1. Would propose as well to increase the severity of this ticket. [~mumrah], [~cmccabe], [~hachikuji] is this something c…
- **Edoardo Comar:** We were also able to reproduce this with 3.0.0 - and corresponding zookeeper 3.6.3 The easiest way to reproduce for us (in Kubernetes) is : Initiate a kafka rollout, and while that is running, delete the zookeeper pod that is the current zookeeper leader. it may take a different number of attempt…
- **Edoardo Comar:** [~acldstkusr] can you take a look at https://issues.apache.org/jira/browse/KAFKA-13407 ? It might be symptoms of the same underlying issue. Would you be able to try reproduce this issue with the fix we propose in https://issues.apache.org/jira/browse/KAFKA-13407 ?
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

- **Justine Olshan:** There was code to change this in [https://github.com/apache/kafka/pull/9590,] but if we want to fix faster, we should just make a new PR.  Replacing  // we do not clean beyond the first unstable offset  log.firstUnstableOffset, with  // we do not clean beyond the lastStableOffset (and therefore…
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
- **Guozhang Wang:** I just did that in a recent PR: https://github.com/apache/kafka/pull/11252/files#diff-1060876874aba52f23e63e730ca6d26aac41e9be5f43fde4e5dcfaad5f76f927R65 I do not have a concrete framework in mind for how to extend that for new operators / configuration permutations though, do you have something in…
- **Victoria Xia:** Hey [~guozhang] we've already got KTableKTableForeignKeyInnerJoinMultiIntegrationTest.java for testing foreign key joins with differing number of partitions on the source tables, and [https://github.com/apache/kafka/pull/11368] is adding coverage for source tables with custom partitioners. Is this t…
- **Guozhang Wang:** Yup, I think KAFKA-13261 would be fully covering it. I'm going to close this one.

## KAFKA-13269: Kafka Streams Aggregation data loss between instance restarts and rebalances
Bug · Open · Major · components: streams · created 2021-09-03

Using Kafka Streams 2.6.2 and doing count based aggregation of messages. Also setting Processing Guarantee - EXACTLY_ONCE_BETA and NUM_STANDBY_REPLICAS_CONFIG = 1. Sending some messages and restarting instances in middle while processing to test fault tolerance. The output count is incorrect because of data loss while restoring state.
It looks like the streams task becomes active and starts processing even when the state is not fully restored but is within the acceptable recovery lag (default i…

- **A. Sophie Blee-Goldman:** Hey [~rohitbobade], thanks for the report. Unfortunately I don't think the acceptable recovery lag is directly responsible, as that config is only used within the assignor to figure out the placement of tasks. Assigning a task as "Active" just means that the instance should try to process it, the ta…
- **Rohit Bobade:** Thanks [~ableegoldman], will check this and also debug further. Just to add details - I noticed the same behavior (data loss between instance restarts and rebalances) even without EOS

## KAFKA-13270: Kafka may fail to connect to ZooKeeper, retry forever, and never start
Bug · Resolved (Fixed) · Blocker · created 2021-09-03 · resolved 2021-09-06

The implementation of https://issues.apache.org/jira/browse/ZOOKEEPER-3593 in ZooKeeper version 3.6.0 decreased the default value for the ZooKeeper client's `jute.maxbuffer` configuration from 4MB to 1MB.  This can cause a problem if Kafka tries to retrieve a large amount of data across many znodes -- in such a case the ZooKeeper client will repeatedly emit a message of the form "java.io.IOException: Packet len <####> is out of range" and the Kafka broker will never connect to ZooKeeper and fail…


## KAFKA-13271: Error while fetching metadata with correlation id 219783 : LEADER_NOT_AVAILABLE
Bug · Open · Major · components: producer  · created 2021-09-03

Hi dear kafka support
We are getting below error after a new connector creation
[2021-09-02 19:15:23,878] WARN [Producer clientId=producer-178] Error while fetching metadata with correlation id 219783 : \{ tkr_prd2.tkr.glrep_file2=LEADER_NOT_AVAILABLE} (org.apache.kafka.clients.NetworkClient)
[2021-09-02 19:15:23,982] WARN [Producer clientId=producer-178] Error while fetching metadata with correlation id 219784 : \{ tkr_prd2.tkr.glrep_file2=LEADER_NOT_AVAILABLE} (org.apache.kafka.clients.Netw…


## KAFKA-13272: KStream offset stuck after brokers outage
Bug · Open · Major · components: core · created 2021-09-03

Our KStream app offset stay stuck on 1 partition after outage possibly when exactly_once is enabled.
Running with KStream 2.8, kafka broker 2.8,
 3 brokers.
commands topic is 10 partitions (replication 2, min-insync 2)
 command-expiry-store-changelog topic is 10 partitions (replication 2, min-insync 2)
 events topic is 10 partitions (replication 2, min-insync 2)
with this topology
Topologies:
[code/log omitted]
h3.  
h3. Attempt 1 at reproducing this issue
Our stream app runs with pro…

- **Guozhang Wang:** Hello [~fmethot], I looked at the ticket and I suspect it is caused by the same issue as reported in https://issues.apache.org/jira/browse/KAFKA-13174. In a quick sum, this seems to be a broker-side issue that after an unclean shutdown the producer's dangling txn was not yet aborted, and hence causi…
- **Guozhang Wang:** cc [~hachikuji], have you observed this before?
- **F Méthot:** Hi [~guozhang] Thanks for your feedback. We were puzzled by this error that kept coming back on partition 9 on our consumer  [code/log omitted] Even after after we had deleted and recreated that source topic, got rid of Exactly_once, even deleted the __transaction topic.  The pattern was:  * We…
- **Guozhang Wang:** I looked into the source code and I have a suspicion it is a broker side bug. Here's my theory: * In the transaction coordinator, when we want to send markers to the data partition hosts, there's a condition that if the leader of that data partition is unknown, then we would skip sending this marke…
- **A. Sophie Blee-Goldman:** [~guozhang] any updates here? I'm seeing almost weekly reports of Streams EOS apps getting stuck in restoration – a few of them I believe are actually https://issues.apache.org/jira/browse/KAFKA-13295, but most of them don't report any ProducerFencedException or TaskMigratedException which would rul…
- _…5 more comments_

## KAFKA-13273: Add support for Java 17
Improvement · Resolved (Fixed) · Major · created 2021-09-05 · resolved 2021-09-06

Java 17 is at release candidate stage and it will be a LTS release once
it's out (previous LTS release was Java 11).


## KAFKA-13274: Ensure system tests run successfully with Java 17
Improvement · Resolved (Fixed) · Major · created 2021-09-05 · resolved 2025-01-10

- **Ismael Juma:** This was done a while back.

## KAFKA-13356: Use "delete" retention policy only for stream-stream join windowed stores
Improvement · Resolved (Duplicate) · Major · components: streams · created 2021-10-06 · resolved 2021-10-07

Today stream-stream join associated window stores, like any other window stores, use "delete,compact" as their retention policies. However, since today we add sequence number to disable de-duplication of keys, "compaction" would never be able to compact any keys, but only result in 1) CPU waste on the cleaner thread on brokers, 2) some additional feature of brokers that relies on "delete" policy to not be able to apply.
Until we change the store format potentially in the future to not use seque…


## KAFKA-13357: Controller snapshot contains producer ids records but broker does not
Sub-task · Resolved (Fixed) · Blocker · components: kraft · created 2021-10-06 · resolved 2021-11-24

MetadataDelta ignores PRODUCER_IDS_RECORDS. A broker doesn't need this state for its operation. The broker needs to handle this records if we want to hold the invariant that controllers snapshots are equivalent to broker snapshots.


## KAFKA-13358: Not able to replicate groups in MirrorMaker 2.0 
Bug · Open · Critical · components: mirrormaker · created 2021-10-07

I had created a *group PizzaGroup from kafka-console-consumer* so that I can read the content of the *Pizza* topic in the *source* cluster. 
Now I want to replicate the *same group to the destination* cluster.
Even though I have left the *groups.blacklist as empty* in the *connect-mirror-maker.properties*, even then the groups are not getting replicated. The properties file has been attached for reference.
We are using SSL protocol.
*The topics and their offsets are getting replicated but th…


## KAFKA-13359: Round Robin Kafka Producer Routes to only half the partitions when even number of partitions
Bug · Open · Minor · components: producer  · created 2021-10-07

When you have 1 message per batch, in the round robin Partitioner. The messages go only to half the partitions beacuse it always skips 1 partition. This works out for odd number of partitions because skipping 1 will mean all partitions get a hit eventually, but with an even number half the partitions never get selected.
So if you have partitions 1, 2, 3, 4 
Message 1: Partion 1
Message 2: Partion 3
Message 3: Partion 1 ... so on. [ Here 2 and 4 are never selected]
If you have partitions 1,…

- **Luke Chen:** The root cause of this issue should be KAFKA-9965.

## KAFKA-13360: Wrong SSL messages when handshake fails
Bug · Open · Major · components: network · created 2021-10-08

When a consumer tries to connect to a Kafka broker and there is an error in the SSL handshake, like the server sending a certificate that cannot be validated for not matching the common name with the server/domain name, Kafka sends out erroneous SSL messages before sending an SSL alert. This error occurs in client but also can be seen in server.
Because of the nature of the problem it seems it will happen in more if not all handshake errors.
I've debugged and analyzed the Kafka networking code…

- **David Mao:** Very thorough writeup, nice find!

## KAFKA-13361: Support fine-grained compression options
Improvement · In Progress · Major · components: clients, core · labels: needs-kip · created 2021-10-10

Adds the following options into the Producer, Broker, and Topic configurations:
 * compression.gzip.buffer: the buffer size that feeds raw input into the Deflator or is fed by the uncompressed output from the Deflator. (available: [512, ), default: 8192(=8kb).)
 * compression.snappy.block: the block size that snappy uses. (available: [1024, ), default: 32768(=32kb).)
 * compression.lz4.block: the block size that lz4 uses. (available: [4, 7], (means 64kb, 256kb, 1mb, 4mb respectively), default…

- **Cheng-Kai, Zhang:** Hi [~dongjin]  [~mimaison] I am interested to this issue, and it seems to be manageable for a newbie like me.  Do you think I could help on this one? My plan is to follow current structure [~mimaison]  currently working on to add those config. There is a draft PR in a very early stage available [h…
- **Mickael Maison:** Dongjin had written a KIP ([KIP-780|https://cwiki.apache.org/confluence/display/KAFKA/KIP-780%3A+Support+fine-grained+compression+options]) but it hasn't been accepted. I'm currently working on getting [KIP-390|https://cwiki.apache.org/confluence/display/KAFKA/KIP-390%3A+Support+Compression+Level],…
- **Cheng-Kai, Zhang:** [~mimaison]  much thanks for providing me with more detail. :) I would start by studying the changes in your [PR|https://github.com/apache/kafka/pull/15516] and figure out how to further add in features of KIP-780

## KAFKA-13362: KafkaConnect authorization failure using SCRAM-SHA-512 and OPA
Bug · Open · Major · components: connect · created 2021-10-11

Using Kafka Strimzi Operator and superuser client credentials to connect to a KafkaCluster set up to use OPA for authorization, authentication is successful but authorization fails for connect-offsets Topic.
[code/log omitted]
Expected behavior: No authorization is required.
Superuser account does not require authorization and there is no trace in OPA Server indicating an attempt at verifying the users permssions.
Note:
Using TLS Authentication, there is no issue.


## KAFKA-13363: Add support for asynchronous authorization
Improvement · Open · Minor · components: security · labels: authorization, security · created 2021-10-11

In KIP-504 there was mention to [Make authorize() asynchronous|https://cwiki.apache.org/confluence/display/KAFKA/KIP-504+-+Add+new+Java+Authorizer+Interface#KIP504AddnewJavaAuthorizerInterface-Makeauthorize()asynchronous], saying _"In future, we can add async authorize as a new method on the API if required."_  Many high-performance systems out there (_Envoy, Kubernetes, ...)_ have external authorization mechanisms and I think it would be nice if Kafka did the same.  I am currently working on a…


## KAFKA-13364: SQL Processor Alerts Creation when Failed
New Feature · Resolved (Invalid) · Major · components: streams · labels: alerts, channels, reuse_existing_alert_channels, streams · created 2021-10-11 · resolved 2022-08-10

Using the existing configured Alert channels, I
Scenario 1: Should alert when SQL Processor gets into failed state because of any errorneous message and the error message payload should be sent through the alert
Scenario 2: Should alert when SQL Processor continues to be in Not Running / Failed state for a certain period of time (this time should be configurable)
Scenario 3: Should alert when SQL Processor doesn't produce any message for certain period of time even though there are input mess…

- **Matthias J. Sax:** Not sure if I understand this request. Also, what do you mean by "SQL Processor"? What are "the existing configured Alert channels" ?

## KAFKA-13365: Improve MirrorMaker2's client configuration
Bug · In Progress · Critical · components: mirrormaker · labels: needs-kip · created 2021-10-11

As of present, MirrorMaker 2 (aka MM2) 's client configurtaion feature has some problems:
 # The replication-level client configuration works only to the common properties like {{bootstrap.servers}}, {{security.protocol}}, ssl, sasl, etc; that is, a configuration like {{'A→B.producer.batch.size'}} is ignored.
 ## Also, which admin client is affected by the replication-level configuration like A→B.admin.retry.backoff.ms is unclear; MM2 uses two admin clients for both upstream and downstream clu…

- **Ivan Yurchenko:** In what version does it happen?
- **Dongjin Lee:** I found it in 3.0.0 (see [here|https://github.com/dongjinleekr/kafka/blob/etc/mm2-client-config-bug/connect/mirror/src/test/java/org/apache/kafka/connect/mirror/MirrorMakerConfigTest.java#L77]), but it seems like it affects all the previous versions from 2.4.0. It seems like there was some mistake i…
- **Omnia Ibrahim:** [~dongjin] I believe KAFKA-13876 may also be related to this.

## KAFKA-13366: JMX metric for leader.imbalance.per.broker.percentage value
Improvement · Open · Minor · components: metrics · labels: jmx, metrics · created 2021-10-12

The value of leader.imbalance.per.broker.percentage is calculated by Controller.
It could be useful to expose the current value as JMX metric.


## KAFKA-13416: Add topic ids to any metrics that has topic and partition tags
Bug · Open · Major · labels: topic-id · created 2021-10-28

With [KIP-516|https://cwiki.apache.org/confluence/display/KAFKA/KIP-516%3A+Topic+Identifiers] introducing Topic ID to more APIs, broker and client' metrics will need to expose topic UUID as part of any metric with the topic and partition tags.
Currently, metrics will be a bit confusing when the topic gets re-created as it wouldn't be evident that the topic got re-created.


## KAFKA-13417: Dynamic thread pool re-configurations may not get processed
Bug · Resolved (Fixed) · Major · created 2021-10-28 · resolved 2021-11-09

`DynamicBrokerConfig.updateCurrentConfig` includes the following logic to update the current configuration and to let each `Reconfigurable` process the update:
[code/log omitted]
The problem here is that `currentConfig` gets initialized as `kafkaConfig` which means that the first call to `kafkaConfig.updateCurrentConfig(newConfig)` ends up mutating `currentConfig` and consequently `oldConfig`. The problem with this is that some of the `reconfigure` implementations will only apply a new configu…


## KAFKA-13418: Brokers disconnect intermittently with TLS1.3
Bug · Resolved (Fixed) · Minor · components: clients · created 2021-10-29 · resolved 2022-03-29

Using TLS1.3 (with JDK11) is causing a regression and an increase in inter-broker p99 latency, as mentioned by Yiming in [Kafka-9320|https://issues.apache.org/jira/browse/KAFKA-9320?focusedCommentId=17401818&page=com.atlassian.jira.plugin.system.issuetabpanels:comment-tabpanel#comment-17401818]. We tested this with Kafka 2.8.
The issue seems to be because of a renegotiation exception being thrown by 
[code/log omitted]
 & 
[code/log omitted]
 in 
_clients/src/main/java/org/apache/kafka/com…

- **shylaja kokoori:** After enabling SSL logging (javax.net.debug=ssl,handshake), I see that unwrap call in the SslTransportLayer.read function returns handshakeStatus=NEED_WRAP when ssl key_update takes place. (log snippet below) Based on documentation provided in [https://datatracker.ietf.org/doc/html/rfc8446] key_u…
- **Ismael Juma:** [~skokoori] Thanks for the report. Can you please submit a pull request? See https://kafka.apache.org/contributing .
- **Ismael Juma:** cc [~rajinisivaram@gmail.com]
- **shylaja kokoori:** [~ijuma] Thank you. Let me test with the latest trunk and will submit a pull request
- **Yiming Zang:** Thanks [~skokoori] for creating this issue, and [~ijuma] for reviewing the pull request. This will solve the TLS issue Twitter has been seeing since upgrading to 2.7 with TLS 1.3
- _…4 more comments_

## KAFKA-13419: sync group failed with rebalanceInProgress error might cause out-of-date ownedPartition in Cooperative protocol
Bug · Resolved (Fixed) · Major · components: clients · created 2021-10-29 · resolved 2022-02-23

In KAFKA-13406, we found there's user got stuck when in rebalancing with cooperative sticky assignor. The reason is the "ownedPartition" is out-of-date, and it failed the cooperative assignment validation.
Investigate deeper, I found the root cause is we didn't reset generation and state after sync group fail. In KAFKA-12983, we fixed the issue that the onJoinPrepare is not called in resetStateAndRejoin method. And it causes the ownedPartition not get cleared. But there's another case that the…

- **Kirk True:** [~showuon] - this Jira is marked as in progress, yet I see that the corresponding PR has been merged already. Is this still in progress? If not, please update the fixed version and mark as fixed. Thanks!
- **Luke Chen:** [~kirktrue] , thanks for the reminder. Updated.
- **Shawn Wang:** Hi [~showuon]  After i applied this fix and my previous change to make this fix work[https://github.com/apache/kafka/pull/12140, |https://github.com/apache/kafka/pull/12140]what we are seeing is that: sometimes consumer will revoker almost all partitions with cooperative enabled. detail:  * we ha…
- **A. Sophie Blee-Goldman:** {quote}  can we just treat the ownedPartition in previous generation legal if there are no same partition claimed by other member?  {quote} Huh, I thought that's already what the cooperative assignor does? Maybe we intentionally left/took it out of the constrained case algorithm for some reason? O…
- **Luke Chen:** [~ableegoldman] , you are right. We have the logic to handle multiple consumers owned the same partitions case.
- _…4 more comments_

## KAFKA-13420: consumer protocol should include "generation" field for assignor to distinguish between new/old OwnedPartitions
Improvement · Open · Major · components: clients, consumer · labels: need-kip · created 2021-10-29

In [KIP-429|https://cwiki.apache.org/confluence/display/KAFKA/KIP-429%3A+Kafka+Consumer+Incremental+Rebalance+Protocol], we add a new field: `OwnedPartitions` into consumer protocol, for cooperative protocol do partition revoking things. But recently, we found the `ownedPartitions` info might be out-of-date due to some reasons (ex: unstable network), and the out-of-date  `ownedPartitions` causes unexpected rebalance stuck issue (ex: KAFKA-12984, KAFKA-13406). To fix it, we should consider to add…


## KAFKA-13421: Fix ConsumerBounceTest#testRollingBrokerRestartsWithSmallerMaxGroupSizeConfigDisruptsBigGroup
Bug · Reopened · Major · labels: clients, consumer, flaky-test, unit-test · created 2021-10-30

ConsumerBounceTest#testRollingBrokerRestartsWithSmallerMaxGroupSizeConfigDisruptsBigGroup is failing with this error:
[code/log omitted]

- **Guozhang Wang:** Re-opening this ticket since the test is still failing.
- **Jose Armando Garcia Sancio:** This test is currently getting skipped. Moving this Jira to 3.4.0
- **A. Sophie Blee-Goldman:** bumping this to 3.5.0 as we are past code freeze for 3.4
- **Philip Nee:** I think the original issue (org.apache.zookeeper.KeeperException$NodeExistsException: KeeperErrorCode = NodeExists)  is different to what I'm seeing now. It could be a different issue. The test sets hb interval to 1s, I wonder if that's too short
- **Mickael Maison:** We are past code freeze for 3.5 so moving to the next release.
- _…8 more comments_

## KAFKA-13422: Even if the correct username and password are configured, when ClientBroker or KafkaClient tries to establish a SASL connection to ServerBroker, an exception is thrown: (Authentication failed: Invalid username or password)
Bug · Open · Major · components: clients, core · created 2021-10-30

h1. Foreword:
When deploying a Kafka cluster with a higher version (2.7.1), I encountered an exception of communication identity authentication failure between brokers. In the current latest version 3.0.0, this problem can also be reproduced.
h1. Problem recurring:
h2. 1）broker Version is 3.0.0
h3. The content of kafka_server_jaas.conf of each broker is exactly the same, the content is as follows：
[code/log omitted]
h3. broker server.properties：
One of the broker configuration files is pr…

- **RivenSun:** Hi [~showuon] and  [~guozhang], Do you have any suggestions for this issue? I think we can take the first and second points from Suggestion & Solutions to consider solving this problem. WDYT?
- **Luke Chen:** [~RivenSun], I haven't read through all the description, but I guess it's this issue. Please take a look: [https://github.com/apache/kafka/pull/11430]
- **RivenSun:** [~showuon] These are two problems.  My problem is that the jaasConf file between each broker is the same [code/log omitted] and [code/log omitted] But the password sent by ClientBroker is the password "admin_scram_password" in ScramLoginModule.  The password expected by ServerBroker is "kJTVDz…
- **Luke Chen:** [~RivenSun], I've read through all the content. Nice RCA! It makes sense to me. However, I'm not quite familiar with the jaas component, and might not be the good person to ask for comments. I'd suggest that since you've traced the source codes and found the suspicious (or bug) places, you can try t…
- **RivenSun:** Hi [~showuon] ,  Thank you for taking time to read through this issue :D And hi [~rajinisivaram@gmail.com] , [~ijuma] and [~manikumar] Can you read this issue and give some suggestions  Thanks
- _…35 more comments_

## KAFKA-13423: Error falsely reported on Kafka Streams app when GlobalKTables are used 
Bug · Resolved (Fixed) · Minor · components: streams · created 2021-10-30 · resolved 2022-02-06

It seems that error of this form:
_ERROR streams.KafkaStreams: stream-client [testAppId-56832986-6ff0-4583-8aaf-85fafd7b4fe4] Global thread has died. The streams application or client will now close to ERROR._
are being reported when Streams are closed gracefully. This seems to be not right. See attached files for repro case


## KAFKA-13424: Redundant cleanup operations in TopicChangeHandler or TopicDeletionManager
Improvement · Open · Major · components: controller · created 2021-10-31

In `*TopicDeletionManager.completeDeleteTopic()*`, `*controllerContext.removeTopic(topic)*` will be done after deleting topic znode in `*client.deleteTopic(topic, controllerContext.epochZkVersion)*`. This will trigger `*TopicChangeHandler*`, and process `*controllerContext.removeTopic*` again in `*processTopicChange*`. 
It is equivalent to deleting Topic once and executing `*controllerContext.removeTopic*` twice. Is this the expected situation？


## KAFKA-13425: KafkaConsumer#pause() will lose its effect after groupRebalance occurs, which maybe cause data loss on the consumer side
Bug · Open · Major · components: consumer · labels: new-consumer-threading-should-fix · created 2021-11-01

h1. Foreword:
Since I want to achieve the decoupling of the two processes of polling messages and consuming messages on the KafkaConsumer side, I use the "poll --> push" architecture model on the Kafka consumer side.
.
h2. Architecture
 see picture "architecture_picture"
h3. 1）ThreadPoolExecutor
The key parameters of ThreadPoolExecutor threadPool are:
h4. (1) Select ArrayBlockingQueue<Runnable> for workQueue type
h4. (2) The handler uses the RejectedExecutionHandler interface
h4. (3)thr…

- **RivenSun:** Hi [~showuon] and  [~guozhang], Do you have any suggestions for this issue? Thanks.
- **Guozhang Wang:** Hello [~RivenSun], for such scenario, my common recommendation is to use {Consumer#pause / resume} functions. I.e. when the blocking queue is full and {publish} failed, the consumer could pause all the currently assigned partitions, and then subsequent {Consumer#poll} would return no more data but o…
- **RivenSun:** [~guozhang] hello，Thank you for your reply Please take more time to read through this issue At the beginning, I did try it like your advice, and my approach is more violent.. When blocking queue is full or push failed, pause will be called before every poll call, but the poll method will *still re…
- **Luke Chen:** [~RivenSun], thanks for reporting this issue. But I think the original design of pause/resume is that: *Rebalance does not preserve pause/resume state.* (check KAFKA-2350) So, back to your suggestions:  # Precise semantics of kafkaConsumer#pause(…)  --> I agree that the java doc is not clear abo…
- **RivenSun:** Haha,  [~showuon] thank you for your reply and recognition of me:D 1. Thank you for your suggestion, and I think it is better to print the relevant prompt log when cleaning the paused mark. 2. {quote}{{When we execute invokePartitionsRevoked(revokedPartitions), do we consider the need to clean up…
- _…8 more comments_

## KAFKA-13426: Add recordMetadata to StateStoreContext
Improvement · Resolved (Fixed) · Minor · components: streams · labels: kip · created 2021-11-01 · resolved 2021-11-16

KIP-791: [https://cwiki.apache.org/confluence/display/KAFKA/KIP-791%3A+Add+Record+Metadata+to+State+Store+Context]
In order for state stores to provide stronger consistency in the future (e.g., RYW consistency) they need to be able to collect record metadata (e.g., offset information).
Today, we already make record metadata available in the AbstractProcessContext (recordMetadata()), but the call is not currently exposed through the StateStoreContext interface that is used by the state store.…


## KAFKA-13464: SCRAM does not validate client-final-message's nonce
Bug · Open · Minor · created 2021-11-18

[https://datatracker.ietf.org/doc/html/rfc5802#section-5.1]
Relevant part, in "r="
      nonce it initially specified.  The server MUST verify that the
      nonce sent by the client in the second message is the same as the
      one sent by the server in its first message.
[https://github.com/apache/kafka/blob/8a1fcee86e42c8bd1f26309dde8748927109056e/clients/src/main/java/org/apache/kafka/common/security/scram/internals/ScramSaslServer.java#L149-L161]
The only verification of client-final…

- **Travis Bischel:** AFAICT this compromises no integrity. I'm not sure the purpose of this final check. The important part is the client-proof, which hashes the `c-nonce s-nonce` into it. Sending the c-nonce s-nonce back in plaintext doesn't seem to provide much benefit.

## KAFKA-13465:  when auto create topics enable,server create inner topic of MirrorMaker unexpectedly
Bug · Open · Major · components: mirrormaker · created 2021-11-19

Hi Team
Mirror Maker: 2.7.0
when i enable auto create topic in both side: 
auto.create.topics.enable=true
sometimes，mirror maker inner topic create by server not expected，mirror naker start error.
```
[2021-11-19 18:03:56,707] ERROR [Worker clientId=connect-2, groupId=pr-mm2] Uncaught exception in herder work thread, exiting: (org.apache.kafka.connect.runtime.distributed.DistributedHerder)
org.apache.kafka.common.config.ConfigException: Topic 'mm2-configs.pr.internal' supplied via the 'co…

- **ZhenChun Pan:** I already have a patch for this issue, maybe the issue can assgin to me?
- **Dongjin Lee:** It seems like you created the topic 'mm2-configs.pr.internal' with 'cleanup.policy=delete' (default) by producing a record; It does not seem created by MM2. Could you have a check?
- **ZhenChun Pan:** Yeah,  I already check it.  Except MM2, no producer producing records  with 'mm2-configs.pr.internal' . It seems sometimes MM2 producing or consumering topics before MM2 creart topics. This issue trigger from MM2，but should not create MM2 topics by 'auto.create.topics.enable=true',  the fix is to av…

## KAFKA-13466: delete unused config batch.size in kafka-console-producer.sh
Bug · Resolved (Fixed) · Minor · components: core · created 2021-11-19 · resolved 2022-03-05

official docs:
!image-2021-11-19-04-05-15-754.png!
shell scripts is:
!image-2021-11-19-04-09-28-299.png!
in fact, the batch-size config is already not used everywhere in the code anymore, so delete this and may not have a misunderstanding in the future


## KAFKA-13467: Clients never refresh cached bootstrap IPs
Improvement · Open · Minor · components: clients, network · created 2021-11-19

Follow up ticket to https://issues.apache.org/jira/browse/KAFKA-13405.
For certain broker rolling upgrade scenarios, it would be beneficial to expired cached bootstrap server IP addresses and re-resolve those IPs to allow clients to re-connect to the cluster without the need to restart the client.

- **Deng Ziming:** Since clients have no visibility to changes in bootstrap IPs, it seems that the only mechanism we have for updating the cached IPs is connection establishment. By closing the broker side of the connection, clients would be forced to reconnect and receive an updated set of  bootstrap IPs. what do you…
- **Matthias J. Sax:** I am not familiar with the details. [~rsivaram] should be able to help. – I don't think that we would need a KIP for this change though.
- **Matthew de Detrich:** I am currently having a look at this issue although due to the nature of the ticket I am diving a bit in the deep end. [~rsivaram] , [~ijuma] [~mimaison] would be able to give my some pointers on how to best approach this? Following what [~dengziming] said earlier, I am currently looking at SocketSe…
- **Ismael Juma:** There is an ancient Jira where this was proposed and there were some concerns (at the time). We should continue the discussion there instead of creating a new issue. Now, to find that issue. :)
- **Matthew de Detrich:** [~ijuma] are you talking about https://issues.apache.org/jira/browse/KAFKA-13405, if so its already closed?
- _…5 more comments_

## KAFKA-13468: Consumers may hang because IOException in Log#<init> does not trigger KafkaStorageException
Bug · Open · Major · components: log · created 2021-11-20

When the Kafka Log class (`core/src/main/scala/kafka/log/Log.scala`) is initialized, it may encounter an IO exception in the locally block, e.g., when the log directory cannot be created due to permission issue or IOException in  `initializeLeaderEpochCache`, `initializePartitionMetadata`, etc.
[code/log omitted]
We found that the broker encountering the IO exception prints an KafkaApi error log like the following and proceeds.
[code/log omitted]
But all the consumers that are consuming data…


## KAFKA-13469: End-of-life offset commit for source task can take place before all records are flushed
Bug · Resolved (Fixed) · Blocker · components: connect · created 2021-11-22 · resolved 2021-11-30

When we fixed KAFKA-12226, we made offset commits for source tasks take place without blocking for any in-flight records to be acknowledged. While a task is running, this change should yield significant benefits in some cases and allow us to continue to commit offsets even when a topic partition on the broker is unavailable or the producer is unable to send records to Kafka as quickly as they are produced by the task.
However, this becomes problematic when a task is scheduled for shutdown with…

- **Chris Egerton:** Approved as a 3.1 blocker on the [3.1 release thread|https://mail-archives.apache.org/mod_mbox/kafka-dev/202111.mbox/%3CCAHn4u3tPba%2BOQuyawfg%2BmrfyAMnZYFBOrmzruZNGsdJy%2BrBJXg%40mail.gmail.com%3E].
- **Randall Hauch:** Merged to the following branches: * `trunk` for the next 3.2 release * `3.1` for the upcoming 3.1.0 release * `3.0` for the next 3.0.1 patch release

## KAFKA-13470: Test the handling of secure controller ports
Improvement · Open · Major · created 2021-11-22

It should be possible to configure the controller to use secure ports. We need a junit integration test for this

- **Colin McCabe:** We do not include the controller listener in the 'listeners' configuration. I will remove that part of this from the Description.

## KAFKA-13471: Test rolling change of KRaft controller endpoints
Improvement · Open · Major · components: controller, kraft · labels: test · created 2021-11-22

We should have a test of making a rolling change to KRaft controller endpoints. For example, going from PLAINTEXT or SSL. (This would involve going through an intermediate stage where the controllers exposed both endpoints.)


## KAFKA-13472: Connect can lose track of last committed offsets for topic partitions after partial consumer revocation
Bug · Resolved (Fixed) · Blocker · components: connect · created 2021-11-22 · resolved 2021-11-29

The Connect framework tracks the last successfully-committed offsets for each topic partition that is currently assigned to the consumer of each sink task. If a sink task throws an exception from {{{}SinkTask::preCommit{}}}, the consumer is "rewound" by seeking to those last successfully-committed offsets for each topic partition, so that the same records can be redelivered to the task again.
With the changes from KAFKA-12487, we failed to correctly update the logic for tracking these last-comm…

- **Chris Egerton:** Approved as a 3.1 blocker on the [3.1 release thread|https://mail-archives.apache.org/mod_mbox/kafka-dev/202111.mbox/%3CCAHn4u3tPba%2BOQuyawfg%2BmrfyAMnZYFBOrmzruZNGsdJy%2BrBJXg%40mail.gmail.com%3E].
- **Konstantine Karantasis:** Merged to `trunk` and cherry-picked to 3.1 and 3.0 branches.

## KAFKA-13473: Log cleaner Dynamic configs aren't applied after a restart
Bug · Open · Minor · components: config, core · created 2021-11-23

Upon restarting kafka, dynamically configured log cleaner configs aren't picked up and applied.
Here are some logs from a local kafka when I up the threads to 2 using the kafka-config tool - Noting the last 2 lines where it starts up 2 log cleaner threads.
[code/log omitted]
And now after a restart, at no point does it ever start 2 threads, even though it clearly knows about the configs
[code/log omitted]
When investigating from the kafka config tool all looks well.
[code/log omitted]
But…


## KAFKA-13474: Regression in dynamic update of broker certificate
Bug · Resolved (Fixed) · Critical · components: core · created 2021-11-24 · resolved 2022-07-09

h1. Problem
It seems, after updating listener SSL certificate with dynamic broker configuration update, old certificate is somehow still used for broker client SSL factory. Because of this broker fails to create new connection to controller after old certificate expires.
h1. History
Back in KAFKA-8336 there was an issue, when client-side SSL factory wasn't updating certificate, when it was changed with dynamic configuration. That bug have been fixed in version 2.3 and I can confirm, that dyna…

- **Igor Shipenkov:** Tried to reproduce problem on kafka 2.8.1. And problem is still there: I've updated certificate, I can see that listener use new certificate, but it still uses old certificate for client connections and when certificate expires, this broker can't connect to others, for example connection to controll…
- **Igor Shipenkov:** Well, I tried version 3.0.0 and I can reproduce this problem on it just fine. Same "SSL handshake failed" error, still can see old client certificate in traffic dump. Guess I'll just add this to affected version too.
- **Ismael Juma:** Thanks for the report. We should triage this before the next release.
- **Bruno Cadonna:** Moving to the next release since code freeze for 3.2.0 has passed.
- **Divij Vaidya:** I have been able to reproduce this via a test in Kafka code. I assigned this ticket to myself and am working on filing a PR with the fix.
- _…1 more comments_

## KAFKA-13520: Quickstart does not work at topic creation step
Bug · Open · Minor · components: website · created 2021-12-08

Step 3 fails
[code/log omitted]
Also needs `replication-factor`
Correct statement is: 
[code/log omitted]

- **Robin Moffatt:** https://github.com/apache/kafka-site/pull/387
- **Luke Chen:** [~rmoff] , thanks for the report. But this bug is fixed in KAFKA-13396, and will be in V3.1.0/V3.0.1. Thanks.
- **Robin Moffatt:** Thanks Luke, good that it will be fixed. Is the release of those imminent? The problem is that today anyone following the quickstart will have a bad time, so would be good to fix in the interim.
- **Luke Chen:** Make sense! Thanks.
- **ASF GitHub Bot:** bbejeck merged pull request #387: URL: https://github.com/apache/kafka-site/pull/387 --  This is an automated message from the Apache Git Service. To respond to the message, please log on to GitHub and use the URL above to go to the specific comment. To unsubscribe, e-mail: dev-unsubscribe@kafka.apa…
- _…1 more comments_

## KAFKA-13521: Supress changelog schema version breaks migration
Bug · Open · Major · components: streams · created 2021-12-08

Hi,
We recently updated the kafka-streams library in one of our apps from v2.5.0 to v2.5.1. This upgrade changes the header format of the state store for suppress changelog topics (see https://issues.apache.org/jira/browse/KAFKA-10173 and [https://github.com/apache/kafka/pull/8905)]
What we noticed was that, introducing a new version on the binary schema header breaks older clients. I.e. applications running on v2.5.1 can parse the v3, v2, v1 and 0 headers, while the ones running on 2.5.0 (and…


## KAFKA-13522: IQv2: Implement position tracking and bounding in API
Sub-task · Resolved (Fixed) · Major · created 2021-12-08 · resolved 2021-12-28


## KAFKA-13523: Implement IQv2 support in global stores
Improvement · Open · Major · components: streams · labels: IQv2 · created 2021-12-08

Global stores pose one significant problem for IQv2: when they start up, they skip the regular ingest pipeline and instead use the "restoration" pipeline to read up until the current end offset. Then, they switch over to the regular ingest pipeline.
IQv2 position tracking expects to track the position of each record from the input topic through the ingest pipeline and then get the position headers through the restoration pipeline via the changelog topic. The fact that global stores "restore" th…


## KAFKA-13524: IQv2: Implement KeyQuery from the RecordCache
Sub-task · Resolved (Fixed) · Major · created 2021-12-08 · resolved 2022-01-27

The Record Cache in Kafka Streams is more properly termed a write buffer, since it only caches writes, not reads, and its intent is to buffer the writes before flushing them in bulk into lower store layers.
Unlike scan-type queries, which require scanning both the record cache and the underlying store and collating the results, the KeyQuery (and any other point lookup) can straightforwardly be served from the record cache if it is buffered or fall through to the underlying store if not.
In con…


## KAFKA-13525: IQv2: Implement KeyQuery from the KIP
Sub-task · Resolved (Fixed) · Major · created 2021-12-08 · resolved 2021-12-20


## KAFKA-13526: IQv2: Consider more generic logic for mapping between binary and typed queries
Improvement · Open · Minor · components: streams · labels: IQv2 · created 2021-12-08

Right now, typed queries (like KeyQuery) need to be specially handled and translated to their binary counterparts (like RawKeyQuery). This happens in the Metered store layers, where the serdes are known. It is necessary because lower store layers are only able to handle binary data (because they don't know the serdes).
This situation is not ideal, since the Metered store layers will grow to host quite a bit of query handling and translation logic, because the relationship between typed queries…

- **John Roesler:** Tried the serde passing thing, which didn't work that well. I might have missed something simple, though: https://github.com/apache/kafka/pull/11583
- **John Roesler:** Here's another attempt, which seems to work better: https://github.com/apache/kafka/pull/11614
- **John Roesler:** Here's an add-on demonstrating lazy deserialization of responses: https://github.com/vvcephei/kafka/pull/1

## KAFKA-13527: Add top-level error code field to DescribeLogDirsResponse
Bug · Resolved (Fixed) · Major · created 2021-12-09 · resolved 2022-02-01

Ticket for KIP-784: https://cwiki.apache.org/confluence/display/KAFKA/KIP-784%3A+Add+top-level+error+code+field+to+DescribeLogDirsResponse


## KAFKA-13528: KRaft RegisterBroker should validate that the cluster ID matches
Bug · Resolved (Fixed) · Major · created 2021-12-09 · resolved 2022-01-08


## KAFKA-13529: kafka mm2 consumer configurattion invalid
Bug · Open · Major · labels: mirror-maker · created 2021-12-10

set  auto.offset.reset = latest
but  MirrorMaker2 seeks source topic to offset 0


## KAFKA-13530: Flaky test ReplicaManagerTest
Test · Open · Critical · components: core, unit tests · labels: flaky-test · created 2021-12-10

kafka.server.ReplicaManagerTest.[1] usesTopicIds=true
{quote}org.opentest4j.AssertionFailedError: expected: <true> but was: <false> at org.junit.jupiter.api.AssertionUtils.fail(AssertionUtils.java:55) at org.junit.jupiter.api.AssertTrue.assertTrue(AssertTrue.java:40) at org.junit.jupiter.api.AssertTrue.assertTrue(AssertTrue.java:35) at org.junit.jupiter.api.Assertions.assertTrue(Assertions.java:162) at kafka.server.ReplicaManagerTest.assertFetcherHasTopicId(ReplicaManagerTest.scala:3502) at kaf…

- **Matthias J. Sax:** Failed a second time.
- **Matthias J. Sax:** And one more.
- **Matthias J. Sax:** And again.
- **Matthias J. Sax:** +1
- **Matthias J. Sax:** Again.
- _…8 more comments_

## KAFKA-13597: Memory leak with kafka-clients 3.0.0
Bug · Resolved (Not A Problem) · Major · components: clients · created 2022-01-17 · resolved 2022-01-18

I'm having this issue reported here: [https://github.com/spring-projects/spring-kafka/issues/2056]
It is a Spring Boot 2.5.7 application that started failing (out of memory) when updated to Spring Boot 2.6.1.
This updated *kafka-clients {color:#00875a}2.7.1{color}* to *{color:#ff0000}3.0.0{color}* and started causing the memory leak.
The service is using a standard spring *katkaTemplate* to send messages.
[code/log omitted]
This producer is quite heavy (~2.5k messages/s).
My kafka config:…

- **Luke Chen:** [~willian.wd] , thanks for reporting the issue. Did this issue happen in Kafka-clients v2.8.x? Also, did you `flush()` the producer, or set `autoFlush` in spring katkaTemplate?  Thanks.
- **Luke Chen:** And, please also provide the producer config. Thank you.
- **Willian Dallastella:** [~showuon] I just tested with 2.8.1 and also works fine, the issue is just with 3.0.0. Also, there is no auto-flush set, here is my kafka config: [code/log omitted]
- **Luke Chen:** Thanks for the response. I'll investigate it.
- **Luke Chen:** [~willian.wd] , there is a config *ack* set to 1, are you meaning the *acks* config in producer? (ref: [https://kafka.apache.org/documentation/#producerconfigs_acks)] If so, could you help try to remove the *ack* config (i.e, use default `all`) and explicitly add `enable.idempotence=true`, and then…
- _…8 more comments_

## KAFKA-13598: idempotence producer is not enabled by default if not set explicitly
Bug · Resolved (Fixed) · Major · components: clients, config · created 2022-01-18 · resolved 2022-02-07

In KAFKA-10619, we intended to enable idempotence by default, but this was not achieved due to a bug in the config validation logic. The change from acks=1 to acks=all worked correctly, however.
This is the following up for KIP-679: [https://cwiki.apache.org/confluence/display/KAFKA/KIP-679%3A+Producer+will+enable+the+strongest+delivery+guarantee+by+default]
Note: In KAFKA-13673, we'll disable idempotent producer when acks/retries/max.in.flight config conflicts, to avoid breaking existing prod…

- **Ismael Juma:** [~showuon] it would be good to determine if this is a 3.1.0 blocker. cc [~dajac] [~kirktrue]
- **David Jacot:** That seems to be a bug and not a regression introduced in 3.1 so I lean towards fixing it in 3.0.1 and 3.1.1. What do you guys think? I will take a close look into it tomorrow.
- **Luke Chen:** Since the memory leak issue: KAFKA-13597 is confirmed to be a bad dependency version for the interceptor, I think we don't have to fix this in v3.1.0. Thank you.
- **David Jacot:** Sounds good. Thanks [~showuon].
- **Derek Troy-West:** This represents a breaking change where:  # Broker version is < 2.8.0  # Cluster has ACL configured, but no IDEMPOTENT_WRITE permission set  # Producer has default configuration (or no config captured in KAFKA-13673)  # Kafka Client library version is bumped to 3.2.0 in the producing application…
- _…4 more comments_

## KAFKA-13599: Upgrade RocksDB to 6.27.3
Task · Resolved (Fixed) · Major · components: streams · created 2022-01-18 · resolved 2023-02-24

RocksDB v6.27.3 has been released and it is the first release to support s390x. RocksDB is currently the only dependency in gradle/dependencies.gradle without s390x support.
RocksDB v6.27.3 has added some new options that require an update to streams/src/main/java/org/apache/kafka/streams/state/internals/RocksDBGenericOptionsToDbOptionsColumnFamilyOptionsAdapter.java but no other changes are needed to upgrade.
A compatibility report is attached for the current version 6.22.1.1 -> 6.27.3

- **Bruno Cadonna:** Hi [~jonathan.albrecht]!  Thank you for the analysis! Are you interested in opening a PR for the upgrade?
- **Jonathan Albrecht:** Hi [~cadonna], Yes, I'm testing a PR right now. I'm just in the process of requesting to be added to the jira contributer's list so I can assign this to myself.

## KAFKA-13600: Rebalances while streams is in degraded state can cause stores to be reassigned and restore from scratch
Bug · Resolved (Fixed) · Major · components: streams · created 2022-01-19 · resolved 2022-03-28

Consider this scenario:
 # A node is lost from the cluster.
 # A rebalance is kicked off with a new "target assignment"'s(ie the rebalance is attempting to move a lot of tasks - see https://issues.apache.org/jira/browse/KAFKA-10121).
 # The kafka cluster is now a bit more sluggish from the increased load.
 # A Rolling Deploy happens triggering rebalances, during the rebalance processing continues but offsets can't be committed(Or nodes are restarted but fail to commit offsets)
 # The most c…

- **Guozhang Wang:** [~tim.patterson] Thanks for filing this ticket. I'd like to clarify a few things to help my own understanding here: in step 5, "The most caught up nodes now aren't within `acceptableRecoveryLag` and so the task is started in it's "target assignment" location" could you explain a bit more about this…
- **Tim Patterson:** [~guozhang] Thats the desired result and the change I've made. The current Implementation in Master only considers placing the task on nodes returned by this method [https://github.com/apache/kafka/blob/trunk/streams/src/main/java/org/apache/kafka/streams/processor/internals/assignment/HighAvailab…
- **Tim Patterson:** Thinking about it, the same problem can be hit when we lose a node and some of the standby tasks for the lost actives have fallen a bit behind for whatever reason, In this case it wont promote the standbys to actives but instead start restoring those tasks from scratch on some other node
- **Bruno Cadonna:** [~tim.patterson] I checked the assignor code and I agree with you that we only distinguish between caught-up and not caught-up. IIRC, we decided to go that way since considering task load and the rank of non caught-up clients turned out to be more complicated that we wanted to make the assignment al…
- **Tim Patterson:** Thanks [~cadonna]  I'm not sure I have the perfect solution either, more just raising this to point out a bit of a hole in the existing implementation. I do wonder if simply changing the definition of "caught up" in `tasksToCaughtUpClients` from "within acceptableRecoveryLag of the head of the cha…
- _…6 more comments_

## KAFKA-13601: Add option to support sync offset commit in Kafka Connect Sink
New Feature · Resolved (Won't Do) · Major · components: connect · created 2022-01-19 · resolved 2022-04-06

Exactly once in s3 connector with scheduled rotation and field partitioner can be achieved with consumer offset sync' commit after message batch flushed to sink successfully
Currently, WorkerSinkTask committing the consumer offsets asynchronously and at regular intervals of WorkerConfig.OFFSET_COMMIT_INTERVAL_MS_CONFIG 
[https://github.com/apache/kafka/blob/371f14c3c12d2e341ac96bd52393b43a10acfa84/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSinkTask.java#L203]
[https:…

- **Chris Egerton:** [~dasarianil] I don't see how synchronous offset commits would guarantee exactly once. What if the worker dies in between the task writing data and its consumer committing an offset?
- **Anil Dasari:** Filed partitioner uses starting offset of the batch in the file name and is the only varying parameter. There will be only one parquet file per worker (consumer/partition) (that is out of sync with offsets) present in destination (s3 in my case) if worker dies before committing an offset. So new or…
- **Chris Egerton:** Thanks for the clarification! Doesn't that mean that this new behavior wouldn't actually provide exactly-once guarantees? As an aside–I believe that, when configured correctly, the Confluent S3 sink connector already provides exactly-once guarantees (or at least, something close to them) by perform…
- **Anil Dasari:** Hello [~ChrisEgerton] , thanks for the response. new proposed option provides exactly once guarantees in case of field partitioner and size or time rotation based flush strategy considering no duplicates in kafka topic. S3 sink connector can provide exactly once guarantee with async offset commit o…
- **Chris Egerton:** Sorry, I don't think this is correct: {quote}new proposed option provides exactly once guarantees in case of field partitioner and size or time rotation based flush strategy considering no duplicates in kafka topic. {quote} What would be necessary for exactly-once in this situation is either dete…
- _…1 more comments_

## KAFKA-13602: Allow to broadcast a result record
New Feature · Resolved (Fixed) · Major · components: streams · labels: kip, newbie++ · created 2022-01-20 · resolved 2022-12-30

From time to time, users ask how they can send a record to more than one partition in a sink topic. Currently, this is only possible by replicate the message N times before the sink and use a custom partitioner to write the N messages into the N different partitions.
It might be worth to make this easier and add a new feature for it. There are multiple options:
 * extend `to()` / `addSink()` with a "broadcast" option/config
 * add `toAllPartitions()` / `addBroadcastSink()` methods
 * allow S…

- **Florin Akermann:** Hi [~sagarrao] , [~mjsax]  May I have a go at this?
- **Sagar Rao:** Hey @florin , I have already sent out a Kip for this. Here is the link : [https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=211883356.|https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=211883356] Review is awaited still. You can also share your review comments on the d…
- **Florin Akermann:** Ok cool, thanks for the quick reply.
- **A. Sophie Blee-Goldman:** Reverting in 3.4 due to logging-related perf/security issue, and some open semantic questions. Retargeting for 3.5

## KAFKA-13603: empty active segment can trigger recovery after clean shutdown and restart
Improvement · Resolved (Fixed) · Major · created 2022-01-20 · resolved 2022-01-27

Within a LogSegment, the TimeIndex and OffsetIndex are lazy indices that don't get created on disk until they are accessed for the first time. If the active segment is empty at the time of the clean shutdown, the disk will have only the log file but no index files.
However, Log recovery logic expects the presence of an offset index file on disk for each segment, otherwise, the segment is considered corrupted.
We need to address this issue: create the index files for empty active segments durin…

- **Jun Rao:** merged the PR to trunk.

## KAFKA-13604: Add pluggable logging framework support
Improvement · Open · Major · components: connect, core · created 2022-01-20

[discussion thread|https://lists.apache.org/thread/xwgt8ydvnvnqwvhpq2cobgb5wk5mg52t]
As of present, Apache Kafka is using log4j 1.x and planning to migrate into log4j 2.x. Dislike Kafka Streams, it calls log4j's API directly, making it hard for the users to replace the logging framework - also making Kafka vulnerable to log4j's security vulnerabilities.
Apache Kafka (with Connect) is calling log4j's API directly to support the dynamic logger level change feature; SLF4j does not support this fe…


## KAFKA-13605: Checkpoint position in state stores
Sub-task · Resolved (Fixed) · Critical · created 2022-01-20 · resolved 2022-03-24

There are cases in which a state store neither has an in-memory position built up nor has it gone through the state restoration process. If a store is persistent (i.e., RocksDB), and we stop and restart Streams, we will have neither of those continuity mechanisms available. This ticket is to fill in that gap.


## KAFKA-13606: MirrorCheckpointTask doesn't check offsets sync result
Bug · Open · Major · components: mirrormaker · created 2022-01-21

{{MirrorCheckpointTask}} doesn't check the result of calling {{AdminClient#alterConsumerGroupOffsets}} method that could return a failed Future for instance due to incorrect ACL in the target kafka cluster.
[https://github.com/apache/kafka/blob/3.0.0/connect/mirror/src/main/java/org/apache/kafka/connect/mirror/MirrorCheckpointTask.java#L302]
I guess it should at least log or even rethrow the exception.

- **Kvicii.Yu:** hi, [~savulchik] Can you elaborate on how this problem needs to be optimized?
- **Stanislav Savulchik:** Hi, [~Kvicii]. I propose to just log the exception of a returned failed Future in order to make it visible in logs because right now we have no traces of the problem. Re-throwing the exception seems a bad option to me because a task could sync offsets of many consumer groups and we shouldn't preve…
- **Kvicii.Yu:** [~savulchik]  Therefore, my understanding is that we should call partitionResult in the method syncGroupOffset to handle whether an exception occurs, and record the log if an exception occurs.

## KAFKA-13607: Cannot use PEM certificate coding when parent defined file-based
Bug · Open · Major · components: clients, config, connect · created 2022-01-21

The problem applies to the situation when we create a Kafka client based on prepopulated config. If we have only partial control on the input we can attempt to reset some values.
KIP-651 added a new cool feature to use PEM coding of certificates as an alternative to file stores. I have observed a problem in Confluent Replicator. We have shifted the common configuration to the worker level and assumed the connectors define only what is specific for them. The security setup is mTLS, i.e. we need…

- **Kirk True:** [~psmolinski] - if you're working on this, can you assign the Jira to yourself? Thanks.
- **Sergey Ivanov:** Hello, We also faced an issue with DefaultSslEngineFactory.java In our case we use Kafka Connect with config provider, which has the following properties: [code/log omitted] And base on real Kafka connection properties the Conmfig Provider includes coresponding values. For example, for Kafka wit…

## KAFKA-13667: add a constraints in listeners in combined mode
Improvement · Open · Major · components: kraft · created 2022-02-15

While updating the description in example properties file for kraft mode, we think we should add a constraint for "listeners" for combined mode. Both broker listener and controller listener should be explicitly set, to avoid confusion.
Please check this discussion:
[https://github.com/apache/kafka/pull/11616#discussion_r806399392]

- **Deng Ziming:** we can't only list controller listener for `listeners` in combined mode because `advertised.listeners` must be a subset of `listeners` and advertised listener can not be empty. so we must always set both controller and broker listeners.

## KAFKA-13668: Failed cluster authorization should not be fatal for producer
Bug · Resolved (Fixed) · Major · created 2022-02-15 · resolved 2023-05-04

The idempotent producer fails fatally if the initial `InitProducerId` returns CLUSTER_AUTHORIZATION_FAILED. This makes the producer unusable until a new instance is constructed. For some applications, it is more convenient to keep the producer instance active and let the administrator fix the permission problem instead of going into a crash loop. Additionally, most applications will probably not be smart enough to reconstruct the producer instance, so if the application does not handle the error…

- **Luke Chen:** Nice suggestion! We should improve it!
- **Ismael Juma:** cc [~kirktrue]

## KAFKA-13669: Log messages for source tasks with no offsets to commit are noisy and confusing
Bug · Resolved (Fixed) · Major · components: connect · created 2022-02-15 · resolved 2022-02-17

The [messages|https://github.com/apache/kafka/blob/71cbff62b685ef2b6b3169c2e69693687ddf7b3f/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSourceTask.java#L493-L500] that Connect emits during offset commit for source tasks that haven't accrued any new offsets since their last commit are logged at INFO level, which has confused some users who saw them and believed that something was wrong with their connector.
We introduced these fairly recently as part of the work in [http…

- **Jorge Esteban Quilcate Otoya:** I've experienced this messages on Kafka Datagen Source Connector using Confluent Platform (7.0.1) / Apache Kafka 3.0.1. Very confusing, thought there was an issue, but data was still been produced. Lowering the log level to DEBUG make sense to me.
- **Giovanni Marigi:** Seen this with replicator and my customer thought it was an issue. Lowering the log level to DEBUG make sense to me.

## KAFKA-13670: Consume in assign mode, If the group is null, the consumption can still be performed
Bug · Open · Major · components: clients · created 2022-02-16

If consume group is not configured in Assign mode, consumption can still be carried out, but offset is not submitted. However, if subscribe mode is used, the program directly reports an error


## KAFKA-13671: Power (ppc64le) support for kafka
Improvement · Resolved (Fixed) · Major · components: build · created 2022-02-16 · resolved 2022-03-07

Support for Power architecture (ppc64le) for apache kafka.
What is IBM Power architecture?
It is a RISC architecture and IBM has recently made its ISA (Instruction Set Architecture) opensource and in doing so, they have significantly contributed back to the opensource community at large. Many of the pioneers of banking and HPC industries today run on ppc64le architecture.
As an ongoing effort to enable open-source projects where Power architecture can add value, we are trying to enable kafka…

- **Abhijit:** On the ppc64le VM provided to community, I built kafka & ran UT and IT. All passed (one failure that passed on re-run). jdk-11 and scala-2.13 was used. Logs attached. I am yet to hear back on the Jira (https://issues.apache.org/jira/browse/INFRA-22612). A jenkins build stage can be added for ppc64l…
- **Mickael Maison:** I've opened a PR to run unit tests on the ppc64le node. It looks like there's a permission issue as tests are failing to access /tmp: For example: java.nio.file.AccessDeniedException: /tmp/kafka-streams/dummy-topology-test-driver-app-id--1504216085/0_0/.checkpoint See https://ci-builds.apache.org…
- **Abhijit:** I cleared the /tmp dir that contained some stale dirs from previous runs. Now, the unit tests should be able to run.

## KAFKA-13672: Race condition in DynamicBrokerConfig
Bug · Resolved (Fixed) · Blocker · created 2022-02-16 · resolved 2022-03-24

Stacktrace:
[code/log omitted]
Job: https://ci-builds.apache.org/job/Kafka/job/kafka-pr/job/PR-11751/5/testReport/

- **Bruno Cadonna:** https://ci-builds.apache.org/job/Kafka/job/kafka-pr/job/PR-11752/8/testReport/kafka.server/DynamicBrokerReconfigurationTest/Build___JDK_11_and_Scala_2_13___testThreadPoolResize__/ [code/log omitted]
- **Liam Clarke-Hutchinson:** I've renamed this issue (was {_}Flaky test {{kafka.server.DynamicBrokerReconfigurationTest.testThreadPoolResize()}}{_}) because the test was actually exposing a race condition in {{DynamicBrokerConfig}} that occurred when the broker under test was running sufficiently slowly. Many thanks are due to…
- **Luke Chen:** Great to hear that! But I'm wondering why this happened recently only, not before? Did we change anything cause that?

## KAFKA-13673: disable idempotent producer when acks/retries/max.in.flight config conflicts
Improvement · Resolved (Fixed) · Major · created 2022-02-17 · resolved 2022-03-03

In KAFKA-13598, we enabled idempotent producer by default. When idempotence is enabled, there are some constraints:
 - acks=all
 - retries > 0
 - max.in.flight.requests.per.connection <= 5
We found the default idempotence enabled setting will break some tests because the `acks`, `retries` config are overridden, and conflict with idempotence. And we believe there are many users also overriding these configs in current producers. We should avoid to break the existing producers after user upgra…


## KAFKA-13674: Failure on ZOS due to IOException when attempting to fsync the parent directory
Bug · Resolved (Fixed) · Major · components: clients · labels: pull-request-available · created 2022-02-17 · resolved 2022-02-28

It appears to be the similar issue with  [KAFKA-13391|https://issues.apache.org/jira/browse/KAFKA-13391] on ZOS due to fsync the parent directory. Kafka 3.0.0 failed to start on z/OS against the below error:
{panel}
ERROR Error while writing to checkpoint file /xxxx/recovery-point-offset-checkpoint (kafka.server.LogDirFailureChannel) java.io.IOException: EDC5121I Invalid argument.
 at kafka.log.LogManager$$Lambda$553/0x00000000067b3f30.apply(Unknown Source)
 at kafka.log.LogManager$$Lambda$5…

- **Hong Yi Zhang:** https://github.com/apache/kafka/pull/11793
- **Hong Yi Zhang:** Code has been merged into the trunk in the below PR: https://github.com/apache/kafka/pull/11793

## KAFKA-13675: Null pointer exception with kafka streams application reset tool with --to-datetime
Bug · Open · Major · created 2022-02-17

When I try to run the the reset tool with {{{}--to-datetime{}}}, such as:
[code/log omitted]
{{I get the following exception}}
[code/log omitted]
Note when I run the above with --to-earliest or --to-offset instead of {{-to-datetime, the tool runs successfully.}}

- **Bruno Cadonna:** [~pcallahan] thank you for the report, This seems to be a duplicate of https://issues.apache.org/jira/browse/KAFKA-9527. Could you confirm that this is fixed in 3.0.0?

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


## KAFKA-13717: KafkaConsumer.close throws authorization exception even when commit offsets is empty
Bug · Resolved (Fixed) · Major · components: unit tests · created 2022-03-08 · resolved 2022-03-10

When offsets is empty and coordinator is unknown, KafkaConsumer.close doesn't throw exception before commit [https://github.com/apache/kafka/commit/4b468a9d81f7380f7197a2a6b859c1b4dca84bd9|https://github.com/apache/kafka/commit/4b468a9d81f7380f7197a2a6b859c1b4dca84bd9,].  After this commit, Kafka.close may throw authorization exception.
Root cause is because in the commit, the logic is changed to call lookupCoordinator even if offsets is empty. 
Even if a consumer doesn't have access to a grou…


## KAFKA-13718: kafka-topics describe topic with default config will show `segment.bytes` overridden config 
Bug · Resolved (Fixed) · Major · components: tools · labels: newbie, newbie++ · created 2022-03-08 · resolved 2022-06-03

Following the quickstart guide[1], when describing the topic just created with default config, I found there's a overridden config shown:
_> bin/kafka-topics.sh --describe --topic quickstart-events --bootstrap-server localhost:9092_
_Topic: quickstart-events   TopicId: 06zRrzDCRceR9zWAf_BUWQ    PartitionCount: 1    ReplicationFactor: 1    *Configs: segment.bytes=1073741824*_
    _Topic: quickstart-events    Partition: 0    Leader: 0    Replicas: 0    Isr: 0_
This config result should be empt…

- **Mickael Maison:** This has been the case for many releases, I get the same behavior with 2.2.0. At this stage, it probably makes more sense to update the quickstart.
- **Luke Chen:** >  I get the same behavior with 2.2.0. Oh, really! > it probably makes more sense to update the quickstart. Maybe we can have a better definition about what we expected to be shown in the `configs` value. My understanding is it showed the overridden configs. If so, it should be a bug. If not, we…
- **Richard Joerger:** I'd love to help out on this particular Jira. I'm new to the project so I apologize for any silly questions. It seems that we as a community need to discuss what the output of the kafka-topics tooling should look like. When we're looking at the documentation, I don't see any documentation explicitly…
- **Deng Ziming:** Hello [~rjoerger]   # this issue is enough to track the problem so another issue is unnecessary  # We are not intend to include default `segment.bytes` in the output but it was printed(due to an bug), but this bug has been around for a long time so [~mimaison] suggest we keep this bug in the futur…
- **Luke Chen:** Thanks for the answers, [~dengziming] ! [~rjoerger] , as Ziming said, we are unsure the root cause of this issue. Maybe you can investigate it first, and see if you find anything. My thought is that, since we didn't provide any new configs during create topics: _> bin/kafka-topics.sh --create --to…
- _…4 more comments_

## KAFKA-13719: connector restart cause duplicate tasks
Bug · Resolved (Fixed) · Critical · components: connect · created 2022-03-09 · resolved 2022-03-30

Restart connector with parameter includeTasks=true&onlyFailed=false cause duplicate tasks and duplicate message。


## KAFKA-13720: Few topic partitions remain under replicated after broker lose connectivity to zookeeper
Bug · Resolved (Fixed) · Major · components: controller · created 2022-03-09 · resolved 2022-06-17

Few topic partitions remain under replicated after broker lose connectivity to zookeeper.
It only happens when brokers lose connectivity to zookeeper and it results in change in active controller. Issue does not occur always but randomly.
Issue never occurs when there is no change in active controller when brokers lose connectivity to zookeeper.
Following error message i found in the log file.
[2022-02-28 04:01:20,217] WARN [Partition __consumer_offsets-4 broker=1] Controller failed to updat…

- **Dhirendra Singh:** Some more information split brain issue is happening with the controller. when brokers (including the active controller) lose connection with zookeeper, for few seconds 2 brokers are the active controller. following is the log of broker 1 and broker 0. At the time when connection to zookeeper was…
- **Luke Chen:** [~dhirendraks@gmail.com], thanks for reporting the issue. I can confirm this issue is fixed (indirectly) in Kafka v3.1 and later. The root cause of this issue is that when controller is changing, the ISR update request should keep retrying, until the "real" controller got this request. So, in the lo…
- **Luke Chen:** KAFKA-14010 is created to make sure it works as expected, although after v3.1.0, the AlterIsr request will send to Controller "as long as the follower keeps fetching data from leader"

## KAFKA-13721: Left-join still emit spurious results in stream-stream joins in some cases
Bug · Resolved (Fixed) · Major · components: streams · created 2022-03-09 · resolved 2022-03-15

Stream-stream joins seems to still emit spurious results for some window configurations.
From my tests, it happened when setting before to 0 and having a grace period smaller than the window duration. More precisely it seems to happen when setting before and 
window duration > grace period + before
h2. how to reproduce
[code/log omitted]
Stdout of previous code is
[code/log omitted]
However it should be
[code/log omitted]


## KAFKA-13722: Update internal interfaces that use ProcessorContext to use StateStoreContext instead
Improvement · Reopened · Major · components: streams · created 2022-03-09

This is a remainder that when we remove the deprecated public APIs that uses the ProcessorContext, like `StateStore.init`, we should also consider updating the internal interfaces with the ProcessorContext as well. That includes:
1. Segments and related util classes which use ProcessorContext.
2. For state stores that leverage on ProcessorContext.getXXXTime, their logic should be moved out of the state store impl but to the processor node level that calls on these state stores.

- **Matthias J. Sax:** We needed to revet one PR for 4.1 release, as it introduces a regression bug: [https://github.com/apache/kafka/pull/18292] Re-opening to make sure we complete this issue with 4.2 release – as we did only revert in 4.1 branch, but not in trunk, also filed https://issues.apache.org/jira/browse/KAFKA-…

## KAFKA-13723: max.compaction.lag.ms implemented incorrectly
Bug · Resolved (Not A Problem) · Major · components: core · created 2022-03-09 · resolved 2022-03-09

In https://issues.apache.org/jira/browse/KAFKA-7321, we introduced max.compaction.lag.ms to guarantee that a record be cleaned before a certain time. 
The implementation in LogCleanerManager has the following code. The path for earliestDirtySegmentTimestamp < cleanUntilTime seems incorrect. In that case, it seems that we should set the delay to 0 so that we could trigger cleaning immediately since the segment has been dirty for longer than max.compaction.lag.ms. 
[code/log omitted]

- **Jun Rao:** [~xiongqiwu] and [~jjkoshy]  : Could you check if this is a real issue? Thanks.
- **xiongqi wu:** [~junrao]  Hi Jun, this function is supposed to capture violation that pass-by the max compaction delay.  e.g,  if maxCompactionDelay > 0, which mean it has violated the policy (e.g, the log is not compacted within the maxCompaction config time), and the log should be compact immediately.  if max…
- **Jun Rao:** [~xiongqiwu] : Thanks for the explanation. Make sense. So, this is not an issue.

## KAFKA-13724: Fix Vulnerability CVE-2021-43859 - Upgrade com.thoughtworks.xstream_xstream
Bug · Open · Major · created 2022-03-09

Our security scanner detected the following vulnerablity. Please upgrade to version noted in Fix Status column.
|CVE ID|Severity|Packages|Package Version|CVSS|Fix Status|
|CVE-2021-43859|high|com.thoughtworks.xstream_xstream|1.4.18|7.5|fixed in 1.4.19|


## KAFKA-13725: KIP-768 OAuth code mixes public and internal classes in same package
Bug · Resolved (Fixed) · Major · components: clients, security · labels: OAuth · created 2022-03-09 · resolved 2022-09-23

The {{org.apache.kafka.common.security.oauthbearer.secured}} package from KIP-768 incorrectly mixed all of the classes (public and internal) in the package together.
This bug is to remove all but the public classes from that package and move the rest to a new {{{}org.apache.kafka.common.security.oauthbearer.internal.{}}}{{{}secured{}}} package. This should be back-ported to all versions in which the KIP-768 OAuth work occurs.


## KAFKA-13726: Fix Vulnerability CVE-2022-23181 -Upgrade org.apache.tomcat.embed_tomcat-embed-core
Bug · Open · Major · created 2022-03-09

Our security scanner detected the following vulnerablity. Please upgrade to version noted in Fix Status column.
|CVE ID|Severity|Packages|Package Version|CVSS|Fix Status|
|CVE-2022-23181|high|org.apache.tomcat.embed_tomcat-embed-core|9.0.54|7|fixed in 10.0.0, 9.0.1|

- **Shivakumar:** getting this vulnerability in *3.1.1 Kafka* version as well.

## KAFKA-13727: Edge case in cleaner can result in premature removal of ABORT marker
Bug · Resolved (Fixed) · Major · created 2022-03-11 · resolved 2022-03-15

The log cleaner works by first building a map of the active keys beginning from the dirty offset, and then scanning forward from the beginning of the log to decide which records should be retained based on whether they are included in the map. The map of keys has a limited size. As soon as it fills up, we stop building it. The offset corresponding to the last record that was included in the map becomes the next dirty offset. Then when we are cleaning, we stop scanning forward at the dirty offset…

- **Jason Gustafson:** I realized that this bug is more likely to occur than I first suspected. In fact, it only requires one incomplete cleaner pass over a segment. The problem is that the first pass fails to recreate the transaction index correctly since the aborted transactions are incomplete. Effectively the data from…

## KAFKA-13753: Log cleaner should retain transaction metadata in index until corresponding marker is removed
Bug · Open · Major · created 2022-03-17

Currently the log cleaner will remove aborted transactions from the index as soon as it detects that the data from the transaction is gone. It does not wait until the corresponding marker has also been removed. Although it is extremely unlikely, it seems possible today that a Fetch might fail to return the aborted transaction metadata correctly if a log cleaning occurs concurrently. This is because the collection of aborted transactions is only done after the reading data from the log. It would…


## KAFKA-13754: Follower should reject Fetch request while the leader is recovering
Task · Open · Major · created 2022-03-17

In the PR for KIP-704 we removed leader recovery state validation from the FETCH. This is okay because the leader immediately recovers the partition.
We should enable this validation before implementing log recovery from unclean leader election.
The old implementation and test is in this commit: https://github.com/apache/kafka/pull/11733/commits/c7e54b8f6cef087deac119d61a46d3586ead72b9


## KAFKA-13755: Broker heartbeat event should have deadline
Bug · Resolved (Fixed) · Minor · components: controller · labels: kip-500 · created 2022-03-18 · resolved 2022-06-19

When we schedule the event for processing the broker heartbeat request in QuroumController, we do not give a deadline. This means that the event will only be processed after all other events which do have a deadline. In the case of the controller's queue getting filled up with deadline (i.e., "deferred") events, we may not process the heartbeat before the broker attempts to send another one.

- **Bruno Cadonna:** Removing from the 3.2.0 release since code freeze has passed.
- **Colin McCabe:** As of 3.3, we now use {{config.brokerHeartbeatIntervalMs}} as the deadline It should be a good improvement for clusters under load

## KAFKA-13756: Connect validate endpoint should return proper response for invalid connector class
Improvement · Patch Available · Major · components: connect · created 2022-03-21

Currently, if there is an issue with  the connector class, the validate endpoint returns a 400 or a 500 response.
Instead, it should return a well formatted response containing a proper validation error message.


## KAFKA-13757: Improve the annotations of all related methods of DelegationToken in the Admin class
Improvement · Open · Major · components: admin · created 2022-03-22

DelegationToken is a great and lightweight feature, but when users actually use it, they get confused.
From the existing official documents/comments on methods/comments on method parameters, the user cannot know what is the specific processing logic of the server and what is the meaning of the returned fields after he calls the XXXDelegationToken(...) method.
After reading the source code, I briefly sorted out the processing logic of the XXXDelegationToken(...) method on the server side.
1. c…

- **RivenSun:** Hi [~omkreddy]  [~guozhang] and  [~showuon]  Could you give some advice? Thanks.
- **RivenSun:** Hi [~dajac]  [~rsivaram] Could you give some suggestions for this issue? Thanks.

## KAFKA-13758: Exclusive locking in kafka.coordinator.group.GroupMetadata.inLock(GroupMetadata.scala:227
Bug · Open · Major · created 2022-03-22

{quote} [2022-03-22 15:15:03,127] *ERROR* [GroupMetadataManager brokerId=#] Appending metadata message for group ... failed due to unexpected *error:* _org.apache.kafka.common.errors.UnknownServerException_ (kafka.coordinator.group.GroupMetadataManager){quote}
Probably Issues is here: CoreUtils.scala inLock()
  /**
   * Execute the given function inside the lock
   */
  def inLock[T](lock: Lock)(fun: => T): T = {
    lock.lock()
    try {
      fun
    } finally {
      lock.unlock()…

- **Sree Vaddi:** Work Around: - restart the broker node. ({*}tried and worked{*}) - clear the lock file of offset / partition / consumer / consumer group in zk data.folder.

## KAFKA-13759: Disable producer idempotence by default in producers instantiated by Connect
Bug · Resolved (Fixed) · Major · components: connect · created 2022-03-22 · resolved 2022-03-23

https://issues.apache.org/jira/browse/KAFKA-7077 was merged recently referring to KIP-318. Before that in AK 3.0 idempotence was enabled by default across Kafka producers. 
However, some compatibility implications were missed in both cases. 
If idempotence is enabled by default Connect won't be able to communicate via its producers with Kafka brokers older than version 0.11. Perhaps more importantly, for brokers older than version 2.8 the {{IDEMPOTENT_WRITE}} ACL is required to be granted to t…

- **Konstantine Karantasis:** This issue has been now been merged on the 3.2 and 3.1 branches to avoid a breaking change when Connect contacts older brokers and idempotence is enabled in the producer by default.  [~cadonna] [~tombentley] fyi.  Hopefully this fix makes to the upcoming releases but please let me know if the targ…

## KAFKA-13760: Kafka 2.8.1 : log clean skip __consumer__offsets-45
Bug · Open · Major · components: log cleaner · created 2022-03-23

I upgraded Kafka from 2.12_2.4.1 to 2.13_2.8.1 version. From then, __consumer_offsets-45 log cannot clean.
kafka version：2.13_2.8.1
jdk version: openjdk 11.0.2
linux version: 4.4.71-1.el7.elrepo.x86_64 (mockbuild@Build64F25) (gcc version 4.8.5 20150623 (Red Hat 4.8.5-11) 
log-cleaner.log info
[code/log omitted]
cleaner-offset-checkpoint info 
[code/log omitted]


## KAFKA-13761: KafkaLog4jAppender deadlocks when idempotence is enabled
Bug · Resolved (Fixed) · Major · components: log · created 2022-03-23 · resolved 2024-11-03

KafkaLog4jAppender instantiates a KafkaProducer to append log entries to a Kafka topic. The producer.send operation may need to acquire locks during its execution. This can result in deadlocks when a log entry from the producer network thread is also at a log level that results in the entry being appended to a Kafka topic (KAFKA-6415).
[https://github.com/apache/kafka/pull/11691] enables idempotence by default, and it introduced another place where the producer network thread can hit a deadlock…

- **Luke Chen:** Nice find!
- **Ismael Juma:** I think we probably want to disable idempotence for the log4j appender.
- **Luke Chen:** [~ijuma] , I agree. And we should further throw exception to note users that log4j appender doesn't support idempotent producer before this bug is fixed. After all, log4j appender is depredated in KIP-719, and should be removed in the future. WDYT?
- **Dongjin Lee:** Hi [~yyu1993] [~showuon], It seems like this issue is a counterpart of LOG4J2-3256, which disables logging from {{org.apache.kafka.common}} and {{org.apache.kafka.clients}} packages. How about add a similar logic to log4j-appender?
- **Ismael Juma:** I suggest we do the simplest change first (disable idempotence) and then follow up with more complicated change.
- _…1 more comments_

## KAFKA-13762: Kafka brokers are not coming up 
Bug · Open · Blocker · created 2022-03-23

Out of 9 brokers only 3 brokers coming up. Totally 3 VMs Each VM is having 3 brokers
We are getting below error 
Exception in thread "main" java.lang.reflect.InvocationTargetException

- **Jordan Moore:** [~kkameshm90] Please lower the priority as it is not a project blocker. Your error is caused by the JMX exporter from Prometheus you've custom added to your broker startup process, and so is really unrelated to any issues with Kafka project. You need to stop whatever other process has already boun…

## KAFKA-13763: Improve unit testing coverage and flexibility for IncrementalCooperativeAssignor
Improvement · Resolved (Done) · Minor · components: connect · created 2022-03-23 · resolved 2022-05-12

The [tests|https://github.com/apache/kafka/blob/dcd09de1ed84b43f269eb32fc2baf589a791d468/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/distributed/IncrementalCooperativeAssignorTest.java] for the {{IncrementalCooperativeAssignor}} class provide a moderate level of coverage and cover some non-trivial cases, but there are some areas for improvement that will allow us to iterate on the assignment logic for Kafka Connect faster and with greater confidence.
These improvements includ…

- **Chris Egerton:** Discussed earlier during review of https://github.com/apache/kafka/pull/10367

## KAFKA-13802: Uncaught exception in scheduled task 'flush-log' (kafka.utils.KafkaScheduler)
Bug · Resolved (Fixed) · Major · created 2022-04-06 · resolved 2022-04-11

Apr 06 07:13:18 kafka07-messaging-ovh kafka-server-start.sh[1569498]: [2022-04-06 07:13:18,962] ERROR Uncaught exception in scheduled task 'flush-log' (kafka.utils.KafkaScheduler)
Apr 06 07:13:18 kafka07-messaging-ovh kafka-server-start.sh[1569498]: java.util.NoSuchElementException
Apr 06 07:13:18 kafka07-messaging-ovh kafka-server-start.sh[1569498]:         at java.base/java.util.concurrent.ConcurrentSkipListMap$SubMap$SubMapIter.advance(Unknown Source)
Apr 06 07:13:18 kafka07-messaging-ovh…

- **Luke Chen:** Fixed in [#11605|https://github.com/apache/kafka/pull/11605]

## KAFKA-13803: Refactor Leader API Access
Improvement · Resolved (Fixed) · Major · created 2022-04-06 · resolved 2022-06-03

Currently, AbstractFetcherThread has a series of protected APIs which control access to the Leader. ReplicaFetcherThread and ReplicaAlterLogDirsThread respectively override these protected APIs and handle access to the Leader in a remote broker leader and a local leader context.
We propose to move these protected APIs to a LeaderEndPoint interface, which will serve all fetches from the Leader. We will implement a RemoteLeaderEndPoint and a LocalLeaderEndPoint accordingly. This change will great…

- **Jun Rao:** merged the PR to trunk

## KAFKA-13804: Log broker shutdown reason during startup at the end of log output
Improvement · Resolved (Fixed) · Major · components: core · created 2022-04-07 · resolved 2022-05-06

Currently, when the broker hit exception during startup, we will first log the exception, ex:
_ERROR [KafkaServer id=0] Fatal error during KafkaServer startup. Prepare to shutdown (kafka.server.KafkaServer)_
_java.io.IOException: No space left on device_
And then go through the shutdown process, to close all the resources (i.e. threads, sockets, metrics...), and in the end, output:
_[KafkaServer id=0] shut down completed (kafka.server.KafkaServer)_
_ERROR Exiting Kafka (kafka.Kafka$)_
Some…


## KAFKA-13805: Upgrade vulnerable dependencies march 2022
Bug · Resolved (Fixed) · Blocker · labels: secutiry · created 2022-04-07 · resolved 2023-01-12

https://nvd.nist.gov/vuln/detail/CVE-2020-36518
|Packages|Package Version|CVSS|Fix Status|
|com.fasterxml.jackson.core_jackson-databind| 2.10.5.1| 7.5|fixed in 2.13.2.1|
|com.fasterxml.jackson.core_jackson-databind|2.13.1|7.5|fixed in 2.13.2.1|
Our security scan detected the above vulnerabilities
upgrade to correct versions for fixing vulnerabilities

- **Bruno Cadonna:** [~shivakumar] Are you referring to the following CVE? https://nvd.nist.gov/vuln/detail/CVE-2020-36518 This CVE seems to affect 2.8.1, 3.0.1 but not 3.1.1 and 3.2.0 since the latter ones use 2.12.6.1 (see  KAFKA-13658).
- **Kirk True:** According to [https://mvnrepository.com/artifact/com.fasterxml.jackson.core/jackson-databind,] 2.13.0 still has the vulnerability. 2.13.2.1 looks to be the first version in the 2.13.x line that has the fix.
- **Bruno Cadonna:** [~kirktrue] Under "Known Affected Software Configurations" the CVE says "Up to (excluding) 2.12.6.1". We are not using the 2.13.x line.
- **Kirk True:** [~cadonna] - Sorry for the confusion... I was mentioning the 2.13.x line because the description stated that the issue was "fixed in 2.13.0", which I don't believe is accurate.
- **Bruno Cadonna:** [~kirktrue] Ah, got it! You are right! I updated the description.
- _…1 more comments_

## KAFKA-13806: Check CRC when reading snapshots
Sub-task · Resolved (Duplicate) · Major · created 2022-04-07 · resolved 2022-07-26


## KAFKA-13807: Ensure that we can set log.flush.interval.ms with IncrementalAlterConfigs
Bug · Resolved (Fixed) · Major · created 2022-04-07 · resolved 2022-05-19


## KAFKA-13808: Mirrormaker2  stop sync data when modify topic partition in "Running a dedicated MirrorMaker cluster" mode
Bug · Closed (Duplicate) · Major · components: connect, mirrormaker · created 2022-04-08 · resolved 2022-04-14

When use the mirrormaker2 with the "Running a dedicated MirrorMaker cluster" mode by 3 nodes, once we modify the topic partition , then the mm2 stop sync data with the following ERROR :
[2022-02-18 10:26:19,410] ERROR Error forwarding REST request (org.apache.kafka.connect.runtime.rest.RestClient)
java.lang.IllegalArgumentException: Invalid URI host: null (authority: null)
    at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:515)
    at java.base/java.util.conc…

- **Chris Egerton:** This is a duplicate of https://issues.apache.org/jira/browse/KAFKA-9981. [~jitabc] if you'd like to work on this issue can you link it to that ticket instead of this one, and leave any comments there instead of here? Thanks!
- **YANGLiiN:** yeah，same as the https://issues.apache.org/jira/browse/KAFKA-9981
- **YANGLiiN:** 3.5.0 fixed.

## KAFKA-13809: FileStreamSinkConnector and FileStreamSourceConnector should propagate full configuration to tasks
Improvement · Resolved (Fixed) · Major · components: connect · created 2022-04-08 · resolved 2022-08-15

The 2 example connectors do not propagate the full connector configuration to the tasks. This makes it impossible to override built-in configs, such as producer/consumer overrides.
This causes an issue even when used for testing purposes.

- **Daniel Urban:** Connector configs are used for consumer/producer overrides, converter classes, etc. Not necessary to propagate all configs to tasks.
- **Chris Egerton:** [~durban] FWIW this would actually still serve some value as long as https://issues.apache.org/jira/browse/KAFKA-9228 is open since the only known workaround (which just happens to be implemented by nearly every connector out there _except_ for the file stream connectors) is exactly what's proposed…

## KAFKA-13810: Document behavior of KafkaProducer.flush() w.r.t callbacks
Improvement · Resolved (Fixed) · Major · created 2022-04-08 · resolved 2025-01-23

The javadoc (3.1.0) for KafkaProducer says
{panel}
The post-condition of {{flush()}} is that any previously sent record will have completed (e.g. {{{}Future.isDone() == true{}}}). 
{panel}
It does not say anything about callbacks, though. It is not clear whether all callbacks have returned when {{flush()}} returns.

- **Luke Chen:** [~kspang_impala_76b0] , are you interested in submitting a PR to improve it?
- **Karsten Spang:** [~showuon] I assume that all callbacks are supposed to be called, but I am not sure. If I am right, I can update the javadoc accordingly.
- **Luke Chen:** Yes, after flush, all the requests are completed, which also means all producer callback is called.
- **Karsten Spang:** [~showuon] Please trigger a build.

## KAFKA-13811: Investigate sliding windows performance
Task · Open · Major · components: streams · labels: perfomance · created 2022-04-08

We recently fixed a bug in sliding windows so that a grace period of 0ms is properly calculated, see https://issues.apache.org/jira/browse/KAFKA-13739. Before this patch, sliding windows with a grace period of 0ms would just skip all records so nothing would get put into the store.
When we ran benchmarks for the 3.2 release we saw a significant drop in performance for sliding windows on both the 3.2 and trunk branches, see the `sliding windows` results [here|[http://kstreams-benchmark-results.s…


## KAFKA-13812: Kraft TopicsDelta finishSnapshot maybe loss data
Bug · Resolved (Not A Bug) · Major · created 2022-04-09 · resolved 2022-04-09

kafka.server.metadata.BrokerMetadataListener.HandleCommitsEvent will restore the image from the snapshot and delete the topic not in the snapshot, but if a topic has been created, and start producing data, when the broker restores the snapshot which does not contain the new topic, it will delete the new topic and the data will lost.


## KAFKA-13868: Website updates to satisfy Apache privacy policies
Bug · Resolved (Fixed) · Critical · components: website · created 2022-05-03 · resolved 2022-07-28

The ASF has updated its privacy policy and all websites must be compliant.
The full guidelines can be found in [https://privacy.apache.org/faq/committers.html]
The Kafka website has a few issues, including:
- It's missing a link to the privacy policy: [https://privacy.apache.org/policies/privacy-policy-public.html]
- It's using Google Analytics
- It's using Google Fonts
- It's using scripts hosted on Cloudflare CDN
- Embedded videos don't have an image placeholder
As per the email sent t…

- **ASF GitHub Bot:** divijvaidya opened a new pull request, #420: URL: https://github.com/apache/kafka-site/pull/420    As per the [Apache privacy policy](https://privacy.apache.org/faq/committers.html), Google Fonts are recommended to be hosted along with the website.    This change  adds the fonts locally in the code…
- **Divij Vaidya:** Fixed "It's using Google Fonts" -> [https://github.com/apache/kafka-site/pull/420]  [~mimaison] please review.
- **ASF GitHub Bot:** divijvaidya commented on PR #420: URL: https://github.com/apache/kafka-site/pull/420#issuecomment-1183179393    @ijuma @mimaison please review.
- **ASF GitHub Bot:** divijvaidya opened a new pull request, #421: URL: https://github.com/apache/kafka-site/pull/421    **Why**    As per the [Apache branching policy](https://www.apache.org/foundation/marks/pmcs#navigation), every project website's main navigation system must feature certain text links back to key pag…
- **Divij Vaidya:** Addressed "It's missing a link to the privacy policy" -> [https://github.com/apache/kafka-site/pull/421] cc: [~mimaison] for review
- _…44 more comments_

## KAFKA-13869: Update quota callback metadata in KRaft
Bug · Resolved (Duplicate) · Major · labels: kip-500 · created 2022-05-03 · resolved 2025-07-22

The `ClientQuotaCallback` interface implements a method `updateClusterMetadata`, which allows the callback to take partition assignments into account when assigning quotas. For zk , this method is called after receiving `UpdateMetadata` requests from the controller. We do not yet have this implemented in KRaft for updates from the metadata log.


## KAFKA-13870: support both Suppressed untilTimeLimit and maxBytes without using emitEarlyWhenFull()
New Feature · Open · Major · labels: needs-kip · created 2022-05-04

My use case is to use  ** *untilTimeLimit* with *maxBytes,* but when the buffer is full, the application is breaking, but with using *{{emitEarlyWhenFull}}* {{{}application is not breaking but{}}}{*}{{}}{*} it sends out the same key record multiple times in a particular window when the buffer exceeds max bytes 
for eg:-
*Suppressed.untilTimeLimit(Duration.ofMinutes(15),Suppressed.BufferConfig.maxBytes(10000).emitEarlyWhenFull())*
messages flow : (A,1) (A,2) (A,3) -> aggregation result : (A,6)…

- **Matthias J. Sax:** I think you mix up two concepts: windowing is about "grouping" records according to their timestamp. Thus, the _window-size_ you define via `TimeWindows.withSizeAndGrace()` (or similar) defines into which window a record falls into. On the other hand suppression has nothing to do with the definitio…

## KAFKA-13871: The documentation for the configuration item QUORUM_FETCH_TIMEOUT of the RaftConfig class is incorrect
Improvement · Closed (Fixed) · Minor · components: kraft · created 2022-05-04 · resolved 2022-05-13

The syntax of the field QUORUM_FETCH_TIMEOUT_MS_DOC is incorrect. `a election`  should be changed to `an election`.
[code/log omitted]

- **lqjacklee:** https://github.com/apache/kafka/pull/12132

## KAFKA-13872: Partitions are truncated when leader is replaced
Bug · Resolved (Won't Fix) · Major · created 2022-05-04 · resolved 2023-08-31

Sample setup:
 * a topic with one partition and RF=3
 * a producer using acks=1
 * min.insync.replicas to 1
 * 3 brokers 1,2,3
 * Preferred leader of the partition is brokerId 0
Steps to reproduce the issue
 * Producer keeps producing to the partition, leader is brokerId=0
 * At some point, replicas 1 and 2 are falling behind and removed from the ISR
 * The leader broker 0 has an hardware failure
 * Partition transition to offline
 * This leader is replaced with a new broker with an e…

- **Luke Chen:** [~fvisconte] , thanks for reporting the issue. But I think this is the expected behavior, isn't it? We always take the logs in partition leader as source of truth. I'd like to know what your expected behavior is in this case. Thanks.
- **Francois Visconte:** I was expecting the partition to stay offline until I decide to set the unclean.leader.election to true and one of the lagging replica to take ownership
- **Jack Vanlightly:** I presume you would need to perform a broker decommissioning process to remove that broker from the cluster before adding a new empty broker with the same id? Is there documentation for how to decommission a dead broker safely?
- **Francois Visconte:** transitioning to won't fix as this seems the expected behaviour.
- **Jack Vanlightly:** This will be fixed by KIP-966. [https://cwiki.apache.org/confluence/display/KAFKA/KIP-966%3A+Eligible+Leader+Replicas.]

## KAFKA-13873: Add ability to Pause / Resume KafkaStreams Topologies
New Feature · Resolved (Fixed) · Major · components: streams · labels: kip · created 2022-05-04 · resolved 2022-06-16

In order to reduce resources used or modify data pipelines, users may want to pause processing temporarily.  Presently, this would require stopping the entire KafkaStreams instance (or instances).  
This work would add the ability to pause and resume topologies.  When the need to pause processing has passed, then users should be able to resume processing.
KIP-834: [https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=211882832]


## KAFKA-13874: Avoid synchronization in SocketServer metrics
Improvement · Open · Major · created 2022-05-05

For performance reasons, we should avoid synchronization in SocketServer metrics like NetworkProcessorAvgIdlePercent


## KAFKA-13875: update docs to include topoicId for kafka-topics.sh --describe output
Improvement · Resolved (Fixed) · Major · components: admin · labels: newbie · created 2022-05-05 · resolved 2023-06-23

The topic describe output in quickstart doc here: [https://kafka.apache.org/quickstart] should be updated now.
[code/log omitted]
After Topic Id implementation, we included the topic id info in the output now. Also the configs is not empty now. The doc should be updated to avoid new users get confused.

- **Richard Joerger:** The Jira which was blocking this previously has been resolved. Please let me know in the PR if there are any other changes which should be made to the documentation. Thanks!
- **Manyanda Chitimbo:** Closing the Jira as it has been fixed by https://github.com/apache/kafka/pull/12170

## KAFKA-13876: Mirrormaker-2 consumer settings not working
Bug · Open · Minor · components: mirrormaker · created 2022-05-05

I am starting a mirrormaker connect cluster using ./bin/connect-mirror-maker.sh and a properties file.
I followed the guide at [https://github.com/apache/kafka/tree/trunk/connect/mirror] to attempt to configure the consumer properties, however, no matter what I set, the timeout for the consumer remains fixed at the default, confirmed both by kafka outputting its config in the log and by timing how long between disconnect messages I get.  e.g. I set:
{{CLOUD_EU.consumer.request.timeout.ms=12000…


## KAFKA-13877: Flaky RackAwarenessIntegrationTest.shouldDistributeStandbyReplicasOverMultipleClientTags
Bug · Resolved (Fixed) · Major · components: streams, unit tests · labels: newbie · created 2022-05-05 · resolved 2022-08-03

The following test fails on local testbeds about once per 10-15 runs:
[code/log omitted]

- **Levani Kokhreidze:** I will take this on.
- **Guozhang Wang:** Thanks [~lkokhreidze]!
- **Guozhang Wang:** Hello [~lkokhreidze], are you still actively working on this flaky test?
- **Guozhang Wang:** [~lkokhreidze] ping again, please let me know if you are still working on it.
- **Guozhang Wang:** I've re-tested this case locally with 5+ times, each with 50 runs, and identified it is a flakiness by itself, not a real bug. The fix is summarized in https://github.com/apache/kafka/pull/12468. On a side note, I think it's an overkill to really introduce the whole test class as an integration tes…

## KAFKA-13878: Connect deadlock in WorkerConnector on desired state change
Bug · Open · Major · components: connect · created 2022-05-05

We've experienced multiple instances of deadlocks where the connector thread is blocked indefinitely with the following stacktrace:
[code/log omitted]
This appears to be caused by a race condition where a notify() is never delivered to a task, causing the connector thread to wait indefinitely for a notify() call that never comes.
This causes the connector to be unable to process further state changes, or generate task configurations.


## KAFKA-13934: Consider consolidating TimeWindow / SessionWindow / SlidingWindow
Improvement · Open · Major · components: streams · labels: needs-kip · created 2022-05-24

In Streams windowing operations we have several inherited classes from `Window`, as listed in the title of the ticket. They represent differences for:
1) Serialization of the window as part of the windowed key.
2) Window operations which is based on inclusive/exclusiveness of the window start/end.
As a result, we have resulted in lots of duplicated code to handle those different windows in windowed aggregations.
We can consider if it's worth serializing those window types differently (especi…


## KAFKA-13935: Factor out static IBP usages from broker
Sub-task · Resolved (Fixed) · Major · created 2022-05-24 · resolved 2022-08-22

We pass the IBP down to the log layer for checking things like compression support. Currently, we are still reading this from KafkaConfig. In ZK mode this is fine, but in KRaft mode, reading the IBP from the config is not supported.
Since KRaft only supports IBP/MetadataVersion greater than 3.0 (which supports the compression mode we check for), we may be able to avoid using a dynamic call and/or volatile to get the current version.


## KAFKA-13936: Invalid consumer lag when monitoring from a kafka streams application
Bug · Resolved (Fixed) · Major · components: streams · created 2022-05-25 · resolved 2022-06-30

I have a kafka streams application and I'm trying to monitor the consumer lag via stream metrics.
Here's some code snippet
[code/log omitted]
Here MONITOR_CONSUMER_LAG is {{{}records-lag-max{}}}.
However these numbers dont match with the consumer lag we see in the kafka UI . is records-lag-max the right metric to track for a kafka streams application when the objective is to get consumer lag?

- **Matthias J. Sax:** > we see in the kafka UI  There is no "Kafka UI" – at least not as part of Apache Kafka. If you are using some other "external" UI, it's unclear how they compute/display the lag. Two thories:  * The don't sum the lag over all partitions but take the max over all partitions?  * They compute the l…
- **Prashanth Joseph Babu:** [~mjsax] Apologies for not being specific . by kafka-ui I meant https://github.com/provectus/kafka-ui . We're seeing the same data as kafka-ui tool when we query the broker directly via kafka-cli.  We're seeing a huge difference in numbers though , for a partition it would be around 10,000 in the st…
- **Matthias J. Sax:** As mentioned above, offsets are by default committed every 30 seconds and thus the difference between committed offset to end offset (as reported by Kafka CLI tools, and presumably by provectus) are expected to be larger than the metric directly reported by the consumer that report the difference of…
- **Prashanth Joseph Babu:** [~mjsax] Considering the explanation mentioned regarding one metric reporting lag based on committed offset (kafka broker) and the other reporting based on current offset ( kafka streams application ) , this makes sense and is expected behavior . I wasn't able to find documentation explaining this d…
- **Matthias J. Sax:** Might be worth to document for this case :) – Would you be interested to do a PR?
- _…5 more comments_

## KAFKA-13937: StandardAuthorizer throws "ID 5t1jQ3zWSfeVLMYkN3uong not found in aclsById" exceptions into broker logs
Bug · Resolved (Duplicate) · Major · created 2022-05-25 · resolved 2022-05-25

I'm trying to use the new {{StandardAuthorizer}} in a Kafka cluster running in KRaft mode. When managing the ACLs using the Admin API, the authorizer seems to throw a lot of runtime exceptions in the log. For example ...
When creating an ACL rule, it seems to create it just fine. But it throws the following exception:
[code/log omitted]
However, when I describe the ACL rules (again using the Admin API), they seem to be created and seem to work fine despite these errors.
Similarly, deleting t…

- **Andrew Grant:** Thanks for the report. Looks similar to https://issues.apache.org/jira/browse/KAFKA-13909.
- **Luke Chen:** OK, I'll take a look when investigating KAFKA-13909.
- **Colin McCabe:** I believe this is KAFKA-13649, which was fixed recently. The issue came about because we accidentally shared the same authorizer object between c-located controller and broker.

## KAFKA-13938: Jenkins builds are timing out after streams integration tests
Task · Open · Major · components: build · created 2022-05-25

Jenkins PR builder is sporadically failing with timeouts. A few examples:
https://ci-builds.apache.org/job/Kafka/job/kafka-pr/view/change-requests/job/PR-12136/5/execution/node/137/log/
https://ci-builds.apache.org/job/Kafka/job/kafka-pr/view/change-requests/job/PR-12207/1/execution/node/137/log/
https://ci-builds.apache.org/job/Kafka/job/kafka-pr/view/change-requests/job/PR-12062/7/execution/node/138/log/
In these examples, the timeout occurs after 
22:14:00  streams-5: SMOKE-TEST-CLIENT-C…

- **Jason Gustafson:** I looked at a few of the recent builds. It seems like one of the recently kraft-converted tests in `LogOffsetTest` is hanging.  For example: [https://ci-builds.apache.org/job/Kafka/job/kafka-pr/view/change-requests/job/PR-12062/7/execution/node/138/log/] We see this test started on jdk17: ``` *1…
- **Jason Gustafson:** I posted a PR to add a timeout to `LogOffsetTest` here: https://github.com/apache/kafka/pull/12213.
- **João Pedro Fonseca:** Hi, [~mumrah]! Since Jenkins was disabled yesterday, could this taks be closed?

## KAFKA-13939: Memory Leak When Logging Is Disabled In InMemoryTimeOrderedKeyValueBuffer
Bug · Resolved (Fixed) · Blocker · components: streams · created 2022-05-25 · resolved 2022-06-16

If `loggingEnabled` is false, the `dirtyKeys` Set is not cleared within `flush()`, see [https://github.com/apache/kafka/blob/3.2/streams/src/main/java/org/apache/kafka/streams/state/internals/InMemoryTimeOrderedKeyValueBuffer.java#L262.] However, dirtyKeys is still written to in the loop within `evictWhile`. This causes dirtyKeys to continuously grow for the life of the buffer.

- **Jackson Newhouse:** One way to patch this would be something like [code/log omitted] Since `loggingEnabled` is final, we can just not track the dirty keys. The set is only read from if `loggingEnabled` is true.
- **Jackson Newhouse:** If you search Stack Overflow you'll find occasional instances of people running into this problem, such as [https://stackoverflow.com/questions/59239783/kafka-streams-suppressed-feature-causes-oom-heavy-gc]  and [https://stackoverflow.com/questions/70651437/kafka-stream-oom-out-of-memory|https://s…
- **Matthias J. Sax:** Thanks for reporting this issue – sound rather severs – I bumped the priority to blocker. As you already have a fix, would you like to open a PR on GitHub?
- **Guozhang Wang:** Thanks [~jnewhouse], I looked at the code you pointed it out and I agree it's a bug indeed, and should be fixed asap. Please let us know if you'd like to open a PR to fix it.
- **Jackson Newhouse:** I'll open a PR.
- _…3 more comments_

## KAFKA-13940: DescribeQuorum returns INVALID_REQUEST if not handled by leader
Bug · Resolved (Fixed) · Major · created 2022-05-25 · resolved 2022-08-17

In `KafkaRaftClient.handleDescribeQuorum`, we currently return INVALID_REQUEST if the node is not the current raft leader. This is surprising and doesn't work with our general approach for retrying forwarded APIs. In `BrokerToControllerChannelManager`, we only retry after `NOT_CONTROLLER` errors. It would be more consistent with the other Raft APIs if we returned NOT_LEADER_OR_FOLLOWER, but that also means we need additional logic in `BrokerToControllerChannelManager` to handle that error and re…


## KAFKA-13941: Re-enable ARM builds following INFRA-23305
Task · Resolved (Fixed) · Major · components: build · created 2022-05-26 · resolved 2022-05-27

Once https://issues.apache.org/jira/browse/INFRA-23305 is resolved, we should re-enable ARM builds in the Jenkinsfile.

- **Divij Vaidya:** [~mumrah] ARM build have been timing out consistently lately. The problem might have resurfaced. Could you please look into it or guide the community on how to debug the root cause? Note that the failing ARM build almost always causes the entire build to fail. Example: https://ci-builds.apache.org/…

## KAFKA-13942: LogOffsetTest occasionally hangs during Jenkins build
Bug · Resolved (Fixed) · Minor · components: unit tests · created 2022-05-26 · resolved 2022-06-08

[~hachikuji] parsed the log output of one of the recent stalled Jenkins builds and singled out LogOffsetTest as a likely culprit for not completing.
I looked closely at the following build which appeared to be stuck and found this test case had STARTED but not PASSED or FAILED.
15:19:58  LogOffsetTest > testFetchOffsetByTimestampForMaxTimestampWithUnorderedTimestamps(String) > kafka.server.LogOffsetTest.testFetchOffsetByTimestampForMaxTimestampWithUnorderedTimestamps(String)[2] STARTED


## KAFKA-13943: Fix flaky test QuorumControllerTest.testMissingInMemorySnapshot()
Bug · Resolved (Fixed) · Major · components: unit tests · labels: flaky-test · created 2022-05-27 · resolved 2022-07-06

Test failed at [https://ci-builds.apache.org/blue/organizations/jenkins/Kafka%2Fkafka-pr/detail/PR-12197/3/tests] 
[code/log omitted]
[code/log omitted]

- **Divij Vaidya:** The test is failing because in some situation the KRaftClient.scheduleAppend() for a message of type `bootstrapMetadata` is being called from  a node which is either not the current leader/controller OR from a leader with wrong epoch because the test is creating a file with LONG_MAX offset at [https…
- **Divij Vaidya:** I have fixed the bug which was causing a snapshot with LONG_MAX at [https://github.com/apache/kafka/pull/12224]  Also note that there are other tests such as QuorumControllerTest.testSnapshotOnlyAfterConfiguredMinBytes failing due to same bug [code/log omitted]

## KAFKA-13944: Shutting down broker can be elected as partition leader in KRaft
Bug · Resolved (Fixed) · Major · labels: kip-500 · created 2022-05-27 · resolved 2022-06-08

When a broker requests shutdown, it transitions to the CONTROLLED_SHUTDOWN state in the controller. It is possible for the broker to remain unfenced in this state until the controlled shutdown completes. When doing an election, the only thing we generally check is that the broker is unfenced, so this means we can elect a broker that is in controlled shutdown. 
Here are a few snippets from a recent system test in which this occurred:
[code/log omitted]

- **Jose Armando Garcia Sancio:** When fixing this lets improve the logging so that the replica control manager logs the reason that triggered the election.
- **Jose Armando Garcia Sancio:** Looks like this issue is addressed by https://issues.apache.org/jira/browse/KAFKA-13916
- **David Jacot:** This has been fixed by https://github.com/apache/kafka/pull/12240.

## KAFKA-14010: alterISR request won't retry when receiving retriable error
Bug · Resolved (Fixed) · Major · components: core · created 2022-06-20 · resolved 2022-07-01

When submitting the AlterIsr request, we register a future listener to handle the response [here|https://github.com/apache/kafka/blob/trunk/core/src/main/scala/kafka/cluster/Partition.scala#L1585-L1610]. When receiving retriable error, we expected the AlterIsr request will get retried. And then, we'll re-submit the request again. 
However, before the future listener got called, we didn't clear the `unsentIsrUpdates`, which causes we failed to "enqueue" the request because we thought there's an…


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

- **Jordan Moore:** "topic.creation" configs are only available for source connectors, for topics that source connectors will write to, not dead letter topics. "admin" prefix will only attempt to modify the AdminClient config, which does not include any topic configs, such as retention time.  If you are allowing the b…

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

- **Matthew de Detrich:** So interestingly I worked on another ticket that reported the exact same test as being flaky (see https://issues.apache.org/jira/browse/KAFKA-13531) and I couldn't reproduce any flakiness (hence the reason why that ticket is closed). I rebased my fork of Kafka to the latest version in trunk and sta…
- **Matthew de Detrich:** Okay so I just noticed the linked builds with different JDK versions (11/17 versus my 16) so I will rerun the tests using those JDK versions to see if I can simulate the CI.
- **Matthew de Detrich:** So I ran the tests overnight with JDK 11 and have no failure with ~10k runs, I suspect that JDK 17 will also provide the same result. This means that a few more possibilities are opened up when it comes to why I may not be able to reproduce the failure locally 1. This is gradle specific (going to…
- **Bruno Cadonna:** [~mdedetrich-aiven] Thank you for looking into this! KAFKA-13531 reported the same test but the failure was different. It could also be that the test was refactored and the message changed. I saw this failure a lot in the CI builds. I would bet on point 3 in your list. However, I would also not e…
- **Matthew de Detrich:** [~cadonna] So I did some debugging on this ticket over the past week and I found out some interesting things. To start off with I did manage to predictably replicate the test's flakiness and it does appear to be related to load, i.e. the test is more flaky the less CPU resources it has. I am using…
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
- **Guozhang Wang:** In the long run, as we refactored our rebalance protocol (KIP incoming :) this issue should be gone as we would not have REBALANCE_IN_PROGRESS anymore, since the brokers take full responsibility on the installation of the new assignment. At the moment, though, I feel changing the broker code may no…
- **Shawn Wang:** [~guozhang] do you mean, set assignment's generation to current generation if client get a REBALANCE_IN_PROGRESS in syncGroupResponse? Yes, I think that can work.  Client will ignore 1 round of assignment  * if the assignment is adding partition: the partition will be paused 1 more round of rebala…
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

- **John Roesler:** {color:#1d1c1d}FYI, just setting the partitioner back to the {color}{{DefaultPartitioner}}{color:#1d1c1d} does not appear to help. The throughput of that test was 105k±2k records per second.{color} {color:#1d1c1d}Code under test: {color}[https://github.com/apache/kafka/commit/6c67adb8beedafca0316d1…
- **John Roesler:** Hey [~alivshits] , thanks for your work on [https://github.com/apache/kafka/pull/12365] . I've just re-run the same benchmark above and confirmed that your PR fixes the perf regression. Thank you! As a reminder, this was the baseline for "good" performance: Commit: [{{e3202b9}}|https://github.com…
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

- **Ashmeet Lamba:** Hi, I am new to Kafka and noticed that this issue is tagged as newbie. I would like to pick this issue up. I have gone through the PR attached. I also did go through the KRaft's README. Reading through the code base I believe the changes required would be in this file - [BrokerMetadataListener|htt…

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
- **Randall Hauch:** Following up with some additional detail: This issue can affect users that are upgrading to AK 3.2.0, even if they don't modify any Connect worker config or connector configurations. For example, if a user has a pre-AK 3.2.0 Connect installation running with one or more source connector configurati…
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
- **Gian Luca:** This is my report implementation: [code/log omitted] And this is the main class: [code/log omitted] On execution, the values of the 'request-total' metric are notified once (through the metricChange() method) with value 0.0, then no more updates happen.
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

- **Deng Ziming:** > it must catch up to the current metadata before it is unfenced. Currently, we have changed the behavior to unfence a broker when it catch up to it's own RegisterBrokerRecord.

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

- **Artem Livshits:** > 1. Broker 1 loses its session in Zookeeper.  I think if we treat this error as fatal (fence itself or maybe just flush and restart), it should handle a whole class of split brain issues.  ZK timeouts are generally set such that the client would timeout before the ephemeral zknode is removed, so t…

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
- **Guozhang Wang:** Hi [~aglicacha] [~vongosling] The main motivation for using two connection sockets for the coordinator and partition leader is to not block coordination related requests such as join/sync by fetching requests (which could be long polling, and during that time we cannot send other requests using the…

## KAFKA-14190: Corruption of Topic IDs with pre-2.8.0 ZK admin clients
Bug · Resolved (Won't Fix) · Major · components: admin, core, zkclient · created 2022-08-30 · resolved 2024-10-15

h3. Scope
The problem reported below has been verified to occur in Zookeeper mode. It has not been attempted with Kraft controllers, although it is unlikely to be reproduced in Kraft mode given the nature of the issue and clients involved.
h3. Problem Description
The ID of a topic is lost when an AdminClient of version < 2.8.0 is used to increase the number of partitions of that topic for a cluster with version >= 2.8.0. This results in the controller re-creating the topic IDs upon restart, e…

- **Ismael Juma:** Thanks for the JIRA. To clarify, the issue is not using an older topics command, it's using an older topics command _with the_ –zookeeper flag, right? That is, they can use older topics command with the --bootstrap-server flag and the problem would not occur?
- **Ismael Juma:** {quote}The ID of a topic is lost when an AdminClient of version < 2.8.0 is used to increase the number of partitions of that topic for a cluster with version >= 2.8.0 {quote} Is the above actually true? The command you outlined doesn't use admin client at all, it updates zookeeper directly.
- **Alexandre Dupriez:** Hi Ismael, Thanks for the follow-up. You are right that the problem requires to use the {{--zookeeper}} flag (which has been removed from the newest versions). If topic changes are applied via broker RPCs, no topic ID is lost. This brings us to your second comment: indeed it requires modifying the…
- **Ismael Juma:** `AdminZkClient` is an internal class and compatibility was never offered (or should have been expected) for that. The `–zookeeper` flag for for `TopicCommand` has been deprecated since Apache Kafka 2.2.0 ([https://github.com/apache/kafka/blob/2.2.0/core/src/main/scala/kafka/admin/TopicCommand.scala#…
- **Divij Vaidya:** Adding reports of users facing this bug which would help us determine priority of fixing this. 1. User on mailing list [https://lists.apache.org/thread/jzk4tyd1xs1wwj0bpkdnxpw0m152qw1f] 2. User on #kafka channel [https://the-asf.slack.com/archives/CE7HWJPHA/p1671529649633529]
- _…4 more comments_

## KAFKA-14191: Add end-to-end latency metrics to Connectors
Improvement · Open · Major · components: connect, metrics · labels: connect, needs-kip · created 2022-08-30

Request to add latency metrics to connectors to measure transformation latency and e2e latency on the sink side.
KIP: https://cwiki.apache.org/confluence/display/KAFKA/KIP-864%3A+Add+End-To-End+Latency+Metrics+to+Connectors


## KAFKA-14192: Move registering and unregistering changelogs to state updater
Improvement · Resolved (Duplicate) · Major · components: streams · created 2022-08-31 · resolved 2026-05-04

Currently, we register and unregister changelogs when we initialize and close/recycle a task. 
When we will remove the old code path for restoration and we will only use the state updater, we should consider to move registering and unregistering changelogs inside the state udpater. In such a way, we would put registering and unregistering changelogs in one place and we would only have changelog registered when it is actually needed, i.e., during restoration of active tasks and updating of stand…

- **Nikita Shupletsov:** Looks like it was done in [https://github.com/apache/kafka/pull/12638] as a part of https://issues.apache.org/jira/browse/KAFKA-10199 [~cadonna] could you please confirm? or is there anything else needed? thank you in advance!
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
- **Luke Chen:** [~pnee] , thanks for the analysis. Yes, we forgot about during the following poll, the offset might advance while we're waiting for the old async offset commit completion. Actually, while checking the code, even if we don't do the change for KAFKA-14024,and KAFKA-13310, (that is, changing sync comm…
- **Philip Nee:** Thanks Luke, per your suggestion, could you elaborate more about the reason to terminate the poll? I've got a few questions to clarify here:  # I don't think we need to pause the fetch if the previous async commit (autocommit) hasn't yet go through, for the normal situation (not rebalancing)? Beca…
- **Guozhang Wang:** [~pnee] Thanks for reporting this. While reviewing KAFKA-13310 I have realized this, but as Luke said this is not a new regression (we would potentially have duplicates even before this, since as we commit sync, and if the commit fails, we still log a warning and move forward with the revocation, in…
- _…8 more comments_

## KAFKA-14197: Kraft broker fails to startup after topic creation failure
Bug · Resolved (Duplicate) · Blocker · components: kraft · created 2022-09-02 · resolved 2022-09-06

In kraft ControllerWriteEvent, we start by trying to apply the record to controller in-memory state, then sent out the record via raft client. But if there is error during sending the records, there's no way to revert the change to controller in-memory state[1].
The issue happened when creating topics, controller state is updated with topic and partition metadata (ex: broker to ISR map), but the record doesn't send out successfully (ex: RecordBatchTooLargeException). Then, when shutting down th…

- **Luke Chen:** I think we should have a way to notify ReplicationControlManager the topic doesn't get created successfully, so that it won't send out the partitionChangeRecords while controlled shutdown. But I don't have a good idea how we can achieve that gracefully. cc [~hachikuji]  [~cmccabe] [~jsancio] [~deng…
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

- **Chris Egerton:** [~LucentWong] would monitoring the consumer lag metric help in this case? I believe that would allow users to detect when MM2 is lagging behind on consumption from the source cluster; it may not highlight this specific issue, but it would still indicate a general issue with the MM2 cluster. I'm hes…
- **Yu Wang:** [~ChrisEgerton] I am afraid monitoring lag now working in this case. Actually, we are monitoring both *records-age* from MirrorSourceTask and *records-lag* from KafkaConsumer. It's not work because MirrorSourceTask only refresh the *records-age* metrics after success poll from consumer, but it thro…
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

- **Guozhang Wang:** Hello [~mathieu.amblard], thanks for reporting this use case. I'm wondering in your scenario if all topics have the same num. partitions, and have similar data traffic as well? I'm asking this because one of the primarily goals of partition assignors is to achieve workload balance, so if topics hav…
- **Mathieu Amblard:** Hello [~guozhang] , Thanks for your comment that's a good question, All topics have not the same number of partition, they are sized accordingly to the data traffic. If we have to consume a large amount of data, we simply scale up the number of pods (so the number of consumer). Using this partiti…
- **Mathieu Amblard:** Too specific use case, the KIP-874 has been rejected.

## KAFKA-14270: Kafka Streams logs exception on startup
Bug · Resolved (Fixed) · Minor · components: streams · created 2022-09-30 · resolved 2022-10-04

Kafka Streams expects a version resource at /kafka/kafka-streams-version.properties. It is read by {{{}ClientMetrics{}}}, initialised by
[https://github.com/apache/kafka/blob/3.3.0/streams/src/main/java/org/apache/kafka/streams/KafkaStreams.java#L894]
When the resource is not found,
[https://github.com/apache/kafka/blob/3.3.0/streams/src/main/java/org/apache/kafka/streams/internals/metrics/ClientMetrics.java#L55]
logs a warning at startup:
org.apache.kafka.streams.internals.metrics.ClientMe…

- **Guozhang Wang:** Thanks for filing the bug [~eikemeier], will take a look. From your description, it seems whenever Kafka Streams is started, with whatever integration tooling besides groovy, it will always log a warning?
- **Oliver Eikemeier:** Yes. Sorry about the “Groovy” tag, the Gradle build script is written in Groovy, so this fix is in Groovy code.
- **Bruno Cadonna:** [~eikemeier] Thanks for the fix! I tested your code manually and merged your PR. I also added you o the contributors group in Jira so that I could assign this ticket to you.

## KAFKA-14271: Topic recreation fails in KRaft mode when topic contains collidable characters
Bug · Resolved (Duplicate) · Major · components: kraft · created 2022-09-30 · resolved 2022-12-12

We recently updated one of our clusters from 3.2.0 to 3.3.0 (primarily to get the fix for KAFKA-13909). This cluster is running KRaft mode.
This is a cluster used for some integration tests - each test deletes the topics it uses before the test to ensure a clean slate for the test; the brokers get restarted in-between tests, but the broker data isn't deleted.
With 3.3.0, this semi-crashes Kafka. The brokers stay running, but the topic creation fails:
[code/log omitted]
This appears to be bec…

- **Jeffrey Tolar:** It's possible this isn't specific to KRaft-mode; I haven't tried reproducing it with a Zookeeper-based cluster. edit: after a quick script update, it looks like Zookeeper-mode is unaffected [code/log omitted]
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
- **John Krupka:** We're using a custom replication policy. Here are the contents of the mm2-msc.json file. Is this what you're asking for? I'm new to this so I'm unsure exactly what all constitutes the policy. [code/log omitted]
- **Mickael Maison:** Thanks for the details. The ReplicationPolicy [javadoc|https://kafka.apache.org/33/javadoc/org/apache/kafka/connect/mirror/ReplicationPolicy.html#upstreamTopic-java.lang.String-] states that upstreamTopic can return null to indicate a topic is not remote. So this is a bug in MirrorSourceConnector.i…
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

- **Kirk True:** This looks related to KAFKA-10228, but that Jira is still open and seems to suggest only a logging change. I _believe_ we want to change the behavior to complete the batch using a different {{Errors}} type.
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
- **Sergey Ivanov:** Hi, We faced similar problem. I described it in ticket KAFKA-14817, these may be related issues.

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

- **Mickael Maison:** I took a look at these APIs to see what can be done.  * Scram Credentials It already possible to retrieve credential details for multiple users in a single call: [code/log omitted]  * Quotas  DescribeClientQuotasRequest/Response and Admin.describeClientQuotas() accepts multiple resources but th…
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

- **A. Sophie Blee-Goldman:** Weird, thanks for finding this – I'm guessing the first one is broken due to an extra '/documentation' in the link, it should presumably be directing to [https://kafka.apache.org/documentation/#security] As for the 2nd one, it's a little less clear what it should be pointing to – oddly there does n…
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
- **A. Sophie Blee-Goldman:** {quote}I would have thought that an orderly rebalance wouldn't cause any duplication {quote} Well in general it shouldn't, actually, because even if the offset commit fails/is preventing while the rebalance is in progress, if any partitions are migrated from one consumer to another then the origin…
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
- **Chetan:** Hi [~pnee] , We were able to finally recreate the scenario in a lower environment. 1. Consumer node 1  stopped at 4:58 PM IST/11:28 UTC  and started at 5:00PM IST/11:30 UTC 2. Consumer node 2 stopped at 5:04PM IST/11:34 UTC and started at 5:07PM IST/11:37 UTC 3. Consumer node 3 stopped at 5:11PM…
- **Philip Nee:** Hey [~Chetu] - two questions  # How do you setup your rebalance listener, as you aren't doing autocommit, are you calling commitSync upon onPartitionsRevoked?  # How and where do you log the committed offset?   Thanks P
- **Chetan:** Hi [~pnee],  # We have created a custom Listener from ConsumerRebalanceListener and onPartitionsRevoked() we are doing commitSync offset  # Each message consumed is logged with partition, offset, and topic information in the application log. Do you see if there is any issue or if the way we do it…
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

- **David Arthur:** I did some investigation on this. Running {{./gradlew -PmaxParallelForks=1 :core:integrationTest}} to better capture the leaked objects, I took a heap dump after 30 minutes. Several KafkaRaftManager instances were hanging around. !image-2022-12-01-13-53-57-886.png! This anonymous function "Partiti…

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

- **Jason Gustafson:** Yeah, we've had so many compatibility breaks due to error code usage. Putting the errors into the spec would also enable better enforcement. One option could be something like this: [code/log omitted] Here "enum16" indicates a 2-byte enumeration where the values are provided in the `values` field.…
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

- **Matthias J. Sax:** What you observe is behavior by-design (the design is no ideal...). Note that the local checkpoint files only contain metadata... And for EOS they are not updated regularly, but actually read on startup and deleted afterwards, and only written again on a clean stop. It's a known issue, but not a bu…
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
- **Ismael Juma:** [code/log omitted] `duplicate` doesn't copy the buffer.

## KAFKA-14542: Deprecate OffsetFetch/Commit version 0 and remove them in 4.0
Improvement · Resolved (Duplicate) · Major · created 2022-12-21 · resolved 2025-03-20

We should deprecate OffsetFetch/Commit APIs and remove them in AK 4.0. Those two APIs are used by old clients to write offsets to and read offsets from ZK.
We need a small KIP for this.

- **Ismael Juma:** [https://cwiki.apache.org/confluence/display/KAFKA/KIP-896%3A+Remove+old+client+protocol+API+versions+in+Kafka+4.0] covers this and more.
- **David Jacot:** Addressed by https://issues.apache.org/jira/browse/KAFKA-14560.

## KAFKA-14543: Move LogOffsetMetadata to storage module
Sub-task · Resolved (Fixed) · Major · created 2022-12-21 · resolved 2022-12-28

- **Satish Duggana:** [~mimaison]  `LogOffsetMetadata` refactoring to move to storage module is being done as part of https://issues.apache.org/jira/browse/KAFKA-14480. Glad to raise PR against https://issues.apache.org/jira/browse/KAFKA-14543 for that specific change if you have not yet started working on that.
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
- **Matthias J. Sax:** {quote}This is an anti-pattern, as frequent poll()s are expected to keep kafka consumers in contact with the kafka cluster. {quote} Well, not really. Note that the JavaDoc you quote is about a consumer that is part of a consumer group. However, the restore consumer is a "stand along" consumer and…
- **Greg Harris:** > Note that the JavaDoc you quote is about a consumer that is part of a consumer group. However, the restore consumer is a "stand along" consumer and not part of any group and thus periodic polling is not necessary. There is no consumer group, group management, or heart beating etc. Yes, I understa…
- **Greg Harris:** [~mjsax] Thanks for your patience on this issue. I will no longer be pursuing this specific change. I explored the above proposed fix more deeply, and it appears that it is not reasonable to add to streams. This is because it is illegal to call poll() on a consumer with no active subscriptions, whi…
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

- **Nikolay Izhikov:** Hello [~omnia_h_ibrahim]  Can I assign this ticket to myself?  I want to implement it and it seems that you working on another "move utility" ticket in the moment.
- **Omnia Ibrahim:** [~nizhikov] sure
- **Omnia Ibrahim:** Hi [~nizhikov], just a note, I moved the methods `{{{}TestUtils.setReplicationThrottleForPartitions{}}}` and `{{{}TestUtils.removeReplicationThrottleForPartitions`  from `{}}}{{{}TestUtils` to `{}}}{{{}ToolsTestUtils{}}}{{{}` {}}}{{ as they are used only }} by `TopicCommand` and `ReassignPartitionCo…
- **Nikolay Izhikov:** [~omnia_h_ibrahim] Thanks to let me know!
- **Nikolay Izhikov:** Hello To reduce changes and make them reviewable I propose to split task into several. As a first step it seems feasible to move value-objects(sealed case classes and traits) from scala code to java. These classes are: * PartitionMove * LogDirMoveState * MissingReplicaMoveState and other LogDi…
- _…2 more comments_

## KAFKA-14596: Move TopicCommand to tools
Sub-task · Resolved (Fixed) · Major · created 2023-01-05 · resolved 2023-10-17


## KAFKA-14597: [Streams] record-e2e-latency-max is not reporting correct metrics 
Bug · Resolved (Fixed) · Major · components: metrics, streams · created 2023-01-05 · resolved 2026-08-10

I was following this KIP documentation ([https://cwiki.apache.org/confluence/display/KAFKA/KIP-613%3A+Add+end-to-end+latency+metrics+to+Streams]) and kafka streams documentation ([https://kafka.apache.org/documentation/#kafka_streams_monitoring:~:text=node%2Did%3D(%5B%2D.%5Cw%5D%2B)-,record%2De2e%2Dlatency%2Dmax,-The%20maximum%20end]) . Based on these documentations , the *record-e2e-latency-max* should monitor the full end to end latencies, which includes both *consumption latencies* and  {*}pr…

- **Bruno Cadonna:** [~talestonini] Thank you for the ticket! I noticed that in your screenshot record {{record-e2e-latency-max.jpg}} the metric {{process-total}} is 0 which means that no records were processed when the metric {{record-e2e-latency-max}} got recorded. That would explain why {{record-e2e-latency-max}} is…
- **Tales Tonini:** Hi [~cadonna] , I went through [KIP-613|https://cwiki.apache.org/confluence/display/KAFKA/KIP-613%3A+Add+end-to-end+latency+metrics+to+Streams], its discussion thread, the associated PRs, the trunk code and the related tests. AFAIU:  # right before starting the source node processing, the processor…
- **Atul Jain:** Hi [~cadonna] ,  {quote}Could you run your Streams application and ensure that {{process-total}} is 1 or greater when you look at {{{}record-e2e-latency-max{}}}? Please, let us know whether the value of the metric makes more sense then. {quote} In order to report this issue, I started the Stream…
- **Tales Tonini:** Hi [~atuljainiitk] , may I ask what Kafka Streams version you have in your app? Thanks.
- **Atul Jain:** I currently have 2.6.0 version
- _…6 more comments_

## KAFKA-14598: Fix flaky ConnectRestApiTest
Bug · Reopened · Minor · components: connect · labels: flaky-test · created 2023-01-06

ConnectRestApiTest sometimes fails with the message
{{ConnectRestError(404, '<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html;charset=ISO-8859-1"/>\n<title>Error 404 Not Found</title>\n</head>\n<body><h2>HTTP ERROR 404 Not Found</h2>\n<table>\n<tr><th>URI:</th><td>/connector-plugins/</td></tr>\n<tr><th>STATUS:</th><td>404</td></tr>\n<tr><th>MESSAGE:</th><td>Not Found</td></tr>\n<tr><th>SERVLET:</th><td>-</td></tr>\n</table>\n\n</body>\n</html>\n', 'http://172.31.1.75:8083/conn…

- **Ashwin Pankaj:** Did not see this occuring recently - closing this issue.
- **Ashwin Pankaj:** Did not observe this recently
- **Greg Harris:** [~ashwinpankaj] The PR for this is a one line fix, and you already proved that it was fixing a flakey failure. I don't think this should be closed as the problem has not been addressed. If you no longer wish to work on this, leave it open and unassigned.

## KAFKA-14599: MirrorMaker pluggable interfaces missing from public API
Bug · Patch Available · Major · components: mirrormaker · created 2023-01-06

MirrorMaker exposes a few pluggable APIs, including:
ConfigPropertyFilter
GroupFilter
TopicFilter
ForwardingAdmin
These are currently missing from our javadoc.

- **Nikolay Izhikov:** Hello, [~mimaison] , [~ChrisEgerton]  Can you, please, take a look at my changes? https://github.com/apache/kafka/pull/13157

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

- **Satish Duggana:** [~ivanyu] Assigned to you as you are already working on this with https://github.com/apache/kafka/pull/13067/ Please feel free to reassign if needed.
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
- **hzh0425:** Thanks for your reply! [~satish.duggana] [~Hangleton]  So what is your solution? Let RLMM subscribe to all topics? Have you considered using rocksdb to store the full amount of metadata? I'm looking forward to having the opportunity to implement Tiered-Stoarge with you, because I am now promoting…
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

- **Matthias J. Sax:** Did you upgrade with two rolling bounced leveraging `upgrad_from` config? I assume is related to https://issues.apache.org/jira/browse/KAFKA-13769 Of course, K13769 could have introduced some bug, but we actually to test rolling upgrades and would hope it would have caught it (otherwise, we need t…
- **Jochen Schalanda:** {quote}Did you upgrade with two rolling bounced leveraging `upgrad_from` config? {quote} [~mjsax] Ah, in fact we didn't. I assumed (incorrectly) that this would only be necessary when updating across major versions. I found [https://kafka.apache.org/33/documentation/streams/upgrade-guide] which c…
- **Matthias J. Sax:** Thanks for following up – glad to hear that it's in the docs... And I hope it resolved the problem.
- **Jochen Schalanda:** Unfortunately the two rolling updates (with {{upgrade.from="3.2"}} and then removing the setting again) didn't help. We still see the same exception: [code/log omitted] [~mjsax] Do you have any hints how to resolve this issue? We see it in only 2 topologies out of 15 and I'm afraid that downgradi…
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

- **Soumyajit Sahu:** This is not a bug. You are listing your topics as ANONYMOUS user and your topic now has an acl for User:test. If you try to list the topics as user test, it should list it for you. Try the --command.config parameter to pass a jaas config.
- **Soumyajit Sahu:** This isn't a big. You are listing topics as ANONYMOUS user while your topic has an acl for User:test only. Try using the --command.config to pass a jaas config and run the command as User:test.
- **Gabriel Lukacs:** ok, thanks for clarification, my fault, i was not familiar with acl/jaas, but now it is clear. sorry for inconveniences, pls close this bug.

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

## KAFKA-14744: NPE while converting OffsetFetch from version < 8 to version >= 8
Bug · Resolved (Fixed) · Major · created 2023-02-23 · resolved 2023-02-23

While refactoring the OffsetFetch handling in KafkaApis, we introduced a NullPointerException (NPE). The NPE arises when the FetchOffset API is called with a client using a version older than version 8 and using null for the topics to signal that all topic-partition offsets must be returned. This means that this bug mainly impacts admin tools. The consumer does not use null.
This NPE is here: https://github.com/apache/kafka/commit/24a86423e9907b751d98fddc7196332feea2b48d#diff-0f2f19fd03e2fc5aa9…


## KAFKA-14745: MirrorSourceConnector keeps creating ReplicationPolicy instances
Improvement · Resolved (Fixed) · Major · components: mirrormaker · created 2023-02-23 · resolved 2023-03-03

In MirrorSourceConnector.findTargetTopicPartitions() we call MirrorSourceConfig.checkpointsTopic() for each remote topic or all topics when using IdentityReplicationPolicy.
The issue is that checkpointsTopic() calls MirrorSourceConfig.replicationPolicy() which always creates a new instance of the ReplicationPolicy.


## KAFKA-14746: Throwing in Connector.taskConfigs in distributed mode generates a lot of logs
Improvement · Open · Major · components: connect · created 2023-02-23

If a Connector throws in its taskConfigs() method, the runtime ends up retrying using DistributedHerder.RECONFIGURE_CONNECTOR_TASKS_BACKOFF_MS which is a fixed value (250ms). For each retry, the runtime prints the connector configuration and the enriched configuration so this can quickly generate a lot of logs.
There is some value in throwing in taskConfigs() as it allows to fail fast in case the connector is given bad credentials. For example this is what some of the Debezium connectors do: ht…

- **Mickael Maison:** https://issues.apache.org/jira/browse/KAFKA-14732 describes pretty much the same issue. With the exponential backoff we don't spam the logs with errors. However it's still kind of unclear what's going on from a user point of view without looking at the logs. If the connector throws in taskConfigs()…
- **Chris Egerton:** [~mimaison] do you think it's worth considering a KIP to alter the behavior in this scenario? I know that some connectors may be relying on the infinite-retry logic for the {{taskConfigs}} method but in my experience a lot of the time it's unintentional and there's a false expectation that throwing…
- **Mickael Maison:** To be honest I'm not sure if we should change this behavior or simply document it. I tend to agree that the retry logic was likely intended to handle failures communicating with the leader instead of exceptions from taskConfigs().
- **Yash Mayya:** I agree that the intent of the retries seems to be mainly to handle failures while communicating with the leader - this infinite retry mechanism covering exceptions thrown from connectors' taskConfigs method doesn't seem to make sense intuitively and was probably an oversight. [~ChrisEgerton] are yo…
- **Chris Egerton:** Hi Yash, {quote}are you suggesting a KIP to modify the existing retry mechanism to not cover exceptions thrown from connectors' taskConfigs method? {quote} Yep, exactly. But it's not high-priority and given Mickael's thoughts I don't think we should move forward with it for now. The suggestion to…

## KAFKA-14747: FK join should record discarded subscription responses
Improvement · Resolved (Fixed) · Minor · components: streams · labels: beginner, newbie · created 2023-02-23 · resolved 2024-03-04

FK-joins are subject to a race condition: If the left-hand side record is updated, a subscription is sent to the right-hand side (including a hash value of the left-hand side record), and the right-hand side might send back join responses (also including the original hash). The left-hand side only processed the responses if the returned hash matches to current hash of the left-hand side record, because a different hash implies that the lef- hand side record was updated in the mean time (includin…

- **Koma Zhang:** [~mjsax]  i am new here, can i take this task?
- **Matthias J. Sax:** Sure. Not sure if we need a KIP or not. [~guozhang] WDYT?
- **Matthias J. Sax:** Talking to [~guozhang] it seem we don't need a KIP :) – I removed the label.
- **Guozhang Wang:** Echoing that, I think we can piggy-back on the existing `dropped-records`, as it has also been replacing other old sensors like `expired-window-record-drop` as well in KIP-743.
- **Koma Zhang:** Thank u guys, so for me as the developer, which branch i can use to checkout the development branch for this task? [~mjsax]
- _…6 more comments_

## KAFKA-14845: Broker ZNode creation can fail due to lost Zookeeper Session ID
Bug · Resolved (Won't Fix) · Minor · created 2023-03-24 · resolved 2024-10-15

Our production environment faced a use case where registration of a broker failed due to the presence of a "conflicting" broker znode in Zookeeper. This case is not without familiarity to that fixed by KAFKA-6584 and induced by the Zookeeper bug (or feature) tracked in ZOOKEEPER-2985 opened as of today.
A network partition disturbed communication channels between the Kafka and Zookeeper clusters for about 20% of the brokers in the cluster. One of this broker was not able to re-register with Zoo…

- **Alexandre Dupriez:** I could reproduce without forcefully renewing the ZK session. In a nutshell, it is possible (at least with the Netty client for ZK used for reproduction and run in production) to have the Zookeeper server create an active session then process messages under its authority (including znode creation)…
- **Alexandre Dupriez:** The reproduction test case has been update and is available [in github|https://github.com/Hangleton/kafka-tools/tree/master/kafka-broker-reg]. The logs of a run of this test have been attached to this ticket. It does not require any forced session renewal but just reproduce the use case using:  *…
- **Mickael Maison:** We're now removing ZooKeeper support, so closing

## KAFKA-14846: Fix overly large record batches in ZkMigrationClient
Sub-task · Resolved (Fixed) · Major · created 2023-03-24 · resolved 2024-08-09

ZkMigrationClient should not create overly large record batches

- **Colin McCabe:** We did add a limit on batch size for ZkMigrationClient. Marking as fixed.

## KAFKA-14847: Separate the callers of commitAllTasks v.s. commitTasks for EOS(-v2) and ALOS
Improvement · Open · Major · components: streams · created 2023-03-24

Today, EOS-v2/v1 and ALOS shares the same internal callpath inside TaskManager/TaskExecutor for committing tasks from various scenarios, the call path {{commitTasksAndMaybeUpdateCommitableOffsets}} -> {{commitOffsetsOrTransaction}} takes in a list of tasks as its input, which can be a subset of the tasks that thread / task manager owns. For EOS-v1 / ALOS, this is fine to commit just a subset of the tasks; however for EOS-v2, since all tasks participate in the same txn it could lead to dangerous…


## KAFKA-14848: KafkaConsumer incorrectly passes locally-scoped deserializers to FetchConfig
Sub-task · Resolved (Fixed) · Major · components: clients, consumer · labels: consumer-threading-refactor · created 2023-03-25 · resolved 2023-04-25

[~rayokota] found some {{{}NullPointerException{}}}s that originate because of a recently introduced error in the {{KafkaConsumer}} constructor. The code was changed to pass the deserializer variables into the {{FetchConfig}} constructor. However, this code change incorrectly used the locally-scoped variables, not the instance-scoped variables. Since the locally-scoped variables could be {{{}null{}}}, this results in the {{FetchConfig}} storing {{null}} references, leading to downstream breakage…


## KAFKA-14849: Kafka consumers receive INCONSISTENT_GROUP_PROTOCOL error even the configuration of all consumers is same
Bug · Open · Major · components: consumer · created 2023-03-26

# At first, we modify the group.instance.id for consumers wrongly, so different consumers have the same group.instance.id for a while.
2. After we rollbak the configuration about group.instance.id, consumers receive INCONSISTENT_GROUP_PROTOCOL error even the configuration of all consumers is same
3. Coordinator of this group accepts ten thousands of join group request from consumers
4. Consumers can get message normally after restarting the coordinator of this group. I have upload the log abo…


## KAFKA-14850: Introduce InMemoryLeaderEpochCheckpoint to allow quick write/read
Sub-task · Resolved (Fixed) · Major · created 2023-03-27 · resolved 2023-04-05


## KAFKA-14851: Move StreamResetterTest to tools
Sub-task · Resolved (Fixed) · Minor · created 2023-03-27 · resolved 2023-07-21

This came up as a suggestion here: https://github.com/apache/kafka/pull/13127#discussion_r1105688687


## KAFKA-14852: Propagate Topic Ids to the Group Coordinator for Offset Fetch
Sub-task · Resolved (Won't Do) · Major · created 2023-03-27 · resolved 2024-12-19

This task is the sibling of KAFKA-14793 which propagates topic ids in the group coordinator on the offset commit (write) path. The purpose of this JIRA is to change the interfaces of the group coordinator and its adapter to propagate topic ids in a similar way.
KAFKA-14691 will add the topic ids to the OffsetFetch API itself so that topic ids are propagated from clients to the coordinator on the offset fetch path. 
Changes to the persisted data model (group metadata and keys) are out of scope.

- **Mickael Maison:** We're past feature freeze for 3.5.0, so I"m moving this to 3.6.0.
- **Satish Duggana:** Moving it to 3.7.0 as we are near code freeze and it is not a blocker.

## KAFKA-14853: the serializer/deserialize which extends ClusterResourceListener is not added to Metadata
Bug · Resolved (Fixed) · Minor · created 2023-03-27 · resolved 2023-03-29

I noticed this issue when reviewing  KAFKA-14848


## KAFKA-14854: Refactor inter broker send thread to handle all interbroker requests on one thread
Sub-task · In Progress · Major · created 2023-03-27

Currently we create a new thread for each interbroker request that implements InterbrokerSendThread. It would be better to implement a single thread that multiple request types can use with their custom logic. 
I propose creating a single thread that takes a collection of "managers" for each request and sends the requests generated.


## KAFKA-14855: Harden integration testing logic for asserting that a connector is deleted
Improvement · Resolved (Fixed) · Minor · components: connect · created 2023-03-27 · resolved 2023-09-19

In the Connect embedded integration testing framework, the [EmbeddedConnectClusterAssertions::assertConnectorAndTasksAreStopped method|https://github.com/apache/kafka/blob/31440b00f3ed8de65f368d41d6cf2efb07ca4a5c/connect/runtime/src/test/java/org/apache/kafka/connect/util/clusters/EmbeddedConnectClusterAssertions.java#L411-L428] is used in several places to verify that a connector has been deleted. (This method may be renamed in an upcoming PR to something like {{{}assertConnectorAndTasksAreNotR…


## KAFKA-14898: [ MirrorMaker ] sync.topic.configs.enabled not working as expected
Bug · Resolved (Fixed) · Major · components: mirrormaker · labels: mirrormaker · created 2023-04-12 · resolved 2023-04-12

Hello,
In my replication set up , i do not want to sync the topic configs, the use case is to have different retention time for the topic on the target cluster, I am passing the config
[code/log omitted]
but this is not working as expected the topic retention time is being set to whatever is being set in the source cluster, looking at the mirrormaker logs i can see that MirrorSourceConnector is still setting the above config as true
[code/log omitted]
Can you please let me know if i am miss…

- **Greg Harris:** [~bseenu] Are you running MM2 with the MirrorMaker dedicated launcher? There's a known issue where a multi-node cluster is unable to persist configuration changes: https://issues.apache.org/jira/browse/KAFKA-10586 which has a fix to be released in 3.5.0. You can verify that the above is affecting y…
- **Srinivas Boga:** [~gharris1727] Thanks for your help on this Yes i could see that log message which you pointed out, i was running mirrormaker in distributed mode having 3 nodes and 10 tasks on each I have verified by running only on one node and it is working as expected Thanks, -srini

## KAFKA-14899: Revisit Action Queue
Sub-task · Open · Major · created 2023-04-12

With Kafka-14561 we introduced a notion for callback requests. It would be nice to standardize and combine action queue usage here. However, the current implementation of the callback request assumes local time is computed upon response send. 
This same paradigm may not be the case with the action queue. We should follow up and see what changes need to be made to combine the two.


## KAFKA-14900: Flaky test AuthorizerTest failing with NPE
Test · Resolved (Fixed) · Minor · components: kraft · labels: flaky-test · created 2023-04-12 · resolved 2023-04-14

The AuthorizerTest has multiple tests that appear to have the same flaky failure:
[code/log omitted]

- **Greg Harris:** This will be addressed in https://github.com/apache/kafka/pull/13543

## KAFKA-14901: Flaky test ExactlyOnceSourceIntegrationTest.testConnectorReconfiguration
Test · Resolved (Cannot Reproduce) · Major · components: connect · labels: flaky-test · created 2023-04-12 · resolved 2023-08-24

The EOS Source test appears to be very rarely failing (<5% chance) with the following error:
[code/log omitted]
which appears to be triggered by the following failure inside the broker:
[code/log omitted]

- **Greg Harris:** cc [~jolshan] [~dajac] [~hachikuji] [~mimaison] I have not seen this failure mode before, and I'm worried that this might be a recent regression. It also doesn't look like an error that is intended to be surfaced by the API in normal operations (I might expect a disconnect or ProducerFencedExceptio…
- **Justine Olshan:** So many transaction/init producer ID issues lately. I had to check this wasn't the same as https://issues.apache.org/jira/browse/KAFKA-14830  I've seen some init producer ID failures a few times as well (seeming more frequently) when testing. I was also wondering if this change could be related, b…
- **Mickael Maison:** [~gharris1727] Do you think this is a blocker for 3.5? I've not been able to reproduce this failure and nobody has taken the time to investigate this yet.
- **Mickael Maison:** Reducing severity and moving to the next release.
- **Greg Harris:** This flakiness is no longer present on trunk. I believe that another bug fix resolved the flakiness but I don't know which.

## KAFKA-14902: KafkaBasedLog infinite retries can lead to StackOverflowError
Bug · Resolved (Fixed) · Major · components: connect · created 2023-04-13 · resolved 2023-04-18

KafkaBasedLog subclasses use an infinite retry on producer sends, using a callback. Sometimes, when specific errors are encountered, the callback is invoked in the send call, on the calling thread. If this happens enough times, a stack overflow happens.
Example stacktrace from 2.5 (but the newest code can also encounter the same):
[code/log omitted]
Note the repeated KafkaProducer.send -> KafkaProducer.doSend -> KafkaStatusBackingStore$4.onCompletion calls, causing the issue.


## KAFKA-14903: MM2 Topic And Group Listener (KIP-918)
New Feature · Patch Available · Major · created 2023-04-13

MM2 has a dynamic topic and group filter mechanism, in which the replicated topics/groups can dynamically change, either due to changes in the available topics/groups, or changes in the filter settings.
In order to monitor the currently replicated topics/groups, MM2 should support a TopicListener and GroupListener plugin, which is triggered when MM2 changes the set of replicated topics/groups.


## KAFKA-14904: Flaky Test  kafka.api.TransactionsBounceTest.testWithGroupId()
Test · Resolved (Fixed) · Blocker · created 2023-04-13 · resolved 2023-04-20

After merging KAFKA-14561 I noticed this test still occasionally failed via 
org.apache.kafka.common.errors.TimeoutException: Timeout expired after 60000ms while awaiting EndTxn(true)
I will investigate the cause. 
Note: This error occurs when we are waiting for the transaction to be committed.

- **Justine Olshan:** Jenkins truncates this out since the bounced broker leads to a ton of aborted transaction errors, but after that we see: [code/log omitted] And a TON more out of sequence errors (probably most of the partitions). Will investigate further if this is a result of my change and if there are ways to fi…
- **Justine Olshan:** Further investigation shows this occurs after the verification failed with CONCURRENT_TRANSACTIONS error.  I will debug further and fix this case.
- **Justine Olshan:** The issue is the first request we verify is still in pending state. I suspect if we check the transaction is in pending ongoing state + verify + confirm the transaction we should be good to proceed. However, I will need to look a bit closer at what pending means here.
- **Justine Olshan:** Marking as a blocker since the commit that caused this regressed the previous behavior. Any verification that occurs too fast will cause OutOfSequence errors.

## KAFKA-14905: Failing tests in MM2 ForwardingAdmin test since KIP-894
Test · Resolved (Fixed) · Major · components: mirrormaker · labels: flaky-test · created 2023-04-13 · resolved 2023-04-21

There are three tests which are consistently failing in MirrorConnectorsWithCustomForwardingAdminIntegrationTest since the merge of KIP-894 in KAFKA-14420:
 * testReplicationIsCreatingTopicsUsingProvidedForwardingAdmin()
 * testCreatePartitionsUseProvidedForwardingAdmin()
 * testSyncTopicConfigUseProvidedForwardingAdmin()
[code/log omitted]


## KAFKA-14906: Extract the coordinator service log from server log
Improvement · Patch Available · Major · components: core · created 2023-04-14

Currently, the coordinator service log and server log are mixed together. When troubleshooting the coordinator problem, it is necessary to filter from the server log, which is not very convenient. Therefore, the coordinator log is separated like the controller log.

- **hudeqi:** This change will be reintroduced in version 4.x.
- **hudeqi:** This change will be reintroduced in version 4.x.
- **David Jacot:** Removed the fix version as this work is not planned in 4.0.

## KAFKA-14907: Add the traffic metric of the partition dimension in BrokerTopicStats
Improvement · Patch Available · Major · components: core · labels: KIP-922 · created 2023-04-14

{color:#172b4d}Currently, there are two metrics for measuring the traffic in topic dimensions: MessagesInPerSec, BytesInPerSec, but there are two problems:{color}
{color:#172b4d}1. It is difficult to intuitively reflect the problem of topic partition traffic inclination through these indicators, and it is impossible to clearly see which partition has the largest traffic and the traffic situation of each partition. But the partition dimension can solve this.{color}
{color:#172b4d}2. For the sud…


## KAFKA-14908: Sporadic "Address already in use" when starting kafka cluster embedded within tests
Bug · Reopened · Major · components: unit tests · created 2023-04-14

We have an integration test suite that starts/stops a kafka cluster before/after each test.   Kafka is being started programmatically within the same JVM that is running the tests.
Sometimes we get sporadic failures from with Kafka as it tries to bind the server socket.
[code/log omitted]
Investigation has shown that the socket is in the timed_wait state from a previous test.
I know Kafka supports ephemeral ports, but this isn't convenient to our use-case.  
I'd like to suggest that Kafka i…

- **Keith Wall:** Opened PR: https://github.com/apache/kafka/pull/13572
- **Divij Vaidya:** re-opening this since it was reverted
- **Divij Vaidya:** This is the second most frequent reason for build failures in the last 28 days: [https://ge.apache.org/scans/failures?search.relativeStartTime=P28D&search.rootProjectNames=kafka&search.timeZoneId=Europe/Berlin]  Raising the priority to Major
- **Luke Chen:** Thanks [~divijvaidya] , but I cannot see the `Address already in use` error from the gradle error output. How do you identify it?
- **Satish Duggana:** Moving it to 3.7.0 as we are near code freeze and it is not a blocker.
- _…3 more comments_

## KAFKA-14978: ExactlyOnceWorkerSourceTask does not remove parent metrics
Bug · Resolved (Fixed) · Major · components: connect · created 2023-05-09 · resolved 2023-05-11

ExactlyOnceWorkerSourceTask removeMetrics does not invoke super.removeMetrics, meaning that only the transactional metrics are removed, and common source task metrics are not.


## KAFKA-14979: Incorrect lag was calculated when markPartitionsForTruncation in ReplicaAlterLogDirsThread
Improvement · Resolved (Not A Problem) · Major · components: core · created 2023-05-09 · resolved 2023-08-24

When the partitions of ReplicaFetcherThread finished truncating, the ReplicaAlterLogDirsThread to which these partitions belong needs to be marked truncate. The lag value in the newState (PartitionFetchState) obtained in this process is still the original value (state.lag). If the truncationOffset is smaller than the original state.fetchOffset, then the original lag value is incorrect and needs to be updated. It should be the original lag value plus the difference between the original state.fetc…

- **hudeqi:** [GitHub Pull Request #13692|https://github.com/apache/kafka/pull/13692] is expired.

## KAFKA-14980: MirrorMaker consumers don't get configs prefixed with source.cluster
Bug · Resolved (Fixed) · Blocker · components: mirrormaker · created 2023-05-09 · resolved 2023-05-19

As part of KAFKA-14021, we made a change to MirrorConnectorConfig.sourceConsumerConfig() to grab all configs that start with "source.". Previously it was grabbing configs prefixed with "source.cluster.". 
This means existing connector configuration stop working, as configurations such as bootstrap.servers are not passed to source consumers.
For example, the following connector configuration was valid in 3.4 and now makes the connector tasks fail:
[code/log omitted]
The connector attempts to…

- **Mickael Maison:** cc [~ChrisEgerton]

## KAFKA-14981: Set `group.instance.id` in streams consumer so that rebalance will not happen if a instance is restarted
Improvement · Open · Minor · components: streams · created 2023-05-09

`group.instance.id` enables static membership so that if a consumer is restarted within `session.timeout.ms`, rebalance will not be triggered and originally assignment can be returned directly from broker. We can set this id in Kafka streams using `threadId` so that no rebalance is trigger within `session.timeout.ms`

- **Matthias J. Sax:** Very interesting idea – given that we persist the thread-id (aka process-id) in the state directory on local disk, it could help. And even if we don't persist it (because there is no local storage), it seems no harm would be done if the id changes every single time. Wondering if we would need a KIP…
- **A. Sophie Blee-Goldman:** Have we resolved all the known issues with static membership? IIRC there were some that required broker-side changes, could we accidentally introduce correctness-related bugs in Streams applications running against older clusters?  Maybe I'm being paranoid, but I thought we had begun to recommend a…
- **Matthias J. Sax:** I was not aware that there was (or maybe still are) issue. Are there any tickets for it?
- **Bruno Cadonna:** I have the same feeling as [~ableegoldman]. So, we should first ensure that the issues are solved, before proceeding with this ticket. In general, I would welcome Streams using static membership by default.

## KAFKA-14982: Improve the kafka-metadata-quorum output
Improvement · Resolved (Fixed) · Major · labels: need-kip · created 2023-05-10 · resolved 2023-05-29

When running kafka-metadata-quorum script to get the quorum replication status, I found the LastFetchTimestamp and LastCaughtUpTimestamp output is not human readable. The timestamp 1683701749161 is just a random integer to me. We should convert it into date/time (ex: May 10, 08:00 UTC), or if possible, convert it into strings like "10 seconds ago", "5 minutes ago"...
[code/log omitted]

- **Federico Valeri:** https://cwiki.apache.org/confluence/display/KAFKA/KIP-927%3A+Improve+the+kafka-metadata-quorum+output

## KAFKA-14983: Upgrade jetty-server to 9.4.51
Task · Resolved (Fixed) · Minor · created 2023-05-10 · resolved 2023-05-15

Kafka latest versions e.g. 3.4.0 includes jetty-server-9.4.48.v20220622.jar that includes 2 vulnerabilities: CVE-2023-26048 and CVE-2023-26049. Upgrading them to 9.4.51 would fix those issues.

- **Divij Vaidya:** There is a PR open for this [https://github.com/apache/kafka/pull/13673]  Although, I doubt that this will make it into 3.5.0 since it's past the code freeze date. The vulnerabilities are moderate/low in nature. I will let folks familiar with Connect framework chime in here but AFAIK, the first one…

## KAFKA-14984: DynamicBrokerReconfigurationTest.testThreadPoolResize() test is flaky 
Test · Resolved (Duplicate) · Major · labels: flaky-test · created 2023-05-10 · resolved 2023-08-25

The test sometimes fails with the below log 
[code/log omitted]

- **Justine Olshan:** Ah I missed this yesterday. I filed https://issues.apache.org/jira/browse/KAFKA-15404. Looks like someone assigned themselves, so I will close this one.

## KAFKA-14985: ConnectionQuotasTest.testListenerConnectionRateLimitWhenActualRateAboveLimit() test is flaky
Test · Resolved (Duplicate) · Major · created 2023-05-10 · resolved 2023-05-10

The test sometimes fails with the following error
[code/log omitted]

- **Manyanda Chitimbo:** A quick fix will be to bump the epsilon to a bigger value e.g 8 on [https://github.com/apovzner/kafka/blob/508a754f397b5a1939c44dfcba72ba996bc912c5/core/src/test/scala/unit/kafka/network/ConnectionQuotasTest.scala#L400] but I am not sure if that's enough to make the test  resilient , what do you thi…
- **Divij Vaidya:** We already have an open Jira (and a pending PR) for this: [https://issues.apache.org/jira/projects/KAFKA/issues/KAFKA-12319?filter=allopenissues]  Resolving this as duplicate. [~manyanda], in future, please search for existing Jira before creating new ones.
- **Divij Vaidya:** Resolving as duplicate of existing open JIRA.
- **Manyanda Chitimbo:** Thanks [~divijvaidya]

## KAFKA-14986: security vulnerability in jose4j-0.7.9.jar 
Bug · Open · Critical · labels: security-issue, vulnerabilities · created 2023-05-11

Kafka has a depenedency on the jose4j-0.7.9.jar 
jose4j-0.7.9.jar  has been identified with the WS-2023-0116. 
[https://www.mend.io/vulnerability-database/WS-2023-0116] 
could you please confirm is Kafka impacted by this security vulnerability.


## KAFKA-14987: Implement Group/Offset expiration
Sub-task · Resolved (Fixed) · Major · created 2023-05-11 · resolved 2023-10-12


## KAFKA-14988: Upgrade scalaCollectionCompact to v2.9 for CVE-2022-36944
Improvement · Resolved (Fixed) · Minor · created 2023-05-11 · resolved 2023-05-15

Current version of ScalaCollectionCompact library in trunk 2.6.0 suffers from a critical [CVE-2022-36944|https://github.com/advisories/GHSA-8qv5-68g4-248j]
The CVE does not impact Kafka as per https://issues.apache.org/jira/browse/KAFKA-14267  (hence, not marking this as critical) and is fixed in ScalaCollectionCompact v2.9 as per [https://github.com/scala/scala-collection-compat/pull/569]

- **Divij Vaidya:** [https://github.com/apache/kafka/pull/13673]

## KAFKA-15037: initialize unifiedLog with remoteStorageSystemEnable correctly
Sub-task · Resolved (Fixed) · Major · created 2023-05-30 · resolved 2023-06-05

UnifiedLog relied on the `remoteStorageSystemEnable` to identify if the broker is enabling remote storage, but we never pass this value from the config into UnifiedLog. So it'll always be false.


## KAFKA-15038: Use topic id/name mapping from the Metadata cache in the RemoteLogManager
Task · Patch Available · Minor · components: core · created 2023-05-30

Currently, the {{RemoteLogManager}} maintains its own cache of topic name to topic id [[1]|https://github.com/apache/kafka/blob/trunk/core/src/main/java/kafka/log/remote/RemoteLogManager.java#L138] using the information provided during leadership changes, and removing the mapping upon receiving the notification of partition stopped.
It should be possible to re-use the mapping in a broker's metadata cache, removing the need for the RLM to build and update a local cache thereby duplicating the in…

- **Divij Vaidya:** Alex is on leave. He has informed me that this could be picked up by someone else as well.
- **Divij Vaidya:** [~hudeqi] since you mentioned that you are interested in picking up items here: https://issues.apache.org/jira/browse/KAFKA-14912 , would you like to pick this one?
- **Owen C.H. Leung:** [~divijvaidya] I'd like to pick this up. I've done a bit diving and would like to clarify if my understanding is correct :  So essentially, in this ticket we want to remove the use of {*}ConcurrentMap<TopicPartition, Uuid> topicPartitionIds{*}, and leverage the cache available in *RemoteLogManagerC…
- **Divij Vaidya:** Hi [~owen-leung]  Than you for looking into this. Yes, we want to replace *ConcurrentMap<TopicPartition, Uuid> topicPartitionIds* cache in RemoteLogManager. However, instead we want to cache available in every broker called the Metadata cache [1]which will be the single source of authority on a bro…
- **hudeqi:** Hi, [~owen-leung]  Are you still following this issue? If you don't have time, I can take over. Thanks.
- _…6 more comments_

## KAFKA-15039: Reduce logging level to trace in PartitionChangeBuilder.tryElection()
Improvement · Resolved (Fixed) · Major · components: kraft · created 2023-05-30 · resolved 2023-06-01

A CPU profile in a large cluster showed PartitionChangeBuilder.tryElection() taking significant CPU due to logging.  Decrease the logging statements in that method from debug level to trace to mitigate the impact of this CPU hog under normal operations.

- **Divij Vaidya:** Thank you for the find. Could you please share the CPU profile and attach it to this ticket? It would be interesting to compare it with non-kraft profiles such as captured in https://issues.apache.org/jira/browse/KAFKA-14633

## KAFKA-15040: segment copy to remote storage won't work in KRaft mode
Sub-task · Resolved (Fixed) · Major · created 2023-05-31 · resolved 2023-06-09

Currently, when received LeaderAndIsr request, we'll notify remoteLogManager about this  leadership changed to trigger the following workflow. But LeaderAndIsr won't be sent in KRaft mode, instead, the topicDelta will be received.


## KAFKA-15041: Source Connector auto topic creation fails when topic is deleted and brokers don't support auto topic creation
Bug · Resolved (Won't Fix) · Major · components: connect · created 2023-05-31 · resolved 2024-05-22

[KIP-158|https://cwiki.apache.org/confluence/display/KAFKA/KIP-158%3A+Kafka+Connect+should+allow+source+connectors+to+set+topic-specific+settings+for+new+topics]  allows the source connectors to create topics even when the broker doesn't allow to do so. It does so by checking for every record if a topic needs to be created [https://github.com/apache/kafka/blob/trunk/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/AbstractWorkerSourceTask.java#L500.] To not always keep checking for…

- **Sagar Rao:** Ideally a worker restart should fix this but it didn't quite happen on my local testing.
- **Sagar Rao:** For now, setting the config `producer.override.max.block.ms` at a connector config level  or `producer.max.block.ms` at a worker config level to a lower value should fix this value. The problem is that the default value for the above config is[ set to Long.MAX_VALUE |https://github.com/apache/kafka/…

## KAFKA-15042: Clarify documentation on Tagged fields
Wish · Patch Available · Major · components: docs · created 2023-05-31

Hello,
I am currently working on an implementation of the Kafka protocol.
So far, all my code is working as intended through serialising requests and deserialising response as long as I am not using the flex requests system.
I am now trying to implement the flex requests system but the documentation is scarce on the subject of tagged fields.
If we take the Request Header v2:
[code/log omitted]
Here, the BNF seems violated. TAG_BUFFER is not a value in this situation. It appears to be a typ…

- **Adrian Preston:** [~smashingquasar], Looking at the hex dump of your APIVersions request, I think you are correctly encoding the empty tag field as a single 0x00 byte. It looks, however, like the compact string encoding (used for the 'client_software_name' and 'client_software_version' fields) is adding an unexpecte…

## KAFKA-15043: Create a kcontroller metric for expired broker heartbeats
Improvement · Open · Major · created 2023-05-31


## KAFKA-15044: Snappy v.1.1.9.1 NoClassDefFound on ARM machines
Bug · Resolved (Fixed) · Major · created 2023-05-31 · resolved 2023-05-31

We upgraded our snappy dependency but v1.1.9.1 has compatibility issues with arm. We should upgrade to v1.1.10.0 which resolves this issue.


## KAFKA-15045: Move Streams task assignor to public configs
New Feature · Resolved (Fixed) · Major · components: streams · labels: kip · created 2023-05-31 · resolved 2024-06-19

https://cwiki.apache.org/confluence/display/KAFKA/KIP-924%3A+customizable+task+assignment+for+Streams


## KAFKA-15046: Produce performance issue under high disk load
Improvement · Resolved (Fixed) · Major · components: core · labels: performance · created 2023-06-01 · resolved 2023-11-29

* Phenomenon:
 ** !image-2023-06-01-12-46-30-058.png|width=259,height=236!
 ** Producer response time 99%ile got quite bad when we performed replica reassignment on the cluster
 *** RequestQueue scope was significant
 ** Also request-time throttling happened at the incidental time. This caused producers to delay sending messages in the mean time.
 ** The disk I/O latency was higher than usual due to the high load for replica reassignment.
 *** !image-2023-06-01-12-56-19-108.png|width=255,h…

- **Haruki Okada:** If the suggestion (stop fsync-ing) makes sense, I'm happy to submit a patch.
- **Divij Vaidya:** Thank you for the investigation folks. We have an active PR right now [1] which makes producer snapshot flush to disk asynchronously. The thread blocking problem due to fsync will be resolved by it. [1] https://github.com/apache/kafka/pull/13782
- **Haruki Okada:** Oh I haven't noticed there's another ticket and already the fix is available. Thank you, I will take a look!
- **Haruki Okada:** Hm, when I dug into further this, I noticed there's another path that causes essentially same phenomenon. [code/log omitted] LeaderEpoch checkpointing also calls fsync with holding Log#lock and blocking request-handler threads to append in the meantime. This is called by scheduler thread on log-s…
- **Divij Vaidya:** Yes that is right, leaderEpochCheckpoint is another I/O operation Kafka performs while holding the global partition lock.  IMO, we need to move to async disk I/O using [io_uring|https://unixism.net/loti/what_is_io_uring.html] to prevent thread blocking (and lock contention) while performing disk I/…
- _…12 more comments_

## KAFKA-15047: Handle rolling segments when the active segment's retention is breached incase of tiered storage is enabled.
Improvement · Resolved (Fixed) · Major · created 2023-06-01 · resolved 2023-11-28

Active segments are not copied by remote storage subsystem. But they can be eligible for retention cleanup. 
So, we need to roll the active segment incase remote storage is enabled so that this can be eligible to be copied by the remote storage subsystem and eventually picked up for retention cleanup.

- **Henry Cai:** I created a topic with local.retention.ms=120000 (2 minutes) ``` bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic topic1 --config remote.storage.enable=true --config segment.bytes=512000 --config retention.ms=360000000 --config local.retention.ms=120000 ``` The segments are…
- **Luke Chen:** [~hcai@pinterest.com] , the retention implementation PR is under review now: [https://github.com/apache/kafka/pull/13561] . FYI

## KAFKA-15096: CVE 2023-34455 - Vulnerability identified with Apache kafka
Bug · Resolved (Fixed) · Major · created 2023-06-16 · resolved 2023-06-19

A new vulnerability CVE-2023-34455 is identified with apache kafka dependency. The vulnerability is coming from snappy-java:1.1.8.4
Version 1.1.10.1 contains a patch for this issue. Please upgrade the snappy-java version to fix this issue
snappy-java is a fast compressor/decompressor for Java. Due to use of an unchecked chunk length, an unrecoverable fatal error can occur in versions prior to 1.1.10.1.
The code in the function hasNextChunk in the fileSnappyInputStream.java checks if a given s…

- **Manyanda Chitimbo:** Thank you for reporting the issue [~Sasikumarms] an PR has been opened in  [https://github.com/apache/kafka/pull/13865] to bump the version.  Once merged, I'll let the release managers determine how far the fix can be backported.
- **Josep Prat:** I cherry-picked this to 3.3, 3.4 and 3.5

## KAFKA-15097: NoSuchFileException in LogCleaner Operation.
Bug · Open · Blocker · components: log cleaner · created 2023-06-16

Currently we are facing NoSuchFileException in LogCleaner, which is critical error as result platform get shutown.
We are running Kafka in Kraft Mode.
The cluster is having 3 Node.
Kafka version - 3.3.1
We are  facing issue systematically, which occurs after retention reached.
Here's the logs of Node 1 for consumer offset 4146 for which we have faced NoSuchFileException on 24 may 2023
Config :
[^config.txt]
^Logs :^
^Server Node 1 [^server.log]^
Log Cleaner :
[^log-cleaner.log]
^__co…

- **Mukesh Mishra:** There is something wired in log 4146 of consumer offset : In 00000000000004146.log.swap, i can see below records : [code/log omitted] baseOffset (7435, 7740) mentioned in 00000000000004146.log.swap which is already present in 00000000000006340.log (they should present only in  6340.log) [code/lo…
- **Said BOUDJELDA:** I really want to take this ticket and start first by reproducing the issue, [~mksmsr]  I'll of course need your to at least reproduce this bug

## KAFKA-15098: KRaft migration does not proceed and broker dies if authorizer.class.name is set
Bug · Resolved (Fixed) · Blocker · components: kraft · created 2023-06-16 · resolved 2023-06-22

[ERROR] 2023-06-16 20:14:14,298 [main] kafka.Kafka$ - Exiting Kafka due to fatal exception
java.lang.IllegalArgumentException: requirement failed: ZooKeeper migration does not yet support authorizers. Remove authorizer.class.name before performing a migration.


## KAFKA-15099: Flaky Test kafka.api.TransactionsTest.testBumpTransactionalEpoch(String).quorum=kraft
Bug · Open · Major · components: unit tests · labels: flaky-test · created 2023-06-16

This one often fails with: 
org.apache.kafka.common.errors.TimeoutException: Timeout expired after 60000ms while awaiting InitProducerId
seems like a Kraft only issue.

- **Divij Vaidya:** Another instance for kraft only failure: [https://ci-builds.apache.org/job/Kafka/job/kafka-pr/job/PR-12976/3/testReport/junit/kafka.api/TransactionsTest/Build___JDK_8_and_Scala_2_12___testBumpTransactionalEpoch_String__quorum_kraft_2/]

## KAFKA-15100: Unsafe to call tryCompleteFetchResponse on request timeout
Bug · Resolved (Fixed) · Major · components: kraft · created 2023-06-17 · resolved 2023-08-09

When the fetch request times out the future is completed from the "raft-expiration-executor" SystemTimer thread. KafkaRaftClient assumes that tryCompleteFetchResponse is always called from the same thread. This invariant is violated in this case.
[code/log omitted]
One solution is to always build an empty response if the future was completed exceptionally. This works because the ExpirationService completes the future with a `TimeoutException`.
A longer-term solution is to use a more flexible…


## KAFKA-15101: Improve testRackAwareRangeAssignor test
Improvement · Open · Major · components: unit tests · labels: flaky-test · created 2023-06-19

testRackAwareRangeAssignor has been really flaky recently. As a mitigation, we have increased the timeouts to 30s in the test. This should already improve it. However, it may be better to revise the entire test to avoid those.

- **Kirk True:** Looks like a duplicate of KAFKA-15020.

## KAFKA-15102: Mirror Maker 2 - KIP690 backward compatibility
Bug · Closed (Fixed) · Major · components: mirrormaker · created 2023-06-19 · resolved 2023-08-15

According to KIP690, "When users upgrade an existing MM2 cluster they don’t need to change any of their current configuration as this proposal maintains the default behaviour for MM2."
Now, the separator is subject to customization.
As a consequence, when an MM2 upgrade is performed, if the separator was customized with replication.policy.separator, the name of this internal topic changes. It then generates issues like:
It has been observed that the replication can then be broken sometimes se…

- **Chris Egerton:** [~ddufour1a] Thanks for raising this. I believe if we wanted to preserve backward compatibility perfectly, we would have had to ignore the custom separator when creating topics affected by KIP-690, and possibly introduced separate opt-in configuration logic to disable that behavior (i.e., resume tak…
- **Omnia Ibrahim:** Thanks, [~ddufour1a] for raising this. The backward compatibility mentioned in the KIP accounted only for using the default separator configuration and didn't address the usage custom separator (my mistake here). [~ChrisEgerton] I think having `{{{}replication.policy.internal.topic.separator.enabled…
- **Chris Egerton:** [~omnia_h_ibrahim] Good call 👍 we should definitely update the compatibility section in the KIP to mention this. We may also want list the affected versions and link to this issue for further context.
- **Omnia Ibrahim:** [~ChrisEgerton] I updated the compatibility section in the KIP with the impacted versions and linked to this JIRA. I can open a small KIP to have `{{{}replication.policy.internal.topic.separator.enabled` if you don't have time to do it. {}}}
- **Chris Egerton:** Thanks [~omnia_h_ibrahim], I'd love it if you could take on that KIP!
- _…6 more comments_

## KAFKA-15103: Flaky test KRaftClusterTest.testCreateClusterAndPerformReassignment
Bug · Open · Major · components: core · labels: flaky-test · created 2023-06-19

{{The test kafka.server.KRaftClusterTest.testCreateClusterAndPerformReassignment() is failing: [https://ci-builds.apache.org/job/Kafka/job/kafka-pr/job/PR-13865/2/testReport/junit/kafka.server/KRaftClusterTest/Build___JDK_8_and_Scala_2_12___testCreateClusterAndPerformReassignment__/]}}
h3. Error Message
[code/log omitted]
h3. Stacktrace
[code/log omitted]

- **Josep Prat:** h3. Standard Output [code/log omitted]

## KAFKA-15104: Flaky test MetadataQuorumCommandTest for method testDescribeQuorumReplicationSuccessful
Bug · Patch Available · Major · components: tools · labels: flaky-test · created 2023-06-19

The MetadataQuorumCommandTest has become flaky on CI, I saw this failing: org.apache.kafka.tools.MetadataQuorumCommandTest.[1] Type=Raft-Combined, Name=testDescribeQuorumReplicationSuccessful, MetadataVersion=3.6-IV0, Security=PLAINTEXT
Link to the CI: https://ci-builds.apache.org/job/Kafka/job/kafka-pr/job/PR-13865/2/testReport/junit/org.apache.kafka.tools/MetadataQuorumCommandTest/Build___JDK_8_and_Scala_2_12____1__Type_Raft_Combined__Name_testDescribeQuorumReplicationSuccessful__MetadataVers…

- **Divij Vaidya:** Another instance - [https://ci-builds.apache.org/job/Kafka/job/kafka-pr/job/PR-13831/7/]
- **Justine Olshan:** I saw this fail many times here:  [https://ci-builds.apache.org/blue/organizations/jenkins/Kafka%2Fkafka-pr/detail/PR-15183/3/tests]
- **Lianet Magrans:** This is still flaky, showing on [https://github.com/apache/kafka/actions/runs/28885044689/job/85685508767?pr=22768] Added the flaky tag
- **Edmond Abraham:** Pull request: https://github.com/apache/kafka/pull/23466 The previously quarantined test passed 60 generated KRaft invocations after the UpdateVoter changes.

## KAFKA-15105: Flaky test FetchFromFollowerIntegrationTest.testFetchFromLeaderWhilePreferredReadReplicaIsUnavailable
Bug · Open · Major · components: core · labels: flaky-test · created 2023-06-19

Test  integration.kafka.server.FetchFromFollowerIntegrationTest.testFetchFromLeaderWhilePreferredReadReplicaIsUnavailable() became flaky. An example can be found here: https://ci-builds.apache.org/job/Kafka/job/kafka-pr/job/PR-13865/2/testReport/junit/integration.kafka.server/FetchFromFollowerIntegrationTest/Build___JDK_11_and_Scala_2_13___testFetchFromLeaderWhilePreferredReadReplicaIsUnavailable___2/
The error might be caused because of a previous kafka cluster used for another test wasn't cle…

- **Max Riedel:** I would like to work on this issue. I'm still trying to understand how the build infrastructure works. Can someone give me a hint, how to reproduce the behavior?
- **Josep Prat:** Hi [~riedelmax], feel free to assign this issue to yourself :) {quote}I'm still trying to understand how the build infrastructure works. Can someone give me a hint, how to reproduce the behavior? {quote} In this rely part of the problem, many times these issues are not easily reproducible on your…
- **Max Riedel:** Hi [~josep.prat]  Thanks for giving me the necessary Jira rights. I was able to assign the ticket to me now. So far, all test runs I did on my local environment passed. But I will try the option to run until failure and see what I can learn from that. My question was about the CI. Is it correct t…
- **Josep Prat:** Hi [~riedelmax] , Only maintainers + a subgroup of collaborators can rerun builds in CI, but even for them, they can just run them as they are (no more detailed output). And sorry, I just realized I copy pasted the wrong ci build link. This is the right one: [https://ci-builds.apache.org/job/Kafka/…

## KAFKA-15106: AbstractStickyAssignor may stuck in 3.5
Bug · Resolved (Fixed) · Major · components: clients · created 2023-06-19 · resolved 2023-08-04

this could reproduce in ut easy,
just int org.apache.kafka.clients.consumer.internals.AbstractStickyAssignorTest#testLargeAssignmentAndGroupWithNonEqualSubscription,
plz set 
partitionCount=200, 
consumerCount=20,  you can see 
isBalanced will return false forever.

- **Kirk True:** [~flashmouse] Thank you for the test case. I was able to reproduce the hanging behavior. I would have assumed that the {{@Timeout}} would have stopped the test after 90 seconds, but it didn't appear to when I ran it 🤔 I'm not familiar with this area of the code, so I'm not sure if the stated values…
- **li xiangyuan:** I wonder whether modify the line in function `isBalanced` could solve it. current: [code/log omitted] fixed: [code/log omitted]
- **li xiangyuan:** [~rajinisivaram@gmail.com]  I notice you are the writer, could u give a check?
- **li xiangyuan:** I deem the root cause is the check `isBalanced` have some logical error so the function `performReassignments` will run the whole loop body, this loop is very slow, each time pick one partition, compare its current assignor with all consumers subscribe the partition and try to find one hold fewer pa…

## KAFKA-15178: Poor performance of ConsumerCoordinator with many TopicPartitions
Bug · Open · Minor · components: consumer · labels: easyfix, patch-available · created 2023-07-11

Doing some profiling of my Kafka Streams application, I noticed that the {{pollPhase}} suffers from a minor performance issue.
See the pink tree on the left of the flame graph below.  !pollPhase.png|width=1028,height=308!
{{ConsumerCoordinator.poll}} calls {{{}rejoinNeededOrPending{}}}, which checks the current {{metadataSnapshot}} against the {{{}assignmentSnapshot{}}}. This comparison is a deep-equality check, and if there's a large number of topic-partitions being consumed by the applicatio…

- **A. Sophie Blee-Goldman:** Nice catch!

## KAFKA-15179: Add integration tests for the FileStream Sink and Source connectors
Test · Resolved (Done) · Minor · created 2023-07-11 · resolved 2023-09-07

Add integration tests for the FileStream Sink and Source connectors covering various different common scenarios.


## KAFKA-15180: Generalize integration tests to change use of KafkaConsumer to Consumer
Sub-task · Resolved (Fixed) · Major · components: clients, consumer · labels: consumer-threading-refactor · created 2023-07-11 · resolved 2023-07-14

For the consumer threading refactor project, we're introducing a new implementation of the {{Consumer}} interface. However, most of the instances in the integration tests specifically use the concrete implementation {{{}KafkaConsumer{}}}. This task is to generalize those uses where possible to use the {{Consumer}} interface.


## KAFKA-15181: Race condition on partition assigned to TopicBasedRemoteLogMetadataManager 
Sub-task · Resolved (Fixed) · Major · components: core · labels: tiered-storage · created 2023-07-12 · resolved 2023-09-07

TopicBasedRemoteLogMetadataManager (TBRLMM) uses a cache to be prepared whever partitions are assigned.
When partitions are assigned to the TBRLMM instance, a consumer is started to keep the cache up to date.
If the cache hasn't finalized to build, TBRLMM fails to return remote metadata about partitions that are store on the backing topic. TBRLMM may not recover from this failing state.
A proposal to fix this issue would be wait after a partition is assigned for the consumer to catch up. A si…

- **Abhijeet Kumar:** Hi [~jeqo] . I am curious to understand why TBRLMM may not recover from the failing state at all. Could you elaborate?
- **Jorge Esteban Quilcate Otoya:** Sure. The TBRLMM is not the one not recovering, but the Replica Fetcher.  My understanding is that this issue happens when a Replica is recovering its state after being offline. TBRLMM receives partitions assigned, starts managed, and is marked as initialized and open to receive requests; however t…
- **Abhijeet Kumar:** As far as I know, the ReplicaFetcher keeps retrying and should eventually be able to find the metadata in the RLMM. We should not be blocking while waiting for the consumers to catch up as the ReplicaFetcher acquires a global lock and it will prevent other ReplicaFetchers from running as well as Lea…
- **Abhijeet Kumar:** The changes discussed on [https://github.com/apache/kafka/pull/14012] were addressed in [https://github.com/apache/kafka/pull/14127|https://github.com/apache/kafka/pull/14127.]. The ReplicaFetcher thread will receive a retryable exception if the cache is not initialized for the topic partition. The…

## KAFKA-15182: Normalize offsets before invoking SourceConnector::alterOffsets
Improvement · Resolved (Fixed) · Major · components: connect · created 2023-07-12 · resolved 2023-07-14

See discussion [here|https://github.com/apache/kafka/pull/13945#discussion_r1260946148]
TLDR: When users attempt to externally modify source connector offsets via the {{PATCH /offsets}} endpoint (introduced in [KIP-875|https://cwiki.apache.org/confluence/display/KAFKA/KIP-875%3A+First-class+offsets+support+in+Kafka+Connect]), type mismatches can occur between offsets passed to {{SourceConnector::alterOffsets}} and the offsets that are retrieved by connectors / tasks via an instance of {{OffsetS…


## KAFKA-15183: Add more controller, loader, snapshot emitter metrics
Improvement · Resolved (Fixed) · Major · created 2023-07-12 · resolved 2023-08-25

Add the controller, loader, and snapshot emitter metrics from KIP-938.

- **Colin McCabe:** Most of the KIP-938 metrics are now implemented for 3.6. The exception is the ForwardingManager metrics, which will have to wait until 3.7.

## KAFKA-15184: New consumer internals refactoring and clean up
Sub-task · Resolved (Resolved) · Blocker · components: clients, consumer · labels: consumer-threading-refactor, kip-848-e2e, kip-848-preview · created 2023-07-12 · resolved 2023-10-24

Minor refactoring of the new consumer internals including introduction of the {{RequestManagers}} class to hold references to the {{RequestManager}} instances.

- **Kirk True:** See pull request [#14406|https://github.com/apache/kafka/pull/14406].

## KAFKA-15185: Consumers using the latest strategy may lose data after the topic adds partitions
Bug · Resolved (Duplicate) · Major · components: consumer · created 2023-07-13 · resolved 2023-07-14

h2. condition:
1. Business topic adds partition
2. The configuration metadata.max.age.ms of producers and consumers is set to five minutes.
But the producer discovered the new partition before the consumer, and generated 100 messages to the new partition.
3. The consumer parameter auto.offset.reset is set to *latest*
h2. result:
Consumers will lose these 100 messages
First of all, we cannot directly set auto.offset.reset to {*}earliest{*}.
Because the user's demand is that a newly subscr…

- **RivenSun:** Hi [~showuon]  [~guozhang]  can you give any suggestion? Thanks.
- **Haruki Okada:** FYI: maybe duplicated with https://issues.apache.org/jira/browse/KAFKA-12478, https://issues.apache.org/jira/browse/KAFKA-12261
- **RivenSun:** Thanks

## KAFKA-15186: AppInfo metrics don't contain the client-id
Task · Resolved (Fixed) · Major · components: metrics · labels: need-kip · created 2023-07-13 · resolved 2025-09-21

All Kafka components register AppInfo metrics to track the application start time or commit id.
The AppInfoParser class registers a JMX MBean with the provided client-id but when it adds metrics to the Metrics registry the client-id is not included. 
This means if you use a custom MetricsReporter, the metrics you get don't have the client-id.

- **Prem Kamal:** Hey [~mimaison], this task looks good for a newbie. Can I assign it myself?
- **Mickael Maison:** The logic should not be hard to implement but as this adds metrics it requires a small KIP. See the process on https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Improvement+Proposals
- **Prem Kamal:** Sure will go through the process and if possible will raise a KIP. Thanks.
- **Ken Huang:** Hello [~Prem237], If you won't work on this, may I take this issue?

## KAFKA-15187: Add headers to partition method.
New Feature · Open · Major · created 2023-07-13

Add headers to partition method.
This will enable selecting partitions based on header values.

- **Jacob Tomy:** Can someone help me assign this to me.  These are my planned changes : https://github.com/apache/kafka/pull/13981
- **Bruno Cadonna:** I added you to the contributor group. Now you should be able to assign the ticket to yourself.
- **Bruno Cadonna:** In the PR, I see that you want to change the `Partitioner` interface. Since that is a public interface, you need to write a KIP and get it accepted. See https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Improvement+Proposals
- **Jacob Tomy:** Hi [~cadonna]  Thanks for adding me to the contributors group. I was facing trouble accessing the confluence last day. I'm able to access it now. I will create the KPI and proceed.
- **Jacob Tomy:** KPI : https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=263424937
- _…1 more comments_

## KAFKA-15188: Implement more of the remaining PrototypeAsyncConsumer APIs
Sub-task · Resolved (Fixed) · Blocker · components: clients, consumer · labels: consumer-threading-refactor, kip-848-e2e, kip-848-preview · created 2023-07-13 · resolved 2023-10-24

There are several {{Consumer}} APIs that only touch the {{ConsumerMetadata}} and/or {{SubscriptionState}} classes; they do not perform network I/O or otherwise block. These can be implemented without needing {{RequestManager}} updates and include the following APIs:
 - {{committed}}
 - {{currentLag}}
 - {{metrics}}
 - {{pause}}
 - {{paused}}
 - {{position}}
 - {{resume}}
 - {{seek}}
 - {{seekToBeginning}}
 - {{seekToEnd}}
 - {{subscribe}}

- **Kirk True:** See PR [#14406|https://github.com/apache/kafka/pull/14406].

## KAFKA-15289: Support KRaft mode in RequestQuotaTest
Sub-task · Resolved (Fixed) · Major · labels: newbee · created 2023-08-01 · resolved 2023-08-14

we are calling `zkBrokerApis` in RequestQuotaTest, we should ensure kraft broker apis are also supported, so use clientApis as far as possible.use zkBrokerApis.clientApis instead of ApiKeys.zkBrokerApis.


## KAFKA-15290: Add support to onboard existing topics to tiered storage
Sub-task · Resolved (Fixed) · Major · created 2023-08-01 · resolved 2023-08-24

This task is about adding support to enable tiered storage for existing topics in the cluster.

- **Divij Vaidya:** When implementing this Jira, please ensure that this comments is addressed: [https://github.com/apache/kafka/pull/13947#discussion_r1294782503]
- **Divij Vaidya:** When implementing this Jira, please ensure that this comment is addressed: https://github.com/apache/kafka/pull/13947#discussion_r1300052574
- **Kamal Chandraprakash:** [~divijvaidya]  The below comment is not addressed, we can take it together with [KIP-950|https://cwiki.apache.org/confluence/display/KAFKA/KIP-950%3A++Tiered+Storage+Disablement]: [https://github.com/apache/kafka/pull/13947#discussion_r1294782503]

## KAFKA-15291: Implement Versioned interfaces in common Connect plugins
Improvement · Resolved (Fixed) · Major · components: connect · created 2023-08-01 · resolved 2023-08-10

In KAFKA-14863, we changed the plugin scanning logic to allow plugins to opt-in to the Versioned interface individually, when previously it was limited to Connector plugins.
To take advantage of this change, we should have all of the plugins built via the Kafka repository opt-in, and provide the environment's Kafka version from the AppInfoParser.getVersion().
See the FileStreamSinkConnector as an example of the the version() method implementation.
All subclasses of Converter, HeaderConverter,…

- **Aindriú Lavelle:** Hey [~gharris1727] I can pick this up. if you want to assign it to me. Thanks! Also let me know if its desirable to also update test subclasses with this implementation.
- **Greg Harris:** [~aindriú] Thanks for looking at this! Please include most of test classes as well. We should probably leave one plugin which is left un-Versioned to test out the UNDEFINED_VERSION behavior.
- **Aindriú Lavelle:** PR [https://github.com/apache/kafka/pull/14159] has been opened to implement these changes. StringConverter has been left un implemented so that the UNDEFINED_VERSION behaviour can be tested.

## KAFKA-15292: Flaky test IdentityReplicationIntegrationTest#testReplicateSourceDefault()
Test · Resolved (Fixed) · Major · components: mirrormaker · labels: flaky-test, mirror-maker, mirrormaker · created 2023-08-01 · resolved 2024-08-06

The test testReplicateSourceDefault in `org.apache.kafka.connect.mirror.integration.IdentityReplicationIntegrationTest is flaky about 2% of the time as shown in [Gradle Enterprise|[https://ge.apache.org/scans/tests?search.relativeStartTime=P90D&search.rootProjectNames=kafka&search.timeZoneId=America/Los_Angeles&tests.container=org.apache.kafka.connect.mirror.integration.IdentityReplicationIntegrationTest&tests.sortField=FLAKY]].
[code/log omitted]

- **Greg Harris:** The listed exception is shadowing the real exception, which is probably a shutdown timeout. I've opened KAFKA-15392 to resolve the exception shadowing which should hopefully make it easier to diagnose this flakiness.
- **Chris Egerton:** This test is no longer failing on trunk and [has been green for the last week|https://ge.apache.org/scans/tests?search.rootProjectNames=kafka&search.startTimeMax=1722970250359&search.startTimeMin=1722312000000&search.tags=trunk&search.timeZoneId=America%2FNew_York&tests.container=org.apache.kafka.co…

## KAFKA-15293: Update metrics doc to add tiered storage metrics
Sub-task · Resolved (Fixed) · Critical · components: documentation · created 2023-08-02 · resolved 2023-09-05


## KAFKA-15294: Make remote storage related configs as public (i.e. non-internal)
Sub-task · Resolved (Fixed) · Blocker · created 2023-08-02 · resolved 2023-08-28

We should publish all the remote storage related configs in v3.6.0. It can be verified by:
[code/log omitted]
{{}}


## KAFKA-15295: Add config validation when remote storage is enabled on a topic
Sub-task · Resolved (Fixed) · Major · created 2023-08-02 · resolved 2023-08-15

If system level remote storage is not enabled, then enabling remote storage on a topic should throw exception while validating the configs. 
See https://github.com/apache/kafka/pull/14114#discussion_r1280372441 for more details

- **Luke Chen:** [~ckamal] , are you still working on this? If you don't have time, I can work on it. Please let me know. Thanks.
- **Kamal Chandraprakash:** [~showuon]  I'm not working on this one currently. Thanks for taking it forward!

## KAFKA-15296: Allow committing offsets for Dropped records via SMTs
Bug · Open · Major · components: connect · created 2023-08-02

Currently the connect Runtime doesn't commit the offsets of records which have been dropped due to SMT. This can lead to issues if the dropped record's partition reflects a source partition and the connector depends upon the committed offsets to make progress. In such cases, the connector might just stall. We should enable committing offsets for dropped records as well. Note that today if a record is dropped because exactly-once support is enabled and the connector chose to abort the batch conta…


## KAFKA-15297: Cache flush order might not be topological order 
Bug · Open · Major · components: streams · created 2023-08-02

The flush order of the state store caches in Kafka Streams might not correspond to the topological order of the state stores in the topology. The order depends on how the processors and state stores are added to the topology. 
In some cases downstream state stores might be flushed before upstream state stores. That means, that during a commit records in upstream caches might end up in downstream caches that have already been flushed during the same commit. If a crash happens at that point, thos…

- **A. Sophie Blee-Goldman:** Were you able to (re)produce this issue? I'm a bit surprised because I always thought the state stores were maintained in strict topological order, both when building them initially and then when registering them. The stores are flushed in the order that they are registered, which corresponds to th…
- **Matthias J. Sax:** The ticket description contains an example to reproduce it (and there is also a png attachment visualizing the topology).  {quote}which in turn *should* reflect the topological order of the attached processor nodes. {quote} That's not always the case unfortunately.
- **Bruno Cadonna:** [~ableegoldman] You can observe the flush order by feeding some records into the input topics, waiting for a commit, and looking for the following log message: https://github.com/apache/kafka/blob/2e1947d240607d53f071f61c875cfffc3fec47fe/streams/src/main/java/org/apache/kafka/streams/processor/inte…
- **Guozhang Wang:** I think this is indeed a general issue, that state stores are initialized in the order of the topology which is essentially the "processor node order", as in ``InternalTopologyBuilder#build``. This works when a state store is only associated with one processors, or when a store is associated with mu…
- **Bruno Cadonna:** [~guozhang] Yes, I agree the issue is when state stores are connected to PAPI operators because they can basically connect to state stores at any location in the topology graph. I also thought about the solution you describe and discussed it with [~mjsax], [~wcarlson5], [~lihaosky], and [~alisa23].…
- _…2 more comments_

## KAFKA-15298: Disable DeleteRecords on Tiered Storage topics
Sub-task · Resolved (Won't Fix) · Major · labels: tiered-storage · created 2023-08-02 · resolved 2023-08-09

Currently the DeleteRecords API does not work with Tiered Storage. We should ensure that this is reflected in the responses that clients get when trying to use the API with tiered topics.

- **Kamal Chandraprakash:** [~christo_lolov] Could you explain why DeleteRecords API won't work with tiered storage? The DELETE_RECORDS API increments the log-start-offset and waits for the low-watermark to move till the requested offset. With {{deleteLogStartOffsetBreachedSegments}} in [https://github.com/apache/kafka/pull/1…
- **Christo Lolov:** Heya [~ckamal]! Thanks for pointing me to the pull request. I had not reviewed it so I wasn't aware of this particular change (https://github.com/apache/kafka/pull/13561/files#diff-10e27a71dc3dec3463df7752ab07f6227cf70bcee70a93a86b5984e020beae05L984) which I believe addresses my concern. Give me som…

## KAFKA-15299: Support left stream-table join on foreign key
New Feature · Resolved (Incomplete) · Major · components: streams · labels: kip · created 2023-08-02 · resolved 2025-01-04

KIP-955: [https://cwiki.apache.org/confluence/display/KAFKA/KIP-955%3A+Add+stream-table+join+on+foreign+key]
Currently in Kafka Streams DSL, KStream to KTable joins could only be performed with the keys. However in practice it is often required to join the messages in Kafka topics using message field as a "foreign key" with the following pattern:  
streamX.leftJoin(tableY, RecordTableY::getForegnKey, joiner).to("output-topic-name")
The left loin on foreign key operation will result in a strea…

- **Matthias J. Sax:** Closing this ticket as "incomplete". The KIP discussion did not lead to a resolution. We can of course reopen this ticket and restart the KIP discussion at any time.

## KAFKA-15371: MetadataShell is stuck when bootstrapping
Bug · Resolved (Fixed) · Major · created 2023-08-17 · resolved 2025-04-14

I  downloaded the 3.5.1 package and startup it, then use metadata shell to inspect the data
[code/log omitted]
Then process will stuck at loading.
!image-2023-08-17-10-35-36-067.png!

- **liran avi:** Hi  I get this issue in version 3.6.0 and also in 3.5.1  in my case rarely I can access to the CLI but I didn't get all the options there (missing folders) more than that sometimes I get this error : !image-2023-10-31-09-04-53-966.png|width=654,height=184! when I run the lsof command it looks l…
- **Christian Lefebvre:** Weirdly, I had the same case than [~dengziming], without any output, but this morning I've the same exception message than [~lirangazer]  The difference is perhaps because the server was running today but stopped yesterday : maybe a race condition causes the error when the topic is written by serve…
- **Christian Lefebvre:** It becomes more and more weird ...  * with stopped node, command hangs on "loading..."  * if I set {{{}log4j.rootLogger=INFO{}}}, I get the prompt  * with started server, I often get the NonWritableChannelException but sometimes I get the prompt When I got the prompt, exploring node tree works f…
- **Oleg Opolev:** I was never able to read the metadata in the cluster. Versions kafka 3.6.0 ./bin/kafka-metadata-shell.sh -s ../kafka_2.13-3.6.0/log/__cluster_metadata-0/00000000000008838965.log Loading... [2024-01-11 12:23:15,640] ERROR Encountered shell fault: Error loading metadata log record from offset 10032…
- **Rashmi:** Facing similar error message as [~endoftime] , but executing a different workflow: 3 Node cluster with instance of Kafka in KRaft mode running on each node.  Simulating an unexpected shutdown by powering off all VMs in the cluster. Then, bringing them back by powering on all the VMs. We see Kafka…
- _…3 more comments_

## KAFKA-15372: MM2 rolling restart can drop configuration changes silently
Bug · Resolved (Fixed) · Major · components: mirrormaker · created 2023-08-17 · resolved 2023-12-12

When MM2 is restarted, it tries to update the Connector configuration in all flows. This is a one-time trial, and fails if the Connect worker is not the leader of the group.
In a distributed setup and with a rolling restart, it is possible that for a specific flow, the Connect worker of the just restarted MM2 instance is not the leader, meaning that Connector configurations can get dropped.
For example, assuming 2 MM2 instances, and one flow A->B:
 # MM2 instance 1 is restarted, the worker in…

- **Greg Harris:** Hi [~durban] Thanks for the bug report. Is this reproducible with 3.5.0 and `dedicated.mode.enable.internal.rest` set to `true`? This configuration was added in [https://cwiki.apache.org/confluence/display/KAFKA/KIP-710%3A+Full+support+for+distributed+mode+in+dedicated+MirrorMaker+2.0+clusters] .
- **Daniel Urban:** Hi [~gharris1727], I don't have a deterministic reproduction of the issue. The reproduction of the problem requires multiple MM2 instances, but the internal REST is not needed at all (the startup and Connector config update does not touch the REST). Encountered this on a 3.4 build which contains t…
- **Greg Harris:** [~durban] I should clarify, I believe the behavior you described is the expected (but undesirable) behavior for versions before 3.5.0 and earlier, and for 3.5.0+ with the configuration set to the default `false`. When the internal REST API is enabled, the worker which is starting (that is not the l…
- **Daniel Urban:** [~gharris1727]  Not sure if I follow this part: "should forward configurations to the leader via the internal REST API." I checked org.apache.kafka.connect.mirror.MirrorMaker#configureConnector which then calls org.apache.kafka.connect.runtime.distributed.DistributedHerder#putConnectorConfig, and I…
- **Daniel Urban:** [~gharris1727] I have a bit more information: we managed to deterministically reproduce the issue if we use a 2 instance cluster, and make a change in the config, then wait a long time between the instance restarts. In our specific test we wait 3 minutes after stopping the first MM2 instance, then w…
- _…5 more comments_

## KAFKA-15373: AdminClient#describeTopics should not throw InvalidTopicException if topic ID is not found
Bug · Resolved (Fixed) · Major · created 2023-08-17 · resolved 2024-09-19

Similar to KAFKA-7808.
In {{KafkaAdminClient#handleDescribeTopicsByIds}}, when the topic is not found by ID, an {{InvalidTopicException}} is thrown.
[code/log omitted]
It would be better to use an {{UnknownTopicIdException}} in this case, which better aligns to the use of {{UnknownTopicOrPartitionException}} for the same scenario when describing topics by name.


## KAFKA-15374: ZK migration fails on configs for default broker resource
Bug · Resolved (Fixed) · Critical · created 2023-08-17 · resolved 2023-08-25

This error was seen while performing a ZK to KRaft migration on a cluster with configs for the default broker resource
[code/log omitted]
This is due to not considering the default resource type when we collect the broker IDs in ZkMigrationClient#migrateBrokerConfigs.


## KAFKA-15375: When running in KRaft mode, LogManager may creates CleanShutdown file by mistake 
Bug · Resolved (Fixed) · Major · created 2023-08-17 · resolved 2023-09-06

Consider following sequence when running Kafka in KRaft mode:
 # A partition log "log1" is created under "logDir1", and some records are appended to it.
 # Broker crashes. No clean shutdown file is created in "logDir1".
 # Broker is restarted. BrokerServer.startup is called.
 # On a different thread, LogManager.startup is called by BrokerMetadataPublisher.
 # Before LogManager.startup finishing recovering logs under "logDir1", fatal exception is thrown in BrokerServer.startup.
 # In except…

- **Satish Duggana:** Moving it to 3.7.0 as we are near code freeze and it is not a blocker.
- **José Armando García Sancio:** [~satish.duggana] this is major bug that should be included in 3.6.0. It looks like Colin cherry-picked it to the 3.6 branch. I will add the fix version back and resolve this issue.

## KAFKA-15376: Explore options of removing data earlier to the current leader's leader epoch lineage for topics enabled with tiered storage.
Task · Reopened · Major · components: core · created 2023-08-18

Followup on the discussion thread:
[https://github.com/apache/kafka/pull/13561#discussion_r1288778006]

- **hudeqi:** Can I take over this issue? [~satish.duggana]
- **Kamal Chandraprakash:** This task was already addressed in the code, so closing the ticket: https://sourcegraph.com/github.com/apache/kafka@3.6/-/blob/core/src/main/java/kafka/log/remote/RemoteLogManager.java?L1043-1061
- **Divij Vaidya:** Hey [~ckamal]  I think the motivation of this ticket to determine whether there are alternative options to remove leader epoch. As an example, in current implementation, if the non-current leader epoch chain becomes current, we will end up losing data in remote. With this ticket we wanted to explor…
- **Kamal Chandraprakash:** [~divijvaidya]  The [example|https://github.com/apache/kafka/pull/13561#discussion_r1293286722] provided in the discussion is misleading. Let's divide the example into two to navigate it easier: Assume that there are two replicas Broker A and Broker B for partition tp0: *Case-1* Both the replica…
- **Kamal Chandraprakash:** With unclean-leader-election enabled, there can be log-divergence, log-loss, and exactly-once-delivery is not applicable. We are trying to extend the same contract that is for local storage to remote when this feature is enabled. There are pros and cons to this feature: *Pros* 1. The replica will…
- _…3 more comments_

## KAFKA-15377: GET /connectors/{connector}/tasks-config endpoint exposes externalized secret values
Bug · Resolved (Fixed) · Major · components: connect · created 2023-08-18 · resolved 2023-08-24

The {{GET /connectors/\{connector}/tasks-config}} endpoint added in [https://cwiki.apache.org/confluence/display/KAFKA/KIP-661%3A+Expose+task+configurations+in+Connect+REST+API] exposes externalized secret values in task configurations (see [https://cwiki.apache.org/confluence/display/KAFKA/KIP-297%3A+Externalizing+Secrets+for+Connect+Configurations)]. A similar bug was fixed in https://issues.apache.org/jira/browse/KAFKA-5117 / [https://github.com/apache/kafka/pull/6129] for the {{GET /connecto…

- **Yash Mayya:** [~mimaison] [~ChrisEgerton] even though this will technically change the response for a public REST API, I'm not sure it requires a KIP since it should be classified as a bug. What do you folks think?
- **Chris Egerton:** I don't think a KIP is necessary, for the same reasons that a KIP wasn't required the first time this issue surfaced with the other endpoint.
- **Mickael Maison:** Yeah I don't think this needs a KIP. If I remember correctly, in another thread we noticed this endpoint is pretty much identical to GET /connectors/{connector}/tasks. If they really contain the same data maybe we could even remove it completely?
- **Yash Mayya:** Yeah, we'd discussed this previously here - [https://github.com/apache/kafka/pull/13424#discussion_r1144727886.] I'd be in favor of removing it completely; would we be able to do so with a single KIP (i.e. skipping deprecation followed by removal) targeting the next major release (4.0)?
- **Mickael Maison:** Considering it should be a simple KIP, we should have time to deprecate it first before removing it in 4.0.
- _…3 more comments_

## KAFKA-15378: Rolling upgrade system tests are failing
Task · Resolved (Fixed) · Major · components: streams, system tests · created 2023-08-18 · resolved 2023-10-20

The system tests are having failures for these tests:
[code/log omitted]
See [https://jenkins.confluent.io/job/system-test-kafka-branch-builder/5801/console] for logs and other test data.
Note that system tests currently only run with [this fix](https://github.com/apache/kafka/commit/24d1780061a645bb2fbeefd8b8f50123c28ca94e), I think some CVE python library update broke the system tests...

- **Chris Egerton:** [~lbrutschy] the [https://jenkins.confluent.io/job/system-test-kafka-branch-builder/5801/console] link is blocked for non-Confluent employees. Can you please add any relevant information directly to this ticket? Thanks!
- **Lucas Brutschy:** Thanks, [~ChrisEgerton] , I didn't realize that even the jenkins jobs for AK are not accessible. The direct output is  [code/log omitted] The detailed logs seem to be accessible though, here:  http://testing.confluent.io/confluent-kafka-branch-builder-system-test-results/?prefix=system-test-kafka…
- **Arpit Goyal:** [~lbrutschy]  As per description do you mean   the fix will work with this change ? install_requires=["ducktape<0.9", "requests==2.31.0"], I am trying to reproduce the issue locally , but I am getting this error  [code/log omitted] But it does not seem to matching the logs attached in the ticket…
- **Lucas Brutschy:** The requests python library downgrade was just required to get the tests running, but does not fix the actual test failure The bouncing upgrade test from 0.10 to 3.6 that seem to fail for you are probably yet another problem. Did you not get the test failures described in the ticket?
- **Arpit Goyal:** [~lbrutschy]  Not yet , I just tried to reproduce the issue but it is stuck at this error , Do you know the reason for this error ? Could not detect Kafka Streams version 3.6.0-SNAPSHOT on ducker@ducker12
- _…1 more comments_

## KAFKA-15379: Add option for Grace period Joins to disable changelog creation 
New Feature · Open · Minor · components: streams · labels: needs-kip · created 2023-08-18

Right now if you are preforming a buffered join with a grace period there is no way to avoid the creation of a changelog


## KAFKA-15380: Try complete actions after callback
Sub-task · Resolved (Fixed) · Blocker · created 2023-08-18 · resolved 2023-09-11

KIP-890 part 1 introduced the callback request type. It is used to execute a callback after KafkaApis.handle has returned. We did not account for tryCompleteActions at the end of handle when making this change.
In tests, we saw produce p99 increase dramatically (likely because we have to wait for another request before we can complete DelayedProduce). As a result, we should add the tryCompleteActions after the callback as well. In testing, this improved the produce performance.


## KAFKA-15381: Controller waiting for migration should only allow failover when transactions are supported
Bug · Resolved (Duplicate) · Major · created 2023-08-18 · resolved 2024-09-10

After a KRaft controller starts up in migration mode, it enters the "pre-migration" state. Unless transactions are supported, it is not safe for the controller to fail over in pre-migration mode. This is because a migration could have been partially committed when the failover occurs.

- **Satish Duggana:** Moving it to 3.7.0 as we are near code freeze and it is not a blocker.
- **Stanislav Kozlovski:** Changing target fix version to 3.8 since this is not a blocker and we are cutting a 3.7 RC
- **Josep Prat:** Changing target fix version to 3.9 since this is not a blocker and we are past code freeze
- **Colin McCabe:** We resolved this in KAFKA-17457 by not allowing migration to start with a MetadataVersion that doesn't support transactions.
- **Colin McCabe:** Removing fix version 3.9 for this duplicate JIRA since it is confusing release.py

## KAFKA-15473: Connect connector-plugins endpoint shows duplicate plugins
Bug · Resolved (Fixed) · Blocker · components: connect · created 2023-09-18 · resolved 2023-09-19

In <3.6.0-rc0, duplicates of a plugin would be shown if it subclassed multiple interfaces. For example:
[code/log omitted]
In 3.6.0-rc0, there are many more listings for the same plugin. For example:
[code/log omitted]
These duplicates appear to happen when a plugin with the same class name appears in multiple locations/classloaders.
When interpreting a connector configuration, only one of these plugins will be chosen, so only one is relevant to show to users. The REST API should only displ…

- **Greg Harris:** it appears that the bug which prompted the fix in KAFKA-15244 (wrong PluginType being inferred) also could cause duplicates. For example: [code/log omitted] Here, the second entry should have been "header_converter". So while there are more duplicates in 3.6.0-rc0 than there were in <3.6.0-rc0, th…
- **Greg Harris:** Plugins could also appear multiple times <3.6.0-rc0 if multiple versions were on the plugin path concurrently. The DelegatingClassLoader would prefer the one with the latest version, but all of the different versions would be visible in the REST API. It also treated the undefined version as distinc…
- **Greg Harris:** I've opened [https://github.com/apache/kafka/pull/14398] with strategy (3) from above. We can always implement (1) in the future and change the PluginInfo::equals implementation to show these duplicates, so we can hide them for now. I think (2) removes functionality from the API and would count as a…
- **Satish Duggana:** [~gharris1727] Is this API documented that it does not return duplicate entries? Can we also get an opinion from PMC/Committers and other KafkaConnect experts on whether this issue is a release blocker? If we agree that it is not a release blocker then we can have a release note clarifying this…
- **Sagar Rao:** [~satish.duggana], No the API documentation doesn't mention anything about the presence/absence of duplicate entries. This is what it says: [code/log omitted] I think the implicit assumption is that these would always return unique values but as Greg pointed out above, even pre-3.6 there could be…

## KAFKA-15474: AbstractCoordinator.testWakeupAfterSyncGroupReceivedExternalCompletion seems flaky
Test · Resolved (Fixed) · Minor · labels: flaky-test · created 2023-09-18 · resolved 2025-03-10

Ran into test failures when running the full AbstractCoordinatorTest unit test suit.
It is not very easy to reproduce, I seem to need to run the full unit module to "sometimes" reproduce it.
[code/log omitted]
testWakeupAfterSyncGroupReceived also appears flaky:
[code/log omitted]

- **Philip Nee:** [code/log omitted]

## KAFKA-15475: Request might retry forever even if the user API timeout expires
Bug · Resolved (Fixed) · Critical · components: clients, consumer · labels: consumer-threading-refactor, timeout · created 2023-09-18 · resolved 2024-02-20

If the request timeout in the background thread, it will be completed with TimeoutException, which is Retriable.  In the TopicMetadataRequestManager and possibly other managers, the request might continue to be retried forever.
There are two ways to fix this
 # Pass a timer to the manager to remove the inflight requests when it is expired.
 # Pass the future to the application layer and continue to retry.

- **Lianet Magrans:** Heads up, the TopicMetadataManager and CommitRequestManager already solved this, in a similar way. Still needed to be verified/fixed in other requests if applicable.
- **Kirk True:** [~lianetm] / [~pnee] —I need to refresh my memory about what it means for an exception to be retriable. Does it mean that the operation is automatically retried at some layer of the client, or does it simply mean that it's a transient failure that the caller _could_ retry, if desired?
- **Kirk True:** [~lianetm] would you kindly point me at the code in the two {{RequestManager}} implementations that have solved this?
- **Lianet Magrans:** Sure, TopicMetadataManager [here|https://github.com/apache/kafka/blob/fbbfafe1f556f424bf511697db6f399e5a622aa3/clients/src/main/java/org/apache/kafka/clients/consumer/internals/TopicMetadataRequestManager.java#L212] and CommitRequestManager [here|https://github.com/apache/kafka/blob/fbbfafe1f556f424…
- **Lianet Magrans:** Regarding your previous question about the retriable behaviour, short answer would be that yes, we do want to retry internally, but it depends on the request. Ex. TopicMetadata requests are retried internally by the manager whenever they fail on a Retriable error, also sync offset Commit and offsetF…

## KAFKA-15476: Improve checkstyle performance
Improvement · Resolved (Fixed) · Minor · created 2023-09-19 · resolved 2023-09-19

Checkstyle is not using cache during build due to absolute file paths. See details in description at [https://github.com/apache/kafka/pull/14344]

- **Divij Vaidya:** PR: https://github.com/apache/kafka/pull/14344

## KAFKA-15477: Kafka won't shutdown when deleting remote segments
Bug · Open · Minor · components: core · created 2023-09-19

When brokers are busy deleting a bunch of segments (following a topic removal using tiered storage), brokers won't respond to sigterm signal and cleanly shutdown. 
Intead, they keep removing remote segment until it's fully completed (which can take time for topics with long retention).

- **Francois Visconte:** cc [~satishd]
- **Divij Vaidya:** Ideally, deletion of remote segments (from Kafka perspective) is simply deleting the metadata from RLMM (which should be fast and not time consuming). But in 3.6 implementation, we synchronously delete the segments from remote storage, that is why you are facing this problem. The fix is scheduled fo…

## KAFKA-15478: Update connect to use ForwardingAdmin
New Feature · Open · Major · labels: need-kip · created 2023-09-19

Connect uses AdminClients to create topics; while this simplifies the implementation of Connect it has the following problems 
 * It assumes that whoever runs Connect must have admin access to both source and destination clusters. This assumption is not necessarily valid all the time.
 * It creates conflict in use-cases where centralised systems or tools manage Kafka resources. 
It would be easier if customers could provide how they want to manage Kafka topics through admin client or using th…


## KAFKA-15479: Remote log segments should be considered once for retention breach
Task · Resolved (Fixed) · Major · created 2023-09-19 · resolved 2023-09-25

When a remote log segment contains multiple epoch, then it gets considered for multiple times during breach by retention size/time/start-offset. This will affect the deletion by remote log retention size as it deletes the number of segments lesser than expected. This is a follow-up of KAFKA-15352

- **Henry Cai:** This is also related to https://issues.apache.org/jira/browse/KAFKA-15620, can the fix be back ported to Kafka 3.6 branch?

## KAFKA-15480: Add RemoteStorageInterruptedException
Task · Open · Major · components: core · labels: kip · created 2023-09-20

Introduce `RemoteStorageInterruptedException` to propagate interruptions from the plugin to Kafka without generated (false) errors. 
It allows the plugin to notify Kafka an API operation in progress was interrupted as a result of task cancellation, which can happen under changes such as leadership migration or topic deletion.

- **Stanislav Kozlovski:** Changing target fix version to 3.8 since this is not a blocker and we are cutting a 3.7 RC
- **Colin McCabe:** Moving to 4.0 since we're past feature freeze on 3.9.
- **David Jacot:** Removed the first version as this work is not planned in 4.0.

## KAFKA-15481: Concurrency bug in RemoteIndexCache leads to IOException
Bug · Resolved (Fixed) · Major · created 2023-09-20 · resolved 2023-11-16

RemoteIndexCache has a concurrency bug which leads to IOException while fetching data from remote tier.
Below events in order of timeline -
Thread 1 (cache thread): invalidates the entry, removalListener is invoked async, so the files have not been renamed to "deleted" suffix yet.
Thread 2: (fetch thread): tries to find entry in cache, doesn't find it because it has been removed by 1, fetches the entry from S3, writes it to existing file (using replace existing)
Thread 1: async removalListen…

- **Divij Vaidya:** FYI [~satishd] [~Kamal C] [~christo_lolov] [~showuon]
- **Luke Chen:** Nice find, [~divijvaidya]! So, the issue is because we time gap between entry invalidation and the file renaming (i.e. removalListener got invoked).  One thing to confirm, this is not a blocker for v3.6.0, right? I don't think it is since tiered storage is just a tech preview feature.
- **Divij Vaidya:** > the issue is because we time gap between entry invalidation and the file renaming Correct. >  this is not a blocker for v3.6.0, right?  Yes, I wouldn't consider this as a blocker since it's a race condition and shouldn't impact happy cases. I will add an entry to the early access document thoug…
- **Luke Chen:** About the solution to change to sync way, I have a question: Currently, we use readLock for both RemoteIndexCache#getIndexEntry and RemoteIndexCache#remove. That means, the original will still appear after using sync way: Thread 1 (cache thread): (readLock) invalidates the entry, removalListener i…
- **Luke Chen:** After re-reading the suggestion in Caffeine [doc|https://github.com/ben-manes/caffeine/wiki/Removal], the `evictionListener` only get invoked when "object eviction", not removal explicitly. We should use `internalCache.asMap().computeIfPresent()` instead, which I think will fix the issue I mentioned…
- _…13 more comments_

## KAFKA-15482: kafka.utils.TestUtils Depends on MockTime Which is Not in Any Jar
Bug · Closed (Invalid) · Major · created 2023-09-20 · resolved 2023-09-20

Commit 
7eea2a3908fdcee1627c18827e6dcb5ed0089fdd 
Moved it to server-commons, but it is not included in the jar.

- **Ismael Juma:** Can you please provide more details on how you arrived to the conclusion that the class is not in the jar? Note that it would be in the server-commons _test_ jar.
- **Gary Russell:** My apologies; I didn't see that jar in Maven Central. Please close.

## KAFKA-15483: Update metrics documentation for the new metrics implemented as part of KIP-938
Task · Resolved (Fixed) · Major · components: docs, documentation · created 2023-09-21 · resolved 2023-10-04

Update the kafka-site documentation for 3.6 release with the newly introduced metrics in 3.6 for KIP-938.

- **Satish Duggana:** [~cmccabe] [~mumrah] Please help in updating the kafka-site documentation for 3.6 release with the newly introduced metrics in 3.6 for KIP-938.
- **Satish Duggana:** [~mumrah] Assigning it to you as you raised [PR-548|https://github.com/apache/kafka-site/pull/548] to address this issue.
- **ASF GitHub Bot:** satishd commented on code in PR #548: URL: https://github.com/apache/kafka-site/pull/548#discussion_r1333360366 ########## 36/ops.html: ########## @@ -1980,6 +1980,28 @@ <h5 class="anchor-heading"><a id="kraft_quorum_monitoring" class="anchor-link"><      <td>The average fraction of time the client'…
- **ASF GitHub Bot:** satishd commented on PR #548: URL: https://github.com/apache/kafka-site/pull/548#issuecomment-1729990446    @mumrah  I do not see the documentation in the latest kafka-site docs for the below metrics that are part of KIP-866, correct me if I missed them in the existing docs.     ```    ZkWriteBehi…
- **ASF GitHub Bot:** mumrah commented on PR #548: URL: https://github.com/apache/kafka-site/pull/548#issuecomment-1730131962    Thanks for calling those out, @satishd. I've added them as well.
- _…1 more comments_

## KAFKA-15589: Flaky  kafka.server.FetchRequestTest
Task · Resolved (Duplicate) · Major · created 2023-10-11 · resolved 2023-10-11

I've been seeing a lot of test failures recently for  kafka.server.FetchRequestTest
Specifically: !image-2023-10-11-13-19-37-012.png!

- **Justine Olshan:** Duplicate of https://issues.apache.org/jira/browse/KAFKA-15566

## KAFKA-15590: Replica.updateFetchStateOrThrow should also fence updates with stale leader epoch
Bug · Open · Major · created 2023-10-11

This is a follow-up ticket for KAFKA-15221.
There is another type of race that a fetch request with stale leader epoch can update the fetch state.


## KAFKA-15591: Trogdor produce workload reports errors in KRaft mode
Bug · Resolved (Fixed) · Blocker · created 2023-10-12 · resolved 2026-09-09

The Kafka benchmark in the Dacapo Benchmark Suite uses the Trogdor's exec mode ([https://github.com/dacapobench/dacapobench/pull/224)]  to test the Kafka broker.
I am trying to update the benchmark to use the KRaft protocol. We use single Kafka instant that plays both controller and broker following the guide in Kafka README.md (https://github.com/apache/kafka#running-a-kafka-broker-in-kraft-mode).
However, the Trogdor producing workload  (tests/spec/simple_produce_bench.json) reports the NOT_…

- **Ron Dagostino:** > Is this caused by that in KRaft protocal, Kafka doesn't not elect leaders immediately after a new topic created but rather do that on-demand after receiving the first message on the topic?  No, that is not correct.  The leader for each partition is identified at the time the topic-partition is cr…
- **Xi Yang:** Thanks for your reply [~rndgstn].  >If the broker is responding that it does not know about that partition then it could be the case that it has not replicated and acted upon the records in the metadata log that created the partition and identified it as the leader. But in this case, there is only…
- **Xi Yang:** I print out the topic description after creating the topic. It looks like the partitions are correctly elected before Trogdor starts producing messages. However, the producer still reports the NOT_LEADER_OR_FOLLOWER error. Topic desc:(name=foo1, internal=false, partitions=(partition=0, leader=local…

## KAFKA-15592: Member does not need to always try to join a group when a groupId is configured
Sub-task · Closed (Duplicate) · Major · components: clients, consumer · labels: kip-848, kip-848-client-support, kip-848-e2e, kip-848-preview · created 2023-10-12 · resolved 2023-10-30

Currently, instantiating a membershipManager means the member will always seek to join a group unless it has failed fatally.  However, this is not always the case because the member should be able to join and leave a group any time during its life cycle. Maybe we should include an "inactive" state in the state machine indicating the member does not want to be in a rebalance group.


## KAFKA-15593: Add 3.6.0 to broker/client upgrade/compatibility tests
Sub-task · Resolved (Fixed) · Major · created 2023-10-12 · resolved 2023-12-08

- **Stanislav Kozlovski:** [~satish.duggana] is this good to close? seems weird to target 3.7 with 3.6 compatibility tests. AFAICT, the PRs are merged
- **Matthias J. Sax:** This ticket is to include upgrade test from 3.6 to 3.7/trunk – can only be done after 3.6 is released – it's WIP.
- **Mickael Maison:** The PR was merged, can we resolve this ticket now?

## KAFKA-15594: Add 3.6.0 to streams upgrade/compatibility tests
Sub-task · Resolved (Fixed) · Major · components: streams, system tests · created 2023-10-12 · resolved 2024-01-26

- **Stanislav Kozlovski:** [~satish.duggana] is anyone going to be assigned to this? Did we release 3.6 without it?
- **Matthias J. Sax:** This ticket is to include upgrade test from 3.6 to 3.7/trunk – can only be done after 3.6 is released – it's WIP.
- **Matthias J. Sax:** This ticket is to include upgrade test from 3.6 to 3.7/trunk – can only be done after 3.6 is released – it's WIP.

## KAFKA-15595: Session window aggregate drops records headers
Bug · Open · Major · components: streams · created 2023-10-12

Hey,
While upgrading to 3.5.1 from 3.2.X I noticed a change in SessionWindow aggregate behaviour, it seems now that custom headers added before the aggregate are dropped.
I could reproduce the behaviour with the following test topology:
[code/log omitted]
Checking evens in the `outputTopic` show that the headers are empty. With 3.2.* the same topology would have propagated the headers.
I can see here: [https://github.com/apache/kafka/blob/2c6fb6c54472e90ae17439e62540ef3cb0426fe3/streams/src…


## KAFKA-15596: Upgrade ZooKeeper to 3.8.3
Improvement · Resolved (Fixed) · Major · created 2023-10-12 · resolved 2023-10-12

ZooKeeper 3.8.3 fixes [CVE-2023-44981|https://www.cve.org/CVERecord?id=CVE-2023-44981] as described in https://lists.apache.org/thread/7o6cch0gm7hzz0zcj2zs16hnl1dxm6oy


## KAFKA-15597: Enable Connect DropHeaders SMT to drop headers on a wildcard/regexp-basis
Improvement · Open · Minor · components: connect · labels: connect-transformation · created 2023-10-12

In many use cases you might not only want to drop a few specific Kafka headers but a set of headers whose names can also dynamically change (e.g. when used with some end-to-end-encryption libraries, tracing etc.). To prevent those headers following a special pattern (which may not comply with downstream system format) to be further forwarded/processed downstream (e.g.header forwarding in Http Sinks), I suggest to add regexp matching to the *apply* method instead of a set-based {*}contains{*}. Li…

- **Roman Schmitz:** KIP created: [https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=272927649]

## KAFKA-15598: Add integration tests for DescribeGroups API, DeleteGroups API and OffsetDelete API
Sub-task · Resolved (Fixed) · Major · created 2023-10-12 · resolved 2023-11-02


## KAFKA-15599: Move classes in kafka.raft from core module to raft module
Sub-task · In Progress · Major · created 2023-10-12

Moving `UnifiedLog` and `LogManager` to the storage layer allows us to fix some compromises we had to do previously. The classes under `kafka.raft` in the `core` module can be moved to the `raft` module and the `raft` module will depend on the `storage` module.
This includes KafkaMetadataLog, KafkaNetworkChannel and RaftManager. As part of the move, we should do a few renames as well:
 # KafkaMetadataLog -> KafkaRaftLog
 # ReplicatedLog -> RaftLog

- **Ismael Juma:** Assigned this to you since you've been working on this.

## KAFKA-15766: Possible request handler thread exhaustion in controller election
Bug · Resolved (Abandoned) · Major · created 2023-10-31 · resolved 2026-04-28

Hello,
This is my first dive into the Kafka source code, so I may be mis-interpreting some of the logic outlined below. Please let me know if my understanding is not correct.
--- 
After upgrading a relatively large Kafka cluster from IPB 2.5 to 3.5 (Kafka version v3.5.0), we've had numerous problems with controller failover and subsequent elections not being properly acknowledged by a subset of the cluster's brokers.  These affected brokers will temporarily become unresponsive due to complete…

- **Cameron:** Closing this issue as it's a few years old now without much traction; I have since moved to a KRaft based Kafka cluster and this issue is no longer reproducible

## KAFKA-15767: Refactor TransactionManager to avoid use of ThreadLocal
Improvement · Resolved (Fixed) · Minor · components: clients, producer  · labels: transactions · created 2023-10-31 · resolved 2025-04-23

A {{TransactionManager}} instance is created by the {{KafkaProducer}} and shared with the {{Sender}} thread. The {{TransactionManager}} has internal states through which it transitions as part of its initialization, transaction management, shutdown, etc. It contains logic to ensure that those state transitions are valid, such that when an invalid transition is attempted, it is handled appropriately. 
The issue is, the definition of "handled appropriately" depends on which thread is making the A…

- **Stanislav Kozlovski:** Changing target fix version to 3.8 since this is not a blocker and we are cutting a 3.7 RC
- **David Jacot:** Removed the fix version as this is not planned for 4.0.

## KAFKA-15768: StateQueryResult#getOnlyPartitionResult should not throw for FailedQueryResult
Bug · Resolved (Fixed) · Major · components: streams · created 2023-10-31 · resolved 2026-05-05

Calling `StateQueryResult#getOnlyPartitionResult` crashes with an incorrect `IllegalArgumentException` if any result is a `FailedQueryResult` (and even if there is only a single FailedQueryResult).
The issue is the internal `filter(r -> r.getResult() != 0)` step, that blindly (and incorrectly) calls `getResult`.
Given the semantics of `getOnlyPartitionResult` we should not care if the result is SuccessQueryResult or FailedQueryResult, but only check if there is a single result or not. (The use…

- **John Roesler:** Hey [~hanyuzheng] , thanks for the bug report! I agree with you that if there is exactly one partition responding and it responds with a FailedQueryResult, then it could make sense to return it instead of throwing an exception. However, I do want to clarify that an expected usage of this method is…
- **Matthias J. Sax:** Thanks for the details [~vvcephei]! {quote}In other words, it should return the result if and only if all queried partitions responded successfully AND at most one partition returned a non-null result. {quote} This was the unclear piece to me, ie, what's the actual user contract. About exception…

## KAFKA-15769: Fix wrong log with exception
Improvement · Resolved (Fixed) · Minor · components: logging · created 2023-11-01 · resolved 2023-11-06

Like under case , log with exception is wrong.
!image-2023-11-01-13-08-43-833.png!


## KAFKA-15770: org.apache.kafka.streams.integration.ConsistencyVectorIntegrationTest.shouldHaveSamePositionBoundActiveAndStandBy is flaky 
Bug · Resolved (Fixed) · Major · components: streams, unit tests · labels: flaky-test · created 2023-11-01 · resolved 2024-02-20

Test fails on CI, passes locally
[https://ci-builds.apache.org/job/Kafka/job/kafka-pr/job/PR-14607/9/testReport/junit/org.apache.kafka.streams.integration/ConsistencyVectorIntegrationTest/Build___JDK_17_and_Scala_2_13___shouldHaveSamePositionBoundActiveAndStandBy/]
[code/log omitted]

- **Sagar Rao:** Noticed an instance here: https://ci-builds.apache.org/blue/organizations/jenkins/Kafka%2Fkafka-pr/detail/PR-14777/1/tests

## KAFKA-15771:  ProduceRequest#partitionSizes() is not an atomic operation
Bug · Resolved (Fixed) · Trivial · components: producer  · created 2023-11-01 · resolved 2023-11-07

Encountered a concurrency issue in method ProduceRequest#partitionSizes() while developing with Kafka. When both Thread 1 and Thread 2 concurrently call method ProduceRequest#partitionSizes(), Thread 2 may receive an incomplete or empty result if Thread 1 is still in the process of initializing partitionSizes. This is an incorrect state. the code to ensure that Thread 2 obtains the final state rather than an intermediate one.


## KAFKA-15772: Flaky test TransactionsWithTieredStoreTest
Test · Open · Minor · components: Tiered-Storage · labels: flaky-test · created 2023-11-02

Multiple tests in this Test class have been flaky. See: [https://ge.apache.org/scans/tests?search.rootProjectNames=kafka&search.startTimeMax=1698915424764&search.startTimeMin=1697320800000&search.tags=trunk&search.timeZoneId=Europe%2FBerlin&tests.container=org.apache.kafka.tiered.storage.integration.TransactionsWithTieredStoreTest] 
Example failure: [https://ci-builds.apache.org/job/Kafka/job/kafka-pr/job/PR-14667/9/testReport/junit/org.apache.kafka.tiered.storage.integration/TransactionsWithTi…

- **Justine Olshan:** I have seen this one be a bit flaky as well. https://ci-builds.apache.org/job/Kafka/job/kafka-pr/job/PR-14629/22/#showFailuresLink
- **Apoorv Mittal:** Another failure: https://ci-builds.apache.org/blue/organizations/jenkins/Kafka%2Fkafka-pr/detail/PR-14699/21/tests/ [code/log omitted]
- **Apoorv Mittal:** Failure of test: `testAbortTransactionTimeout` in `TransactionsWithTieredStoreTest` class https://ci-builds.apache.org/blue/organizations/jenkins/Kafka%2Fkafka-pr/detail/PR-15251/7/tests [code/log omitted]
- **Apoorv Mittal:** Flaky Test: org.apache.kafka.tiered.storage.integration.TransactionsWithTieredStoreTest."testFencingOnSend(String).quorum=kraft" [https://ci-builds.apache.org/job/Kafka/job/kafka-pr/job/PR-16890/3/testReport/org.apache.kafka.tiered.storage.integration/TransactionsWithTieredStoreTest/Build___JDK_21_…
- **Kamal Chandraprakash:** Both TransactionsTest and TransactionsWithTieredStoreTest are flaky. From my recent runs: ``` FAILED ❌ TransactionsWithTieredStoreTest > "testFencingOnSend(String).quorum=zk" FAILED ❌ TransactionsTest > "testSendOffsetsWithGroupId(String).quorum=zk" ```

## KAFKA-15773: Group protocol configuration should be validated
Improvement · Resolved (Fixed) · Minor · components: clients, config, consumer · labels: kip-848-client-support · created 2023-11-02 · resolved 2024-07-18

If the user specifies using the generic group, or not specifying the group.protocol config at all, we should invalidate all group.remote.assignor
If group.local.assignor and group.remote.assignor are both configured, we should also invalidate the configuration
This is an optimization/user experience improvement.

- **PoAn Yang:** Hi [~pnee], I'm interested in this issue. If you're not working on it, may I take it? Thank you.
- **PoAn Yang:** Hi [~pnee], I just created a draft PR [https://github.com/apache/kafka/pull/16543]. Feel free to close it, if you're working on it. Thank you.

## KAFKA-15774: Respect default.dsl.store Configuration Without Passing it to StreamsBuilder
Improvement · Resolved (Fixed) · Major · components: streams · created 2023-11-02 · resolved 2023-11-21

Currently if you only configure `default.dsl.store` as `in_memory` in your `StreamsConfig` it will silently be ignored unless it's also passed into `StreamsBuilder#new(TopologyConfig)`. We should improve this behavior to properly respect it.
This will become more important with the introduction of KIP-954.

- **Almog Gavra:** Note that we decided not to have default.dsl.store work if you only pass it in to the main KafkaStreams constructor for backwards compatibility. Instead you should use the new dsl.store.suppliers configuration

## KAFKA-15775: Implement listTopics() and partitionFor() for the AsyncKafkaConsumer
Sub-task · Resolved (Fixed) · Major · components: clients, consumer · labels: consumer-threading-refactor, kip-848, kip-848-client-support, kip-848-e2e, kip-848-preview · created 2023-11-02 · resolved 2023-12-19

[code/log omitted]

- **Kirk True:** [~schofielaj]—please update the status of this Jira since this is merged. Thanks!

## KAFKA-15776: Update delay timeout for DelayedRemoteFetch request
Task · Resolved (Fixed) · Major · labels: kip-1018 · created 2023-11-02 · resolved 2024-06-11

We are reusing the {{fetch.max.wait.ms}} config as a delay timeout for DelayedRemoteFetchPurgatory. {{fetch.max.wait.ms}} purpose is to wait for the given amount of time when there is no data available to serve the FETCH request.
[code/log omitted]
[https://github.com/apache/kafka/blob/trunk/core/src/main/scala/kafka/server/DelayedRemoteFetch.scala#L41]
Using the same timeout in the DelayedRemoteFetchPurgatory can confuse the user on how to configure optimal value for each purpose. Moreover,…

- **Francois Visconte:** [~ckamal] Any idea on how to move forward on that? I think having to configure a very high fetch.max.wait defeat the purpose of the KIP of not having to proceed adaptations on the consumer side. This issue is annoying on our test environment (using s3): even with a fetch.max.wait of 2s we get flood…
- **Kamal Chandraprakash:** [~fvisconte]  We are cancelling the currently executing fetch [task|https://sourcegraph.com/github.com/apache/kafka@92a67e8571500a53cc864ba6df4cb9cfdac6a763/-/blob/core/src/main/scala/kafka/server/DelayedRemoteFetch.scala?L86] when the timeout happens. When the remote storage degrades, then the con…
- **Kamal Chandraprakash:** > I think having to configure a very high fetch.max.wait defeat the purpose of the KIP of not having to proceed adaptations on the consumer side. Kindly elaborate on this.
- **Francois Visconte:** [~ckamal] What I mean is that one of the interesting property of tiered storage is not having to change anything on the consumer side because the consumer protocol is unchanged. In our case, we have to go over every consumers to adapt their settings, and even with that we have suboptimal consumer pe…
- **Jorge Esteban Quilcate Otoya:** Agree with [~fvisconte] that tweaking an existing config on the consumer side it's undesired given that Tiered Storage aims to be transparent to clients. An additional issue even when caching fetch requests is that remote fetch doesn't only fetch the log segment but potentially also the offset inde…
- _…5 more comments_

## KAFKA-15823: NodeToControllerChannelManager: authentication error prevents controller update
Bug · Resolved (Fixed) · Major · components: core · created 2023-11-14 · resolved 2024-04-01

NodeToControllerChannelManager caches the activeController address in an AtomicReference which is updated when:
 # activeController [has not been set|https://github.com/apache/kafka/blob/832627fc78484fdc7c8d6da8a2d20e7691dbf882/core/src/main/scala/kafka/server/NodeToControllerChannelManager.scala#L422]
 # networkClient [disconnnects from the controller|https://github.com/apache/kafka/blob/832627fc78484fdc7c8d6da8a2d20e7691dbf882/core/src/main/scala/kafka/server/NodeToControllerChannelManager.s…

- **Stanislav Kozlovski:** Changing target fix version to 3.8 since this is not a blocker and we are cutting a 3.7 RC

## KAFKA-15824: SubscriptionState's maybeValidatePositionForCurrentLeader should handle partition which isn't subscribed yet
Bug · Resolved (Fixed) · Major · components: clients · created 2023-11-14 · resolved 2023-11-15

As can be [maybeValidatePositionForCurrentLeader|https://github.com/msn-tldr/kafka/blob/2e2f32c05008cdd7009e5f76fdd92f98996aab84/clients/src/main/java/org/apache/kafka/clients/consumer/internals/SubscriptionState.java#L459] doesn't check if partition is subscribed. It can be done by checking TopicPartitionState cached is null or not, as done by [maybeCompleteValidation|https://github.com/msn-tldr/kafka/blob/2e2f32c05008cdd7009e5f76fdd92f98996aab84/clients/src/main/java/org/apache/kafka/clients/c…


## KAFKA-15825: KRaft controller writes empty state to ZK after migration
Bug · Resolved (Fixed) · Major · components: controller, kraft · created 2023-11-14 · resolved 2023-11-14

Immediately following the ZK migration, there is a race condition where the KRaftMigrationDriver can use an empty MetadataImage when performing the full "SYNC_KRAFT_TO_ZK" reconciliation. 
After the next controller failover, or when the controller loads a metadata snapshot, the correct state will be written to ZK. 
The symptom of this bug is that we see the migration complete, and then all the metadata removed from ZK. For example, 
[code/log omitted]
immediately followed by:
[code/log omit…

- **David Arthur:** This bug was fixed as part of KAFKA-15605

## KAFKA-15826: WorkerSinkTask leaks Consumer if plugin start or stop blocks indefinitely
Bug · Open · Minor · components: connect · created 2023-11-14

The WorkerSourceTask cancel() method closes the Producer, releasing it's resources. The WorkerSInkTask does not do the same for the Consumer, as it does not override the cancel() method.
WorkerSinkTask should close the consumer if the task is cancelled, as progress for a cancelled task will be discarded anyway.

- **Greg Harris:** The BlockingConnectorTest which was leaking the client in our tests was remediated with [https://github.com/apache/kafka/pull/12290] . The core flaw still exists, so I'm going to leave this ticket open.
- **Will Perlichek:** Hi [~gharris1727] do you know if this ticket is still relevant?  I was looking into flaky test failures in https://issues.apache.org/jira/browse/KAFKA-15891 (I have notes in the comments) and now I am wondering if this could be the root cause of the zombie sink tasks which cause the flaky tests, an…

## KAFKA-15827: KafkaBasedLog.withExistingClients leaks clients if start is not called
Bug · Resolved (Fixed) · Minor · components: connect · created 2023-11-14 · resolved 2024-01-19

The KafkaBasedLog base implementation creates consumers and producers, and closes them after they are instantiated. There are subclasses of the KafkaBasedLog which accept pre-created consumers and producers, and have the responsibility for closing the clients when the KafkaBasedLog is stopped.
It appears that the KafkaBasedLog subclasses do not close the clients when start() is skipped and stop() is called directly. This happens in a few tests, and causes the passed-in clients to be leaked.


## KAFKA-15828: Protect clients from broker hostname reuse
Bug · Resolved (Fixed) · Major · components: clients, consumer, producer  · labels: needs-kip · created 2023-11-14 · resolved 2026-07-06

In some environments such as k8s, brokers may be assigned to nodes dynamically from an available pool. When a cluster is rolling, it is possible for the client to see the same node advertised for different broker IDs in a short period of time. For example, kafka-1 might be initially assigned to node1. Before the client is able to establish a connection, it could be that kafka-3 is now on node1 instead. Currently there is no protection in the client or in the protocol for this scenario. If the co…


## KAFKA-15829: How to build Kafka 2.7 with maven instead of gradle?
Wish · Open · Minor · created 2023-11-15

It's difficult to upgrade the version of gradle in kafka building. Is there a solution to build kafka 2.7 with maven?


## KAFKA-15830: Add request/response handling in KafkaApis and update metrics plugin
Sub-task · Resolved (Fixed) · Major · created 2023-11-15 · resolved 2023-12-05

- **Jun Rao:** Merged the PR to trunk.

## KAFKA-15831: List Client Metrics Configuration Resources
Improvement · Resolved (Fixed) · Major · components: admin, clients · labels: kip · created 2023-11-15 · resolved 2023-12-05

This JIRA tracks the development of KIP-1000 (https://cwiki.apache.org/confluence/display/KAFKA/KIP-1000%3A+List+Client+Metrics+Configuration+Resources).

- **Jun Rao:** merged the PR to trunk.

## KAFKA-15832: Trigger client reconciliation based on manager poll
Sub-task · Resolved (Fixed) · Critical · components: clients, consumer · labels: kip-848-client-support, reconciliation · created 2023-11-15 · resolved 2024-02-13

Currently the reconciliation logic on the client is triggered when a new target assignment is received and resolved, or when new unresolved target assignments are discovered in metadata.
This could be improved by triggering the reconciliation logic on each poll iteration, to reconcile whatever is ready to be reconciled. This would require changes to support poll on the MembershipManager, and integrate it with the current polling logic in the background thread. Receiving a new target assignment…


## KAFKA-15833: Restrict Consumer API to be used from one thread
Sub-task · Resolved (Fixed) · Major · components: clients, consumer · labels: consumer-threading-refactor, kip-848-client-support, kip-848-preview · created 2023-11-15 · resolved 2023-11-20

The legacy consumer restricts the API to be used from one thread only. This is not enforced in the new consumer. To avoid inconsistencies in the behavior, we should enforce the same restriction in the new consumer.


## KAFKA-16015: kafka-leader-election timeout values always overwritten by default values 
Bug · Resolved (Fixed) · Minor · components: admin, tools · created 2023-12-15 · resolved 2023-12-29

Using the *kafka-leader-election.sh* I was getting random timeouts like these:
[code/log omitted]
These timeouts were raised from the client side as the controller always finished with all the Kafka leader elections.
One pattern I detected was always the timeouts were raised after about 15 seconds.
So i checked this command has an option to pass configurations
[code/log omitted]
I created the file in order to increment the values of *request.timeout.ms*  and *default.api.timeout.ms.* So ev…

- **Sergio Troiano:** hi [~pprovenzano] , I will open a PR in the 3.6 branch and also in the trunk one as I see the bug is in place, one detail I see is in the trunk the *LeaderElectionCommand.scala* was rewritten in [java here|https://github.com/apache/kafka/blob/trunk/tools/src/main/java/org/apache/kafka/tools/LeaderEl…
- **Proven Provenzano:** Hi [~sergio_troiano@hotmail.com]  I would suggest opening a PR for trunk first so that it can then be cherry-picked to 3.7 branch before code freeze. The 3.6 and 3.5 point releases have already shipped and this isn't a security issue that needs to be immediately addressed so we have more time to g…
- **Sergio Troiano:** Thanks as usual [~pprovenzano]  :) I will open then only the PR for trunk , I will update the ticket when the PR is ready
- **Sergio Troiano:** Pr open, [https://github.com/apache/kafka/pull/15030] Thanks!

## KAFKA-16016: Migrate utility scripts to kafka codebase
Sub-task · Resolved (Fixed) · Blocker · components: core · created 2023-12-15 · resolved 2024-01-08

Migrate the logic implemented in golang to kafka codebase by creating a new entrypoint for docker images

- **Stanislav Kozlovski:** We are discussing in the mailing list thread for [DISCUSS] KIP-975 Docker Image for Apache Kafka about whether this should be considered a blocker for 3.7. I am leaning toward no
- **Stanislav Kozlovski:** Changing the Fix Version here to unblock RC creation for 3.7

## KAFKA-16017: Checkpointed offset is incorrect when task is revived and restoring 
Bug · Resolved (Fixed) · Major · components: streams · created 2023-12-15 · resolved 2023-12-21

Streams checkpoints the wrong offset when a task is revived after a {{TaskCorruptedException}} and the task is then migrated to another stream thread during restoration.
This might happen in a situation like the following if the Streams application runs under EOS:
1. Streams encounters a Network error which triggers a {{TaskCorruptedException}}
2. The task that encountered the exception is closed dirty and revived. The state store directory is wiped out and a rebalance is triggered.
3. Until…


## KAFKA-16018: KafkaStreams can go into a zombie state if UncaughtExceptionHandler is specified via the deprecated method
Bug · Resolved (Won't Do) · Major · components: streams · created 2023-12-15 · resolved 2024-12-09

We have a streams application in which all StreamThreads died due to a lack of disk space. To our surprise, the KafkaStreams instance still reported its state as running. Upon further investigation, it appears this is due to the application setting an UncaughtExceptionHandler via the deprecated method (this application was recently upgraded from 2.4.1): [https://kafka.apache.org/33/javadoc/org/apache/kafka/streams/KafkaStreams.html#setUncaughtExceptionHandler(java.lang.Thread.UncaughtExceptionHa…

- **Matthias J. Sax:** Seems this will "auto fix" in 4.0 when we remove the deprecated API?
- **Tommy Becker:** I think that's true, but wasn't sure on the timing of 4.0.
- **Matthias J. Sax:** Timing is a little unclear to be fair – there is an open discussion if the next release (ie, after 3.7 that we are currently rolling out) will be 3.8 or 4.0... But even if it's 3.8, it's an open question if it's worth to put a fix into 3.8 or just wait for 4.0 (not sure how complex a fix would be...…
- **Matthias J. Sax:** Kafka 4.0 is around the corner. Closing this.

## KAFKA-16019: Some of the tests in PlaintextConsumer can't seem to deterministically invoke and verify the consumer callback
Test · Resolved (Fixed) · Critical · components: clients, consumer · labels: consumer-threading-refactor, integration-tests, timeout · created 2023-12-15 · resolved 2024-02-20

I was running the PlaintextConsumer to test the async consumer; however, a few tests were failing with not being able to verify the listener is invoked correctly
For example `testPerPartitionLeadMetricsCleanUpWithSubscribe`
Around 50% of the time, the listener's callsToAssigned was never incremented correctly.  Event changing it to awaitUntilTrue it was still the same case
[code/log omitted]

- **Kirk True:** {{testPerPartitionLeadMetricsCleanUpWithSubscribe}} is now passing consistently, so marking this as fixed.

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


## KAFKA-16022: AsyncKafkaConsumer sometimes complains “No current assignment for partition {}”
Bug · Closed (Done) · Minor · components: clients, consumer · labels: consumer-threading-refactor, kip-848-client-support · created 2023-12-16 · resolved 2024-08-15

This seems to be a timing issue that before the member receives any assignment from the coordinator, the fetcher will try to find the current position causing "No current assignment for partition {}".  This creates a small amount of noise to the log.

- **Phuc Hong Tran:** [~pnee], were you seeing this exception in the FetchRequestManagerTest or was it some places else?
- **Kirk True:** [~pnee]—can you follow up on [~phuctran]'s question. Thanks!
- **Philip Nee:** hi [~phuctran] - I believe this came up during integration testing.  You can try to see if the fetch request manager test also emits this error.
- **Lianet Magrans:** Hey [~phuctran] , there are already 2 tasks for solving known issues leading to this error: KAFKA-17066 and KAFKA-17064. Those bugs could definitely lead to this.
- **Lianet Magrans:** I've linked all the jiras that we were causing this error. I think we can close this one since it's only an observation of the error and we've identified the specific issues. We can reopen in the future if needed.
- _…2 more comments_

## KAFKA-16023: PlaintextConsumerTest needs to wait for reconciliation to complete before proceeding
Test · Resolved (Fixed) · Critical · components: clients, consumer · labels: consumer-threading-refactor, integration-tests, timeout · created 2023-12-16 · resolved 2024-02-20

Several tests in PlaintextConsumerTest.scala (such as testPerPartitionLagMetricsCleanUpWithSubscribe) uses:
assertEquals(1, listener.callsToAssigned, "should be assigned once")
However, as the timing for reconciliation completion is not deterministic due to asynchronous processing. We actually need to wait until the condition to happen.
However, another issue is the timeout - some of these tasks might not complete within the 600ms timeout, so the tests are deemed to be flaky.

- **Kirk True:** {{testPerPartitionLagMetricsCleanUpWithSubscribe}} is now passing consistently, so marking this as fixed.

## KAFKA-16024: SaslPlaintextConsumerTest#testCoordinatorFailover is flaky
Test · Resolved (Fixed) · Major · components: clients, consumer · labels: flaky-test, integration-tests · created 2023-12-17 · resolved 2025-10-29

The test is flaky with the async consumer as we are observing
[code/log omitted]
I was not able to replicate this on my local machine easily.

- **Colin McCabe:** Changing target fix version to 4.0 since this is not a blocker and we are past code freeze
- **David Jacot:** Changing target fix version to 4.1 since this is not a blocker and we are past code freeze.
- **Mickael Maison:** Moving to the next release as we're now in code freeze for 4.1.0.
- **Kirk True:** Per KAFKA-7605, this test has been flaky since 2018, so it's not specific to the "new" consumer. Per [Develocity|https://develocity.apache.org/scans/tests?search.relativeStartTime=P90D&search.rootProjectNames=kafka&search.timeZoneId=America%2FLos_Angeles&tests.container=kafka.api.SaslSslConsumerTes…

## KAFKA-16025: Streams StateDirectory has orphaned locks after rebalancing, blocking future rebalancing
Bug · Resolved (Fixed) · Major · components: streams · created 2023-12-18 · resolved 2024-01-08

Hello,
We are encountering an issue where during rebalancing, we see streams threads on one client get stuck in rebalancing. Upon enabling debug logs, we saw that some tasks were having issues initializing due to failure to grab a lock in the StateDirectory:
{{2023-12-14 22:51:57.352000Z stream-thread [i-0f1a5e7a42158e04b-StreamThread-14] Could not initialize task 0_51 since: stream-thread [i-0f1a5e7a42158e04b-StreamThread-14] standby-task [0_51] Failed to lock the state directory for task 0_5…

- **Sabit:** Submitted PR: https://github.com/apache/kafka/pull/15088
- **A. Sophie Blee-Goldman:** Nice find and writeup of the race condition – I'll take a look at the fix
- **A. Sophie Blee-Goldman:** FYI [~sabitn] I added you as a Jira contributor so you should now be able to self-assign any tickets you are working on. Thanks again for the fix!

## KAFKA-16105: Reassignment of tiered topics is failing due to RemoteStorageException
Bug · Resolved (Fixed) · Critical · components: Tiered-Storage · labels: tiered-storage · created 2024-01-09 · resolved 2024-06-03

When partition reassignment is happening for a tiered topic in most of the cases it's stuck with RemoteStorageException's on follower nodes saying that it can not construct remote log auxilary state:
[code/log omitted]
Scenario:
A cluster of 3 nodes with a single topic with 30 partitions. All partitions have tiered segments.
Adding 3 more nodes to the cluster and making a reassignment to move all the data to new nodes.
Behavior:
For most of the partitions reassignment is happening smoothly…

- **Anatolii Popov:** FYI [~satishd] [~abhijeetkumar]
- **Kamal Chandraprakash:** [~anatolypopov]  Could you write an integration test to simulate the error scenario? You can refer to some of the existing [tests|https://sourcegraph.com/github.com/apache/kafka@trunk/-/blob/storage/src/test/java/org/apache/kafka/tiered/storage/integration/BaseReassignReplicaTest.java]. Thanks!
- **Anatolii Popov:** Hi [~ckamal] unfortunately it is really hard to write an integration test for this since the actual issue is a race condition.  Instead, I updated a PR with a proper fix with a more detailed explanation of what is happening and why. Hope this helps. Please take a look when you have time.

## KAFKA-16106: group size counters do not reflect the actual sizes when operations fail
Sub-task · Resolved (Fixed) · Major · created 2024-01-09 · resolved 2024-10-04

An expire-group-metadata operation generates tombstone records, updates the `groups` state and decrements group size counters, then performs a write to the log. If there is a __consumer_offsets partition reassignment, this operation fails. The `groups` state is reverted to an earlier snapshot but classic group size counters are not. This begins an inconsistency between the metrics and the actual groups size. This applies to all unsuccessful write operations that alter the `groups` state.
The is…


## KAFKA-16107: Ensure consumer does not start fetching from added partitions until onPartitionsAssigned completes
Sub-task · Resolved (Fixed) · Critical · components: clients, consumer · labels: kip-848-client-support, reconciliation · created 2024-01-10 · resolved 2024-01-24

In the new consumer implementation, when new partitions are assigned, the subscription state is updated and then the #onPartitionsAssigned triggered. This sequence seems sensible but we need to ensure that no data is fetched until the onPartitionsAssigned completes (where the user could be setting the committed offsets it want to start fetching from).
We should pause the partitions newly added partitions until onPartitionsAssigned completes, similar to how it's done on revocation to avoid posit…


## KAFKA-16108: Backport fix for KAFKA-16093 to 3.7
Improvement · Resolved (Done) · Blocker · components: connect · created 2024-01-10 · resolved 2024-05-08

A fix for KAFKA-16093 is present on the branches trunk (the version for which is currently 3.8.0-SNAPSHOT) and 3.6. We are in code freeze for the 3.7.0 release, and this issue is not a blocker, so it cannot be backported right now.
We should backport the fix once 3.7.0 has been released and before 3.7.1 is released.

- **Igor Soarez:** [~ChrisEgerton] is this still relevant? The priority field is set to blocker but the description says it's not a blocker, what's the correct priority?
- **Chris Egerton:** I set it to blocker as a reminder to backport before 3.7.1, which we should still do (I'll get on it later today). It was not a blocker for the 3.7.0 release because that one was already in code freeze.
- **Igor Soarez:** I see you've backported this into the 3.7 branch. Thanks [~ChrisEgerton] !

## KAFKA-16109: Write system tests cover the "simple consumer + commit" use case
Test · Open · Minor · components: clients, consumer, system tests · labels: consumer-threading-refactor, system-tests · created 2024-01-10

- **PoAn Yang:** Hi [~kirktrue], if you're not working on this, may I take it? Thank you.
- **Kirk True:** [~yangpoan]—it's all yours :)
- **Lianet Magrans:** [~kirktrue] do you think this should be Major for 4.0 given that we do have coverage for this path at the integration test level, ex. PlaintextConsumerCommitTest#testCommitMetadata)?
- **Kirk True:** I think we can push it to post-4.0 and/or lower the priority. Thanks!

## KAFKA-16110: Document and publicize performance test results for AsyncKafkaConsumer
Task · Open · Major · components: clients, consumer · labels: consumer-threading-refactor, performance-benchmark · created 2024-01-10

- **Philip Nee:** Hi [~kirktrue] - Thanks for filing this JIRA.  There are two paths forward for the performance testing.  One is using trogdor - which does more than performance testing but also allow us to test different fault scenarios.  Second is implementing our own benchmarking test, I started working on it som…
- **Philip Nee:** My proposal here is - Let's run trogdor to see what can we get out of it. If the current settings is not satisfied then we can add more "specs" to the repo and see if we can get to the point we want. - We also might want to monitor the performance of the head of trunk as we are putting code in.  I…
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

## KAFKA-16112: Review JMX metrics in Async Consumer and determine the missing ones
Task · Resolved (Fixed) · Critical · components: clients, consumer, metrics · labels: consumer-threading-refactor, metrics · created 2024-01-10 · resolved 2024-01-12

- **Philip Nee:** These are the results of this ticket |KAFKA-16113| |KAFKA-16116| |KAFKA-16115|

## KAFKA-16113: AsyncKafkaConsumer: Add missing offset commit metrics
Improvement · Resolved (Fixed) · Critical · components: clients, consumer, metrics · labels: consumer-threading-refactor, metrics · created 2024-01-11 · resolved 2024-01-19

The following metrics are missing from the AsyncKafkaConsumer:
commit-latency-avg
commit-latency-max
commit-rate
commit-total
committed-time-ns-total


## KAFKA-16114: Fix partiton not retention after cancel alter intra broker log dir task 
Bug · Open · Major · components: log · created 2024-01-11

The deletion thread will not work on partition after cancel alter intra broker log dir task 
The steps to reproduce are as follows:
1、Create reassignment.json file
test01-1 on the /data01/kafka/log01 directory of the broker 1003，then move to /data01/kafka/log02 
[code/log omitted]
2、Kick off the reassignment
[code/log omitted]
3、Cancel the reassignment
[code/log omitted]
4、Result, The partition test01-1 on 1003 will not be deleted 
The reason for this problem is the partition has been…

- **wangliucheng:** Hello, are you interested in seeing this issue? I think it's a serious bug. [~dengziming] [~divijvaidya] [~junrao]
- **Divij Vaidya:** Sorry [~albedooooooo] , I won't have bandwidth any time soon to look into this.
- **wangliucheng:** Okay, please take a look later [~divijvaidya]

## KAFKA-16115: AsyncKafkaConsumer: Add missing heartbeat metrics
Improvement · Resolved (Fixed) · Critical · components: clients, consumer, metrics · labels: consumer-threading-refactor, metrics · created 2024-01-11 · resolved 2024-02-02

The following metrics are missing:
|[heartbeat-rate|https://docs.confluent.io/platform/current/kafka/monitoring.html#heartbeat-rate]|
|[heartbeat-response-time-max|https://docs.confluent.io/platform/current/kafka/monitoring.html#heartbeat-response-time-max]|
|[heartbeat-total|https://docs.confluent.io/platform/current/kafka/monitoring.html#heartbeat-total]|
|[last-heartbeat-seconds-ago|https://docs.confluent.io/platform/current/kafka/monitoring.html#last-heartbeat-seconds-ago]|
|[last-rebal…


## KAFKA-16173: Flaky test: testTimeoutMetrics – org.apache.kafka.controller.QuorumControllerMetricsIntegrationTest
Bug · Open · Major · created 2024-01-19

[https://ci-builds.apache.org/blue/organizations/jenkins/Kafka%2Fkafka-pr/detail/PR-15190/3/tests/]
[code/log omitted]


## KAFKA-16174: Flaky test: testDescribeQuorumStatusSuccessful – org.apache.kafka.tools.MetadataQuorumCommandTest
Test · Open · Major · labels: flaky-test · created 2024-01-19

[https://ci-builds.apache.org/blue/organizations/jenkins/Kafka%2Fkafka-pr/detail/PR-15190/3/tests/]
[code/log omitted]

- **Johnny Hsu:** [~apoorvmittal10] may I know if you are working on this ticket? if not I am willing to help :)
- **Johnny Hsu:** the exception is from [https://github.com/apache/kafka/blob/9b8aac22ec7ce927a2ceb2bfe7afd57419ee946c/core/src/main/scala/kafka/server/BrokerServer.scala#L474] when the cluster starts, [https://github.com/apache/kafka/blob/9b8aac22ec7ce927a2ceb2bfe7afd57419ee946c/core/src/test/java/kafka/testkit/Kaf…
- **Jun Rao:** Also saw the following test failure in https://github.com/apache/kafka/actions/runs/16300736076/job/46035062600?pr=20137 [code/log omitted]

## KAFKA-16175: Flaky test: testAsynchronousAuthorizerAclUpdatesDontBlockRequestThreads – kafka.api.SslAdminIntegrationTest
Bug · Open · Major · created 2024-01-19

[https://ci-builds.apache.org/blue/organizations/jenkins/Kafka%2Fkafka-pr/detail/PR-15190/3/tests/]
[code/log omitted]


## KAFKA-16176: Flaky test: testSendToPartitionWithFollowerShutdownShouldNotTimeout – kafka.api.PlaintextProducerSendTest
Bug · Resolved (Fixed) · Major · components: clients, consumer, producer  · labels: integration-test, kip-848-client-support · created 2024-01-19 · resolved 2024-11-19

[https://ci-builds.apache.org/blue/organizations/jenkins/Kafka%2Fkafka-pr/detail/PR-15190/3/tests/]
[code/log omitted]

- **Kirk True:** [~apoorvmittal10]—I am getting this error when testing using the Consumer running with the {{CONSUMER}} group protocol. Do you know if that's the way your test was configured? When I run the test using the {{CLASSIC}} group protocol, I can run it 25 times in a row without an error. When I run it wi…
- **Kirk True:** Closing this as fixed as it is not currently flaky. KAFKA-18040 is opened to address a related issue of the new {{CONSUMER}} group protocol failing.

## KAFKA-16177: Flaky test: testBatchSizeZeroNoPartitionNoRecordKey – kafka.api.PlaintextProducerSendTest
Bug · Open · Major · components: clients, producer  · created 2024-01-19

[https://ci-builds.apache.org/blue/organizations/jenkins/Kafka%2Fkafka-pr/detail/PR-15190/3/tests/]
[code/log omitted]


## KAFKA-16178: AsyncKafkaConsumer doesn't retry joining the group after rediscovering group coordinator
Bug · Resolved (Fixed) · Blocker · components: clients, consumer · labels: client-transitions-issues, consumer-threading-refactor · created 2024-01-19 · resolved 2024-02-12

[code/log omitted]
Some of the consumers don't consume any message. The logs show that after the consumer starts up and successfully logs in,
 # The consumer discovers the group coordinator.
 # The heartbeat to join group fails because "This is not the correct coordinator"
 # The consumer rediscover the group coordinator.
Another heartbeat should follow the rediscovery of the group coordinator, but there's no logs showing sign of a heartbeat request. 
On the server side, there is completel…

- **Philip Nee:** Seems to be an issue with the RequestState - I wonder if we've forgotten to update the lastReceivedMs when receiving these errors.
- **Lianet Magrans:** You're right [~pnee]! I found out while working on KAFKA-16215 (different issue related to rejoin after fencing, but same underlying bug). Patch submitted, will update it here too

## KAFKA-16179: NPE handle ApiVersions during controller failover
Bug · Open · Major · created 2024-01-19

[code/log omitted]

- **Ismael Juma:** Is this a 3.7.0 blocker or only in trunk?
- **Jason Gustafson:** It is probably not a blocker. It looks like it is a race condition on controller shutdown. The impact is probably a failed connection on a shutting down controller.

## KAFKA-16180: Full metadata request sometimes fails during zk migration
Bug · Resolved (Fixed) · Blocker · created 2024-01-20 · resolved 2024-03-14

Example:
[code/log omitted]


## KAFKA-16181: Use incrementalAlterConfigs when updating broker configs by kafka-configs.sh
Improvement · Resolved (Resolved) · Major · created 2024-01-22 · resolved 2024-12-02


## KAFKA-16182: Flaky test - testClientInstanceId() - org.apache.kafka.clients.admin.KafkaAdminClientTest
Bug · Open · Major · components: admin, clients · labels: flaky-test · created 2024-01-22

h3. Error
org.apache.kafka.common.KafkaException: Error occurred while fetching client instance id
Stacktrace
org.apache.kafka.common.KafkaException: Error occurred while fetching client instance id
at app//org.apache.kafka.clients.admin.KafkaAdminClient.clientInstanceId(KafkaAdminClient.java:4477)
at app//org.apache.kafka.clients.admin.KafkaAdminClientTest.testClientInstanceId(KafkaAdminClientTest.java:7082)
at java.base@17.0.7/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native…


## KAFKA-16183: Flaky test - testMetricsDuringTopicCreateDelete(String).quorum=zk – kafka.integration.MetricsDuringTopicCreationDeletionTest
Bug · Resolved (Won't Fix) · Major · labels: flaky-test · created 2024-01-22 · resolved 2024-12-14

[https://ci-builds.apache.org/blue/organizations/jenkins/Kafka%2Fkafka-pr/detail/PR-15214/1/pipeline]
h4. Error
java.lang.AssertionError: assertion failed: Expect UnderReplicatedPartitionCount to be 0, but got: 1
h4. Stacktrace
java.lang.AssertionError: assertion failed: Expect UnderReplicatedPartitionCount to be 0, but got: 1
 at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
 at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAcc…

- **Will Perlichek:** Hi, [~schofielaj]  According to my crude Develocity query (link below), testMetricsDuringTopicCreateDelete has continued to be very flaky, as recently at this week I have two preliminary (newbie) questions before I consider picking this up: 1) Should we mark this with a flaky annotation? How to k…
- **Will Perlichek:** Update: I think this Jira status can be marked as "won't fix" after Kirk True's PR here [https://github.com/apache/kafka/pull/17670/files] which removed the zk param this test.

## KAFKA-16339: Remove Deprecated "transformer" methods and classes
Sub-task · Resolved (Fixed) · Blocker · components: streams · created 2024-03-04 · resolved 2024-12-09

Cf [https://cwiki.apache.org/confluence/display/KAFKA/KIP-820%3A+Extend+KStream+process+with+new+Processor+API]
 * KStream#tranform
 * KStream#flatTransform
 * KStream#transformValue
 * KStream#flatTransformValues
 * and the corresponding Scala methods
Related to https://issues.apache.org/jira/browse/KAFKA-12829, and both tickets should be worked on together.

- **Matthias J. Sax:** [~vrushankpatel] – when do you plan to open a PR for this ticket? (Might make sense to do multiple smaller PRs).
- **João Pedro Fonseca:** Hi, [~mjsax], [~vrushankpatel]! If possible, I would like to help with this task :)
- **Matthias J. Sax:** Seems [~vrushankpatel] did not reply to my last comment. Let's re-assign to you. This might be a larger body of work. Please break it out into multiple smaller PRs, maybe one per method? This simplifies reviewing, and speeds up merging.
- **João Pedro Fonseca:** Alright, I will do this! Thank you, Matthias!
- **João Pedro Fonseca:** [~mjsax], should I base the PRs on the last one of each or the trunk? Thanks!
- _…2 more comments_

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


## KAFKA-16344: Internal topic mm2-offset-syncs<clustername>internal created with single partition is putting more load on the broker
Bug · Open · Major · components: connect · created 2024-03-05

We are using Kafka 3.5.1 version, we see that the internal topic created by mirrormaker 
mm2-offset-syncs<clustername>internal is created with single partition due to which the CPU load on the broker which will be leader for this partition is increased compared to other brokers. Can multiple partitions be  created for the topic so that the CPU load would get distributed 
Topic: mm2-offset-syncscluster-ainternal    TopicId: XRvTDbogT8ytNhqX2YTyrA    PartitionCount: 1ReplicationFactor: 3    Conf…

- **Greg Harris:** Hi [~janardhanag], thanks for the ticket. At the current time, the offset syncs topic cannot have more than 1 partition. If more than one partition is present, the MirrorSourceTask will only write to partition 0, and the MirrorCheckpointTask will only read from partition 0. Changes to both of these…
- **Janardhana Gopalachar:** HI [~gharris1727]  while processing 24k events/second, MM2 internal topic gets 10k events/sec. is the event load the internal topic is getting. Is there any parameters that can be tuned so that CPU load on the broker instance for the internal topic leader can be distributed  Regards Jana
- **Janardhana Gopalachar:** HI [~gharris1727]  Currently in our mirror maker spec  we have offset.lag.max: 0, so should it be set to max 100, Will this reduce the through put on source topics or target topic,  Is the offset.lag.max value set to 0 is contributing for CPU load ? what would be value that could be set if it to…
- **Greg Harris:** Hi [~janardhanag] Yes, you should consider increasing offset.lag.max. 0 is best for precise offset translation, but can significantly increase the amount of traffic on the offset-syncs topic. For topics without offset gaps (e.g. not compacted, not transactional) the offset.lag.max currently behaves…
- **Janardhana Gopalachar:** Hi [~gharris1727]  We tried to perform test in out local setup , we observed for the scenario If messages were written in the Source Kafka  Cluster and the target Kafka cluster is created after a delay , then the no of messages written to mm2-offsetsyncsinternal  is doubled. Is this the expected b…
- _…1 more comments_

## KAFKA-16345: Optionally allow urlencoding clientId and clientSecret in authorization header
Bug · Resolved (Fixed) · Minor · labels: kip · created 2024-03-05 · resolved 2024-07-09

When a client communicates with OIDC provider to retrieve an access token RFC-6749 says that clientID and clientSecret must be urlencoded in the authorization header. (see [https://tools.ietf.org/html/rfc6749#section-2.3.1)] However, it seems that in practice some OIDC providers do not enforce this, so I was thinking about introducing a new configuration parameter that will optionally urlencode clientId & clientSecret in the authorization header. 
Link to the KIP https://cwiki.apache.org/conflu…

- **Kirk True:** [~bachmanity1]—changed the status to reflect that fact that you've already submitted a patch for review. Thanks again for catching this!

## KAFKA-16346: Fix flaky MetricsTest.testMetrics
Bug · Resolved (Fixed) · Minor · created 2024-03-06 · resolved 2024-07-31

[code/log omitted]
The value used to update metrics is calculated by Math.round, so it could be zero if you have a good machine :)
We should verify the `count`  instead of `value`, since it is convincible and more stable.

- **Chia-Ping Tsai:** The count is increased even though the value is zero, so using the count is meaningless currently. Maybe we should update `messageConversionsTimeHist` only if the conversion does happen.
- **PoAn Yang:** Hi [~chia7712], may we change the status to resolved, because related PR is merged? Thanks.

## KAFKA-16347: Bump ZooKeeper to 3.8.4
Bug · Resolved (Fixed) · Major · created 2024-03-06 · resolved 2024-03-06

ZooKeeper 3.8.4 was released and contains a few CVE fixes: https://zookeeper.apache.org/doc/r3.8.4/releasenotes.html
We should update 3.6, 3.7 and trunk to use this new ZooKeeper release.

- **Luke Chen:** There's PR already opened for trunk: https://github.com/apache/kafka/pull/15480
- **Chia-Ping Tsai:** [~kevinztw] FYI
- **Chia-Ping Tsai:** [~kevinztw] I have ship it into trunk. Please file PR to backport it to branch-3.6 and branch-3.7. thanks!
- **Mickael Maison:** Considering it's a small change you should be able to directly cherry-pick it on 3.7. and 3.6.
- **Chia-Ping Tsai:** {quote} Considering it's a small change you should be able to directly cherry-pick it on 3.7. and 3.6. {quote} will copy that
- _…2 more comments_

## KAFKA-16348: Fix flaky TopicCommandIntegrationTest.testDescribeUnderReplicatedPartitionsWhenReassignmentIsInProgress
Bug · Open · Minor · created 2024-03-06

[code/log omitted]


## KAFKA-16349: ShutdownableThread fails build by calling Exit with race condition
Bug · Resolved (Fixed) · Minor · components: core · created 2024-03-06 · resolved 2024-03-29

`ShutdownableThread` calls `Exit.exit()` when the thread's operation throws FatalExitError. In normal operation, this calls System.exit, and exits the process. In tests, the exit procedure is masked with Exit.setExitProcedure to prevent tests that encounter a FatalExitError from crashing the test JVM.
Masking of exit procedures is usually done in BeforeEach/AfterEach annotations, with the exit procedures cleaned up immediately after the test finishes. If the body of the test creates a Shutdowna…

- **Ismael Juma:** Good catch.
- **Greg Harris:** I did some more exploration here.  # Some of the "exit 1" failures I included in my count earlier are caused by https://issues.apache.org/jira/browse/KAFKA-15343 and so was an overestimate. This particular failure doesn't happen all that often.  # There are more places affected than just those usi…
- **Greg Harris:** I added a tactical fix for the Exit class in my PR to resolve this bug. I'll pursue this refactor in a separate ticket KAFKA-16420.

## KAFKA-16358: Update Connect Transformation documentation
Bug · Resolved (Fixed) · Minor · components: connect · created 2024-03-08 · resolved 2024-03-15

When reading the [Kafka Connect docs|https://kafka.apache.org/documentation/#connect_included_transformation] for transformations, there are a few gaps that should be covered:
 * The Flatten, Cast and TimestampConverter transformations are not listed
 * HeadersFrom should be HeaderFrom
 * -InsertHeader is not documented-


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
- **Jeremy Norris:** Yes, if you cannot publish a fixed version of 3.7.0 artifact, then a new 3.7.1 release should be spun. The 3.7.0 artifact is simply broken.
- _…5 more comments_

## KAFKA-16360: Release plan of 3.x kafka releases.
Improvement · Resolved (Invalid) · Major · created 2024-03-11 · resolved 2024-03-12

KIP [https://cwiki.apache.org/confluence/display/KAFKA/KIP-833%3A+Mark+KRaft+as+Production+Ready#KIP833:MarkKRaftasProductionReady-ReleaseTimeline] mentions ,
h2. Kafka 3.7
 * January 2024
 * Final release with ZK mode
But we see in Jira, some tickets are marked for 3.8 release. Does apache continue to make 3.x releases having zookeeper and kraft supported independent of pure kraft 4.x releases ?
If yes, how many more releases can be expected on 3.x release line ?

- **Greg Harris:** Hi [~kaushik srinivas], thanks for your question! The release schedule in that KIP was superseded by a later KIP: [https://cwiki.apache.org/confluence/display/KAFKA/KIP-1012%3A+The+need+for+a+Kafka+3.8.x+release] and so is not accurate any longer. At this time, we expect that 3.8 will be the last…
- **Justine Olshan:** Hey there – there was some discussion on the mailing list. 3.8 should be the last release. See here: [https://lists.apache.org/thread/kvdp2gmq5gd9txkvxh5vk3z2n55b04s5]  There is also a KIP. KIP-1012: [https://cwiki.apache.org/confluence/display/KAFKA/KIP-1012%3A+The+need+for+a+Kafka+3.8.x+release]…
- **Matthias J. Sax:** Please don't use Jira to ask questions. Jira tickets are for bug reports and features only. Question should be asked on the user and/or dev mailing lists: https://kafka.apache.org/contact

## KAFKA-16361: Rack aware sticky assignor minQuota violations
Bug · Open · Major · components: clients · created 2024-03-11

In some low topic replication scenarios the rack aware assignment in the StickyAssignor fails to balance consumers to its own expectations and throws an IllegalStateException, commonly crashing the application (depending on application implementation). While uncommon the error is deterministic, and so persists until the replication state changes. 
We have observed this in the wild in 3.5.1, and 3.6.1. We have reproduced it locally in a test case in 3.6.1 and 3.7.0 (3.5.1 we did not try but like…

- **Laymain:** Hi there, we have the exact same problem here, I was about to open an issue. If it can help, here are some log involving only two hosts (i-0da0437e61e61bf88 and i-0d2e25eb1aebefab5): [^illegalstateexception.log]
- **BDeus:** Is it a regression related to this feature https://issues.apache.org/jira/browse/KAFKA-14450 ?
- **A. Sophie Blee-Goldman:** [~luked] it would help narrow down whether it was a regression vs a long-standing issue if you can try to reproduce it with some earlier versions. For example I believe the rack-aware assignment was added to the StickyAssignor in 3.5, so the first step might be to see if it's reproducible in 3.4. If…
- **li xiangyuan:** please check this [pr |https://github.com/apache/kafka/pull/13965]
- **li xiangyuan:** and I also created a Jira [issue|https://issues.apache.org/jira/browse/KAFKA-15170]
- _…4 more comments_

## KAFKA-16362: Fix type-unsafety in KStreamKStreamJoin caused by isLeftSide
Task · Resolved (Fixed) · Trivial · components: streams · labels: newbie++ · created 2024-03-11 · resolved 2024-06-03

The implementation of KStreamKStreamJoin has several places that the compiler emits warnings for, that are later suppressed or ignored:
 * LeftOrRightValue.make returns a raw LeftOrRightValue without generic arguments, because the generic type arguments depend on the boolean input.
 * Calling LeftOrRightValue includes an unchecked cast before inserting the record into the outerJoinStore
 * emitNonJoinedOuterRecords swaps the left and right values, and performs an unchecked cast
These seem to…

- **Greg Harris:** cc [~mjsax] [~ableegoldman] I looked through the (currently ignored) rawtypes warnings in Streams and this was one that I really didn't have a simple resolution for, and I think needs a real refactor to make type-safe. I don't think there's a bug hidden here, but the code didn't give me any confide…
- **Ramin Gharib:** [~gharris1727] I have been thinking on this one and made some changes, based on your PR, that I would like you to see. Could you please assign me to this task? I will post a (draft/proposal) PR soon!

## KAFKA-16363: Storage tool crashes if dir is unavailable
Sub-task · Resolved (Fixed) · Major · components: tools · created 2024-03-11 · resolved 2024-04-17

The storage tool crashes if one of the configured log directories is unavailable. 
[code/log omitted]
When configured with multiple directories, Kafka tolerates some of them (but not all) being inaccessible, so this tool should be able to handle the same scenarios without crashing.

- **Igor Soarez:** cc [~pprovenzano]
- **Michael Westerby:** [https://github.com/apache/kafka/pull/15733]

## KAFKA-16364: MM2 High-Resolution Offset Translation
New Feature · Open · Minor · components: mirrormaker · labels: needs-kip · created 2024-03-11

The current OffsetSyncStore implementation [https://github.com/apache/kafka/blob/8b72a2c72f09838fdd2e7416c98d30fe876b4078/connect/mirror/src/main/java/org/apache/kafka/connect/mirror/OffsetSyncStore.java#L57] stores a sparse index of offset syncs. This attempts to strike a balanced default behavior between offset translation availability, memory usage, and throughput on the offset syncs topic.
However, this balanced default behavior is not good enough in all circumstances. When precise offset t…

- **M Mehrtens:** This is especially relevant for cluster migration scenarios when consumer group offsets should be replicated with a minimum latency. Ideally, consumer groups could detach from the source cluster and attach to the target cluster without needing to process a batch of duplicate messages. This would req…

## KAFKA-16365: AssignmentsManager mismanages completion notifications
Sub-task · Resolved (Fixed) · Critical · components: jbod · created 2024-03-11 · resolved 2024-04-06

When moving replicas between directories in the same broker, future replica promotion hinges on acknowledgment from the controller of a change in the directory assignment.
ReplicaAlterLogDirsThread relies on AssignmentsManager for a completion notification of the directory assignment change.
In its current form, under certain assignment scheduling, AssignmentsManager both miss completion notifications, or prematurely trigger them.


## KAFKA-16366: Refactor KTable source optimization
Improvement · In Progress · Minor · components: streams · created 2024-03-12

Kafka Streams DSL offers an optimization to re-use an input topic as table changelog, in favor of creating a dedicated changelog topic.
So far, the Processor API did not support any such feature, and thus when the DSL compiles down into a Topology, we needed to access topology internal stuff to allow for this optimization.
With KIP-813 (merged for AK 3.8), we added `Topology#addReadOnlyStateStore` as public API, and thus we should refactor the DSL compilation code, to use this public API to bu…


## KAFKA-16367: Full ConsumerGroupHeartbeat response must be sent when full request is received
Sub-task · Resolved (Fixed) · Major · created 2024-03-12 · resolved 2024-03-19


## KAFKA-16368: Change constraints and default values for various configurations - part 1
Improvement · Resolved (Fixed) · Major · labels: breaking, kip · created 2024-03-13 · resolved 2025-02-05

This Jira is a parent item to track all the defaults and/or constraints that we would like to change with Kafka 4.0. This Jira will be associated with a KIP.
Currently, we are gathering feedback from the community on the configurations that don't have sane defaults.

- **David Jacot:** [~divijvaidya] Are we done with this KIP for 4.0?
- **Divij Vaidya:** Hey [~dajac]  Not yet. The author of the PRs attached is on vacation and will be back this Monday. This is their top priority next week. We are currently stuck on failing tests and discovered some inconsistencies with streams tests such as embedded server having a time which is in the past compared…
- **David Jacot:** Thanks, [~divijvaidya]. What the status now?
- **Divij Vaidya:** [~dajac] Out of 11 changes in the KIP, 9 have been merged and ported to 4.0 branch. The effort for remaining 3 (segment.ms, segment.index.bytes, max.compaction.lag.ms) is significant due to extensive number of test changes involved, hence, we will try to merge them in 4.0 on a best effort basis, i.e…
- **David Jacot:** [~divijvaidya] Any progress on this one? If not, may I ask you to cut another Jira for 5.0 with the remaining work items? It would be great if you could also update the description of this one with what has been done in 4.0. Thanks!
- _…1 more comments_

## KAFKA-16514: Kafka Streams: stream.close(CloseOptions) does not respect options.leaveGroup flag.
Bug · Resolved (Duplicate) · Minor · components: streams · created 2024-04-11 · resolved 2025-10-15

Working with Kafka Streams 3.7.0, but may affect earlier versions as well.
When attempting to shutdown a streams application and leave the associated consumer group, the supplied `leaveGroup` option seems to have no effect. Sample code:
[code/log omitted]
The expected behavior here is that the group member would shutdown and leave the group, immediately triggering a consumer group rebalance. In practice, the rebalance happens after the appropriate timeout configuration has expired.
I underst…

- **Sal Sorrentino:** Digging further into this, it seems the leaveGroup option is only supported if the "group.instance.id" is supplied via the StreamsConfig, however there is not documentation around this. The "group.instance.id" has no representation in the StreamsConfig class, event though it is intended to be a user…
- **Matthias J. Sax:** CloseOption was introduced via [https://cwiki.apache.org/confluence/display/KAFKA/KIP-812%3A+Introduce+another+form+of+the+%60KafkaStreams.close%28%29%60+API+that+forces+the+member+to+leave+the+consumer+group] The reasoning about the design should be on the KIP and corresponding DISCUSS thread. I…
- **A. Sophie Blee-Goldman:** I haven't gone back and re-read the KIP, but IIRC the reason for adding these CloseOptions was specific to solving an issue with static membership, hence why it only takes affect there. That said – I completely agree that there's no reason why this should only work with static membership, and the d…
- **Sal Sorrentino:** The KIP mentions nothing about static membership. I would also add that the current behavior seems to solve the wrong use case. A static member with persistent state is more likely to want to keep membership alive, while a member with transient/non-persistent state would want to relinquish membershi…
- **Matthias J. Sax:** Thanks for the input. I was not reviewing/voting the original KIP nor the PR. Thus, I did just assume there was some mentioning about static groups... As there is nothing about it in the KIP as you pointed out, I did some digging and the PR reveals why it's only implemented for static members: [http…
- _…17 more comments_

## KAFKA-16515: Fix the ZK Metadata cache use of voter static configuration
Sub-task · Resolved (Fixed) · Major · components: core · created 2024-04-11 · resolved 2024-05-28

Looks like because of ZK migration to KRaft the ZK Metadata cache was changed to read the voter static configuration. This needs to change to use the voter nodes reported by  the raft manager or the kraft client.
The injection code is in KafkaServer where it constructs MetadataCache.zkMetadata.

- **Josep Prat:** [~cmccabe] Do I understand right, that this Jira is done now?

## KAFKA-16516: Fix the controller node provider for broker to control channel
Sub-task · Resolved (Fixed) · Major · components: core · created 2024-04-11 · resolved 2024-05-28

The broker to controller channel gets the set of voters directly from the static configuration. This needs to change so that the leader nodes comes from the kraft client/manager.
The code is in KafkaServer where it construct the RaftControllerNodeProvider.

- **Josep Prat:** [~cmccabe] Do I understand right, that this Jira is done now?

## KAFKA-16517: Do not decode metadata records in the internal kraft partition listener
Sub-task · Resolved (Fixed) · Major · components: kraft · created 2024-04-11 · resolved 2026-08-12

The implementation for the internal partition listener for kraft reads and decodes the data record. This is not required and it is only done because it is easier to implement with the current code.


## KAFKA-16518: Storage tool changes for KIP-853
Sub-task · Resolved (Fixed) · Major · components: tools · created 2024-04-11 · resolved 2024-08-02

https://cwiki.apache.org/confluence/display/KAFKA/KIP-853%3A+KRaft+Controller+Membership+Changes#KIP853:KRaftControllerMembershipChanges-kafka-storage

- **Muralidhar Basani:** [~jsancio] can I look into this ? Seems like adding 4 new arguments standalone controller-quorum-voters feature release-version
- **José Armando García Sancio:** Yes, please go ahead. That's correct [~muralibasani] . --release-version is less important and is bit trickier to implement see this KIP [https://cwiki.apache.org/confluence/display/KAFKA/KIP-1022%3A+Formatting+and+Updating+Features.] I am okay if we don't want to implement it in this PR/Jira and we…
- **Muralidhar Basani:** [~jsancio] have a draft pr opened for adding 'standalone' It basically does the below.  * It expects a metadaa log dir to exist  * If dir exists, a meta.properties file is created if it doesn't exist.  * a random id is generated and written to file directory.id what do you think, if am in the r…
- **José Armando García Sancio:** HI [~muralibasani] , All of the new options are under the format command (e.g. {{{}kafka-storage format ...{}}}). The format command already exist and does some of the functionality you describe above like storing the directory.id in the meta.properties. This PR needs to extend this code to support…
- **Muralidhar Basani:** Hi [~jsancio] I see it has to be extended under format command. And yes directory.id is already written under format command [here|https://github.com/apache/kafka/blob/trunk/core/src/main/scala/kafka/tools/StorageTool.scala#L456]. Should this be done only with 'standalone' ? So we don't write direc…
- _…5 more comments_

## KAFKA-16519: Expose the supported and finalized kraft.version in ApiVersions response
Sub-task · Resolved (Duplicate) · Major · components: core · created 2024-04-11 · resolved 2024-07-22

- **Josep Prat:** Changing target fix version to 3.9 since this is not a blocker and we are past code freeze
- **José Armando García Sancio:** This was resolved as part of another issue and pr.
- **Colin McCabe:** Removing fix version 3.9 for this duplicate JIRA since it is confusing release.py

## KAFKA-16520: Changes to DescribeQuorum response
Sub-task · Resolved (Fixed) · Major · components: kraft · created 2024-04-11 · resolved 2024-06-12

- **Nikolay Izhikov:** Hello [~jsancio] Do you need help with this ticket?  I'm ready to work on it.
- **José Armando García Sancio:** Yes [~nizhikov] you can take it. You'll need it for kafka-metadata-quorum describe changes for KIP-853. Looking at the schema changes I suggested, it looks like I never added: [code/log omitted] As suggested by the CLI output: [code/log omitted] I updated the KIP to include this new field in th…
- **Nikolay Izhikov:** Hello [~jsancio]  Do we want to enhance FetchRequest inside this PR? Or I can leave DirectoryId equals to null for cases when `ReplicaState` created while handling FetchRequest?
- **José Armando García Sancio:** {quote}Do we want to enhance FetchRequest inside this PR? {quote} [~nizhikov] , I won't do that part. I am currently working on implementing those changes now as part of https://issues.apache.org/jira/browse/KAFKA-16527 {quote}Or I can leave DirectoryId equals to null for cases when `ReplicaState…
- **Nikolay Izhikov:** [https://github.com/apache/kafka/pull/16106] ready for review.

## KAFKA-16521: kafka-metadata-quorum describe changes for KIP-853
Sub-task · Resolved (Fixed) · Major · components: tools · created 2024-04-11 · resolved 2024-08-01

# [https://cwiki.apache.org/confluence/display/KAFKA/KIP-853%3A+KRaft+Controller+Membership+Changes#KIP853:KRaftControllerMembershipChanges-describe--status]
 # [https://cwiki.apache.org/confluence/display/KAFKA/KIP-853%3A+KRaft+Controller+Membership+Changes#KIP853:KRaftControllerMembershipChanges-describe--replication]

- **Nikolay Izhikov:** Hello, [~jsancio] I have a question regarding KIP: [code/log omitted] First example [code/log omitted] and the second [code/log omitted] - double minus sign used for different words. Is it some kind of typo? Or command format must be exactly like in the KIP?
- **José Armando García Sancio:** Yes. It is a typo. It should be {{{}describe --replication{}}}: [code/log omitted] I updated the KIP. Note that for {{{}describe --status{}}}, you wont be able to implement the committed voters output: [code/log omitted] I haven't implemented that functionality in the controller side. If we mer…
- **José Armando García Sancio:** [~nizhikov] are you currently working on this? I ask because [~alyssahuang] may pick this up.
- **Nikolay Izhikov:** Hello, [~jsancio]  I will provide a patch in a till end of the week.
- **Alyssa Huang:** Hey [~nizhikov], the 3.9.0 release branch was cut and an exception was made for cherry-picking in this item, so we need this in asap - I'm free this week to work on this item so I'll start working on it.  If your patch was ready though, just let me know and I can help review instead

## KAFKA-16522: Admin client changes for adding and removing voters
Sub-task · Resolved (Fixed) · Major · created 2024-04-11 · resolved 2024-06-05

https://cwiki.apache.org/confluence/display/KAFKA/KIP-853%3A+KRaft+Controller+Membership+Changes#KIP853:KRaftControllerMembershipChanges-Admin

- **José Armando García Sancio:** [~phong260702] thanks for assigning this issue to yourself. I updated the issue to show that it is currently blocked by two other issues that need to be implemented first.
- **Colin McCabe:** Implemented by {{KAFKA-16535: Implement AddVoter, RemoveVoter, UpdateVoter RPCs}}

## KAFKA-16523: kafka-metadata-quorum add voter and remove voter changes
Sub-task · Resolved (Fixed) · Major · components: tools · created 2024-04-11 · resolved 2024-08-09

# https://cwiki.apache.org/confluence/display/KAFKA/KIP-853%3A+KRaft+Controller+Membership+Changes#KIP853:KRaftControllerMembershipChanges-add-controller–config%3Cserver.properties%3E
 # https://cwiki.apache.org/confluence/display/KAFKA/KIP-853%3A+KRaft+Controller+Membership+Changes#KIP853:KRaftControllerMembershipChanges-remove-controller--controller-id%3Ccontroller-id%3E--controller-uuid%3Ccontroller-uuid%3E

- **José Armando García Sancio:** [~dengziming] are you working on this? I am working on implementing the AddVoter RPC. It would be good to have this implemented soon after that PR is ready: https://issues.apache.org/jira/browse/KAFKA-16535

## KAFKA-16524: Metrics for KIP-853
Sub-task · Resolved (Fixed) · Major · components: kraft · created 2024-04-11 · resolved 2025-01-30

https://cwiki.apache.org/confluence/display/KAFKA/KIP-853%3A+KRaft+Controller+Membership+Changes#KIP853:KRaftControllerMembershipChanges-Monitoring

- **xiaochen.zhou:** I would like to give a try on this, can I take this ticket?
- **José Armando García Sancio:** [~xiaochen.hi] sounds good. Assign it to yourself. Let me know if you have any question or if there is any missing functionality that you need.

## KAFKA-16677: Replace ClusterType#ALL and ClusterType#DEFAULT by Array
Improvement · Resolved (Fixed) · Minor · created 2024-05-07 · resolved 2024-05-13

Both ClusterType#ALL and ClusterType#DEFAULT are a kind of "tag" instead of true "type". It seems to me they can be removed by using Array. For example:
ClusterType#ALL -> {Type.ZK, Type.KRAFT, Type.CO_KRAFT}
ClusterType#DEFAULT -> {}
There are two benefits
1. That is more readable for "ALL type". 
2. We don't throw the awkward "exception" when seeing "DEFAULT".

- **Chia-Ping Tsai:** For another, we can simplify the code (https://github.com/apache/kafka/blob/trunk/tools/src/test/java/org/apache/kafka/tools/consumer/group/ConsumerGroupCommandTestUtils.java#L77) [code/log omitted]
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

## KAFKA-16684: FetchResponse#responseData could return incorrect data
Bug · Resolved (Fixed) · Minor · created 2024-05-07 · resolved 2024-07-09

[https://github.com/apache/kafka/commit/2b8aff58b575c199ee8372e5689420c9d77357a5] make it accept input to return "partial" data. The content of output is based on the input but we cache the output ... It will return same output even though we pass different input. That is a potential bug.

- **Chia-Ping Tsai:** After [https://github.com/apache/kafka/commit/2b8aff58b575c199ee8372e5689420c9d77357a5] , I don't think the "cache" is useful. Hence, we can just remove the cache to fix this potential bug
- **Johnny Hsu:** hi [~chia7712]  May i know if you are working on this? if not I am happy to help :)
- **Chia-Ping Tsai:** [~m1a2st] thanks for taking over this jira. Please notice the comment: https://github.com/apache/kafka/pull/15966#issuecomment-2206969288
- **Ken Huang:** Yes, I will take care about that comment

## KAFKA-16685: RLMTask warning logs do not include parent exception trace
Improvement · Resolved (Fixed) · Major · components: Tiered-Storage · created 2024-05-07 · resolved 2024-05-08

When RLMTask warning exceptions happen and are logged, it only includes the exception message, but we lose the stack trace.
See [https://github.com/apache/kafka/blob/70b8c5ae8e9336dbf4792e2d3cf100bbd70d6480/core/src/main/java/kafka/log/remote/RemoteLogManager.java#L821-L831]
This makes it difficult to troubleshoot issues.

- **Jorge Esteban Quilcate Otoya:** Merged https://github.com/apache/kafka/pull/15880

## KAFKA-16686: Flakey tests in TopicBasedRemoteLogMetadataManagerTest
Test · Resolved (Fixed) · Major · components: Tiered-Storage · created 2024-05-07 · resolved 2024-05-15

Tests in {{TopicBasedRemoteLogMetadataManagerTest}} flake because {{waitUntilConsumerCatchesUp}} may return before all expected metadata is caught up.
Flakyness report [here|https://ge.apache.org/scans/tests?search.timeZoneId=Europe%2FLondon&tests.container=org.apache.kafka.server.log.remote.metadata.storage.TopicBasedRemoteLogMetadataManagerTest].


## KAFKA-16687: Native memory leak by Unsafe_allocatememory  in Kafka Clients  3.7.0
Bug · Resolved (Invalid) · Major · components: clients, consumer · created 2024-05-07 · resolved 2024-05-25

I am building a Java Project which using Maven dependency Kafka-clients with 3.7.0 version.
My Java application logic is to use Kafka Consumer to poll Kakfa broker topic  continuously. 
I have configured my Java application with JVM options with -Xms8G -Xmx8G  -XX:MaxMetaspaceSize=4G, and then run it. 
Also, there are 16G physical memory on my virtual machine. 
After my Java application running a long time, I have found that resident memory of the Java Process was being grown to more than 14…

- **Philip Nee:** Hey [~fortherightous] - we also observed some (possible) memory leak.  The symptom is particularly obvious when working with large number of partitions.  Have you tried kafka client version 3.6 or earlier?
- **FTR:** That's it, there are some topics with 30 partitions. I have tested Kafka client 2.8.2 before, with same issue.
- **FTR:** BTW, before that I had also encountered heap leak issue in  Kafka client 2.8.2. After upgraded to 3.7.0(>3.4.0) and disabled JMX reporter, and heap leak issue was resolved.
- **Philip Nee:** But this is native memory leak so I suspect it's a different issue than heap leak. would you mind experimenting with 3.6 ? We didn't see the leak using 3.6.
- **FTR:** Surely, let me experiment with 3.6 and then feedback here.
- _…18 more comments_

## KAFKA-16838: Kafka Connect loads old tasks from removed connectors
Bug · Resolved (Fixed) · Major · components: connect · created 2024-05-24 · resolved 2024-06-04

Hello,
When creating connector we faced an error from one of our ConfigProviders about not existing resource, but we didn't try to set that resource as config value:
[code/log omitted]
It looked like there already was connector with the same name and same config, +but it wasn't.+
After investigation we found out, that few months ago on that cloud there was the connector with the same name and another value for config provider. Then it was removed, but by some reason when we tried to create c…

- **Chris Egerton:** I knew this one felt familiar–we actually fixed a more common variant of this bug in [https://github.com/apache/kafka/pull/8444.] However, we missed the case of topic compaction.
- **Sergey Ivanov:** Hi [~ChrisEgerton], thanks for the answer, but still for my understanding, on connector remove we also send tombstone messages for connector "config" and "target" records, why can't we just do the same for "task" and "commit" records?
- **Chris Egerton:** It's probably possible but it might get a bit messy. We'd need to think through some edge cases, such as if a worker that's patched to emit (and presumably handle) tombstones for task configs dies partway through deleting a connector, and then a worker that hasn't been patched yet (either because th…

## KAFKA-16839: Replace KafkaRaftClient's voterNode with leadeNode
Sub-task · Open · Major · created 2024-05-24

The id passed to KafkaRaftClient.voterNode is always the leader id.


## KAFKA-16840: Add a --timeout option to ConfigCommand
Improvement · Open · Minor · components: admin · created 2024-05-25


## KAFKA-16841: ZKMigrationIntegrationTests broken
Task · Resolved (Fixed) · Blocker · created 2024-05-25 · resolved 2024-05-27

A recent merge to trunk seems to have broken tests so that I see 78 failures in the CI. 
I see lots of timeout errors and `Alter Topic Configs had an error`

- **Justine Olshan:** I am suspicious of https://github.com/apache/kafka/pull/16006
- **Justine Olshan:** Reverting that commit seems to fix the tests.
- **Justine Olshan:** I opened [https://github.com/apache/kafka/pull/16082] for now unless someone can fix the issue without reverting.
- **Justine Olshan:** fixed by https://github.com/apache/kafka/commit/bac8df56ffdf8a64ecfb78ec0779bcbc8e9f7c10

## KAFKA-16842: Fix KafkaConfig validation and support unknown voters
Sub-task · Resolved (Fixed) · Major · created 2024-05-25 · resolved 2024-08-16

1. controller.quorum.bootstrap.server is only allowed to be empty when controller.quorum.voter is set.
2. controller.quorum.voter can be empty if the 0-0.checkpoint contains a voter set. This means that we can't really validate this property in KafkaConfig. It needs to be done by the KafkaRaftClient.
3. Fix the KafkaRaftClient implementation to allow unknown voters by adding and user VoterSet#empty.


## KAFKA-16843: Remove preAppendErrors from createPutCacheCallback
Improvement · Resolved (Fixed) · Minor · created 2024-05-26 · resolved 2024-06-05

origin discussion: [https://github.com/apache/kafka/pull/16072#pullrequestreview-2077368462]
The method `createPutCacheCallback` has a input argument `preAppendErrors` [0]. It is used to keep the "error" happens before appending. However, the pre-append error is handled before by calling `responseCallback` [1]. Hence, we can remove `preAppendErrors`.
[0] https://github.com/apache/kafka/blob/trunk/core/src/main/scala/kafka/coordinator/group/GroupMetadataManager.scala#L387
[1] https://github.co…

- **PoAn Yang:** Hi [~chia7712], thanks for filing the ticket. If you're not working on this, I would like to help to remove unused parameter. Thanks.
- **PoAn Yang:** The PR [https://github.com/apache/kafka/pull/16105] is merged. Resolved the issue.

## KAFKA-16844: ByteArrayConverter can't convert ByteBuffer
Improvement · Resolved (Fixed) · Minor · components: connect · created 2024-05-27 · resolved 2024-05-30

In current Schema design, schema type Bytes correspond to two kinds of classes, byte[] and ByteBuffer. But current ByteArrayConverter can only convert byte[]. My suggestion is to add ByteBuffer support in current ByteArrayConverter.

- **Arnav Dadarya:** Can you assign to this, so I can start working on this
- **Fan Yang:** Already sent PR for it.

## KAFKA-16845: Migrate ReplicationQuotasTestRig to new test infra
Sub-task · Resolved (Fixed) · Minor · created 2024-05-27 · resolved 2024-10-24

as title

- **Ken Huang:** I'm interesting in this ticket
- **Dmitry Werner:** [~m1a2st] Hello, are you working on this task? I can grab issue if you have no time.
- **Ken Huang:** [~javakillah], sure you can take it.

## KAFKA-16846: Should TxnOffsetCommit API fail all the offsets if any fails the validation?
Improvement · Open · Major · created 2024-05-27

While working on KAFKA-16371, we realized that the handling of INVALID_COMMIT_OFFSET_SIZE errors while committer transaction offsets, is a bit inconsistent between the server and the client. On the server, the offsets are validated independently from each others. Hence if two offsets A and B are committed and A fails the validation, B is still written to the log as part of the transaction. On the client, when INVALID_COMMIT_OFFSET_SIZE is received, the transaction transitions to the fatal state.…


## KAFKA-16847: Revise the README for recent CI changes 
Improvement · Resolved (Invalid) · Minor · created 2024-05-28 · resolved 2024-05-29

The recent changes [0] removes the test of 11 and 17, and that is good to our CI resources. However, in the root readme we still declaim "We build and test Apache Kafka with Java 8, 11, 17 and 21" 
[0] https://github.com/apache/kafka/commit/adab48df6830259d33bd9705b91885c4f384f267
[1] https://github.com/apache/kafka/blob/trunk/README.md?plain=1#L7

- **Cheng-Kai, Zhang:** hi [~chia7712]  may I take this easy fix? :)
- **Chia-Ping Tsai:** sure, btw please follow the mail https://lists.apache.org/thread/jvz1g2mkjrnqskk52n28sxhwdjo74m34 for possible changes about CI
- **Greg Harris:** Hey FYI the trunk builds still run the full suite, so this isn't inaccurate right now. If the 11 and 17 builds are disabled completely then it will be accurate.
- **Justine Olshan:** +1 to what [~gharris1727] said, I was just coming here to say the same.
- **Chia-Ping Tsai:** {quote} the trunk builds still run the full suite {quote} The README says that we run both "build" and "test" for 11 and 17, but we don't run "test" for 11 and 17, right?
- _…2 more comments_

## KAFKA-16848: Reverting KRaft migration for "Migrating brokers to KRaft" state is wrong
Bug · Patch Available · Major · created 2024-05-28

Hello,
I would like to report a mistake in the {_}Kafka 3.7 Documentation -> 6.10 KRaft -> ZooKeeper to KRaft Migration -> Reverting to ZooKeeper mode During the Migration{_}.
While migrating my Kafka + Zookeeper cluster to KRaft and testing rollbacks at a different migration stages I have noticed, that "{_}Directions for reverting{_}" provided for "{_}Migrating brokers to KRaft{_}" are wrong.
Following the first step provided in documentation you suppose to : _On each broker, remove the proc…


## KAFKA-17036: KIP-919 supports for `createAcls`, `deleteAcls`, `describeAcls`
Sub-task · Resolved (Fixed) · Minor · created 2024-06-25 · resolved 2024-09-13

as title

- **PoAn Yang:** Hi [~chia7712], I'm interested in this issue. If you're not working on it, may I take it? Thank you.

## KAFKA-17037: KIP-919 supports for `describeClientQuotas` and `alterClientQuotas`
Sub-task · Open · Minor · created 2024-06-25

- **Chia-Chuan Yu:** Hi, [~chia7712]  Can I have this one please? thanks!
- **TaiJuWu:** After discussed with [~chiacyu] offline, I will take it over.
- **Lan Ding:** Hi [~taijuwu], are you still working on this? I would like to take over otherwise.
- **TaiJuWu:** Hi [~isding_l] , this ticket was finished for a long time but it lacks reviewers. After finding any reviewer, I will continue to work on this.

## KAFKA-17038: KIP-919 supports for `alterPartitionReassignments` and `listPartitionReassignments`
Sub-task · Resolved (Fixed) · Minor · created 2024-06-25 · resolved 2024-08-27

as title

- **Kuan Po Tseng:** Hi [~chia7712] , If you are not currently working on this issue, I am willing to take it over. Many thanks !

## KAFKA-17039: KIP-919 supports for `unregisterBroker`
Sub-task · Resolved (Fixed) · Minor · created 2024-06-25 · resolved 2025-03-01

as title

- **TengYao Chi:** Gentle ping  [~chia7712] ,if you are not start working I would like to handle this issue
- **TengYao Chi:** Hi [~chia7712]  It seems that our test infra currently only support the controller with plaintext security protocol and it will be a blocker to test the describeDelegationToken and describeUserScramOptions. :P
- **Lan Ding:** Hi [~frankvicky],  If this ticket is still open, may I take it over?
- **TengYao Chi:** Hi [~isding_l]  Thanks for the interest. However, I have already a local patch for this one. Feel free to browse other issue. :)

## KAFKA-17040: Unknown telemetry state: TERMINATED thrown when closing AsyncKafkaConsumer
Bug · Resolved (Fixed) · Major · components: clients, metrics · labels: consumer-threading-refactor · created 2024-06-25 · resolved 2024-12-11

An error is occasionally thrown when closing the {{{}AsyncKafkaConsumer{}}}:
[code/log omitted]
The issue appears to be that the {{TERMINATED}} state is not expected in the switch statement inside [timeToNextUpdate()|https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/common/telemetry/internals/ClientTelemetryReporter.java#L307].
As an aside, the error message might make more sense to be written as "{_}Unexpected{_} telemetry state" instead of "{_}Unknown{_} tele…

- **Apoorv Mittal:** [~kirktrue] Thanks for reporting, I can take it up. Just a quick question, the error only occurs while closing the consumer, correct? Is it under scenarios when consumer close took more time than next network client poll time? I expect that's the only scenario when this issue can occur. I am just wo…
- **Lianet Magrans:** Hey [~apoorvmittal10] , in case it helps, I believe this issue happens when the consumer close cannot wait for the network thread to close (ex. close with low timeout or interrupted). This flow:  # async consumer app thread triggers action to close network thread, and block until it completes (won'…
- **Apoorv Mittal:** Thanks [~lianetm] for adding details. I have created a PR: [https://github.com/apache/kafka/pull/18143,] let me know if it makes sense.

## KAFKA-17041: Add pagination when describe large set of metadata via Admin API 
Improvement · Open · Major · components: admin · created 2024-06-26

Some of the request via Admin API timeout on large cluster or cluster with large set of specific metadata. For example OffsetFetchRequest and DescribeLogDirsRequest timeout due to large number of partition on cluster. Also DescribeProducersRequest and ListTransactionsRequest time out due to too many short lived PID or too many hanging transactions
[KIP-1062: Introduce Pagination for some requests used by Admin API|https://cwiki.apache.org/confluence/display/KAFKA/KIP-1062%3A+Introduce+Paginatio…

- **dujian0068:** Hello： Can I take this task?
- **Omnia Ibrahim:** Hi [~bmilk] the KIP still a draft so it is not ready yet to be picked up. So for the time being I'll keep it unassigned or assigned to me until the KIP get voted.
- **Lin Siyuan:** Hi [~omnia_h_ibrahim] , I have a few questions, because of the presence of ‘futureLogs’, the same partition will appear under a different path in 'kafka.logs.dir', And for DescribeLogDirsRequest the first level category is 'logDir', so I think we might need to add 'logDir' to 'Cursor', don't you thi…
- **Lin Siyuan:** hi [~omnia_h_ibrahim] ,MetadataRequest.json may have some errors :1. Incorrect spelling of pagination; 2.Cursor type is wrong and there should be no groupId !image-2024-08-19-17-32-08-015.png!
- **Lin Siyuan:** hi [~omnia_h_ibrahim] , I have been following this KIP for a long time, if it passes the vote, I hope to be able to participate in the transformation of one of the interfaces, thank you.

## KAFKA-17042: the migration docs should remind users to set "broker.id.generation.enable" when adding broker.id
Improvement · Resolved (Fixed) · Minor · created 2024-06-26 · resolved 2024-07-05

in the section: Enter Migration Mode on the Brokers
it requires users to add "broker.id", but it can produces error "broker.id must be greater than or equal to -1 and not greater than reserved.broker.max.id" too. That is caused by the zk broker is using a generated broker id.
As this phase is temporary, the simple solution is to remind users to add "broker.id.generation.enable=false" if the zk broker is using generated broker id.

- **TengYao Chi:** Hi [~chia7712] , I would like to handle this one. :)

## KAFKA-17043: Strictly Uniform Sticky partition strategy leads to slow handling of command events
Bug · Open · Major · created 2024-06-26

h1. Summary
Performance degradation in command scenario due to implementation of KIP-794 and the making of Strictly Uniform Sticky partition strategy default.
h1. Problem Description
Following KIP-794, the Strictly Uniform Sticky partition strategy has been introduced and set as the default, resulting in the deprecation of the {{{}DefaultPartitioner{}}}.
The new partitioning strategy has led to significant performance degradation within our "command" scenario. Our workflow orchestrator dispa…


## KAFKA-17044: Connector deletion can lead to resource leak during a long running connector startup
Bug · Resolved (Won't Fix) · Major · components: connect · created 2024-06-27 · resolved 2024-07-30

We have identified a gap in the shutdown flow for the connector worker. If the connector is in [INIT|https://github.com/apache/kafka/blob/trunk/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConnector.java#L403-L404] state and still executing the [WorkerConnector::doStart|https://github.com/apache/kafka/blob/trunk/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConnector.java#L207-L218] method, a DELETE API call would invoke the [WorkerConnector::shutdo…

- **Chris Egerton:** [~bgoyal] I think you should reconsider the implementation of your connector. Instead of blocking in {{{}start{}}}, you can perform retries in a separate thread, and whenever a new set of task configurations needs to be generated (e.g., when a db connection has finally been established), invoke [con…
- **Chris Egerton:** [~bgoyal] please let me know if the workaround suggested above can work for your connector. I'd like to close this as "won't fix" if possible, but will hold off for a bit in case you believe it's not a reasonable approach.
- **Bhagyashree:** [~ChrisEgerton] , I agree there are ways to make start method of the connector finish faster. But as part of this JIRA, what I wanted to convey is that the shutdown method relies on connector startup to finish. If a DELETE call is made, the call is not honoured until the connector start completes.…
- **Chris Egerton:** The crux of the issue is that invoking {{stop}} on a connector that's blocked in {{start}} is likely to cause more issues than it fixes. The most trivial way of preventing race conditions with that kind of API would be for connector developers to make both methods {{{}synchronized{}}}, which would h…
- **Chris Egerton:** [~bgoyal] pinging again, please let me know if this can be closed.
- _…2 more comments_

## KAFKA-17045: Move MetadataLogConfig from kafka to kafka.raft
Improvement · Resolved (Duplicate) · Minor · created 2024-06-27 · resolved 2025-03-20

The MetadataLogConfig belongs to raft, move file to raft to mach the package name.

- **Ksolves India Limited:** The file named MetadataLogConfig is written in Scala which is in location kafka/core/src/main/scala/kafka/MetadataLogConfig.scala  and the separate raft package contains the files written in Java. If you are referring this, then we have to create MetadataLogConfig or create a scala package into ra…
- **Lin Siyuan:** If your intention is just to "kafka\core\src\main\scala\kafka\raft", I enclose the PR "https://github.com/apache/kafka/pull/16484/"
- **PoAn Yang:** This will be covered by https://issues.apache.org/jira/browse/KAFKA-15599 with PR https://github.com/apache/kafka/pull/19246.

## KAFKA-17046: Upgrade netty version to 4.1.111.Final
Improvement · Resolved (Fixed) · Minor · created 2024-06-27 · resolved 2024-07-01

- **Ken Huang:** Im intersting in this issue, Could you assign to me?
- **Chia-Ping Tsai:** It seems there is a PR already https://github.com/apache/kafka/pull/16469

## KAFKA-17103: MockClient tight loops when no metadata is present in KafkaProducerTest
Test · Open · Minor · components: clients · labels: newbie · created 2024-07-09

MockClient can throw this exception:
[code/log omitted]
This happens whenever the MockClient.DefaultMockMetadataUpdater#lastUpdate variable is null, which is the case whenever there has not been any mock metadata update.
In practice, this appears to happen in KafkaProducerTest#testTopicExpiryInMetadata, KafkaProducerTest#testTopicRefreshInMetadata, KafkaProducerTest#testTopicNotExistingInMetadata. These three tests also use busy-waiting to have another thread wait for the metadata update requ…

- **Greg Harris:** Also it's possible that there's an existing mechanism in MockClient for performing this sort of thing, or an existing method that can be modified. I'm not sure exactly why these particular tests have this flaw, as it seems like providing metadata updates would be a fairly natural thing to mock out.
- **Sathvik K Basavaraju:** Hey [~gharris1727], I'd Like to look into this. Can you assign this to me?
- **zhengke zhou:** Hi [~gharris1727] I would like to try this.
- **Girish:** [~zzk1] I would like to know your approach towards solving this issue.
- **Chang-Yu Huang:** Hey [~zzk1] [~girishn] are you still watching for this issue? I want to take it and already have a solution.

## KAFKA-17104: InvalidMessageCrcRecordsPerSec is not updated in validating LegacyRecord
Bug · Resolved (Fixed) · Minor · created 2024-07-09 · resolved 2024-07-24

see discussion: https://github.com/apache/kafka/pull/16167#discussion_r1671302401


## KAFKA-17105: Unnecessary connector restarts after being newly created
Bug · Resolved (Fixed) · Minor · components: connect · created 2024-07-09 · resolved 2024-07-17

When a connector is created, it may be restarted unnecessarily immediately after it is first started by the worker to which it has been assigned:
 # Connector config is written to the config topic
 # A worker reads the new record from the config topic, and adds the connector to its connectorConfigUpdates field (see [here|https://github.com/apache/kafka/blob/43676f7612b2155ecada54c61b129d996f58bae2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/distributed/DistributedHerder.java…

- **Chris Egerton:** This likely goes back much further than 3.0.0. To save time I've only included that version and later.

## KAFKA-17106: Enable KafkaConsumerTest#testFetchProgressWithMissingPartitionPosition for AsyncConsumer
Sub-task · Resolved (Fixed) · Minor · components: clients, consumer, unit tests · created 2024-07-10 · resolved 2024-07-14

That test can be fixed by this approach (https://github.com/apache/kafka/pull/16541#discussion_r1671273572)


## KAFKA-17107: Backport of PR-15327
Bug · Open · Major · created 2024-07-10

Due to Potential incorrect access control during migration from ZK mode to KRaft mode, The following CVE
 * [https://nvd.nist.gov/vuln/detail/CVE-2024-27309]
is present in Kafka versions <3.6.2. Further details are present here:
[https://github.com/advisories/GHSA-79vv-vp32-gpp7]
As a user of Kafka 3.5.1, I want to backport the fix from Kafka 3.6.2 to strengthen the security posture of v3.5.1


## KAFKA-17108: Expose EarliestPendingUpload offset spec in ListOffsets API
Sub-task · Resolved (Fixed) · Major · created 2024-07-10 · resolved 2025-08-27


## KAFKA-17109: Reduce log message load for failed locking
Improvement · Resolved (Fixed) · Major · components: streams · created 2024-07-10 · resolved 2024-11-13

The following exception with stack traces is logged many times when state updater is enabled:
[code/log omitted]
The exception is expected since it happens because a lock on the task state directory is not yet been freed by a different stream thread on the same Kafka Streams client after an assignment. But with the state updater acquiring the lock is attempted in each poll iteration which is every 100 ms by default.
One option to reduce the log messages is to reduce the rate at which a lock i…

- **Eduwer Camacaro:** IMO, second option is better. I suggest reduce the logging by removing the exception stacktrace and message because this exception is expected to happen when the stream instance is working with multiple stream threads.
- **Bruno Cadonna:** In the end, we got both options. [~alisa23] implemented the backoff solution in https://github.com/apache/kafka/pull/17209 and [~danicafine] implemented reduced logging in https://github.com/apache/kafka/pull/16705. Like it!

## KAFKA-17110: Enable valid test case in KafkaConsumerTest for AsyncKafkaConsumer
Sub-task · Resolved (Fixed) · Minor · created 2024-07-10 · resolved 2024-07-14

Enable testResetUsingAutoResetPolicy, verifyPollTimesOutDuringMetadataUpdate, testPollThrowsInterruptExceptionIfInterrupted, fetchResponseWithUnexpectedPartitionIsIgnored, testManualAssignmentChangeWithAutoCommitEnabled, testManualAssignmentChangeWithAutoCommitDisabled, testOffsetOfPausedPartitions, and testCloseShouldBeIdempotent for AsyncKafkaConsumer

- **Lianet Magrans:** Hey [~yangpoan] , thanks for taking on this one! Heads-up in case it helps, we've dealt with some KafkaConsumerTests that cannot be applied to the AsyncConsumer just because of the way the are written. In those cases, it's fair to leave them running for the CLASSIC only, and write a separate test on…
- **PoAn Yang:** Hi [~lianetm], thanks for the comment. I will check again all test cases which are only marked with `CLASSIC`. If the case needs to rewrite in AsyncKafkaConsumerTest, I will add new tests to AsyncKafkaConsumerTest and move CLASSIC only test cases to LegacyKafkaConsumerTest. I think this is goal of K…

## KAFKA-17111: ServiceConfigurationError in JsonSerializer/Deserializer during Plugin Discovery
Bug · Resolved (Fixed) · Blocker · components: connect · created 2024-07-10 · resolved 2024-07-11

h3. Problem:
JsonSerializer and JsonDeserializer use objectMapper.findAndRegisterModules(), which attempts to register all Jackson modules implementing com.fasterxml.jackson.databind.Module. This can cause a ServiceConfigurationError when incompatible modules are present in the classpath.
[code/log omitted]
h3. Steps to Reproduce:
1. Start a connect worker with Service loading enabled and with certain connector plugins in plugin path (e.g. AzureBlobSource & BigQuerySink)
2. Observe ServiceC…

- **Greg Harris:** Hi [~vbalani] Thank you for the bug report! I can reproduce it locally. I believe that this should be a cosmetic error, as the error is thrown when the classpath JsonConverter is found via the each plugin.path. These later get excluded to avoid duplicates: [https://github.com/apache/kafka/blob/25d7…

## KAFKA-17112: StreamThread shutdown calls completeShutdown only in CREATED state
Bug · Closed (Fixed) · Minor · components: streams, unit tests · created 2024-07-10 · resolved 2024-08-23

While running tests in `StreamThreadTest.java` in kafka/streams, I noticed the test left many lingering threads. Though the class runs `shutdown` after each test, the shutdown only executes `completeShutdown` if the StreamThread is in CREATED state. See [https://github.com/apache/kafka/blob/0b11971f2c94f7aadc3fab2c51d94642065a72e5/streams/src/test/java/org/apache/kafka/streams/processor/internals/StreamThreadTest.java#L231] and [https://github.com/apache/kafka/blob/0b11971f2c94f7aadc3fab2c51d946…

- **Bruno Cadonna:** [~aoli-al] I think you are right. We are leaking the state updater and processing threads in that test. The issue is that when we create the stream thread we create and start the state updater thread and the processing threads.  Would you be interested to fix this issue?
- **Ao Li:** Yes, I'm happy to submit a patch. I'm thinking of two potential fixes:  1. extend the `shutdown()` method to `shutdown(boolean forceCleanup)`.  [code/log omitted] 2. make `completeShutdown` public and directly call it from the test.  Which one do you think is better?
- **Bruno Cadonna:** [~aoli-al] I think it would be better to change where the state updater and the processing threads are started. I am not sure why we start the threads before we start the stream thread. If we start those threads in the same location where we start the stream thread, we should not need to change anyt…
- **Ao Li:** [~cadonna] Aren't stateUpdater and processingThread expected to be started in some tests since the parameterized tests control them. [code/log omitted] and here  [code/log omitted]
- **Bruno Cadonna:** [~aoli-al] Yes, but I guess they are only expected to be started in tests that also start the stream thread. So ideally, the processing thread and the state updater thread should be started when the stream thread is started. I haven't double checked my assumption.
- _…3 more comments_

## KAFKA-17113: Flaky Test in GlobalStreamThreadTest#shouldThrowStreamsExceptionOnStartupIfExceptionOccurred
Bug · Resolved (Fixed) · Minor · components: streams, unit tests · created 2024-07-10 · resolved 2024-11-27

The `shouldThrowStreamsExceptionOnStartupIfExceptionOccurred` test expects `
globalStreamThread.start` throws `startupException` when startup fails. This may not be true in some slow machines. 
[code/log omitted]
Consider the following schedule:
[code/log omitted]
The function throws `IllegalStateException("Initialization for the global stream thread failed")` instead of `startupexception`

- **Ao Li:** This patch helps to reproduce the failure deterministically https://github.com/aoli-al/kafka/tree/KAFKA-276. The failing test: `GlobalStreamThreadTest::shouldThrowStreamsExceptionOnStartupIfExceptionOccurred`
- **Ao Li:** The CDL has fixed this concurrency issue.

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

## KAFKA-17215: Remove get-prefix for all getters
Improvement · Open · Minor · components: streams, streams-test-utils · labels: needs-kip · created 2024-07-29

Kafka traditionally does not use a `get` prefix for getter methods. However, for multiple public interfaces, we don't follow this common pattern, but actually have a get-prefix.
We might want to clean this up. The upcoming 4.0 release might be a good opportunity to deprecate existing methods and add them back with the "correct" name.
We should maybe also do multiple smaller KIPs instead of just one big KIP. We do know of the following
 * StreamsConfig (getMainConsumerConfigs, getRestoreConsum…

- **Ksolves India Limited:** [~mjsax] I would like to work on creating the necessary KIPs and work on this ticket. However, we need Confluence account which we requested earlier as well. Can you help us to provide the same?  Comment where I asked for access - https://issues.apache.org/jira/browse/INFRA-25451?focusedCommentId=1…
- **Matthias J. Sax:** I cannot help with creating a Confluence account, however, your account should have been created according to https://issues.apache.org/jira/browse/INFRA-25451?focusedCommentId=17867582&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-17867582 ? If your account was no…
- **Ksolves India Limited:** [~mjsax] For now, we didn't get Confluence access. We'll follow up there. In the meantime, we'll review the comments on attached PR & the POC one.

## KAFKA-17216: StreamsConfig STATE_DIR_CONFIG
Bug · Resolved (Invalid) · Major · components: streams · created 2024-07-30 · resolved 2024-08-25

I can't use the class StreamsConfig 
it fail with         Caused by: java.lang.ExceptionInInitializerError at StreamsConfig.java:866
problem is not present in 3.7.0

- **Chia-Ping Tsai:** [~raphaelauv] Could you share more details to us? for example, how to reproduce the error you described?
- **Matthias J. Sax:** The only PR which comes to mind with regard to state.dir is this one: [https://github.com/apache/kafka/commit/d233eb98f7c7e55fe0dd673dbc058ddf619663a7] – otherwise it should be the same between 3.7 and 3.8. As Chia-Ping said, can you provide more details (eg full stack trace, and also what value fo…
- **Matthias J. Sax:** Just saw this other comment: [https://github.com/apache/kafka/pull/13909#discussion_r1696207016] Reading between the lines, sounds like a version mix of older `kafka-clients.jar` and 3.8 `kafka-streams.jar`?
- **Matthias J. Sax:** Cf the reply on GitHub – caused by version miss-match.

## KAFKA-17217: Clients : Optimise batching of requests per node in ShareConsumeRequestManager
Sub-task · Resolved (Fixed) · Major · created 2024-07-30 · resolved 2024-08-09

In ShareConsumeRequestManager, currently every time we perform a commitSync or commitAsync, we create one ShareAcknowledge RPC for the same. Here, we can optimise the number of RPC calls by batching the acknowledgements before the next poll is invoked per node. 
This will ensure that between 2 calls, the acknowledgements are accumulated in one request per node and then sent during poll, resulting in lesser RPC calls.


## KAFKA-17218: kafka-consumer-groups fails to describe all group if one group has been consuming from a deleted topic
Bug · In Progress · Major · created 2024-07-30

`kafka-consumer-groups.sh --describe --all-groups` fails with `org.apache.kafka.common.errors.UnknownTopicOrPartitionException: This server does not host this topic-partition.` if single group has metadata for a topic that was recently deleted. 
As impact this prevent admin from viewing the group metadata for the whole cluster. 
Instead we should either 
- follow the same approach when we calculate the lag which print a place holder `-` when it is not applicable to calculate the metadata. 
-…

- **Dmitry Werner:** [~omnia_h_ibrahim] Hello, if you haven't started work yet, can I do?
- **Omnia Ibrahim:** [~javakillah] thanks for offering help but I am already working on this.

## KAFKA-17219: Adjust system test framework for new protocol consumer
Bug · Resolved (Fixed) · Blocker · components: clients, consumer, system tests · labels: kip-848-client-support, system-tests · created 2024-07-30 · resolved 2024-08-14

The current test framework doesn't work well with the existing tests using the new consumer protocol. There are two main issues I've seen.
First, we sometimes assume there is no rebalance triggered, for instance in {{consumer_test.py::test_consumer_failure}}
[code/log omitted]
The current frame work calculates {{num_rebalances}} by increment by one every time a new assignment is received, so if a reconciliation happened during the failover, {{num_rebalances}} will also be incremented. For new…

- **Kirk True:** Thanks for tracking this down, [~dongnuolyu]. What perplexes me is that we'd uncovered many similar issues in our initial migration of the system tests to support the new consumer. We'd found the same root issue before, namely that the new consumer takes some time to stabilize its groups. Our fix w…
- **Dongnuo Lyu:** ??it's really odd to me that we're still seeing these?? -Yeah at least in `consumer_test` the fix is missing. We can add them back when AK is unblocked.- Oh we do have {{wait_until}} fixes, it's just missing in {{test_consumer_bounce}} and {{test_broker_rolling_bounce}}. It should also fixes the p…
- **David Jacot:** Fixed by https://github.com/apache/kafka/pull/16845.

## KAFKA-17220: Define new metrics for MirrorMaker2
New Feature · In Progress · Major · components: mirrormaker · labels: needs-kip · created 2024-07-30

MirrorMaker2 provides some observability into it's operation, but lacks observability in the following areas:
 * Number of replicated topics/partitions
 * Number of consumer groups & consumer offsets
 * Background job success/failure/latency/duration
 * Checkpoint task startup time
 * Consumer group translation lag/expected redelivered data
 * Error metrics for failed offset translations
These concepts should be more clearly defined and included in a general observability KIP for MM2.

- **PoAn Yang:** Hi [~gharris1727], if you're not working on this, may I try it? I will do my best to create a draft KIP first. Thank you.
- **PoAn Yang:** KIP-1093: [https://cwiki.apache.org/confluence/display/KAFKA/KIP-1093%3A+Add+more+observability+for+MirrorMaker2]

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
- **PoAn Yang:** I create a draft PR to avoid modifying `runnable.pendingCalls.add(this);` to `runnable.newCalls.add(this);`. The step is like following: [https://github.com/apache/kafka/pull/16753]  # Use for-loop instead of iterator to check `pendingCalls`.  # Use a list `toRemove` to collect removed calls in `…

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

- **Bruno Cadonna:** [~rohitbobade] It is not clear to me what you tried to achieve by setting {{group.instance.id}}. Could yo please elaborate? Did you increase {{session.timeout.ms}} as described in the config definition (https://kafka.apache.org/documentation/#consumerconfigs_group.instance.id) Could you describe t…
- **Rohit Bobade:** [~cadonna]  we set the group instance id for sticky partition assignment. Initially the session timeout was set to 8 mins. After upgrading to 3.8.0 - we saw that the partitions were assigned only to a 2 pods out of 20. We have set the acceptable recovery lag as 0. My understanding is that the defau…
- **Rohit Bobade:** Acceptable recovery lag was set to 0 because of these 2 issues -  https://issues.apache.org/jira/browse/KAFKA-13269 https://issues.apache.org/jira/browse/KAFKA-14172 Is it safe to set the acceptable recovery lag to default?
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
- **PoAn Yang:** Hi [~kirktrue], here is related Jira and PR: * https://issues.apache.org/jira/browse/KAFKA-16764 * https://github.com/apache/kafka/pull/16043

## KAFKA-17582: Unpredictable consumer position after transaction abort
Bug · Open · Critical · components: clients, consumer, documentation · labels: abort, offset, transaction · created 2024-09-19

With the official Kafka Java client, version 3.8.0, the position of consumers after a transaction aborts appears unpredictable. Sometimes the consumer moves on, skipping over the records it polled in the aborted transaction. Sometimes it rewinds to read them again. Sometimes it rewinds *further* than the most recent transaction.
Since the goal of transactions is to enable "exactly-once semantics", it seems sensible that the consumer should rewind on abort, such that any subsequent transactions…

- **Kyle Kingsbury:** I've done some more digging here, and written a Jepsen test specifically for rewind-vs-advance behavior: [https://github.com/jepsen-io/redpanda/blob/main/src/jepsen/redpanda/workload/abort.clj]. Try something like: {{lein run test --db kafka -w abort --safe --concurrency 5n --sub-via assign --rate…
- **Justine Olshan:** Hi [Kyle Kingsbury|https://issues.apache.org/jira/secure/ViewProfile.jspa?name=aphyr]. Thanks for taking a look at transactions through Jepsen testing! I’m familiar with the framework and think it is super useful for testing distributed systems.  Can you clarify the test setup? It’s a little unclea…
- **Kyle Kingsbury:** Hi Justine! Thanks for your detailed answer. Yes, this behavior occurs with a transaction that reads from a single topic-partition and writes back to that same topic-partition. I'm not sure what happens when it reads from a different topic-partition than the one it's writing to–if the behavior woul…
- **Justine Olshan:** You are correct in that there isn't a great single source of truth. I've created https://issues.apache.org/jira/browse/KAFKA-17671 to improve the documentation. If there are any specific items/questions that should be included in the documentation, please comment on that ticket. (And to answer your…
- **Kyle Kingsbury:** Thanks Justine–I think having central docs will go a long way towards making transactions easier to understand. I'd also like to encourage the Kafka team to reconsider this behavior. People use Kafka transactions to get "exactly-once" semantics, and if they leave out this manual-rewind step, they'r…
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
- **Matthias J. Sax:** [~christo_lolov] – why is "affects version" set to 3.9.0 while fix version includes 3.8.1? "affects version" should be the earliest version which has this bug. It seem we should at least update it to 3.8.0, but I am wondering if we want to cherry-pick this for 3.7.2 release that we plan to do?
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

- **Greg Harris:** [~yitian998] Here's the error causing the shutdown:  [code/log omitted]
- **George Yang:** Thank you [~gharris1727]. The error indicates that the topic used for storing offset information (mm2-offsets.idcb.internal) does not have the correct cleanup policy. I'm not entirely sure if this theory is accurate, but it seems that Kafka MirrorMaker 2 requires the topic to have a cleanup.policy=…
- **Greg Harris:** > However, I have set the broker configuration log.cleanup.policy=delete. Will this conflict with the above topic-specific setting? The topic-specific setting will take precedence. > Additionally, is there another way to set cleanup.policy=compact without using the kafka-configs.sh command, such a…
- **George Yang:** > These topics, if created by MirrorMaker, should have the cleanup policy already set-up.  [~gharris1727] ,  To my surprise, the topic {{mm2-offsets.idcb.internal}} was supposed to be created automatically by MirrorMaker. The issue where the MirrorMaker pod went into a CrashLoopBackOff state occur…
- **Zhijian Chen:** In the MirrorMaker scenario, a MirrorMaker process runs multiple Herders, each handling different source cluster events. Now if one Herder has an exception, it will cause the MirrorMaker process to exit, causing other Herders that don't have problems to exit, affecting all of them, which I think is…

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
- **Colin McCabe:** Update: Kafka wants to divide up all listeners into either broker listeners or controller listeners. The sets are disjoint: a listener can't be both. BrokerServer will try to open the ports that belong to the broker; ControllerServer will try to open the ports that belong to the controller. You ob…

## KAFKA-17789: State updater stuck when starting with empty state folder
Bug · Resolved (Cannot Reproduce) · Critical · components: streams · created 2024-10-14 · resolved 2026-05-04

In an application with multiple clients, each having multiple threads, when the app is started with an empty storage (without resetting the whole application), only a part of the clients are restoring the changelog topics.
Those non-restoring clients are also not able to shutdown gracefully.
Reproduction steps
> I'm putting all the actual details, while I'm going to make a project to reproduce it locally, and I'll link it inside this ticket.
 * Having the app in a kubernetes environment, wit…

- **Lucas Brutschy:** [~chuckame] did you have time to provide a local reproduction environment for this? We haven't observed this behavior in our own tests. A reproduction would be extremely helpful. Thanks!
- **Nikita Shupletsov:** I wonder if it could be related to https://issues.apache.org/jira/browse/KAFKA-19831 or https://issues.apache.org/jira/browse/KAFKA-19960 or https://issues.apache.org/jira/browse/KAFKA-19994 or something similar where we didn't close some tasks correctly which left some stores not closed, hence the…
- **Guang Zhao:** I'm trying to reproduce the problem locally -- may I ask for more context in the original setting please -- - did the non-restoring clients eventually start restoring on their own (given enough time), or did they remain permanently stuck at zero restorations? - similarly, when trying to stop the s…
- **Matthias J. Sax:** [~chuckame] – can you help on this? Or maybe confirm that the issue was fixed already (eg, with 4.2.0 release)? If we cannot reproduce, we might just want to close the ticket for now, and "hope" that the other fixes do indeed cover it (and if not, well, we can always file a new ticket, or re-open t…
- **Nikita Shupletsov:** Hi [~chuckame]  I would like to ping you one more time. We haven't been able to reproduce the issue, so we would like to close the ticket.
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

- **Martin Sillence:** I feel there are a few options  * make the schema expicit  * an exclude list  * a limit on the number of digits The latter is the least intrusive but possibly the worst in terms of suprises but to quantifiy it: positive exponents: [code/log omitted] negative exponents: [code/log omitted] so…
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

- **Edoardo Comar:** on the topic with 5000 partitions the IncrementalAlterConfigRequest for {color:#00627a}modifyTopicThrottles {color}looks like : {{{color:#000000}AlterConfigOp{opType=SET, configEntry=ConfigEntry(name=leader.replication.throttled.replicas, {color}}} {{{color:#000000}value=0:0,0:1,0:2,1000:0,1000:1,…
- **Edoardo Comar:** https://github.com/apache/kafka/pull/17816
- **Edoardo Comar:** Withe the patched client, the Quorum controller may encounter a ConfigRecord that is too large : see https://issues.apache.org/jira/browse/KAFKA-18020

## KAFKA-17994: Checked exceptions are not handled when deserializing kafka stream record
Bug · Resolved (Fixed) · Blocker · components: streams · created 2024-11-12 · resolved 2024-11-15

When we got a PR to upgrade kafka clients 3.8.1 -> 3.9.0, we saw some failing tests. They were relating to using a DeserializationExceptionHandler with 'log and continue' strategy, however on newest version the stream was just crashing when Jackson was trying to deserialize a faulty json and this handler was not invoked.
In this [KIP-1033|https://cwiki.apache.org/confluence/display/KAFKA/KIP-1033%3A+Add+Kafka+Streams+exception+handler+for+exceptions+occurring+during+processing], specifically in…

- **Matthias J. Sax:** Thanks for filing this ticket. – Can you share your Json `Deserializer` code? What I don't understand right now is, how a checked exception could be thrown? The interface does not declare any exceptions, and thus only `RuntimeException` should be allowed: [https://github.com/apache/kafka/blob/trunk/…
- **Ilya:** Hi [~mjsax] . We use Kotlin and it doesnt have checked exceptions at compile time, so even deserializer like this would compile: [code/log omitted] And the error in runtime would be exactly that without wrapping: [code/log omitted] I suppose, its the same problem for Scala. And its also technica…
- **Matthias J. Sax:** Ah. Thanks for clarification. That's helpful. I agree that we should fix this... As it's a regression, I'll mark is as blocker for 3.9.1 and 4.0.0. Current work-around for 3.9.0 would be adding `try-catch` and re-throw as `RuntimeException`.
- **Chia-Ping Tsai:** trunk: https://github.com/apache/kafka/commit/f02c28b21dc4d89e1d7f2e16f8f9e067a9575e61 3.9: https://github.com/apache/kafka/commit/2127ae63290e1309e0d1ebbc84f6ef3a6f81bae2

## KAFKA-17995: Large value for `retention.ms` could prevent remote data cleanup in Tiered Storage
Bug · Resolved (Fixed) · Major · components: Tiered-Storage · labels: newbie · created 2024-11-12 · resolved 2024-11-14

If a user has configured value of "retention.ms" to a value > current unix timestamp epoch, then at this line of code [1] , cleanupUntilMs becomes negative. This is because cleanupUntilMs is calculated as (current unix epoch ms - retention.ms) [1]. 
This leads to cleaner failures at [https://github.com/apache/kafka/blob/5a5239770ff3565233e5cbecf11446e76339f8fe/core/src/main/java/kafka/log/remote/RemoteLogManager.java#L2218] and hence, all cleaning for that topic partition stops.
[1] [https://g…

- **PoAn Yang:** Hi [~divijv], if you're not working on this, may I take it? Thank you.
- **Divij Vaidya:** Hi [~yangpoan]  Sure. Please feel free to assign it to yourself.

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
- **Hyunsang Han:** I'm currently working on this issue. Would it be okay if I proceed to submit a PR? I'm new to contributing to Apache projects. :)
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

- **Chu Cheng Li:** Hi [~chia7712]  I think this has been finished, see below links: 1. [ClassicKafkaConsumer#acquire|https://github.com/peterxcli/kafka/blob/38aca3a045474a9e52ae25bde28d8a013b04f92b/clients/src/main/java/org/apache/kafka/clients/consumer/internals/ClassicKafkaConsumer.java#L1222-L1231] 2. [AsyncKafk…
- **Chia-Ping Tsai:** [~peterxcli] thanks for your inforamtion

## KAFKA-18066: Misleading/mismatched StreamThread id in logging
Bug · Resolved (Fixed) · Minor · components: streams · labels: newbie, newbie++ · created 2024-11-22 · resolved 2025-07-29

While debugging a test application I was confused to see a number of log lines where the StreamThread name appeared twice but had a different thread id/index in the same message. For example:
[code/log omitted]
Generally you would expect that the actual Logger prefix (the first thread name, in this case StreamThread-1) is the same as the LogContext prefix (the second thread name, ie the StreamThread-3 in this example). I dug into it and figured out that this happens for all of the messages log…

- **Chu Cheng Li:** Hi [~ableegoldman], may I take this ticket? Thanks!
- **A. Sophie Blee-Goldman:** [~peterxcli]  Go for it!
- **Chu Cheng Li:** Hi [~ableegoldman]  I’m working on this and would like to hear your thoughts.:D Currently, if we move the *creation* logic directly into the {{StreamThread}} constructor, it becomes harder to refactor tests that use mocks. For reference, see the [current test cases|https://github.com/peterxcli/kaf…
- **Uladzislau Blok:** Hey [~peterxcli], Are you still looking into that? If not I could pick this up
- **Chu Cheng Li:** Sure
- _…3 more comments_

## KAFKA-18067: Kafka Streams can leak Producer client under EOS
Bug · Resolved (Fixed) · Major · components: streams · labels: newbie, newbie++ · created 2024-11-22 · resolved 2025-04-03

Under certain conditions Kafka Streams can end up closing a producer client twice and creating a new one that then is never closed.
During a StreamThread's shutdown, the TaskManager is closed first, through which the thread's producer client is also closed. Later on we call #unsubscribe on the main consumer, which can result in the #onPartitionsLost callback being invoked and ultimately trying to reset/reinitialize the StreamsProducer if EOS is enabled. This in turn includes closing the current…

- **TengYao Chi:** Hi [~ableegoldman]  I would like to give it a try, may I have this issue ?
- **A. Sophie Blee-Goldman:** imo we should just add a "closed" flag to the StreamsProducer and skip the reset method entirely if its already been closed.
- **A. Sophie Blee-Goldman:** [~frankvicky] Go for it!
- **Bruno Cadonna:** We had to revert the fix for this bug (https://github.com/apache/kafka/pull/19078) because it introduces a blocking bug for AK 4.0.  The issue is that the fix prevented Kafka Streams from re-initializing its transactional producer under exactly-once semantics. That led to an infinite loop of {{Prod…
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
- **Rhishikesh Joshi:** Hi [~khoanetapp]  Thanks that would be very helpful. Unfortunately I don't have the expertise to take this one on anyway. But if you need any help or more information, I can definitely help you.
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
- **Tom Thornton:** The issue appears to be from errors.tolerance. We do not specify a config so it defaults to "none" [code/log omitted] However the connector is still skipping messages, as we see the Grafana metric  kafka_connect_task_error_metrics_total_records_skipped will start reporting skipped records when we…
- **Tom Thornton:** https://github.com/apache/kafka/pull/18146
- **Greg Harris:** Hmm, yeah this is a regression introduced by KAFKA-6738, added to 2.0.0. The PR and KIP say that it's backwards-compatible, but <2.0 RetriableExceptions caused tasks to fail, and >= 2.0 RetriableExceptions cause the record to be dropped. I think you can work-around this with a config: [https://kafk…
- **Tom Thornton:** [~gharris1727] Can we also backport to the other supported releases of 3.9, 3.8, and 3.7? I am happy to put out the PR to each respectively named branch.
- _…2 more comments_

## KAFKA-18074: Add kafka client compatibility matrix
Task · Resolved (Fixed) · Blocker · created 2024-11-23 · resolved 2025-03-12

in 4.0 we have many major breaking changes - JDK upgrade and protocol cleanup - that may confuse users in rolling upgrade and setup env. Hence, we should add a matrix for all our client modules - client, streams, and connect
the matrix consists of following item.
1. supported JDKs
2. supported broker versions

- **Ken Huang:** Hello, [~chia7712] , if you wont work on this, may I take the issue? Thank you.
- **Ken Huang:** JDK Compatibility Across Kafka Versions ||*Module*||*Kafka Version*||*Java 8*||*Java 11*||*Java 17*||*Java 23*|| |*Client*|4.0.0|❌|✅|✅|✅| |*Streams*|4.0.0|❌|✅|✅|✅| |*Connect*|4.0.0|❌|❌|✅|✅| |*Server*|4.0.0|❌|❌|✅|✅| Server Compatibility ||*KRaft Cluster Version*||*Compatibility 4.0 Server (dyn…
- **Ismael Juma:** I made this a top level issue instead of a sub-task of KAFKA-14560 because it's broader than KAFKA-14560.
- **ASF GitHub Bot:** m1a2st opened a new pull request, #669: URL: https://github.com/apache/kafka-site/pull/669    After merge https://github.com/apache/kafka/pull/18091, we need to add footer for `compatibility-summary`
- **ASF GitHub Bot:** frankvicky commented on PR #669: URL: https://github.com/apache/kafka-site/pull/669#issuecomment-2716382989    before:    ![image](https://github.com/user-attachments/assets/5961bf47-3e0d-4b38-b596-dd1b05e0ed77)    after:    ![image](https://github.com/user-attachments/assets/1224757b-78a2-4029-a…
- _…1 more comments_

## KAFKA-18264: Remove NotLeaderForPartitionException
Improvement · Resolved (Fixed) · Minor · created 2024-12-16 · resolved 2024-12-18

It is deprecated by KAFKA-10223 (4 years ago)

- **Nick Guo:** Hi [~chia7712] ,if you are not working on this,may I take over this?
- **Chia-Ping Tsai:** trunk: [https://github.com/apache/kafka/commit/21b7bb2265951d55efb8c0cb93340b664a5783a6] 4.0: https://github.com/apache/kafka/commit/5a6e1204dd533af9f6f8072fe80330c5ea9f6fa7

## KAFKA-18265: Optimizing SharePartition locking to improve fetch speed
Sub-task · Resolved (Fixed) · Major · created 2024-12-16 · resolved 2025-11-18


## KAFKA-18266: Re-order validation for TimeIndex sanity check
Improvement · Resolved (Not A Problem) · Minor · labels: newbie · created 2024-12-16 · resolved 2025-01-20

Currently, when validating the sanity of TimeIndex, we perform multiple validations. With this change, we want to re-order the validations such that the expensive ones are performed at the end. 
i.e., we want to do [https://github.com/apache/kafka/blob/9cc1547672a8b261c08f453f45277265dfb44808/storage/src/main/java/org/apache/kafka/storage/internals/log/TimeIndex.java#L79] after [https://github.com/apache/kafka/blob/9cc1547672a8b261c08f453f45277265dfb44808/storage/src/main/java/org/apache/kafka/…

- **Pramithas Dhakal:** Hi [~jaytee] , if you're not working on this, may I take it? Thank you.
- **Jason Taylor:** Sure [~pramithas] i'll reassign it to you as I still have other open PR's i need to prioritise. Weirdly it won't let me assign it to you. [~divijvaidya] can u reassign please?

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
- **Chia-Ping Tsai:** trunk: https://github.com/apache/kafka/commit/a52aedd6ff9ade0230c0f41b473e8fbdfa2e0345 4.0: https://github.com/apache/kafka/commit/efdfa0184259a41e0c22359df36a169c8d97214d

## KAFKA-18389: Do not lose votedKey on transition to LeaderState
Improvement · Patch Available · Minor · components: kraft · created 2025-01-02

After KAFKA-17642 is merged in, all epoch state transitions (other than the transition to Leader) will preserve votedKey and leaderId state. We should make the transition to LeaderState consistent with this.

- **Yunseop Eom:** Hi, I opened a PR for this issue: https://github.com/apache/kafka/pull/22203 The patch preserves the candidate `votedKey` when transitioning to `LeaderState`. Previously, `LeaderState.election()` returned an elected-leader state with an empty `votedKey`, so the candidate's self-vote could be drop…
- **Yunseop Eom:** Follow-up on PR #22203: https://github.com/apache/kafka/pull/22203 The latest commit, da42f3920a, removes the stale unrelated transition comment requested in review. The branch also contains the votedKey toString assertion, focused candidate-to-leader regression coverage, and concise LeaderState Ja…
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
- **TengYao Chi:** Hi [~dajac]  In short, this is not a must-do item for version 4.0, as `log4j-1.2-api` already provides log4j1 compatibility mode for log4j2. The reason why this issue hasn't been addressed yet: In log4j1, we used properties files as the configuration format, which has a flat structure where new c…
- **Chia-Ping Tsai:** [~frankvicky] I think this is a blocker issue as by default we mount the log4j2 yaml - and users will expect those envs should work as before.
- **TengYao Chi:** I will try to get this done before next week.

## KAFKA-18397: Fix the scenario where acknowledgement callback is being called on null acknowledgements
Sub-task · Resolved (Fixed) · Major · created 2025-01-03 · resolved 2025-01-08

- **Shivsundar R:** [~peterxcli] , I have a fix for this, can I take this ticket up?
- **Chu Cheng Li:** Sure, thanks!

## KAFKA-18398: Log a warning if actual topic configs are inconsistent with the required topic configs
Task · Open · Major · components: streams · labels: kip1071 · created 2025-01-03

- **Matthias J. Sax:** I think we need to be careful with this ticket – cf the one I just linked. In general, we should really define what it absolutely necessary to check, and limit to these cases. Kafka Streams as always benefited to have good defaults, but not enforce them and give advanced users ways to change stuff.…
- **Lucas Brutschy:** It seems to me the linked ticket is all the more a reason to log a warning, right? If a certain internal topic is configured incorrectly because the topology was evolved, the user may want to fix that. [~mjsax] Do you suggest to not log a warning at all? Or do you think there is a subset of configs…
- **Matthias J. Sax:** I think there is two things:  * Is there any actually _invalid_ configs, which we should disallow? For this case, we should maybe log a WARN (or even fail)?  * If there is diff between code and configs, but it's a totally valid config, we should not log but just apply the config to the topic, and…
- **Lucas Brutschy:** Yes, we could make this slightly less annoying by distinguishing the invalid configs from non-default configs. Maybe it would still be good to output an "INFO" log for the non-default ones, as people may want to know about it. It also seems to be a "good" log message. It's perfectly clear and would…

## KAFKA-18595: Remove AuthorizerUtils#sessionToRequestContext
Sub-task · Resolved (Fixed) · Major · created 2025-01-19 · resolved 2025-01-22

This methods is unused since we are removing zk.

- **Christo Lolov:** The PR has been reviewed and merged both in trunk and 4.0

## KAFKA-18596: Cleanup LogConfig
Improvement · Closed (Fixed) · Major · created 2025-01-19 · resolved 2025-01-19

- **TengYao Chi:** I think this is a duplicate with 18544 https://issues.apache.org/jira/browse/KAFKA-18544 You can open a PR and link the old issue.

## KAFKA-18597: max-buffer-utilization-percent is always 0
Bug · Resolved (Fixed) · Minor · created 2025-01-19 · resolved 2025-01-27

see [https://github.com/apache/kafka/blob/516d5240b98916feb3e51c8a143dede05a4edad1/core/src/main/scala/kafka/log/LogCleaner.scala#L127]
  private def maxOverCleanerThreads(f: CleanerThread => Double): Int =
    cleaners.foldLeft(0.0d)((max: Double, thread: CleanerThread) => math.max(max, f(thread))).toInt
  /* a metric to track the maximum utilization of any thread's buffer in the last cleaning */
  metricsGroup.newGauge(MaxBufferUtilizationPercentMetricName,
    () => maxOverCleanerThreads…

- **Chia-Ping Tsai:** trunk: https://github.com/apache/kafka/commit/356f0d815cf99668e5acea427004bf01d8068439
- **Chia-Ping Tsai:** 3.9: [https://github.com/apache/kafka/commit/85658e5e33f550c6953ae58e37cc1808fd56b879] 3.8: https://github.com/apache/kafka/commit/5ea660bf940a3d26cbcad414c2e523871543b94d

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
- **Aldan Brito:** hi [~yangpoan] , yes you can
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
- **Luke Chen:** [~yangpoan] , I shutdown the client only because IIRC, if I shutdown the node, it won't get ` NOT_LEADER_OR_FOLLOWER` error and retry. Is that what you saw?
- **PoAn Yang:** > Is that what you saw? No, I can run the test without error.
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
- **Chia-Ping Tsai:** trunk: https://github.com/apache/kafka/commit/1132f08c57d46e80bc502965aa6d6330f85857bc 4.0: https://github.com/apache/kafka/commit/546d9ce39bde54a393573a62babe3b0217b49052

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

- **TengYao Chi:** Hi [~showuon]  I'd like to take over this one. Do you think this needs a KIP?
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

- **Yunseop Eom:** Update on PR #22946: https://github.com/apache/kafka/pull/22946 The PR adds schema-evolution coverage with distinct parent and child specifications, exercises common-struct evolution through MetadataSchemaCheckerTool, and verifies that a field present in both message versions but missing from the c…
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

- **Yunseop Eom:** Update on PR #22948: https://github.com/apache/kafka/pull/22948 The PR enables Gradle Module Metadata publication for kafka-clients so Gradle consumers can resolve published variants and capabilities. Validation completed: - :clients:generateMetadataFileForMavenJavaPublication - :clients:check e…
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

- **Kamal Chandraprakash:** [~yangpoan]  Are you working on this issue? Thanks!
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

- **Chia-Ping Tsai:** # rename KRaftConfigs to KRaftConfig  # move related getters from KafkaConfig to KRaftConfig  # move variables from MetadataLogConfig to KRaftConfig  # remove MetadataLogConfig
- **Ismael Juma:** Hmm, there are two separate things:  # Server configs related to kraft (things like process.roles)  # Metadata related configs I don't think these should be the same. `1` should to be in `server` while `2` should be in `metadata`.
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

- **Shivsundar R:** After this PR went in to AK - [https://github.com/apache/kafka/pull/19781,] we stopped seeing the error logs related to state epoch, and the test has had clean runs for the past 7 days. Develocity link - [https://develocity.apache.org/scans/tests?search.tags=trunk&search.timeZoneId=Asia%2FCalcutta&…

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

- **Chia-Ping Tsai:** related code: https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/common/requests/ListOffsetsRequest.java#L69 https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/common/requests/ListOffsetsRequest.java#L84
- **Ismael Juma:** We should replace the hardcoded value with `ApiKeys.LIST_OFFSETS.oldestVersion()`.
- **Chia-Ping Tsai:** {quote} We should replace the hardcoded value with `ApiKeys.LIST_OFFSETS.oldestVersion()`. {quote} good idea!

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

- **sanghyeok An:** Hi, [~squah-confluent] . If you are not working in this task, May I take a look?
- **Sean Quah:** Hi, [~chickenchickenlove]. Sure, please feel free to reassign the task to yourself. I'm not currently working on it.
- **sanghyeok An:** [~squah-confluent] Thanks a lot!  Self assigned!
- **sanghyeok An:** Hi [~squah-confluent] ! During my investigation of both __consumer_offsets and  {{__transaction_state}} alongside this work,  I realized that this issue extends to all internal topics.  Also, the documentation explicitly discourages modifying the partition count for internal topics post-deploymen…

## KAFKA-19425: local segment on disk never deleted forever when remote storage initial failed
Bug · Resolved (Fixed) · Critical · components: Tiered-Storage · created 2025-06-21 · resolved 2025-07-28

remote storage initial failed is silence so that the disk keep increasing forever.
[stop the server when fail to initialize to avoid local segment never got deleted. by jiafu1115 · Pull Request #20007 · apache/kafka|https://github.com/apache/kafka/pull/20007]

- **fujian:** [~yangpoan] hi. can you help to take I look? thanks!   I see you are the only person which is active on this module:)
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

- **RivenSun:** [~guozhang] [~dajac]  Could you please help me look into this issue?  Thank you very much!
- **Sean Quah:** [~RivenSun] to help diagnose the issue, could you attach the broker logs and the output of {{{}kafka-topics --describe --topic __consumer_offsets{}}}?
- **RivenSun:** The above document has posted the client log and coordinator broker log when the problem occurs. The coordinator broker log is posted here in text form. We can see that two OOM exceptions occurred: [code/log omitted] Today I used rivenTest6 to start the consumer again and found that this group ca…
- **RivenSun:** Add additional information. When the consumer is not started, the broker's log is normal. There are only two topics in the cluster, details of the test topic. !image-2025-06-24-10-50-17-396.png!
- **David Jacot:** [~RivenSun] Thanks for the Jira. Could you please share a heap dump of the broker when the issue happens? It would help to diagnose what consumes a lot of memory. For the context, the byte buffers that you highlighted in the description are indeed kept by the group coordinator. It has one per __cons…
- _…29 more comments_

## KAFKA-19428: IOException during writing max timestamp should not be ignored
Bug · Resolved (Not A Problem) · Minor · created 2025-06-23 · resolved 2025-06-25

this is similar to KAFKA-19221. The IOException caused by writing max timestamp is currently ignored.
[code/log omitted]
That could be an issue since we assume the last entry is the max timestamp after restarting. If the write fails, the loading log should re-build the index to ensure it catches the "correct" max timestamp.

- **Gaurav Narula:** -Mind if I take this one as well [~chia7712] ?:)- Edit: nvm, I see Lan is already working on it. Happy to help with the review.
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
- **Matthias J. Sax:** Well, that's all up for discussion I guess :) – And there is multiple issue we need to consider.  # The idea to maybe reuse `DeserializationExceptionHandler` was, to avoid having too many callback interfaces, and to keep the API surface area small. Even if this error is not really about deserializa…
- **Uladzislau Blok:** I'm not fully sure for now what would be the best way to handle the error. About CONTINUE case: exception is threw by Kafka consumer when we're trying read butch of messages, not sure how we can skip only one message, if we don't know which one from the butch is corrupted. From my perspective, we…
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

- **Jimmy Wang:** Hi [~cmccabe] , I think I could help with this issue :)
- **Jimmy Wang:** Hi [~cmccabe] , sorry for the late response. I'm a bit confused because currently, for the broker, both the periodic resend timeout and the RPC timeout are set to {{{}broker.heartbeat.interval.ms{}}}. I wonder if I've missed something or if I didn't understand your point correctly. Could you help to…

## KAFKA-19434: Move logic for state store initiation to StreamThread handover
Task · Resolved (Fixed) · Blocker · components: streams · created 2025-06-24 · resolved 2026-02-20

When starting a Kafka Streams instance, if it has pre-existing state, the state stores are initialized on the main thread. Part of this
initialization registers the stateful metrics with the JMX thread-id tag of {{{}main{}}}. This breaks the KIP-1076 implementation where need to
register metrics with thread-id tags of {{{}xxxStreamThread-N{}}}. This is necessary due to the fact that the {{StreamsMetric}} is a singleton shared
by all {{StreamThread}} instances, so we need to make sure only add…

- **Eduwer Camacaro:** Hi, I opened this PR that proposes an alternative solution to this issue [https://github.com/apache/kafka/pull/20749]. Let me know what you think about this approach that basically proposes some changes in the StateStores lifecycle, but this will require modifications in KIP-1035.
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
- **Andrew Schofield:** [https://cwiki.apache.org/confluence/display/KAFKA/KIP-1191%3A+Dead-letter+queues+for+share+groups] [~isding_l] I was thinking of using this Jira for the KIP, as opposed to creating a new one. wdyt?
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
- **Lan Ding:** During the process of fixing this issue, I seem to have discovered another issue. When parseRecord fails and throws a {{{}SerializationException{}}}, the following code executes: [code/log omitted] In the outer code, the exception is not caught and is directly thrown: [code/log omitted] This ult…
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

- **Rajani Karuturi:** created a PR https://github.com/apache/kafka/pull/20125 for the fix  Also added a test to test a scenario where HWM is changed

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
- **Stig Rohde Døssing:** I've raised https://github.com/apache/kafka/pull/20333 to fix this. [~gongxuanzhang] Sorry, I didn't notice your comment until now, I didn't mean to steal this issue, it just kind of happened since I did the previous spotbugs-related work too. Feel free to let me know if you have a better fix than…

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

- **Stanislav Kozlovski:** [~gnarula] are you planning to work on this, or should we keep it unassigned? I'm hitting this same issue fwiw
- **Gaurav Narula:** Hi [~stanislavkozlovski]! I'm picking this up now. I suspect the issue is because some classes are missing from native image reachability metadata. Will update this ticket as I dig more

## KAFKA-19585: Avoid noisy NPE logs when closing consumer after constructor failures
Bug · Resolved (Fixed) · Minor · components: clients, consumer · created 2025-08-07 · resolved 2025-09-08

If there's a failure in the kafka consumer constructor, we attempt to close it https://github.com/lianetm/kafka/blob/2329def2ff9ca4f7b9426af159b6fa19a839dc4d/clients/src/main/java/org/apache/kafka/clients/consumer/internals/AsyncKafkaConsumer.java#L540
In that case, it could be the case that some components may have not been created, so we should consider some null checks to avoid noisy logs about NPE. 
This noisy logs have been reported with the console share consumer in a similar scenario, s…

- **Francis Godinho:** Hi [~lianetm], I'm new to contributing to Kafka and would be happy to take a stab at this. Can I assign this ticket to myself?
- **Lianet Magrans:** Hi [~francisgodinho]! Thanks for your interest! There is already someone from the team working on this :S  But stay on the lookout for new issue that we create, and also maybe check what's already out with minor/trivial complexity (ex. [this filter|https://issues.apache.org/jira/browse/KAFKA-15642?…

## KAFKA-19586: Kafka broker freezes and gets fenced during rolling restart with KRaft mode
Bug · Open · Blocker · components: core · created 2025-08-07

After upgrading our Kafka clusters to *Kafka 3.9.0* with *KRaft mode enabled* in production, we started observing strange behavior during rolling restarts of broker nodes — behavior we had never seen before.
When a broker is {*}gracefully shut down by the KRaft controller{*}, it immediately restarts. Shortly afterward, while it is busy {*}replicating missing data{*}, the broker suddenly {*}freezes for approximately 20–50 seconds{*}. During this time, it produces {*}no logs, no metrics{*}, and *…

- **Tal Asulin:** Sharing a 5m Flame graph profiling snapshot that was taken after a broker restart that experienced this exact issue - [^flame3.html]. The Kafka cluster spec during the simulation was:  * 12 Broker nodes  * Using 8 vCPUs, 32G of RAM & 3.7TB local volume (im4gn.2xlarge AWS instances)  * Disk utili…

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
- **Chia-Ping Tsai:** If all we want is to list the RPC versions of the "voters", this can be done with `DescribeQuorumRequest`. That means we don't need a KIP to support `bootstrap.controller`. By contrast, we would need a KIP if we wanted to list all the RPCs of "observers" [~taijuwu] [~schofielaj] WDYT?
- **TaiJuWu:** If we don't need all controllers including observers, that is good enough. But there is another benefit if we have KIP is we can align the tool usage like [https://cwiki.apache.org/confluence/display/KAFKA/KIP-1147%3A+Improve+consistency+of+command-line+arguments]
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

- **Dejan Stojadinović:** Update: *Mockito* version needs to be upgraded to resolve build issues (see the output of *_./gradlew test_* below). *Related links:*  * https://issues.apache.org/jira/browse/SOLR-17718  * [https://github.com/mockito/mockito/issues/3647]  * [https://github.com/mockito/mockito/releases/tag/v5.20.…
- **Dejan Stojadinović:** *Small update:*  * Gradle version upgrade (8.14.3 -->> 9.1.0) will hopefully end up in trunk in the next few days  * It seems that Apache *{{commons-bcel}}* will release Java 25 compatible version soon enough - this is important for us because SpotBugs Java 25 compatible versions will follow immed…
- **Dejan Stojadinović:** *Update:* * A few of the tests are failing with Java 25 (x) * ticket is created here: KAFKA-19769 (i)
- **Dejan Stojadinović:** Solution has been merged into a trunk: [https://github.com/apache/kafka/commit/ede6c90dfb5fa5faa7472541dde3bcc90cbd68d3] :D Follow-up ticket is created here: KAFKA-19771

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

- **Shashank:** Hi [~lucasbru], since the tests in the cleanup of this file are many, I would like to propose to make incremental changes to this cleanup. - Removal of dead tests and address these 3 comments - [#1|https://github.com/apache/kafka/pull/19275#discussion_r2107811068], [#2|https://github.com/apache/kaf…
- **sanghyeok An:** I think, after this tickets are resolved, https://issues.apache.org/jira/browse/KAFKA-12569 can be resolved as well.
- **Shashank:** You're right! Thank you [~chickenchickenlove]

## KAFKA-19684: Move Gauge#value to MetricValueProvider
Improvement · Resolved (Fixed) · Minor · labels: need-kip · created 2025-09-07 · resolved 2025-10-04

from: https://github.com/apache/kafka/pull/3705#discussion_r140830112

- **Chia-Ping Tsai:** the main benefit is to remove the type check from `KafkaMetric` [code/log omitted] [code/log omitted] Also, the following code could be removed [code/log omitted]
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

- **Chia-Ping Tsai:** 3.9: https://github.com/apache/kafka/commit/4dd35126656e2af2ff3cd67705d1dd495f68c0ec trunk: https://github.com/apache/kafka/commit/0a483618b9cc169a0f923478812141630baf2a4c
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
- **Kuan Po Tseng:** Hi [~lianetm], I took a closer look at this issue and wanted to share a few thoughts. {quote}That 0 ms initial interval causes the HB manager poll to run continuously in a tight loop, executing logic that may not really be needed—it mostly just waits for a response or failure. {quote} This actua…
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

- **Greg F:** Most of the time I run the test, I see this: [INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.880 s – in com.k8sflowprocessor.ChainedEmitStrategyTopologyTest3 [INFO]  [INFO] Results: [INFO]  [INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0 [INFO]  However, like…
- **Greg F:** the goal, of course, is to have unit test that is reliable, i.e. doesn't fail intermittently. I need to understand whether the issue is in my test code (attached) or elsewhere in kafka test framework.
- **Greg F:** I run the test in a loop in a shell script like this: #!/bin/bash set -e for i in \{1..100}; do   echo ========================================================   echo ======================== $i ============================   echo ========================================================   mvn…
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
- **Nikita Shupletsov:** Hi [~goyarpit]  I am already working on it. I will let you know if I need help. thanks!

## KAFKA-19936: ReplicaManager counts duplicated records to BytesInPerSec and MessagesInPerSec metric
Bug · In Progress · Major · created 2025-11-28

For an idempotent producer, duplicated records are not written to disk; however, they still contribute to the {{BytesInPerSec}} and {{MessagesInPerSec}} metrics.
1. If the records are duplicated, UnifiedLog skips these messages.
[https://github.com/apache/kafka/blob/d27d90ccb3b2b98e02de42afd50910fbbbc162d0/storage/src/main/java/org/apache/kafka/storage/internals/log/UnifiedLog.java#L1221-L1234]
2. ReplicaManager counts result from Partition#appendRecordsToLeader to metrics.
[https://github.c…

- **PoAn Yang:** This test case cannot pass in trunk branch, because ReplicaManager counts duplicated records to metrics. [code/log omitted]
- **Luke Chen:** Question: Does the MessagesInPerSec and BytesInPerSec count for the corrupted records?
- **PoAn Yang:** For corrupted records, do you mean records which cannot pass validator and throw CorruptRecordException? These records doesn't contribute to metrics and will get into this catch. [https://github.com/apache/kafka/blob/d27d90ccb3b2b98e02de42afd50910fbbbc162d0/core/src/main/scala/kafka/server/ReplicaM…
- **Luke Chen:** OK, thanks. I just want to confirm the definition of these 2 metrics. Does it mean "the data enter the broker" or "the data enter the disk"? It looks like we only count it when data enter the disk. So this issue is valid. Thank you.

## KAFKA-19937: Use the same reaper thread in Persister as well as NetworkPartitionMetadataClient
Sub-task · Resolved (Fixed) · Major · created 2025-11-28 · resolved 2026-04-28

- **Rion Williams:** I'm happy to take this task if available.  I'd imagine we'd want to simply create a new sharable, standalone `ReaperThread` class that could easily be shared between both of these components. We could also allow the existing `SystemTimerReaper` class to accept and optionally own/manage the thread i…
- **Andrew Schofield:** [~rionmonster] Are you still interested in taking this task?
- **Rion Williams:** [~schofielaj] Sure! I think I have a branch stashed away somewhere where I was experimenting with one of the approaches above. Feel free to assign it to me and I’ll revisit it.
- **Andrew Schofield:** Thank you.
- **Rion Williams:** [~schofielaj]  I've gone ahead and [put together a PR|https://github.com/apache/kafka/pull/21842] that takes the approach detailed earlier in the thread (e.g. extracted previously nested ReaperThread into its own class and extended an instance to be passed into SystemTimerReaper to support sharing)…

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

- **Chia-Ping Tsai:** trunk: https://github.com/apache/kafka/commit/a2eae88a2293ad18e902dcc0abb3bb30b16272b9 4.2: https://github.com/apache/kafka/commit/7ae882623a0b006c99e58c756f7cddbc5a89ff49

## KAFKA-19941: Tidy up the output of `kafka-features.sh`
Improvement · Resolved (Fixed) · Minor · created 2025-11-29 · resolved 2025-12-08

Feature: eligible.leader.replicas.version	SupportedMinVersion: 0	SupportedMaxVersion: 1	FinalizedVersionLevel: 0	Epoch: 408
Feature: group.version	SupportedMinVersion: 0	SupportedMaxVersion: 1	FinalizedVersionLevel: 0	Epoch: 408
Feature: kraft.version	SupportedMinVersion: 0	SupportedMaxVersion: 1	FinalizedVersionLevel: 1	Epoch: 408
Feature: metadata.version	SupportedMinVersion: 3.3-IV3	SupportedMaxVersion: 4.3-IV0	FinalizedVersionLevel: 3.9-IV0	Epoch: 408
Feature: share.version	SupportedMinV…

- **Rion Williams:** I'd be interested in taking this if we elect to make a change. I'm not certain if more tabs would be the answer in terms of improving readability. A few options that come to mind off the top of my head would be: *Indentation Approach* [code/log omitted] *Table Approach* [code/log omitted] The p…
- **Chia-Ping Tsai:** [~rionmonster] Thanks for the feedback. I think a new configuration is overkill and it requires a KIP. I don't recall us having a specific rule for compatibility of console output. Let's start a thread on the dev channel for further feedback
- **Chia-Ping Tsai:** discussion: https://lists.apache.org/thread/jwcn88o4f4c19x1onymxmkddk3dcsckf
- **Rion Williams:** [~chia7712]  Totally makes sense!
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
- **Matthias J. Sax:** If you are using a KV-store, there should not be any retention time, but the changelog topic should be configured with compaction, which ensures that no matter how old a record gets, it's not deleted as long as it's the newest for a key. Kafka Streams should create the topic for you with the right…
- **Uladzislau Blok:** I'm talking about {*}_delete.retention.ms_{*}, so retention time of *tombstones* We have compacted chanelog topic created by KS with default *_delete.retention.ms_* (1 day). The issue is *not that we lost live entities, but removed entities become available* after fail-over to second k8s cluster. T…
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

- **Yunseop Eom:** PR opened: https://github.com/apache/kafka/pull/23024 Prevented premature ISR expansion under min ISR by requiring the follower to satisfy the existing caught-up check, while preserving leader-epoch expansion when the partition is not under min ISR. Added regression coverage for a follower that rea…
- **Yunseop Eom:** Update on PR #23024: https://github.com/apache/kafka/pull/23024 The PR requires the existing caught-up check before expanding ISR while a partition is under min ISR, preventing a follower with only a stale high watermark from entering ISR prematurely. The non-min-ISR leader-epoch behavior is preser…
- **Yunseop Eom:** PR #23024 is open and ready for maintainer review: https://github.com/apache/kafka/pull/23024

## KAFKA-19997: Improve handling and visibility of invalid dynamic configurations
Improvement · Open · Major · labels: need-kip · created 2025-12-16

from: https://github.com/apache/kafka/pull/20334#discussion_r2621722784
Warning messages for invalid dynamic configurations are easily overlooked and difficult to monitor. Therefore, I propose two improvements: 
1) introduce a new configuration, "dynamic.config.failure.policy ", to allow users to halt the server upon validation failure if desired 
2) add a new metric, `InvalidConfigCount`, to expose the invalid configurations via JMX

- **Jimmy Wang:** Hi [~chia7712] , I noticed this issue might need a KIP, and I think I can help with this, thanks!
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
- **Justine Olshan:** > In Transaction V2, brokers enforce strict epoch monotonicity for control batches (markers), requiring marker_epoch > current_epoch. Consequently, the broker rejects the recovery marker with InvalidProducerEpochException. This is not true for 4.0 and 4.1 right? This change was introduced in 4.2? h…
- **Justine Olshan:** But I think your idea makes sense. I'm wondering if there is a clearer way to indicate this for an idempotent retry.
- **Justine Olshan:** I think it would be preferable to check the idempotency on the log side. Ie, if we get a tv2 marker with the same epoch + we haven't opened a new transaction, we can just not return any error.
- _…6 more comments_

## KAFKA-20000: Optimize retry backoff for CONCURRENT_TRANSACTIONS to improve TV2 throughput
Improvement · In Progress · Major · created 2025-12-16

Transaction V2 introduces frequent state transitions (epoch bumps) that briefly reject concurrent requests with CONCURRENT_TRANSACTIONS. The default client retry backoff (100ms) is excessive for these transient locks, leading to unnecessary latency and degraded throughput. Reducing the backoff allows faster retries and smoother performance during state transitions.

- **Chia-Ping Tsai:** The simple improvement is to modify TxnOffsetCommitHandler in TransactionManager.java. When receiving CONCURRENT_TRANSACTIONS, override the default retryBackoffMs with a smaller fixed value (e.g., 20ms) to expedite retries, similar to the existing logic in AddPartitionsToTxnHandler
- **Chia-Ping Tsai:** ping [~jolshan]
- **Justine Olshan:** Hey, I think this backoff is somewhat dependent on the system right? Depending on how quickly inter-broker requests occur 20ms could be too frequent as well right? For AddPartitionsToTxnHandler we had a config. Is this not working correctly for offset commits? From KIP-890: > Feb 2025. Adding addi…
- **Chia-Ping Tsai:** {quote} AddPartitionsToTxnHandler we had a config. Is this not working correctly for offset commits? {quote} Configs like `add.partitions.to.txn.retry.backoff.max.ms` and `add.partitions.to.txn.retry.backoff.ms` apply specifically to the produce path (KafkaApis#handleProduceRequest -> ReplicaMana…
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
- **Lianet Magrans:** All merged into 4.3 (first PR made it before the branch cut, second PR cherry-picked [https://github.com/apache/kafka/commit/aa736157d18ec470c0b97e8dddb3eda80e6fb150] )

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

- **Dejan Stojadinović:** Ok, I have to reply to my self - and it will be quite funny, so to say :) This issue was actually resolved by [~chia7712] and me :D here: https://github.com/apache/kafka/pull/20683 This was a false alarm; closing as _*Not a problem*_

## KAFKA-20109: Complete Kafka cluster dies on incorrect SSL config of a single controller
Bug · In Progress · Major · components: config, controller · created 2026-02-02

Hello,
we've recently run into a bug in Apache Kafka in Kraft mode where a whole mtls-enabled cluster (controllers + brokers) die if a single controller is (re)started with bad ssl principal mapping rules.
The bad config of course was appllied unintentionally when doing some changes in the config management of the system, basically it led to {{ssl.principal.mapping.rules}} missing for the controller listener on that one node. As soon as this single controller was restarted, the whole cluster d…

- **Gergely Harmadás:** Hi [~svdewitmam], I have started looking at the issue, feel free to assign it to me.
- **Sven Dewit:** [~harmadasg] sorry i'm not able to do that.
- **Gergely Harmadás:** Hi [~svdewitmam], here is my analysis: Before going into the details note that  * misconfigured {{ssl.principal.mapping.rules}} config means that a given broker/controller is not able to properly extract the principal names of the other brokers/controllers from the incoming requests  * since not…
- **Sven Dewit:** [~harmadasg] thanks for your analysis. My guess so far was that the issue lies within the "asymmetrical" nature of the outcome of the misconfigured controller: while the controller cannot authorize incoming connections from other nodes, the other nodes will happily accept connections from the miscon…
- **Gergely Harmadás:** [~svdewitmam] {quote}while the controller cannot authorize incoming connections from other nodes, the other nodes will happily accept connections from the misconfigured controller {quote} That is correct as the principal mapping works as expected on the other nodes. I have also tested with 4.2 a…
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

- **Chia-Ping Tsai:** trunk: [https://github.com/apache/kafka/commit/5acd1ffe2071ce575af6695547ec8e0ee951e33c] 4.2: https://github.com/apache/kafka/commit/9f8bd7394dd82bbc54ff472a9ad49f22e9f0a517 4.1: https://github.com/apache/kafka/commit/9d24eec731d9ffb62fddc3a7869c87d51196a7e0

## KAFKA-20112: Flaky testAsyncConsumerMaxPollIntervalMsDelayInRevocation
Test · Resolved (Fixed) · Major · components: clients, consumer · created 2026-02-02 · resolved 2026-03-13

Has been flaky on trunk 
https://develocity.apache.org/scans/tests?search.relativeStartTime=P28D&search.rootProjectNames=kafka&search.tags=trunk&search.timeZoneId=America%2FToronto&tests.container=org.apache.kafka.clients.consumer.PlaintextConsumerPollTest&tests.sortField=FLAKY&tests.test=testAsyncConsumerMaxPollIntervalMsDelayInRevocation()%5B1%5D

- **Lianet Magrans:** Haven't had the time to look into this in detail, but seems the failure comes from a timeout when closing the consumer implicitly with the try (not from the core logic being tested, which is the revocation callback on a rebalance). It will probably be helpful to try to repro with logging enabled for…

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

- **sanghyeok An:** {quote}Pack {{backoffDeadlineMs}} and {{requestInFlight}} into the same atomic, by creating a record class to hold them. {quote} Hi, [~squah-confluent]!  I'll go with that option and create a PR!
- **Sean Quah:** Thanks, looking forward to your PR!

## KAFKA-20144: Authority for LIST_CONFIG_RESOURCES should be dependent upon resource type
Improvement · Open · Major · labels: need-kip · created 2026-02-06

KIP-1142 introduced the LIST_CONFIG_RESOURCES RPC as a way of listing Kafka resources for which configuration properties can be described. It built upon KIP-1000 which was specifically concerned with client-metrics resources.
Unfortunately, this RPC requires DESCRIBE_CONFIGS permission on the cluster resource for all resource types. This has the side-effect that you need different permission to list groups (DESCRIBE on CLUSTER) than to list which groups have configs (DESCRIBE_CONFIGS on CLUSTER…

- **Chia-Ping Tsai:** [~brandboat] and I will address this
- **Aditya Kousik:** Hi, drive-by comment here. I see two duplicate KIPs. KIP-1296 is shared by https://issues.apache.org/jira/browse/KAFKA-20144 and https://issues.apache.org/jira/browse/KAFKA-20216 Looking at confluence history, https://issues.apache.org/jira/browse/KAFKA-20216 was the first one to the finish line.
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

- **Kamal Chandraprakash:** [~dyingjiecai] Could you add more details on the data loss that you're observing?  If you want to preserve the remote data while disabling remote storag, then use {{remote.storage.enable=true,remote.log.copy.disable=true}} setting.
- **chomingi:** Hi [~dyingjiecai]  I looked into this issue. Based on your logs, I think the mechanism may differ from the race condition described. Your logs show  - 15:14:37.184: \{{ReplicaFetcherThread-1-1}} increments logStartOffset to 3123750 ("leader offset increment")  - 15:16:37.068: TS disabled, follow…
- **Yunseop Eom:** PR opened: https://github.com/apache/kafka/pull/23025 Fixed remote-log cleanup cancellation ordering so an in-flight expiration task cannot publish a stale log-start-offset update after remote storage is disabled. Cancellation now interrupts and waits for task completion before partition cleanup.…
- **Yunseop Eom:** Update on PR #23025: https://github.com/apache/kafka/pull/23025 The PR serializes remote-log task execution with cancellation cleanup, waits for in-flight work before stopPartitions continues, and prevents stale expiration updates after cancellation. The regression and RemoteLogManagerTest pass, a…
- **Yunseop Eom:** PR #23025 is open and ready for maintainer review: https://github.com/apache/kafka/pull/23025

## KAFKA-20149: C4 Architecture Diagram for Apache Kafka Ecosystem
Improvement · Open · Major · created 2026-02-07

Provide C4 architecture diagram for the Entire Apache kafka ecosystem . This would bring the architecture documentation of Apache Kafka to Industry standards and also codify the software architecture of Apache Kafka and provide better Archiecture Understanding, governance and evolution.
Version-controlled, architecture-as-code diagrams to improve contributor onboarding and Entire Apache kafka ecosystem understanding.


## KAFKA-20150: Spike and explore usage of C4 diagram too like structurizr
Sub-task · Patch Available · Major · components: documentation · labels: architecture, documentation · created 2026-02-07

- **Sujay Hegde:** Pull request  - [https://github.com/apache/kafka/pull/21428.] Please review

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

- **Aman Ahmad:** Hi [~high.lee] , I would like to work on this if you are not working on this yourself. Thanks!
- **Harikrishnan:** [~high.lee] , [~aman82500] I would like to work on this if any one you are not working on this yourself.  Thanks!

## KAFKA-20235: Expose EffectiveMinIsr as a Partition metric
Improvement · Open · Minor · labels: need-kip · created 2026-02-28

from: [https://github.com/apache/kafka/pull/14594#discussion_r2606393474]
Since the EffectiveMinIsr calculation was updated in 3.7.0 (dynamically bouned by the actual replica count), it would be highly beneficial to expose this value as a metric. Exposing `EffectiveMinIsr` allows operators to track the exact real-time threshold protecting `acks=all` produce requests, which is crucial for troubleshooting and monitoring reassignment transition


## KAFKA-20236: Allow kafka-configs.sh to delete all dynamic configs for a group
New Feature · Open · Minor · labels: need-kip · created 2026-03-01

Currently, deleting a group does not automatically remove its associated dynamic configurations, leaving orphaned configs in the cluster. This not only consumes space, but may also cause unexpected behavior if a new group is created with the same name.

- **Jhen-Yung Hsu:** I'm working on this, thanks :)
- **David Jacot:** Hey. This was done intentionally as per KIP-848: [https://cwiki.apache.org/confluence/display/KAFKA/KIP-848%3A+The+Next+Generation+of+the+Consumer+Rebalance+Protocol#KIP848:TheNextGenerationoftheConsumerRebalanceProtocol-DynamicGroupConfiguration]
- **Chia-Ping Tsai:** [~dajac] Thanks for sharing. My intention with this proposal isn't to change that default broker behavior. Instead, I'm looking at this from an operational perspective. The goal here is simply to enhance the kafka-configs.sh CLI tool to allow users to explicitly delete these configs. Do you think t…
- **Andrew Schofield:** My view is that it is worth tidying up a little here.  * I have two consumer groups with no configs defined: andrew@Andrews-MacBook-Pro kafka % bin/kafka-configs.sh --bootstrap-server localhost:9092 --entity-type groups --describe Dynamic configs for group console-consumer-43887 are: Dynamic con…
- **Chia-Ping Tsai:** [~schofielaj] Thanks for sharing this great example. Yes, addressing this can definitely be included in this KIP. The reason the group still exists in the output is that we currently don't have a removal operation in `GroupConfigManager`. We could modify the CLI tool to filter out such groups (thos…
- _…4 more comments_

## KAFKA-20237:  TransactionManager stuck in `INITIALIZING` state after initial SSL handshake failure
Bug · Open · Major · components: clients, producer  · created 2026-03-02

I encountered a scenario where the `KafkaProducer` fails to recover if the initial SSL handshake with the broker fails, even after the underlying SSL configuration is corrected.
*Steps to Reproduce:*
1. Configure a `KafkaProducer` with SSL enabled, but use an incorrect/untrusted certificate on the server side to trigger an `SSLHandshakeException`.
2. Start the Producer and attempt to send a message.
3. The Producer logs show recurring SSL handshake errors. At this point, `TransactionManager`…

- **sanghyeok An:** Transaction Coordinator likely needs further investigation,  but this seems primarily a Kafka Producer issue and appears to affect both TV1 and TV2. For example, an AuthenticationException occurs in the Producer’s sender thread before a message is sent.  Since the initProducerId request that was…
- **Yin Lei:** Thanks for the quick investigation! Your analysis about the initProducerId being dequeued without re-enqueuing perfectly explains the "deadlock" state I observed. Regarding the recovery behavior, I understand that SSL failures are typically long-lasting. However, in containerized or cloud-native en…
- **sanghyeok An:** [~finalecho]  Ah, sorry for the confusion. The comment I left was simply as a contributor: I read through the issue, analyzed it, and shared my thoughts on the pros and cons. Since I’m also just a contributor like you, it’s difficult for me to define or decide the final solution for this issue. Th…
- **Yin Lei:** Hi [~chickenchickenlove]  Thank you for clarifying! I really appreciate the feedback from a fellow contributor, and the links to the KIP process are very helpful. You've raised a crucial point regarding the Public Contract. From my perspective, the current behavior — where the Producer remains per…

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

- **Aleksei Veremeev:** Failed tests: +Streams integration test:+   # IQv2StoreIntegrationTest. initializationError  # KafkaStreamsTelemetryIntegrationTest. "shouldPushGlobalThreadMetricsToBroker(String, String).recordingLevel=TRACE, groupProtocol=streams" +Tools build:+  # JmxToolTest. initializationError +Core buil…
- **Mickael Maison:** Thanks for submitting this issue. Some of these are known to be flaky tests. I suggest you open a PR so we can run the CI and start reviewing the changes.
- **Aleksei Veremeev:** Done. [PR# 21621|https://github.com/apache/kafka/pull/21621]
- **Aleksei Veremeev:** New [PR# 21622|https://github.com/apache/kafka/pull/21622] which includes changed LICENSE-binary ([~chia7712] suggestion)
- **Aleksei Veremeev:** [PR# 21622|https://github.com/apache/kafka/pull/21622] losed as duplicate LICENSE-binary is added to [PR# 21621|https://github.com/apache/kafka/pull/21621]

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

- **Lianet Magrans:** Merged and cherry-picked to: 4.3 - [https://github.com/apache/kafka/commit/6b05369445b00c96f854b798753e45542faceeb8] 4.2 - [https://github.com/apache/kafka/commit/23aaf8129175bf42fceb98e80a0be565ead42f9a]
- **Lianet Magrans:** Reopened for minor gap with wakeup. Small PR in review
- **Lianet Magrans:** Second PR merged and cherry picked: 4.3 -> [https://github.com/apache/kafka/commit/5d6248c4486f48471849caf09861b02db5009cbd]  4.2 -> https://github.com/apache/kafka/commit/6a50244a80de5c3042144a22e6bb65beff372a8d

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
- **ASF GitHub Bot:** nileshkumar3 opened a new pull request, #870: URL: https://github.com/apache/kafka-site/pull/870    ## Summary    Sync the KIP-1271 (header-aware state stores) documentation from    apache/kafka `4.3` branch into `content/en/43/`, following the merge of    apache/kafka#21840.    apache/kafka#218…
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
- **Kartikay Dubey:** Apologize for jumping the gun *😅 .*  Yes, ill be happy to review the PR : )

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
- **Sree Varshini S:** opened a fresh PR where changes already done + addressing of comments on the previous stale PR has been done: [https://github.com/apache/kafka/pull/23236] cc: [~lianetm] - please review, thanks!

## KAFKA-20456: Task not found in StateUpdater throwing an exception and causing unnecessary restoration
Bug · Resolved (Fixed) · Blocker · components: streams · created 2026-04-15 · resolved 2026-04-27

2026-04-14 06:58:52.742 Caused by: java.lang.IllegalStateException: Task 1_12 was not found in the state updater. This indicates a bug. Please report at [https://issues.apache.org/jira/projects/KAFKA/issues] or to the dev-mailing list ([https://kafka.apache.org/contact]). 2026-04-14 06:58:52.742 at org.apache.kafka.streams.processor.internals.TaskManager.waitForFuture(TaskManager.java:710) ~[kafka-streams-4.3.0-SNAPSHOT.jar:?] 2026-04-14 06:58:52.742 at org.apache.kafka.streams.processor.interna…


## KAFKA-20457: Consider to exclude repartition topics from auto.offset.reset
Improvement · Open · Minor · components: streams · created 2026-04-16

In Kafka Streams, repartition topics serve a very special purpose to shuffle intermediate data, that is not fully processed yet. To avoid any data-loss, these topics are configured with infinite retention time and use explicit "delete record" requests.
However, repartition topic still apply auto.offset.reset strategy. While it is expected that auto.offset.rest would only fire a single time at startup, when the repartition topic is still empty (and thus "latest" vs "earliest" does not matter), t…

- **Daeho Kwon:** I'd like to work on this. May I pick this up?
- **Matthias J. Sax:** Sure. Just a note: we are currently overwhelmed with review request. So you need to be patient.
- **Daeho Kwon:** Hi [~mjsax] ,                                                                                                                                                                                                  I've been looking into this. Setting auto.offset.reset=none for repartition topics in Optimi…
- **Matthias J. Sax:** For committing offsets, we need to consider the "classic" and "streams" protocol. For "classic" we create repartition topics during a rebalance on the group leader clients side, so we need to add a second admin call to commit offsets – the problem is, like always, how to handle errors? We cannot ju…
- **Lucas Brutschy:** That sounds incredibly complex to me. Especially triggering this in KIP-1071 from within the broker.  Could we just do the same thing at startup of the streams application, for all protocols? Seems like this would also simplify the error handling, because we do it before joining the group, so we do…
- _…1 more comments_

## KAFKA-20458: AcknowledgeType.RENEW re-delivers records to application via poll() in explicit acknowledgement mode, undocumented and inconsistent with broker-side contract
Bug · Open · Major · created 2026-04-16

AcknowledgeType.RENEW is documented as a way to extend the acquisition lock on a record that is still being processed, without changing the record's state on the broker. However, the client-side implementation silently re-delivers the same records back to the application on the next poll() call. This behavior is nowhere documented, violates the explicit acknowledgement mode invariant, and diverges from the broker-side contract.
RENEW simultaneously satisfies two contradictory contracts:
Contex…

- **Andrew Schofield:** The javadoc for `KafkaShareConsumer` explains the behaviour for renew acknowledgements. It's Option B above.
- **Shekhar Prasad Rajak:** Thanks [~schofielaj] for checking, but is not if we extending the lock means we are processing the record and do not want to get the same record back ? Otherwise we will end up duplicate processing ?  I believe it is better to extend the lock, until consumer alive or till the next poll or till the…
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

- **Hareesh Billa:** As per JDK 25 getSubject() method will not work.  What is the solution to this? Why this LegacyStrategy is invoked? !image-2026-04-16-15-43-54-212.png! !image-2026-04-16-15-45-31-128.png!
- **Hareesh Billa:** Sorry for logging this issue at earliest. Fallback mechanism worked fine. Identied another issue and corrected my client config. Closing this issue. Thanks.
- **Hareesh Billa:** I could not close this. Can anyone close this. Thanks.

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
- **Chia-Ping Tsai:** {quote} Unfortunately 4.3 still has the Scala ConfigCommand. If it's not too much work I think there would be value in having this in 4.3 for the decommissioning log dir process. {quote} Agreed. Once the trunk PR is merged, we will file another PR specifically targeted for 4.3 to handle the diffe…

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

- **majialong:** Hi [~schofielaj] , I noticed that the examples module does not include an example for Share Groups yet. I’d like to add a simple example to help users understand the basic usage of Queues for Kafka / Share Groups. Before starting the work, I’d like to check with you whether this JIRA makes sense.
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

- **Muralidhar Basani:** Hi [~mjsax] , I'd like to pick this up if it's still open. I can add ducktape coverage for the mentioned 42/43/44 scenarios.
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

- **Siddhartha Devineni:** [~pkleindl],  Thank you for the reproducer repo; it made this straightforward to narrow down. The punctuator plus caching combination was the key detail; The mechanism: StreamTask#punctuate sets a dummy ProcessorRecordContext with partition -1, the cache captures it at delete time and replays it a…

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
- **GiminKim:** Thanks for asking. I could not find a Kafka-internal runtime path that directly invokes StreamsGroupDescription.toString(); for example, StreamsGroupCommand accesses the individual fields instead. The failure is reachable by Admin API consumers, though. The convenience describeStreamsGroups(Coll…
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

- **Gaurav Narula:** Thanks for reporting this Chia! I had found the same last week but had covered it under a minor PR at https://github.com/apache/kafka/pull/22987 I've edited its title now and given it this issue number
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

- **Muralidhar Basani:** > Is there an intended supported configuration that allows JWKS TLS trust options to be supplied while retaining the tokenless server-side behavior [~akshatha] can you try adding _unsecuredLoginStringClaim_sub_ workaround (not a fix)? I tried the below jaas config and was able to start the server…
- **akshatha ramesh:** Hi [~muralibasani], Thanks for your quick response. According to the Kafka documentation, this configuration is intended solely for development or testing and is not recommended for production, which makes me hesitant to adopt it. However, unsecuredLoginStringClaim_sub was already tested before ra…
- **Muralidhar Basani:** [~akshatha] I have a fix, you might want to try as. well if it works. https://github.com/apache/kafka/pull/23557

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
