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

- **Mickael Maison:** https://issues.apache.org/jira/browse/KAFKA-14732 describes pretty much the same issue. With the exponential backoff we don't spam the logs with errors. However it's still kind of unclear what's going on from a user point of view without looking at the logs.
 If the connector throws in taskConfigs()…
- **Chris Egerton:** [~mimaison] do you think it's worth considering a KIP to alter the behavior in this scenario? I know that some connectors may be relying on the infinite-retry logic for the {{taskConfigs}} method but in my experience a lot of the time it's unintentional and there's a false expectation that throwing…
- **Mickael Maison:** To be honest I'm not sure if we should change this behavior or simply document it. I tend to agree that the retry logic was likely intended to handle failures communicating with the leader instead of exceptions from taskConfigs().
- **Yash Mayya:** I agree that the intent of the retries seems to be mainly to handle failures while communicating with the leader - this infinite retry mechanism covering exceptions thrown from connectors' taskConfigs method doesn't seem to make sense intuitively and was probably an oversight. [~ChrisEgerton] are yo…
- **Chris Egerton:** Hi Yash,
 {quote}are you suggesting a KIP to modify the existing retry mechanism to not cover exceptions thrown from connectors' taskConfigs method?
 {quote}
 Yep, exactly. But it's not high-priority and given Mickael's thoughts I don't think we should move forward with it for now. The suggestion to…

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

- **Alexandre Dupriez:** I could reproduce without forcefully renewing the ZK session.
 In a nutshell, it is possible (at least with the Netty client for ZK used for reproduction and run in production) to have the Zookeeper server create an active session then process messages under its authority (including znode creation)…
- **Alexandre Dupriez:** The reproduction test case has been update and is available [in github|https://github.com/Hangleton/kafka-tools/tree/master/kafka-broker-reg].
 The logs of a run of this test have been attached to this ticket.
 It does not require any forced session renewal but just reproduce the use case using:
  *…
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

- **Greg Harris:** [~bseenu] Are you running MM2 with the MirrorMaker dedicated launcher? There's a known issue where a multi-node cluster is unable to persist configuration changes: https://issues.apache.org/jira/browse/KAFKA-10586 which has a fix to be released in 3.5.0.
 You can verify that the above is affecting y…
- **Srinivas Boga:** [~gharris1727] Thanks for your help on this
 Yes i could see that log message which you pointed out, i was running mirrormaker in distributed mode having 3 nodes and 10 tasks on each
 I have verified by running only on one node and it is working as expected
 Thanks,
 -srini

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

- **Greg Harris:** cc [~jolshan] [~dajac] [~hachikuji] [~mimaison]
 I have not seen this failure mode before, and I'm worried that this might be a recent regression. It also doesn't look like an error that is intended to be surfaced by the API in normal operations (I might expect a disconnect or ProducerFencedExceptio…
- **Justine Olshan:** So many transaction/init producer ID issues lately. I had to check this wasn't the same as https://issues.apache.org/jira/browse/KAFKA-14830 
 I've seen some init producer ID failures a few times as well (seeming more frequently) when testing.
 I was also wondering if this change could be related, b…
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

- **Justine Olshan:** Jenkins truncates this out since the bounced broker leads to a ton of aborted transaction errors, but after that we see:
 [code/log omitted]
 And a TON more out of sequence errors (probably most of the partitions). Will investigate further if this is a result of my change and if there are ways to fi…
- **Justine Olshan:** Further investigation shows this occurs after the verification failed with CONCURRENT_TRANSACTIONS error. 
 I will debug further and fix this case.
- **Justine Olshan:** The issue is the first request we verify is still in pending state. I suspect if we check the transaction is in pending ongoing state + verify + confirm the transaction we should be good to proceed. However, I will need to look a bit closer at what pending means here.
- **Justine Olshan:** Marking as a blocker since the commit that caused this regressed the previous behavior.
 Any verification that occurs too fast will cause OutOfSequence errors.

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
- **Divij Vaidya:** This is the second most frequent reason for build failures in the last 28 days: [https://ge.apache.org/scans/failures?search.relativeStartTime=P28D&search.rootProjectNames=kafka&search.timeZoneId=Europe/Berlin] 
 Raising the priority to Major
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

- **Matthias J. Sax:** Very interesting idea – given that we persist the thread-id (aka process-id) in the state directory on local disk, it could help. And even if we don't persist it (because there is no local storage), it seems no harm would be done if the id changes every single time.
 Wondering if we would need a KIP…
- **A. Sophie Blee-Goldman:** Have we resolved all the known issues with static membership? IIRC there were some that required broker-side changes, could we accidentally introduce correctness-related bugs in Streams applications running against older clusters? 
 Maybe I'm being paranoid, but I thought we had begun to recommend a…
- **Matthias J. Sax:** I was not aware that there was (or maybe still are) issue. Are there any tickets for it?
- **Bruno Cadonna:** I have the same feeling as [~ableegoldman]. So, we should first ensure that the issues are solved, before proceeding with this ticket.
 In general, I would welcome Streams using static membership by default.

## KAFKA-14982: Improve the kafka-metadata-quorum output
Improvement · Resolved (Fixed) · Major · labels: need-kip · created 2023-05-10 · resolved 2023-05-29

When running kafka-metadata-quorum script to get the quorum replication status, I found the LastFetchTimestamp and LastCaughtUpTimestamp output is not human readable. The timestamp 1683701749161 is just a random integer to me. We should convert it into date/time (ex: May 10, 08:00 UTC), or if possible, convert it into strings like "10 seconds ago", "5 minutes ago"...
[code/log omitted]

- **Federico Valeri:** https://cwiki.apache.org/confluence/display/KAFKA/KIP-927%3A+Improve+the+kafka-metadata-quorum+output

## KAFKA-14983: Upgrade jetty-server to 9.4.51
Task · Resolved (Fixed) · Minor · created 2023-05-10 · resolved 2023-05-15

Kafka latest versions e.g. 3.4.0 includes jetty-server-9.4.48.v20220622.jar that includes 2 vulnerabilities: CVE-2023-26048 and CVE-2023-26049. Upgrading them to 9.4.51 would fix those issues.

- **Divij Vaidya:** There is a PR open for this [https://github.com/apache/kafka/pull/13673] 
 Although, I doubt that this will make it into 3.5.0 since it's past the code freeze date. The vulnerabilities are moderate/low in nature. I will let folks familiar with Connect framework chime in here but AFAIK, the first one…

## KAFKA-14984: DynamicBrokerReconfigurationTest.testThreadPoolResize() test is flaky 
Test · Resolved (Duplicate) · Major · labels: flaky-test · created 2023-05-10 · resolved 2023-08-25

The test sometimes fails with the below log 
[code/log omitted]

- **Justine Olshan:** Ah I missed this yesterday. I filed https://issues.apache.org/jira/browse/KAFKA-15404.
 Looks like someone assigned themselves, so I will close this one.

## KAFKA-14985: ConnectionQuotasTest.testListenerConnectionRateLimitWhenActualRateAboveLimit() test is flaky
Test · Resolved (Duplicate) · Major · created 2023-05-10 · resolved 2023-05-10

The test sometimes fails with the following error
[code/log omitted]

- **Manyanda Chitimbo:** A quick fix will be to bump the epsilon to a bigger value e.g 8 on [https://github.com/apovzner/kafka/blob/508a754f397b5a1939c44dfcba72ba996bc912c5/core/src/test/scala/unit/kafka/network/ConnectionQuotasTest.scala#L400] but I am not sure if that's enough to make the test  resilient , what do you thi…
- **Divij Vaidya:** We already have an open Jira (and a pending PR) for this: [https://issues.apache.org/jira/projects/KAFKA/issues/KAFKA-12319?filter=allopenissues] 
 Resolving this as duplicate. [~manyanda], in future, please search for existing Jira before creating new ones.
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
- **Owen C.H. Leung:** [~divijvaidya] I'd like to pick this up. I've done a bit diving and would like to clarify if my understanding is correct : 
 So essentially, in this ticket we want to remove the use of {*}ConcurrentMap<TopicPartition, Uuid> topicPartitionIds{*}, and leverage the cache available in *RemoteLogManagerC…
- **Divij Vaidya:** Hi [~owen-leung] 
 Than you for looking into this. Yes, we want to replace *ConcurrentMap<TopicPartition, Uuid> topicPartitionIds* cache in RemoteLogManager. However, instead we want to cache available in every broker called the Metadata cache [1]which will be the single source of authority on a bro…
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

- **Adrian Preston:** [~smashingquasar],
 Looking at the hex dump of your APIVersions request, I think you are correctly encoding the empty tag field as a single 0x00 byte. It looks, however, like the compact string encoding (used for the 'client_software_name' and 'client_software_version' fields) is adding an unexpecte…

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
- **Divij Vaidya:** Thank you for the investigation folks. We have an active PR right now [1] which makes producer snapshot flush to disk asynchronously. The thread blocking problem due to fsync will be resolved by it.
 [1] https://github.com/apache/kafka/pull/13782
- **Haruki Okada:** Oh I haven't noticed there's another ticket and already the fix is available.
 Thank you, I will take a look!
- **Haruki Okada:** Hm, when I dug into further this, I noticed there's another path that causes essentially same phenomenon.
 [code/log omitted]
 LeaderEpoch checkpointing also calls fsync with holding Log#lock and blocking request-handler threads to append in the meantime.
 This is called by scheduler thread on log-s…
- **Divij Vaidya:** Yes that is right, leaderEpochCheckpoint is another I/O operation Kafka performs while holding the global partition lock. 
 IMO, we need to move to async disk I/O using [io_uring|https://unixism.net/loti/what_is_io_uring.html] to prevent thread blocking (and lock contention) while performing disk I/…
- _…12 more comments_

## KAFKA-15047: Handle rolling segments when the active segment's retention is breached incase of tiered storage is enabled.
Improvement · Resolved (Fixed) · Major · created 2023-06-01 · resolved 2023-11-28

Active segments are not copied by remote storage subsystem. But they can be eligible for retention cleanup. 
So, we need to roll the active segment incase remote storage is enabled so that this can be eligible to be copied by the remote storage subsystem and eventually picked up for retention cleanup.

- **Henry Cai:** I created a topic with local.retention.ms=120000 (2 minutes)
 ```
 bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic topic1 --config remote.storage.enable=true --config segment.bytes=512000 --config retention.ms=360000000 --config local.retention.ms=120000
 ```
 The segments are…
- **Luke Chen:** [~hcai@pinterest.com] , the retention implementation PR is under review now: [https://github.com/apache/kafka/pull/13561] . FYI

## KAFKA-15096: CVE 2023-34455 - Vulnerability identified with Apache kafka
Bug · Resolved (Fixed) · Major · created 2023-06-16 · resolved 2023-06-19

A new vulnerability CVE-2023-34455 is identified with apache kafka dependency. The vulnerability is coming from snappy-java:1.1.8.4
Version 1.1.10.1 contains a patch for this issue. Please upgrade the snappy-java version to fix this issue
snappy-java is a fast compressor/decompressor for Java. Due to use of an unchecked chunk length, an unrecoverable fatal error can occur in versions prior to 1.1.10.1.
The code in the function hasNextChunk in the fileSnappyInputStream.java checks if a given s…

- **Manyanda Chitimbo:** Thank you for reporting the issue [~Sasikumarms] an PR has been opened in 
 [https://github.com/apache/kafka/pull/13865]
 to bump the version. 
 Once merged, I'll let the release managers determine how far the fix can be backported.
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

- **Mukesh Mishra:** There is something wired in log 4146 of consumer offset :
 In 00000000000004146.log.swap, i can see below records :
 [code/log omitted]
 baseOffset (7435, 7740) mentioned in 00000000000004146.log.swap which is already present in 00000000000006340.log (they should present only in  6340.log)
 [code/lo…
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

- **Josep Prat:** h3. Standard Output
 [code/log omitted]

## KAFKA-15104: Flaky test MetadataQuorumCommandTest for method testDescribeQuorumReplicationSuccessful
Bug · Patch Available · Major · components: tools · labels: flaky-test · created 2023-06-19

The MetadataQuorumCommandTest has become flaky on CI, I saw this failing: org.apache.kafka.tools.MetadataQuorumCommandTest.[1] Type=Raft-Combined, Name=testDescribeQuorumReplicationSuccessful, MetadataVersion=3.6-IV0, Security=PLAINTEXT
Link to the CI: https://ci-builds.apache.org/job/Kafka/job/kafka-pr/job/PR-13865/2/testReport/junit/org.apache.kafka.tools/MetadataQuorumCommandTest/Build___JDK_8_and_Scala_2_12____1__Type_Raft_Combined__Name_testDescribeQuorumReplicationSuccessful__MetadataVers…

- **Divij Vaidya:** Another instance - [https://ci-builds.apache.org/job/Kafka/job/kafka-pr/job/PR-13831/7/]
- **Justine Olshan:** I saw this fail many times here:  [https://ci-builds.apache.org/blue/organizations/jenkins/Kafka%2Fkafka-pr/detail/PR-15183/3/tests]
- **Lianet Magrans:** This is still flaky, showing on [https://github.com/apache/kafka/actions/runs/28885044689/job/85685508767?pr=22768]
 Added the flaky tag
- **Edmond Abraham:** Pull request: https://github.com/apache/kafka/pull/23466
 The previously quarantined test passed 60 generated KRaft invocations after the UpdateVoter changes.

## KAFKA-15105: Flaky test FetchFromFollowerIntegrationTest.testFetchFromLeaderWhilePreferredReadReplicaIsUnavailable
Bug · Open · Major · components: core · labels: flaky-test · created 2023-06-19

Test  integration.kafka.server.FetchFromFollowerIntegrationTest.testFetchFromLeaderWhilePreferredReadReplicaIsUnavailable() became flaky. An example can be found here: https://ci-builds.apache.org/job/Kafka/job/kafka-pr/job/PR-13865/2/testReport/junit/integration.kafka.server/FetchFromFollowerIntegrationTest/Build___JDK_11_and_Scala_2_13___testFetchFromLeaderWhilePreferredReadReplicaIsUnavailable___2/
The error might be caused because of a previous kafka cluster used for another test wasn't cle…

- **Max Riedel:** I would like to work on this issue. I'm still trying to understand how the build infrastructure works. Can someone give me a hint, how to reproduce the behavior?
- **Josep Prat:** Hi [~riedelmax], feel free to assign this issue to yourself :)
 {quote}I'm still trying to understand how the build infrastructure works. Can someone give me a hint, how to reproduce the behavior?
 {quote}
 In this rely part of the problem, many times these issues are not easily reproducible on your…
- **Max Riedel:** Hi [~josep.prat] 
 Thanks for giving me the necessary Jira rights. I was able to assign the ticket to me now.
 So far, all test runs I did on my local environment passed. But I will try the option to run until failure and see what I can learn from that.
 My question was about the CI. Is it correct t…
- **Josep Prat:** Hi [~riedelmax] ,
 Only maintainers + a subgroup of collaborators can rerun builds in CI, but even for them, they can just run them as they are (no more detailed output). And sorry, I just realized I copy pasted the wrong ci build link. This is the right one: [https://ci-builds.apache.org/job/Kafka/…

## KAFKA-15106: AbstractStickyAssignor may stuck in 3.5
Bug · Resolved (Fixed) · Major · components: clients · created 2023-06-19 · resolved 2023-08-04

this could reproduce in ut easy,
just int org.apache.kafka.clients.consumer.internals.AbstractStickyAssignorTest#testLargeAssignmentAndGroupWithNonEqualSubscription,
plz set 
partitionCount=200, 
consumerCount=20,  you can see 
isBalanced will return false forever.

- **Kirk True:** [~flashmouse] Thank you for the test case. I was able to reproduce the hanging behavior. I would have assumed that the {{@Timeout}} would have stopped the test after 90 seconds, but it didn't appear to when I ran it 🤔
 I'm not familiar with this area of the code, so I'm not sure if the stated values…
- **li xiangyuan:** I wonder whether modify the line in function `isBalanced` could solve it.
 current:
 [code/log omitted]
 fixed:
 [code/log omitted]
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
- **Jorge Esteban Quilcate Otoya:** Sure. The TBRLMM is not the one not recovering, but the Replica Fetcher. 
 My understanding is that this issue happens when a Replica is recovering its state after being offline. TBRLMM receives partitions assigned, starts managed, and is marked as initialized and open to receive requests; however t…
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

- **RivenSun:** Hi [~showuon]  [~guozhang] 
 can you give any suggestion?
 Thanks.
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

- **Jacob Tomy:** Can someone help me assign this to me. 
 These are my planned changes : https://github.com/apache/kafka/pull/13981
- **Bruno Cadonna:** I added you to the contributor group. Now you should be able to assign the ticket to yourself.
- **Bruno Cadonna:** In the PR, I see that you want to change the `Partitioner` interface. Since that is a public interface, you need to write a KIP and get it accepted. See https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Improvement+Proposals
- **Jacob Tomy:** Hi [~cadonna] 
 Thanks for adding me to the contributors group.
 I was facing trouble accessing the confluence last day. I'm able to access it now. I will create the KPI and proceed.
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
- **Kamal Chandraprakash:** [~divijvaidya] 
 The below comment is not addressed, we can take it together with [KIP-950|https://cwiki.apache.org/confluence/display/KAFKA/KIP-950%3A++Tiered+Storage+Disablement]:
 [https://github.com/apache/kafka/pull/13947#discussion_r1294782503]

## KAFKA-15291: Implement Versioned interfaces in common Connect plugins
Improvement · Resolved (Fixed) · Major · components: connect · created 2023-08-01 · resolved 2023-08-10

In KAFKA-14863, we changed the plugin scanning logic to allow plugins to opt-in to the Versioned interface individually, when previously it was limited to Connector plugins.
To take advantage of this change, we should have all of the plugins built via the Kafka repository opt-in, and provide the environment's Kafka version from the AppInfoParser.getVersion().
See the FileStreamSinkConnector as an example of the the version() method implementation.
All subclasses of Converter, HeaderConverter,…

- **Aindriú Lavelle:** Hey [~gharris1727] I can pick this up. if you want to assign it to me.
 Thanks!
 Also let me know if its desirable to also update test subclasses with this implementation.
- **Greg Harris:** [~aindriú] Thanks for looking at this!
 Please include most of test classes as well. We should probably leave one plugin which is left un-Versioned to test out the UNDEFINED_VERSION behavior.
- **Aindriú Lavelle:** PR [https://github.com/apache/kafka/pull/14159] has been opened to implement these changes.
 StringConverter has been left un implemented so that the UNDEFINED_VERSION behaviour can be tested.

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
- **Kamal Chandraprakash:** [~showuon] 
 I'm not working on this one currently. Thanks for taking it forward!

## KAFKA-15296: Allow committing offsets for Dropped records via SMTs
Bug · Open · Major · components: connect · created 2023-08-02

Currently the connect Runtime doesn't commit the offsets of records which have been dropped due to SMT. This can lead to issues if the dropped record's partition reflects a source partition and the connector depends upon the committed offsets to make progress. In such cases, the connector might just stall. We should enable committing offsets for dropped records as well. Note that today if a record is dropped because exactly-once support is enabled and the connector chose to abort the batch conta…


## KAFKA-15297: Cache flush order might not be topological order 
Bug · Open · Major · components: streams · created 2023-08-02

The flush order of the state store caches in Kafka Streams might not correspond to the topological order of the state stores in the topology. The order depends on how the processors and state stores are added to the topology. 
In some cases downstream state stores might be flushed before upstream state stores. That means, that during a commit records in upstream caches might end up in downstream caches that have already been flushed during the same commit. If a crash happens at that point, thos…

- **A. Sophie Blee-Goldman:** Were you able to (re)produce this issue? I'm a bit surprised because I always thought the state stores were maintained in strict topological order, both when building them initially and then when registering them.
 The stores are flushed in the order that they are registered, which corresponds to th…
- **Matthias J. Sax:** The ticket description contains an example to reproduce it (and there is also a png attachment visualizing the topology). 
 {quote}which in turn *should* reflect the topological order of the attached processor nodes.
 {quote}
 That's not always the case unfortunately.
- **Bruno Cadonna:** [~ableegoldman] You can observe the flush order by feeding some records into the input topics, waiting for a commit, and looking for the following log message:
 https://github.com/apache/kafka/blob/2e1947d240607d53f071f61c875cfffc3fec47fe/streams/src/main/java/org/apache/kafka/streams/processor/inte…
- **Guozhang Wang:** I think this is indeed a general issue, that state stores are initialized in the order of the topology which is essentially the "processor node order", as in ``InternalTopologyBuilder#build``. This works when a state store is only associated with one processors, or when a store is associated with mu…
- **Bruno Cadonna:** [~guozhang] Yes, I agree the issue is when state stores are connected to PAPI operators because they can basically connect to state stores at any location in the topology graph.
 I also thought about the solution you describe and discussed it with [~mjsax], [~wcarlson5], [~lihaosky], and [~alisa23].…
- _…2 more comments_

## KAFKA-15298: Disable DeleteRecords on Tiered Storage topics
Sub-task · Resolved (Won't Fix) · Major · labels: tiered-storage · created 2023-08-02 · resolved 2023-08-09

Currently the DeleteRecords API does not work with Tiered Storage. We should ensure that this is reflected in the responses that clients get when trying to use the API with tiered topics.

- **Kamal Chandraprakash:** [~christo_lolov]
 Could you explain why DeleteRecords API won't work with tiered storage? The DELETE_RECORDS API increments the log-start-offset and waits for the low-watermark to move till the requested offset. With {{deleteLogStartOffsetBreachedSegments}} in [https://github.com/apache/kafka/pull/1…
- **Christo Lolov:** Heya [~ckamal]! Thanks for pointing me to the pull request. I had not reviewed it so I wasn't aware of this particular change (https://github.com/apache/kafka/pull/13561/files#diff-10e27a71dc3dec3463df7752ab07f6227cf70bcee70a93a86b5984e020beae05L984) which I believe addresses my concern. Give me som…

## KAFKA-15299: Support left stream-table join on foreign key
New Feature · Resolved (Incomplete) · Major · components: streams · labels: kip · created 2023-08-02 · resolved 2025-01-04

KIP-955: [https://cwiki.apache.org/confluence/display/KAFKA/KIP-955%3A+Add+stream-table+join+on+foreign+key]
Currently in Kafka Streams DSL, KStream to KTable joins could only be performed with the keys. However in practice it is often required to join the messages in Kafka topics using message field as a "foreign key" with the following pattern:  
streamX.leftJoin(tableY, RecordTableY::getForegnKey, joiner).to("output-topic-name")
The left loin on foreign key operation will result in a strea…

- **Matthias J. Sax:** Closing this ticket as "incomplete".
 The KIP discussion did not lead to a resolution. We can of course reopen this ticket and restart the KIP discussion at any time.

## KAFKA-15371: MetadataShell is stuck when bootstrapping
Bug · Resolved (Fixed) · Major · created 2023-08-17 · resolved 2025-04-14

I  downloaded the 3.5.1 package and startup it, then use metadata shell to inspect the data
[code/log omitted]
Then process will stuck at loading.
!image-2023-08-17-10-35-36-067.png!

- **liran avi:** Hi 
 I get this issue in version 3.6.0 and also in 3.5.1 
 in my case rarely I can access to the CLI but I didn't get all the options there (missing folders)
 more than that sometimes I get this error :
 !image-2023-10-31-09-04-53-966.png|width=654,height=184!
 when I run the lsof command it looks l…
- **Christian Lefebvre:** Weirdly, I had the same case than [~dengziming], without any output, but this morning I've the same exception message than [~lirangazer] 
 The difference is perhaps because the server was running today but stopped yesterday : maybe a race condition causes the error when the topic is written by serve…
- **Christian Lefebvre:** It becomes more and more weird ...
  * with stopped node, command hangs on "loading..."
  * if I set {{{}log4j.rootLogger=INFO{}}}, I get the prompt
  * with started server, I often get the NonWritableChannelException but sometimes I get the prompt
 When I got the prompt, exploring node tree works f…
- **Oleg Opolev:** I was never able to read the metadata in the cluster. Versions kafka 3.6.0
 ./bin/kafka-metadata-shell.sh -s ../kafka_2.13-3.6.0/log/__cluster_metadata-0/00000000000008838965.log
 Loading...
 [2024-01-11 12:23:15,640] ERROR Encountered shell fault: Error loading metadata log record from offset 10032…
- **Rashmi:** Facing similar error message as [~endoftime] , but executing a different workflow:
 3 Node cluster with instance of Kafka in KRaft mode running on each node. 
 Simulating an unexpected shutdown by powering off all VMs in the cluster. Then, bringing them back by powering on all the VMs.
 We see Kafka…
- _…3 more comments_

## KAFKA-15372: MM2 rolling restart can drop configuration changes silently
Bug · Resolved (Fixed) · Major · components: mirrormaker · created 2023-08-17 · resolved 2023-12-12

When MM2 is restarted, it tries to update the Connector configuration in all flows. This is a one-time trial, and fails if the Connect worker is not the leader of the group.
In a distributed setup and with a rolling restart, it is possible that for a specific flow, the Connect worker of the just restarted MM2 instance is not the leader, meaning that Connector configurations can get dropped.
For example, assuming 2 MM2 instances, and one flow A->B:
 # MM2 instance 1 is restarted, the worker in…

- **Greg Harris:** Hi [~durban] Thanks for the bug report.
 Is this reproducible with 3.5.0 and `dedicated.mode.enable.internal.rest` set to `true`? This configuration was added in [https://cwiki.apache.org/confluence/display/KAFKA/KIP-710%3A+Full+support+for+distributed+mode+in+dedicated+MirrorMaker+2.0+clusters] .
- **Daniel Urban:** Hi [~gharris1727], I don't have a deterministic reproduction of the issue.
 The reproduction of the problem requires multiple MM2 instances, but the internal REST is not needed at all (the startup and Connector config update does not touch the REST).
 Encountered this on a 3.4 build which contains t…
- **Greg Harris:** [~durban] I should clarify, I believe the behavior you described is the expected (but undesirable) behavior for versions before 3.5.0 and earlier, and for 3.5.0+ with the configuration set to the default `false`.
 When the internal REST API is enabled, the worker which is starting (that is not the l…
- **Daniel Urban:** [~gharris1727]  Not sure if I follow this part: "should forward configurations to the leader via the internal REST API."
 I checked org.apache.kafka.connect.mirror.MirrorMaker#configureConnector which then calls org.apache.kafka.connect.runtime.distributed.DistributedHerder#putConnectorConfig, and I…
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
- **Kamal Chandraprakash:** This task was already addressed in the code, so closing the ticket:
 https://sourcegraph.com/github.com/apache/kafka@3.6/-/blob/core/src/main/java/kafka/log/remote/RemoteLogManager.java?L1043-1061
- **Divij Vaidya:** Hey [~ckamal] 
 I think the motivation of this ticket to determine whether there are alternative options to remove leader epoch. As an example, in current implementation, if the non-current leader epoch chain becomes current, we will end up losing data in remote. With this ticket we wanted to explor…
- **Kamal Chandraprakash:** [~divijvaidya] 
 The [example|https://github.com/apache/kafka/pull/13561#discussion_r1293286722] provided in the discussion is misleading. Let's divide the example into two to navigate it easier:
 Assume that there are two replicas Broker A and Broker B for partition tp0:
 *Case-1*
 Both the replica…
- **Kamal Chandraprakash:** With unclean-leader-election enabled, there can be log-divergence, log-loss, and exactly-once-delivery is not applicable. We are trying to extend the same contract that is for local storage to remote when this feature is enabled. There are pros and cons to this feature:
 *Pros*
 1. The replica will…
- _…3 more comments_

## KAFKA-15377: GET /connectors/{connector}/tasks-config endpoint exposes externalized secret values
Bug · Resolved (Fixed) · Major · components: connect · created 2023-08-18 · resolved 2023-08-24

The {{GET /connectors/\{connector}/tasks-config}} endpoint added in [https://cwiki.apache.org/confluence/display/KAFKA/KIP-661%3A+Expose+task+configurations+in+Connect+REST+API] exposes externalized secret values in task configurations (see [https://cwiki.apache.org/confluence/display/KAFKA/KIP-297%3A+Externalizing+Secrets+for+Connect+Configurations)]. A similar bug was fixed in https://issues.apache.org/jira/browse/KAFKA-5117 / [https://github.com/apache/kafka/pull/6129] for the {{GET /connecto…

- **Yash Mayya:** [~mimaison] [~ChrisEgerton] even though this will technically change the response for a public REST API, I'm not sure it requires a KIP since it should be classified as a bug. What do you folks think?
- **Chris Egerton:** I don't think a KIP is necessary, for the same reasons that a KIP wasn't required the first time this issue surfaced with the other endpoint.
- **Mickael Maison:** Yeah I don't think this needs a KIP.
 If I remember correctly, in another thread we noticed this endpoint is pretty much identical to GET /connectors/{connector}/tasks. If they really contain the same data maybe we could even remove it completely?
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
- **Lucas Brutschy:** Thanks, [~ChrisEgerton] , I didn't realize that even the jenkins jobs for AK are not accessible. The direct output is 
 [code/log omitted]
 The detailed logs seem to be accessible though, here: 
 http://testing.confluent.io/confluent-kafka-branch-builder-system-test-results/?prefix=system-test-kafka…
- **Arpit Goyal:** [~lbrutschy]  As per description do you mean   the fix will work with this change ?
 install_requires=["ducktape<0.9", "requests==2.31.0"],
 I am trying to reproduce the issue locally , but I am getting this error 
 [code/log omitted]
 But it does not seem to matching the logs attached in the ticket…
- **Lucas Brutschy:** The requests python library downgrade was just required to get the tests running, but does not fix the actual test failure
 The bouncing upgrade test from 0.10 to 3.6 that seem to fail for you are probably yet another problem.
 Did you not get the test failures described in the ticket?
- **Arpit Goyal:** [~lbrutschy]  Not yet , I just tried to reproduce the issue but it is stuck at this error , Do you know the reason for this error ?
 Could not detect Kafka Streams version 3.6.0-SNAPSHOT on ducker@ducker12
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

- **Greg Harris:** it appears that the bug which prompted the fix in KAFKA-15244 (wrong PluginType being inferred) also could cause duplicates. For example:
 [code/log omitted]
 Here, the second entry should have been "header_converter". So while there are more duplicates in 3.6.0-rc0 than there were in <3.6.0-rc0, th…
- **Greg Harris:** Plugins could also appear multiple times <3.6.0-rc0 if multiple versions were on the plugin path concurrently. The DelegatingClassLoader would prefer the one with the latest version, but all of the different versions would be visible in the REST API.
 It also treated the undefined version as distinc…
- **Greg Harris:** I've opened [https://github.com/apache/kafka/pull/14398] with strategy (3) from above. We can always implement (1) in the future and change the PluginInfo::equals implementation to show these duplicates, so we can hide them for now. I think (2) removes functionality from the API and would count as a…
- **Satish Duggana:** [~gharris1727]
 Is this API documented that it does not return duplicate entries?
 Can we also get an opinion from PMC/Committers and other KafkaConnect
 experts on whether this issue is a release blocker?
 If we agree that it is not a release blocker then we can have a
 release note clarifying this…
- **Sagar Rao:** [~satish.duggana], No the API documentation doesn't mention anything about the presence/absence of duplicate entries. This is what it says:
 [code/log omitted]
 I think the implicit assumption is that these would always return unique values but as Greg pointed out above, even pre-3.6 there could be…

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
- **Luke Chen:** Nice find, [~divijvaidya]! So, the issue is because we time gap between entry invalidation and the file renaming (i.e. removalListener got invoked). 
 One thing to confirm, this is not a blocker for v3.6.0, right? I don't think it is since tiered storage is just a tech preview feature.
- **Divij Vaidya:** > the issue is because we time gap between entry invalidation and the file renaming
 Correct.
 >  this is not a blocker for v3.6.0, right? 
 Yes, I wouldn't consider this as a blocker since it's a race condition and shouldn't impact happy cases. I will add an entry to the early access document thoug…
- **Luke Chen:** About the solution to change to sync way, I have a question:
 Currently, we use readLock for both RemoteIndexCache#getIndexEntry and RemoteIndexCache#remove. That means, the original will still appear after using sync way:
 Thread 1 (cache thread): (readLock) invalidates the entry, removalListener i…
- **Luke Chen:** After re-reading the suggestion in Caffeine [doc|https://github.com/ben-manes/caffeine/wiki/Removal], the `evictionListener` only get invoked when "object eviction", not removal explicitly. We should use `internalCache.asMap().computeIfPresent()` instead, which I think will fix the issue I mentioned…
- _…13 more comments_

## KAFKA-15482: kafka.utils.TestUtils Depends on MockTime Which is Not in Any Jar
Bug · Closed (Invalid) · Major · created 2023-09-20 · resolved 2023-09-20

Commit 
7eea2a3908fdcee1627c18827e6dcb5ed0089fdd 
Moved it to server-commons, but it is not included in the jar.

- **Ismael Juma:** Can you please provide more details on how you arrived to the conclusion that the class is not in the jar? Note that it would be in the server-commons _test_ jar.
- **Gary Russell:** My apologies; I didn't see that jar in Maven Central.
 Please close.

## KAFKA-15483: Update metrics documentation for the new metrics implemented as part of KIP-938
Task · Resolved (Fixed) · Major · components: docs, documentation · created 2023-09-21 · resolved 2023-10-04

Update the kafka-site documentation for 3.6 release with the newly introduced metrics in 3.6 for KIP-938.

- **Satish Duggana:** [~cmccabe] [~mumrah] Please help in updating the kafka-site documentation for 3.6 release with the newly introduced metrics in 3.6 for KIP-938.
- **Satish Duggana:** [~mumrah] Assigning it to you as you raised [PR-548|https://github.com/apache/kafka-site/pull/548] to address this issue.
- **ASF GitHub Bot:** satishd commented on code in PR #548: URL: https://github.com/apache/kafka-site/pull/548#discussion_r1333360366 ########## 36/ops.html: ########## @@ -1980,6 +1980,28 @@ <h5 class="anchor-heading"><a id="kraft_quorum_monitoring" class="anchor-link"><      <td>The average fraction of time the client'…
- **ASF GitHub Bot:** satishd commented on PR #548: URL: https://github.com/apache/kafka-site/pull/548#issuecomment-1729990446    @mumrah  I do not see the documentation in the latest kafka-site docs for the below metrics that are part of KIP-866, correct me if I missed them in the existing docs. 
    ```
    ZkWriteBehi…
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

- **Ron Dagostino:** > Is this caused by that in KRaft protocal, Kafka doesn't not elect leaders immediately after a new topic created but rather do that on-demand after receiving the first message on the topic? 
 No, that is not correct.  The leader for each partition is identified at the time the topic-partition is cr…
- **Xi Yang:** Thanks for your reply [~rndgstn]. 
 >If the broker is responding that it does not know about that partition then it could be the case that it has not replicated and acted upon the records in the metadata log that created the partition and identified it as the leader.
 But in this case, there is only…
- **Xi Yang:** I print out the topic description after creating the topic. It looks like the partitions are correctly elected before Trogdor starts producing messages. However, the producer still reports the NOT_LEADER_OR_FOLLOWER error.
 Topic desc:(name=foo1, internal=false, partitions=(partition=0, leader=local…

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

- **John Roesler:** Hey [~hanyuzheng] , thanks for the bug report!
 I agree with you that if there is exactly one partition responding and it responds with a FailedQueryResult, then it could make sense to return it instead of throwing an exception.
 However, I do want to clarify that an expected usage of this method is…
- **Matthias J. Sax:** Thanks for the details [~vvcephei]!
 {quote}In other words, it should return the result if and only if all queried partitions responded successfully AND at most one partition returned a non-null result.
 {quote}
 This was the unclear piece to me, ie, what's the actual user contract.
 About exception…

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
- **Apoorv Mittal:** Another failure: https://ci-builds.apache.org/blue/organizations/jenkins/Kafka%2Fkafka-pr/detail/PR-14699/21/tests/
 [code/log omitted]
- **Apoorv Mittal:** Failure of test: `testAbortTransactionTimeout` in `TransactionsWithTieredStoreTest` class
 https://ci-builds.apache.org/blue/organizations/jenkins/Kafka%2Fkafka-pr/detail/PR-15251/7/tests
 [code/log omitted]
- **Apoorv Mittal:** Flaky Test: org.apache.kafka.tiered.storage.integration.TransactionsWithTieredStoreTest."testFencingOnSend(String).quorum=kraft"
 [https://ci-builds.apache.org/job/Kafka/job/kafka-pr/job/PR-16890/3/testReport/org.apache.kafka.tiered.storage.integration/TransactionsWithTieredStoreTest/Build___JDK_21_…
- **Kamal Chandraprakash:** Both TransactionsTest and TransactionsWithTieredStoreTest are flaky. From my recent runs:
 ```
 FAILED ❌ TransactionsWithTieredStoreTest > "testFencingOnSend(String).quorum=zk"
 FAILED ❌ TransactionsTest > "testSendOffsetsWithGroupId(String).quorum=zk"
 ```

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

- **Francois Visconte:** [~ckamal] Any idea on how to move forward on that? I think having to configure a very high fetch.max.wait defeat the purpose of the KIP of not having to proceed adaptations on the consumer side.
 This issue is annoying on our test environment (using s3): even with a fetch.max.wait of 2s we get flood…
- **Kamal Chandraprakash:** [~fvisconte] 
 We are cancelling the currently executing fetch [task|https://sourcegraph.com/github.com/apache/kafka@92a67e8571500a53cc864ba6df4cb9cfdac6a763/-/blob/core/src/main/scala/kafka/server/DelayedRemoteFetch.scala?L86] when the timeout happens. When the remote storage degrades, then the con…
- **Kamal Chandraprakash:** > I think having to configure a very high fetch.max.wait defeat the purpose of the KIP of not having to proceed adaptations on the consumer side.
 Kindly elaborate on this.
- **Francois Visconte:** [~ckamal] What I mean is that one of the interesting property of tiered storage is not having to change anything on the consumer side because the consumer protocol is unchanged. In our case, we have to go over every consumers to adapt their settings, and even with that we have suboptimal consumer pe…
- **Jorge Esteban Quilcate Otoya:** Agree with [~fvisconte] that tweaking an existing config on the consumer side it's undesired given that Tiered Storage aims to be transparent to clients.
 An additional issue even when caching fetch requests is that remote fetch doesn't only fetch the log segment but potentially also the offset inde…
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

