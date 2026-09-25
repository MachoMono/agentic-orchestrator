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

- **Greg Harris:** The BlockingConnectorTest which was leaking the client in our tests was remediated with [https://github.com/apache/kafka/pull/12290] .
 The core flaw still exists, so I'm going to leave this ticket open.
- **Will Perlichek:** Hi [~gharris1727] do you know if this ticket is still relevant? 
 I was looking into flaky test failures in https://issues.apache.org/jira/browse/KAFKA-15891 (I have notes in the comments) and now I am wondering if this could be the root cause of the zombie sink tasks which cause the flaky tests, an…

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
- **Proven Provenzano:** Hi [~sergio_troiano@hotmail.com] 
 I would suggest opening a PR for trunk first so that it can then be cherry-picked to 3.7 branch before code freeze.
 The 3.6 and 3.5 point releases have already shipped and this isn't a security issue that needs to be immediately addressed so we have more time to g…
- **Sergio Troiano:** Thanks as usual [~pprovenzano]  :)
 I will open then only the PR for trunk , I will update the ticket when the PR is ready
- **Sergio Troiano:** Pr open,
 [https://github.com/apache/kafka/pull/15030]
 Thanks!

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
- **Kirk True:** Per KAFKA-7605, this test has been flaky since 2018, so it's not specific to the "new" consumer.
 Per [Develocity|https://develocity.apache.org/scans/tests?search.relativeStartTime=P90D&search.rootProjectNames=kafka&search.timeZoneId=America%2FLos_Angeles&tests.container=kafka.api.SaslSslConsumerTes…

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
- **Kamal Chandraprakash:** [~anatolypopov] 
 Could you write an integration test to simulate the error scenario? You can refer to some of the existing [tests|https://sourcegraph.com/github.com/apache/kafka@trunk/-/blob/storage/src/test/java/org/apache/kafka/tiered/storage/integration/BaseReassignReplicaTest.java]. Thanks!
- **Anatolii Popov:** Hi [~ckamal] unfortunately it is really hard to write an integration test for this since the actual issue is a race condition. 
 Instead, I updated a PR with a proper fix with a more detailed explanation of what is happening and why. Hope this helps. Please take a look when you have time.

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

## KAFKA-16112: Review JMX metrics in Async Consumer and determine the missing ones
Task · Resolved (Fixed) · Critical · components: clients, consumer, metrics · labels: consumer-threading-refactor, metrics · created 2024-01-10 · resolved 2024-01-12

- **Philip Nee:** These are the results of this ticket
 |KAFKA-16113|
 |KAFKA-16116|
 |KAFKA-16115|

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
- **Johnny Hsu:** the exception is from [https://github.com/apache/kafka/blob/9b8aac22ec7ce927a2ceb2bfe7afd57419ee946c/core/src/main/scala/kafka/server/BrokerServer.scala#L474]
 when the cluster starts, [https://github.com/apache/kafka/blob/9b8aac22ec7ce927a2ceb2bfe7afd57419ee946c/core/src/test/java/kafka/testkit/Kaf…
- **Jun Rao:** Also saw the following test failure in https://github.com/apache/kafka/actions/runs/16300736076/job/46035062600?pr=20137
 [code/log omitted]

## KAFKA-16175: Flaky test: testAsynchronousAuthorizerAclUpdatesDontBlockRequestThreads – kafka.api.SslAdminIntegrationTest
Bug · Open · Major · created 2024-01-19

[https://ci-builds.apache.org/blue/organizations/jenkins/Kafka%2Fkafka-pr/detail/PR-15190/3/tests/]
[code/log omitted]


## KAFKA-16176: Flaky test: testSendToPartitionWithFollowerShutdownShouldNotTimeout – kafka.api.PlaintextProducerSendTest
Bug · Resolved (Fixed) · Major · components: clients, consumer, producer  · labels: integration-test, kip-848-client-support · created 2024-01-19 · resolved 2024-11-19

[https://ci-builds.apache.org/blue/organizations/jenkins/Kafka%2Fkafka-pr/detail/PR-15190/3/tests/]
[code/log omitted]

- **Kirk True:** [~apoorvmittal10]—I am getting this error when testing using the Consumer running with the {{CONSUMER}} group protocol. Do you know if that's the way your test was configured?
 When I run the test using the {{CLASSIC}} group protocol, I can run it 25 times in a row without an error. When I run it wi…
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

- **Will Perlichek:** Hi, [~schofielaj] 
 According to my crude Develocity query (link below), testMetricsDuringTopicCreateDelete has continued to be very flaky, as recently at this week
 I have two preliminary (newbie) questions before I consider picking this up:
 1) Should we mark this with a flaky annotation? How to k…
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
- **Matthias J. Sax:** Seems [~vrushankpatel] did not reply to my last comment. Let's re-assign to you.
 This might be a larger body of work. Please break it out into multiple smaller PRs, maybe one per method? This simplifies reviewing, and speeds up merging.
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

- **Greg Harris:** Hi [~janardhanag], thanks for the ticket.
 At the current time, the offset syncs topic cannot have more than 1 partition. If more than one partition is present, the MirrorSourceTask will only write to partition 0, and the MirrorCheckpointTask will only read from partition 0. Changes to both of these…
- **Janardhana Gopalachar:** HI [~gharris1727] 
 while processing 24k events/second, MM2 internal topic gets 10k events/sec. is the event load the internal topic is getting. Is there any parameters that can be tuned so that CPU load on the broker instance for the internal topic leader can be distributed 
 Regards
 Jana
- **Janardhana Gopalachar:** HI [~gharris1727] 
 Currently in our mirror maker spec  we have offset.lag.max: 0, so should it be set to max 100, Will this reduce the through put on source topics or target topic, 
 Is the offset.lag.max value set to 0 is contributing for CPU load ?
 what would be value that could be set if it to…
- **Greg Harris:** Hi [~janardhanag] Yes, you should consider increasing offset.lag.max. 0 is best for precise offset translation, but can significantly increase the amount of traffic on the offset-syncs topic.
 For topics without offset gaps (e.g. not compacted, not transactional) the offset.lag.max currently behaves…
- **Janardhana Gopalachar:** Hi [~gharris1727] 
 We tried to perform test in out local setup , we observed for the scenario
 If messages were written in the Source Kafka  Cluster and the target Kafka cluster is created after a delay , then the no of messages written to mm2-offsetsyncsinternal  is doubled. Is this the expected b…
- _…1 more comments_

## KAFKA-16345: Optionally allow urlencoding clientId and clientSecret in authorization header
Bug · Resolved (Fixed) · Minor · labels: kip · created 2024-03-05 · resolved 2024-07-09

When a client communicates with OIDC provider to retrieve an access token RFC-6749 says that clientID and clientSecret must be urlencoded in the authorization header. (see [https://tools.ietf.org/html/rfc6749#section-2.3.1)] However, it seems that in practice some OIDC providers do not enforce this, so I was thinking about introducing a new configuration parameter that will optionally urlencode clientId & clientSecret in the authorization header. 
Link to the KIP https://cwiki.apache.org/conflu…

- **Kirk True:** [~bachmanity1]—changed the status to reflect that fact that you've already submitted a patch for review.
 Thanks again for catching this!

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
- **Chia-Ping Tsai:** {quote}
 Considering it's a small change you should be able to directly cherry-pick it on 3.7. and 3.6.
 {quote}
 will copy that
- _…2 more comments_

## KAFKA-16348: Fix flaky TopicCommandIntegrationTest.testDescribeUnderReplicatedPartitionsWhenReassignmentIsInProgress
Bug · Open · Minor · created 2024-03-06

[code/log omitted]


## KAFKA-16349: ShutdownableThread fails build by calling Exit with race condition
Bug · Resolved (Fixed) · Minor · components: core · created 2024-03-06 · resolved 2024-03-29

`ShutdownableThread` calls `Exit.exit()` when the thread's operation throws FatalExitError. In normal operation, this calls System.exit, and exits the process. In tests, the exit procedure is masked with Exit.setExitProcedure to prevent tests that encounter a FatalExitError from crashing the test JVM.
Masking of exit procedures is usually done in BeforeEach/AfterEach annotations, with the exit procedures cleaned up immediately after the test finishes. If the body of the test creates a Shutdowna…

- **Ismael Juma:** Good catch.
- **Greg Harris:** I did some more exploration here.
  # Some of the "exit 1" failures I included in my count earlier are caused by https://issues.apache.org/jira/browse/KAFKA-15343 and so was an overestimate. This particular failure doesn't happen all that often.
  # There are more places affected than just those usi…
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
- **Jeremy Norris:** Yes, if you cannot publish a fixed version of 3.7.0 artifact, then a new 3.7.1 release should be spun.
 The 3.7.0 artifact is simply broken.
- _…5 more comments_

## KAFKA-16360: Release plan of 3.x kafka releases.
Improvement · Resolved (Invalid) · Major · created 2024-03-11 · resolved 2024-03-12

KIP [https://cwiki.apache.org/confluence/display/KAFKA/KIP-833%3A+Mark+KRaft+as+Production+Ready#KIP833:MarkKRaftasProductionReady-ReleaseTimeline] mentions ,
h2. Kafka 3.7
 * January 2024
 * Final release with ZK mode
But we see in Jira, some tickets are marked for 3.8 release. Does apache continue to make 3.x releases having zookeeper and kraft supported independent of pure kraft 4.x releases ?
If yes, how many more releases can be expected on 3.x release line ?

- **Greg Harris:** Hi [~kaushik srinivas], thanks for your question!
 The release schedule in that KIP was superseded by a later KIP: [https://cwiki.apache.org/confluence/display/KAFKA/KIP-1012%3A+The+need+for+a+Kafka+3.8.x+release] and so is not accurate any longer.
 At this time, we expect that 3.8 will be the last…
- **Justine Olshan:** Hey there – there was some discussion on the mailing list. 3.8 should be the last release. See here: [https://lists.apache.org/thread/kvdp2gmq5gd9txkvxh5vk3z2n55b04s5] 
 There is also a KIP. KIP-1012: [https://cwiki.apache.org/confluence/display/KAFKA/KIP-1012%3A+The+need+for+a+Kafka+3.8.x+release]…
- **Matthias J. Sax:** Please don't use Jira to ask questions. Jira tickets are for bug reports and features only.
 Question should be asked on the user and/or dev mailing lists: https://kafka.apache.org/contact

## KAFKA-16361: Rack aware sticky assignor minQuota violations
Bug · Open · Major · components: clients · created 2024-03-11

In some low topic replication scenarios the rack aware assignment in the StickyAssignor fails to balance consumers to its own expectations and throws an IllegalStateException, commonly crashing the application (depending on application implementation). While uncommon the error is deterministic, and so persists until the replication state changes. 
We have observed this in the wild in 3.5.1, and 3.6.1. We have reproduced it locally in a test case in 3.6.1 and 3.7.0 (3.5.1 we did not try but like…

- **Laymain:** Hi there, we have the exact same problem here, I was about to open an issue.
 If it can help, here are some log involving only two hosts (i-0da0437e61e61bf88 and i-0d2e25eb1aebefab5): [^illegalstateexception.log]
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

- **Greg Harris:** cc [~mjsax] [~ableegoldman] I looked through the (currently ignored) rawtypes warnings in Streams and this was one that I really didn't have a simple resolution for, and I think needs a real refactor to make type-safe.
 I don't think there's a bug hidden here, but the code didn't give me any confide…
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
- **Divij Vaidya:** Hey [~dajac] 
 Not yet. The author of the PRs attached is on vacation and will be back this Monday. This is their top priority next week. We are currently stuck on failing tests and discovered some inconsistencies with streams tests such as embedded server having a time which is in the past compared…
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
- **Matthias J. Sax:** CloseOption was introduced via [https://cwiki.apache.org/confluence/display/KAFKA/KIP-812%3A+Introduce+another+form+of+the+%60KafkaStreams.close%28%29%60+API+that+forces+the+member+to+leave+the+consumer+group]
 The reasoning about the design should be on the KIP and corresponding DISCUSS thread.
 I…
- **A. Sophie Blee-Goldman:** I haven't gone back and re-read the KIP, but IIRC the reason for adding these CloseOptions was specific to solving an issue with static membership, hence why it only takes affect there.
 That said – I completely agree that there's no reason why this should only work with static membership, and the d…
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

- **Muralidhar Basani:** [~jsancio] can I look into this ? Seems like adding 4 new arguments
 standalone
 controller-quorum-voters
 feature
 release-version
- **José Armando García Sancio:** Yes, please go ahead. That's correct [~muralibasani] . --release-version is less important and is bit trickier to implement see this KIP [https://cwiki.apache.org/confluence/display/KAFKA/KIP-1022%3A+Formatting+and+Updating+Features.] I am okay if we don't want to implement it in this PR/Jira and we…
- **Muralidhar Basani:** [~jsancio] have a draft pr opened for adding 'standalone'
 It basically does the below.
  * It expects a metadaa log dir to exist
  * If dir exists, a meta.properties file is created if it doesn't exist.
  * a random id is generated and written to file directory.id
 what do you think, if am in the r…
- **José Armando García Sancio:** HI [~muralibasani] ,
 All of the new options are under the format command (e.g. {{{}kafka-storage format ...{}}}). The format command already exist and does some of the functionality you describe above like storing the directory.id in the meta.properties. This PR needs to extend this code to support…
- **Muralidhar Basani:** Hi [~jsancio] I see it has to be extended under format command.
 And yes directory.id is already written under format command [here|https://github.com/apache/kafka/blob/trunk/core/src/main/scala/kafka/tools/StorageTool.scala#L456]. Should this be done only with 'standalone' ? So we don't write direc…
- _…5 more comments_

## KAFKA-16519: Expose the supported and finalized kraft.version in ApiVersions response
Sub-task · Resolved (Duplicate) · Major · components: core · created 2024-04-11 · resolved 2024-07-22

- **Josep Prat:** Changing target fix version to 3.9 since this is not a blocker and we are past code freeze
- **José Armando García Sancio:** This was resolved as part of another issue and pr.
- **Colin McCabe:** Removing fix version 3.9 for this duplicate JIRA since it is confusing release.py

## KAFKA-16520: Changes to DescribeQuorum response
Sub-task · Resolved (Fixed) · Major · components: kraft · created 2024-04-11 · resolved 2024-06-12

- **Nikolay Izhikov:** Hello [~jsancio]
 Do you need help with this ticket? 
 I'm ready to work on it.
- **José Armando García Sancio:** Yes [~nizhikov] you can take it. You'll need it for kafka-metadata-quorum describe changes for KIP-853.
 Looking at the schema changes I suggested, it looks like I never added:
 [code/log omitted]
 As suggested by the CLI output:
 [code/log omitted]
 I updated the KIP to include this new field in th…
- **Nikolay Izhikov:** Hello [~jsancio] 
 Do we want to enhance FetchRequest inside this PR? Or I can leave DirectoryId equals to null for cases when `ReplicaState` created while handling FetchRequest?
- **José Armando García Sancio:** {quote}Do we want to enhance FetchRequest inside this PR?
 {quote}
 [~nizhikov] , I won't do that part. I am currently working on implementing those changes now as part of https://issues.apache.org/jira/browse/KAFKA-16527
 {quote}Or I can leave DirectoryId equals to null for cases when `ReplicaState…
- **Nikolay Izhikov:** [https://github.com/apache/kafka/pull/16106] ready for review.

## KAFKA-16521: kafka-metadata-quorum describe changes for KIP-853
Sub-task · Resolved (Fixed) · Major · components: tools · created 2024-04-11 · resolved 2024-08-01

# [https://cwiki.apache.org/confluence/display/KAFKA/KIP-853%3A+KRaft+Controller+Membership+Changes#KIP853:KRaftControllerMembershipChanges-describe--status]
 # [https://cwiki.apache.org/confluence/display/KAFKA/KIP-853%3A+KRaft+Controller+Membership+Changes#KIP853:KRaftControllerMembershipChanges-describe--replication]

- **Nikolay Izhikov:** Hello, [~jsancio]
 I have a question regarding KIP:
 [code/log omitted]
 First example [code/log omitted] and the second [code/log omitted] - double minus sign used for different words.
 Is it some kind of typo? Or command format must be exactly like in the KIP?
- **José Armando García Sancio:** Yes. It is a typo. It should be {{{}describe --replication{}}}:
 [code/log omitted]
 I updated the KIP.
 Note that for {{{}describe --status{}}}, you wont be able to implement the committed voters output:
 [code/log omitted]
 I haven't implemented that functionality in the controller side. If we mer…
- **José Armando García Sancio:** [~nizhikov] are you currently working on this? I ask because [~alyssahuang] may pick this up.
- **Nikolay Izhikov:** Hello, [~jsancio] 
 I will provide a patch in a till end of the week.
- **Alyssa Huang:** Hey [~nizhikov], the 3.9.0 release branch was cut and an exception was made for cherry-picking in this item, so we need this in asap - I'm free this week to work on this item so I'll start working on it. 
 If your patch was ready though, just let me know and I can help review instead

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

## KAFKA-16684: FetchResponse#responseData could return incorrect data
Bug · Resolved (Fixed) · Minor · created 2024-05-07 · resolved 2024-07-09

[https://github.com/apache/kafka/commit/2b8aff58b575c199ee8372e5689420c9d77357a5] make it accept input to return "partial" data. The content of output is based on the input but we cache the output ... It will return same output even though we pass different input. That is a potential bug.

- **Chia-Ping Tsai:** After [https://github.com/apache/kafka/commit/2b8aff58b575c199ee8372e5689420c9d77357a5] , I don't think the "cache" is useful. Hence, we can just remove the cache to fix this potential bug
- **Johnny Hsu:** hi [~chia7712] 
 May i know if you are working on this? if not I am happy to help :)
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
- **Dmitry Werner:** [~m1a2st] Hello, are you working on this task?
 I can grab issue if you have no time.
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
- **Chia-Ping Tsai:** {quote}
 the trunk builds still run the full suite
 {quote}
 The README says that we run both "build" and "test" for 11 and 17, but we don't run "test" for 11 and 17, right?
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

- **Chia-Chuan Yu:** Hi, [~chia7712] 
 Can I have this one please? thanks!
- **TaiJuWu:** After discussed with [~chiacyu] offline, I will take it over.
- **Lan Ding:** Hi [~taijuwu], are you still working on this? I would like to take over otherwise.
- **TaiJuWu:** Hi [~isding_l] , this ticket was finished for a long time but it lacks reviewers.
 After finding any reviewer, I will continue to work on this.

## KAFKA-17038: KIP-919 supports for `alterPartitionReassignments` and `listPartitionReassignments`
Sub-task · Resolved (Fixed) · Minor · created 2024-06-25 · resolved 2024-08-27

as title

- **Kuan Po Tseng:** Hi [~chia7712] , If you are not currently working on this issue, I am willing to take it over. Many thanks !

## KAFKA-17039: KIP-919 supports for `unregisterBroker`
Sub-task · Resolved (Fixed) · Minor · created 2024-06-25 · resolved 2025-03-01

as title

- **TengYao Chi:** Gentle ping  [~chia7712] ,if you are not start working I would like to handle this issue
- **TengYao Chi:** Hi [~chia7712] 
 It seems that our test infra currently only support the controller with plaintext security protocol and it will be a blocker to test the describeDelegationToken and describeUserScramOptions. :P
- **Lan Ding:** Hi [~frankvicky],  If this ticket is still open, may I take it over?
- **TengYao Chi:** Hi [~isding_l] 
 Thanks for the interest.
 However, I have already a local patch for this one.
 Feel free to browse other issue. :)

## KAFKA-17040: Unknown telemetry state: TERMINATED thrown when closing AsyncKafkaConsumer
Bug · Resolved (Fixed) · Major · components: clients, metrics · labels: consumer-threading-refactor · created 2024-06-25 · resolved 2024-12-11

An error is occasionally thrown when closing the {{{}AsyncKafkaConsumer{}}}:
[code/log omitted]
The issue appears to be that the {{TERMINATED}} state is not expected in the switch statement inside [timeToNextUpdate()|https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/common/telemetry/internals/ClientTelemetryReporter.java#L307].
As an aside, the error message might make more sense to be written as "{_}Unexpected{_} telemetry state" instead of "{_}Unknown{_} tele…

- **Apoorv Mittal:** [~kirktrue] Thanks for reporting, I can take it up. Just a quick question, the error only occurs while closing the consumer, correct? Is it under scenarios when consumer close took more time than next network client poll time? I expect that's the only scenario when this issue can occur. I am just wo…
- **Lianet Magrans:** Hey [~apoorvmittal10] , in case it helps, I believe this issue happens when the consumer close cannot wait for the network thread to close (ex. close with low timeout or interrupted). This flow:
  # async consumer app thread triggers action to close network thread, and block until it completes (won'…
- **Apoorv Mittal:** Thanks [~lianetm] for adding details. I have created a PR: [https://github.com/apache/kafka/pull/18143,] let me know if it makes sense.

## KAFKA-17041: Add pagination when describe large set of metadata via Admin API 
Improvement · Open · Major · components: admin · created 2024-06-26

Some of the request via Admin API timeout on large cluster or cluster with large set of specific metadata. For example OffsetFetchRequest and DescribeLogDirsRequest timeout due to large number of partition on cluster. Also DescribeProducersRequest and ListTransactionsRequest time out due to too many short lived PID or too many hanging transactions
[KIP-1062: Introduce Pagination for some requests used by Admin API|https://cwiki.apache.org/confluence/display/KAFKA/KIP-1062%3A+Introduce+Paginatio…

- **dujian0068:** Hello：
 Can I take this task?
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

- **Ksolves India Limited:** The file named MetadataLogConfig is written in Scala which is in location kafka/core/src/main/scala/kafka/MetadataLogConfig.scala 
 and the separate raft package contains the files written in Java.
 If you are referring this, then we have to create MetadataLogConfig or create a scala package into ra…
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
- **Bruno Cadonna:** In the end, we got both options. [~alisa23] implemented the backoff solution in https://github.com/apache/kafka/pull/17209 and [~danicafine] implemented reduced logging in https://github.com/apache/kafka/pull/16705.
 Like it!

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

- **Greg Harris:** Hi [~vbalani] Thank you for the bug report! I can reproduce it locally.
 I believe that this should be a cosmetic error, as the error is thrown when the classpath JsonConverter is found via the each plugin.path. These later get excluded to avoid duplicates: [https://github.com/apache/kafka/blob/25d7…

## KAFKA-17112: StreamThread shutdown calls completeShutdown only in CREATED state
Bug · Closed (Fixed) · Minor · components: streams, unit tests · created 2024-07-10 · resolved 2024-08-23

While running tests in `StreamThreadTest.java` in kafka/streams, I noticed the test left many lingering threads. Though the class runs `shutdown` after each test, the shutdown only executes `completeShutdown` if the StreamThread is in CREATED state. See [https://github.com/apache/kafka/blob/0b11971f2c94f7aadc3fab2c51d94642065a72e5/streams/src/test/java/org/apache/kafka/streams/processor/internals/StreamThreadTest.java#L231] and [https://github.com/apache/kafka/blob/0b11971f2c94f7aadc3fab2c51d946…

- **Bruno Cadonna:** [~aoli-al] I think you are right. We are leaking the state updater and processing threads in that test. The issue is that when we create the stream thread we create and start the state updater thread and the processing threads. 
 Would you be interested to fix this issue?
- **Ao Li:** Yes, I'm happy to submit a patch. I'm thinking of two potential fixes: 
 1. extend the `shutdown()` method to `shutdown(boolean forceCleanup)`. 
 [code/log omitted]
 2. make `completeShutdown` public and directly call it from the test. 
 Which one do you think is better?
- **Bruno Cadonna:** [~aoli-al] I think it would be better to change where the state updater and the processing threads are started. I am not sure why we start the threads before we start the stream thread. If we start those threads in the same location where we start the stream thread, we should not need to change anyt…
- **Ao Li:** [~cadonna] Aren't stateUpdater and processingThread expected to be started in some tests since the parameterized tests control them.
 [code/log omitted]
 and here 
 [code/log omitted]
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

- **Ksolves India Limited:** [~mjsax] I would like to work on creating the necessary KIPs and work on this ticket. However, we need Confluence account which we requested earlier as well. Can you help us to provide the same? 
 Comment where I asked for access - https://issues.apache.org/jira/browse/INFRA-25451?focusedCommentId=1…
- **Matthias J. Sax:** I cannot help with creating a Confluence account, however, your account should have been created according to https://issues.apache.org/jira/browse/INFRA-25451?focusedCommentId=17867582&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-17867582 ?
 If your account was no…
- **Ksolves India Limited:** [~mjsax] For now, we didn't get Confluence access. We'll follow up there.
 In the meantime, we'll review the comments on attached PR & the POC one.

## KAFKA-17216: StreamsConfig STATE_DIR_CONFIG
Bug · Resolved (Invalid) · Major · components: streams · created 2024-07-30 · resolved 2024-08-25

I can't use the class StreamsConfig 
it fail with         Caused by: java.lang.ExceptionInInitializerError at StreamsConfig.java:866
problem is not present in 3.7.0

- **Chia-Ping Tsai:** [~raphaelauv] Could you share more details to us? for example, how to reproduce the error you described?
- **Matthias J. Sax:** The only PR which comes to mind with regard to state.dir is this one: [https://github.com/apache/kafka/commit/d233eb98f7c7e55fe0dd673dbc058ddf619663a7] – otherwise it should be the same between 3.7 and 3.8.
 As Chia-Ping said, can you provide more details (eg full stack trace, and also what value fo…
- **Matthias J. Sax:** Just saw this other comment: [https://github.com/apache/kafka/pull/13909#discussion_r1696207016]
 Reading between the lines, sounds like a version mix of older `kafka-clients.jar` and 3.8 `kafka-streams.jar`?
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

- **Kirk True:** Thanks for tracking this down, [~dongnuolyu].
 What perplexes me is that we'd uncovered many similar issues in our initial migration of the system tests to support the new consumer. We'd found the same root issue before, namely that the new consumer takes some time to stabilize its groups. Our fix w…
- **Dongnuo Lyu:** ??it's really odd to me that we're still seeing these??
 -Yeah at least in `consumer_test` the fix is missing. We can add them back when AK is unblocked.-
 Oh we do have {{wait_until}} fixes, it's just missing in {{test_consumer_bounce}} and {{test_broker_rolling_bounce}}. It should also fixes the p…
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
