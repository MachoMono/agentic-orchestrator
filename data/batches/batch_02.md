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
- **F Méthot:** Hi [~guozhang] Thanks for your feedback.
 We were puzzled by this error that kept coming back on partition 9 on our consumer 
 [code/log omitted]
 Even after after we had deleted and recreated that source topic, got rid of Exactly_once, even deleted the __transaction topic. 
 The pattern was:
  * We…
- **Guozhang Wang:** I looked into the source code and I have a suspicion it is a broker side bug. Here's my theory:
 * In the transaction coordinator, when we want to send markers to the data partition hosts, there's a condition that if the leader of that data partition is unknown, then we would skip sending this marke…
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

- **Cheng-Kai, Zhang:** Hi [~dongjin]  [~mimaison]
 I am interested to this issue, and it seems to be manageable for a newbie like me.  Do you think I could help on this one?
 My plan is to follow current structure [~mimaison]  currently working on to add those config. There is a draft PR in a very early stage available [h…
- **Mickael Maison:** Dongjin had written a KIP ([KIP-780|https://cwiki.apache.org/confluence/display/KAFKA/KIP-780%3A+Support+fine-grained+compression+options]) but it hasn't been accepted.
 I'm currently working on getting [KIP-390|https://cwiki.apache.org/confluence/display/KAFKA/KIP-390%3A+Support+Compression+Level],…
- **Cheng-Kai, Zhang:** [~mimaison]  much thanks for providing me with more detail. :)
 I would start by studying the changes in your [PR|https://github.com/apache/kafka/pull/15516] and figure out how to further add in features of KIP-780

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

- **Matthias J. Sax:** Not sure if I understand this request. Also, what do you mean by "SQL Processor"?
 What are "the existing configured Alert channels" ?

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

- **shylaja kokoori:** After enabling SSL logging (javax.net.debug=ssl,handshake),
 I see that unwrap call in the SslTransportLayer.read function returns handshakeStatus=NEED_WRAP when ssl key_update takes place. (log snippet below)
 Based on documentation provided in [https://datatracker.ietf.org/doc/html/rfc8446]
 key_u…
- **Ismael Juma:** [~skokoori] Thanks for the report. Can you please submit a pull request? See https://kafka.apache.org/contributing .
- **Ismael Juma:** cc [~rajinisivaram@gmail.com]
- **shylaja kokoori:** [~ijuma] Thank you. Let me test with the latest trunk and will submit a pull request
- **Yiming Zang:** Thanks [~skokoori] for creating this issue, and [~ijuma] for reviewing the pull request. This will solve the TLS issue Twitter has been seeing since upgrading to 2.7 with TLS 1.3
- _…4 more comments_

## KAFKA-13419: sync group failed with rebalanceInProgress error might cause out-of-date ownedPartition in Cooperative protocol
Bug · Resolved (Fixed) · Major · components: clients · created 2021-10-29 · resolved 2022-02-23

In KAFKA-13406, we found there's user got stuck when in rebalancing with cooperative sticky assignor. The reason is the "ownedPartition" is out-of-date, and it failed the cooperative assignment validation.
Investigate deeper, I found the root cause is we didn't reset generation and state after sync group fail. In KAFKA-12983, we fixed the issue that the onJoinPrepare is not called in resetStateAndRejoin method. And it causes the ownedPartition not get cleared. But there's another case that the…

- **Kirk True:** [~showuon] - this Jira is marked as in progress, yet I see that the corresponding PR has been merged already. Is this still in progress? If not, please update the fixed version and mark as fixed.
 Thanks!
- **Luke Chen:** [~kirktrue] , thanks for the reminder. Updated.
- **Shawn Wang:** Hi [~showuon] 
 After i applied this fix and my previous change to make this fix work[https://github.com/apache/kafka/pull/12140, |https://github.com/apache/kafka/pull/12140]what we are seeing is that: sometimes consumer will revoker almost all partitions with cooperative enabled.
 detail:
  * we ha…
- **A. Sophie Blee-Goldman:** {quote}  can we just treat the ownedPartition in previous generation legal if there are no same partition claimed by other member? 
 {quote}
 Huh, I thought that's already what the cooperative assignor does? Maybe we intentionally left/took it out of the constrained case algorithm for some reason? O…
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

- **RivenSun:** Hi [~showuon] and  [~guozhang],
 Do you have any suggestions for this issue?
 I think we can take the first and second points from Suggestion & Solutions to consider solving this problem.
 WDYT?
- **Luke Chen:** [~RivenSun], I haven't read through all the description, but I guess it's this issue. Please take a look: [https://github.com/apache/kafka/pull/11430]
- **RivenSun:** [~showuon]
 These are two problems.
  My problem is that the jaasConf file between each broker is the same
 [code/log omitted]
 and
 [code/log omitted]
 But the password sent by ClientBroker is the password "admin_scram_password" in ScramLoginModule.  The password expected by ServerBroker is "kJTVDz…
- **Luke Chen:** [~RivenSun], I've read through all the content. Nice RCA! It makes sense to me. However, I'm not quite familiar with the jaas component, and might not be the good person to ask for comments. I'd suggest that since you've traced the source codes and found the suspicious (or bug) places, you can try t…
- **RivenSun:** Hi [~showuon] , 
 Thank you for taking time to read through this issue :D
 And hi [~rajinisivaram@gmail.com] , [~ijuma] and [~manikumar]
 Can you read this issue and give some suggestions
  Thanks
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

- **RivenSun:** Hi [~showuon] and  [~guozhang],
 Do you have any suggestions for this issue?
 Thanks.
- **Guozhang Wang:** Hello [~RivenSun], for such scenario, my common recommendation is to use {Consumer#pause / resume} functions. I.e. when the blocking queue is full and {publish} failed, the consumer could pause all the currently assigned partitions, and then subsequent {Consumer#poll} would return no more data but o…
- **RivenSun:** [~guozhang] hello，Thank you for your reply
 Please take more time to read through this issue
 At the beginning, I did try it like your advice, and my approach is more violent.. When blocking queue is full or push failed, pause will be called before every poll call, but the poll method will *still re…
- **Luke Chen:** [~RivenSun], thanks for reporting this issue. But I think the original design of pause/resume is that:
 *Rebalance does not preserve pause/resume state.* (check KAFKA-2350)
 So, back to your suggestions:
  # Precise semantics of kafkaConsumer#pause(…)
  --> I agree that the java doc is not clear abo…
- **RivenSun:** Haha,  [~showuon] thank you for your reply and recognition of me:D
 1. Thank you for your suggestion, and I think it is better to print the relevant prompt log when cleaning the paused mark.
 2.
 {quote}{{When we execute invokePartitionsRevoked(revokedPartitions), do we consider the need to clean up…
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
- **Randall Hauch:** Merged to the following branches:
 * `trunk` for the next 3.2 release
 * `3.1` for the upcoming 3.1.0 release
 * `3.0` for the next 3.0.1 patch release

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
- **Igor Shipenkov:** Well, I tried version 3.0.0 and I can reproduce this problem on it just fine. Same "SSL handshake failed" error, still can see old client certificate in traffic dump.
 Guess I'll just add this to affected version too.
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

- **Luke Chen:** [~willian.wd] , thanks for reporting the issue. Did this issue happen in Kafka-clients v2.8.x? Also, did you `flush()` the producer, or set `autoFlush` in spring katkaTemplate? 
 Thanks.
- **Luke Chen:** And, please also provide the producer config. Thank you.
- **Willian Dallastella:** [~showuon] I just tested with 2.8.1 and also works fine, the issue is just with 3.0.0.
 Also, there is no auto-flush set, here is my kafka config:
 [code/log omitted]
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
- **Derek Troy-West:** This represents a breaking change where:
  # Broker version is < 2.8.0
  # Cluster has ACL configured, but no IDEMPOTENT_WRITE permission set
  # Producer has default configuration (or no config captured in KAFKA-13673)
  # Kafka Client library version is bumped to 3.2.0 in the producing application…
- _…4 more comments_

## KAFKA-13599: Upgrade RocksDB to 6.27.3
Task · Resolved (Fixed) · Major · components: streams · created 2022-01-18 · resolved 2023-02-24

RocksDB v6.27.3 has been released and it is the first release to support s390x. RocksDB is currently the only dependency in gradle/dependencies.gradle without s390x support.
RocksDB v6.27.3 has added some new options that require an update to streams/src/main/java/org/apache/kafka/streams/state/internals/RocksDBGenericOptionsToDbOptionsColumnFamilyOptionsAdapter.java but no other changes are needed to upgrade.
A compatibility report is attached for the current version 6.22.1.1 -> 6.27.3

- **Bruno Cadonna:** Hi [~jonathan.albrecht]! 
 Thank you for the analysis!
 Are you interested in opening a PR for the upgrade?
- **Jonathan Albrecht:** Hi [~cadonna],
 Yes, I'm testing a PR right now. I'm just in the process of requesting to be added to the jira contributer's list so I can assign this to myself.

## KAFKA-13600: Rebalances while streams is in degraded state can cause stores to be reassigned and restore from scratch
Bug · Resolved (Fixed) · Major · components: streams · created 2022-01-19 · resolved 2022-03-28

Consider this scenario:
 # A node is lost from the cluster.
 # A rebalance is kicked off with a new "target assignment"'s(ie the rebalance is attempting to move a lot of tasks - see https://issues.apache.org/jira/browse/KAFKA-10121).
 # The kafka cluster is now a bit more sluggish from the increased load.
 # A Rolling Deploy happens triggering rebalances, during the rebalance processing continues but offsets can't be committed(Or nodes are restarted but fail to commit offsets)
 # The most c…

- **Guozhang Wang:** [~tim.patterson] Thanks for filing this ticket.
 I'd like to clarify a few things to help my own understanding here: in step 5, "The most caught up nodes now aren't within `acceptableRecoveryLag` and so the task is started in it's "target assignment" location" could you explain a bit more about this…
- **Tim Patterson:** [~guozhang] Thats the desired result and the change I've made.
 The current Implementation in Master only considers placing the task on nodes returned by this method
 [https://github.com/apache/kafka/blob/trunk/streams/src/main/java/org/apache/kafka/streams/processor/internals/assignment/HighAvailab…
- **Tim Patterson:** Thinking about it, the same problem can be hit when we lose a node and some of the standby tasks for the lost actives have fallen a bit behind for whatever reason, In this case it wont promote the standbys to actives but instead start restoring those tasks from scratch on some other node
- **Bruno Cadonna:** [~tim.patterson] I checked the assignor code and I agree with you that we only distinguish between caught-up and not caught-up. IIRC, we decided to go that way since considering task load and the rank of non caught-up clients turned out to be more complicated that we wanted to make the assignment al…
- **Tim Patterson:** Thanks [~cadonna] 
 I'm not sure I have the perfect solution either, more just raising this to point out a bit of a hole in the existing implementation.
 I do wonder if simply changing the definition of "caught up" in `tasksToCaughtUpClients` from "within acceptableRecoveryLag of the head of the cha…
- _…6 more comments_

## KAFKA-13601: Add option to support sync offset commit in Kafka Connect Sink
New Feature · Resolved (Won't Do) · Major · components: connect · created 2022-01-19 · resolved 2022-04-06

Exactly once in s3 connector with scheduled rotation and field partitioner can be achieved with consumer offset sync' commit after message batch flushed to sink successfully
Currently, WorkerSinkTask committing the consumer offsets asynchronously and at regular intervals of WorkerConfig.OFFSET_COMMIT_INTERVAL_MS_CONFIG 
[https://github.com/apache/kafka/blob/371f14c3c12d2e341ac96bd52393b43a10acfa84/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSinkTask.java#L203]
[https:…

- **Chris Egerton:** [~dasarianil] I don't see how synchronous offset commits would guarantee exactly once. What if the worker dies in between the task writing data and its consumer committing an offset?
- **Anil Dasari:** Filed partitioner uses starting offset of the batch in the file name and is the only varying parameter. There will be only one parquet file per worker (consumer/partition) (that is out of sync with offsets) present in destination (s3 in my case) if worker dies before committing an offset. So new or…
- **Chris Egerton:** Thanks for the clarification! Doesn't that mean that this new behavior wouldn't actually provide exactly-once guarantees?
 As an aside–I believe that, when configured correctly, the Confluent S3 sink connector already provides exactly-once guarantees (or at least, something close to them) by perform…
- **Anil Dasari:** Hello [~ChrisEgerton] , thanks for the response. new proposed option provides exactly once guarantees in case of field partitioner and size or time rotation based flush strategy considering no duplicates in kafka topic.
 S3 sink connector can provide exactly once guarantee with async offset commit o…
- **Chris Egerton:** Sorry, I don't think this is correct:
 {quote}new proposed option provides exactly once guarantees in case of field partitioner and size or time rotation based flush strategy considering no duplicates in kafka topic.
 {quote}
 What would be necessary for exactly-once in this situation is either dete…
- _…1 more comments_

## KAFKA-13602: Allow to broadcast a result record
New Feature · Resolved (Fixed) · Major · components: streams · labels: kip, newbie++ · created 2022-01-20 · resolved 2022-12-30

From time to time, users ask how they can send a record to more than one partition in a sink topic. Currently, this is only possible by replicate the message N times before the sink and use a custom partitioner to write the N messages into the N different partitions.
It might be worth to make this easier and add a new feature for it. There are multiple options:
 * extend `to()` / `addSink()` with a "broadcast" option/config
 * add `toAllPartitions()` / `addBroadcastSink()` methods
 * allow S…

- **Florin Akermann:** Hi [~sagarrao] , [~mjsax] 
 May I have a go at this?
- **Sagar Rao:** Hey @florin , I have already sent out a Kip for this. Here is the link : [https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=211883356.|https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=211883356]
 Review is awaited still. You can also share your review comments on the d…
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
- **Stanislav Savulchik:** Hi, [~Kvicii].
 I propose to just log the exception of a returned failed Future in order to make it visible in logs because right now we have no traces of the problem.
 Re-throwing the exception seems a bad option to me because a task could sync offsets of many consumer groups and we shouldn't preve…
- **Kvicii.Yu:** [~savulchik] 
 Therefore, my understanding is that we should call partitionResult in the method syncGroupOffset to handle whether an exception occurs, and record the log if an exception occurs.

## KAFKA-13607: Cannot use PEM certificate coding when parent defined file-based
Bug · Open · Major · components: clients, config, connect · created 2022-01-21

The problem applies to the situation when we create a Kafka client based on prepopulated config. If we have only partial control on the input we can attempt to reset some values.
KIP-651 added a new cool feature to use PEM coding of certificates as an alternative to file stores. I have observed a problem in Confluent Replicator. We have shifted the common configuration to the worker level and assumed the connectors define only what is specific for them. The security setup is mTLS, i.e. we need…

- **Kirk True:** [~psmolinski] - if you're working on this, can you assign the Jira to yourself? Thanks.
- **Sergey Ivanov:** Hello,
 We also faced an issue with DefaultSslEngineFactory.java
 In our case we use Kafka Connect with config provider, which has the following properties:
 [code/log omitted]
 And base on real Kafka connection properties the Conmfig Provider includes coresponding values. For example, for Kafka wit…

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

- **Jorge Esteban Quilcate Otoya:** I've experienced this messages on Kafka Datagen Source Connector using Confluent Platform (7.0.1) / Apache Kafka 3.0.1.
 Very confusing, thought there was an issue, but data was still been produced.
 Lowering the log level to DEBUG make sense to me.
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

- **Abhijit:** On the ppc64le VM provided to community, I built kafka & ran UT and IT. All passed (one failure that passed on re-run). jdk-11 and scala-2.13 was used. Logs attached.
 I am yet to hear back on the Jira (https://issues.apache.org/jira/browse/INFRA-22612). A jenkins build stage can be added for ppc64l…
- **Mickael Maison:** I've opened a PR to run unit tests on the ppc64le node. It looks like there's a permission issue as tests are failing to access /tmp:
 For example:
 java.nio.file.AccessDeniedException: /tmp/kafka-streams/dummy-topology-test-driver-app-id--1504216085/0_0/.checkpoint
 See https://ci-builds.apache.org…
- **Abhijit:** I cleared the /tmp dir that contained some stale dirs from previous runs. Now, the unit tests should be able to run.

## KAFKA-13672: Race condition in DynamicBrokerConfig
Bug · Resolved (Fixed) · Blocker · created 2022-02-16 · resolved 2022-03-24

Stacktrace:
[code/log omitted]
Job: https://ci-builds.apache.org/job/Kafka/job/kafka-pr/job/PR-11751/5/testReport/

- **Bruno Cadonna:** https://ci-builds.apache.org/job/Kafka/job/kafka-pr/job/PR-11752/8/testReport/kafka.server/DynamicBrokerReconfigurationTest/Build___JDK_11_and_Scala_2_13___testThreadPoolResize__/
 [code/log omitted]
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
- **Hong Yi Zhang:** Code has been merged into the trunk in the below PR:
 https://github.com/apache/kafka/pull/11793

## KAFKA-13675: Null pointer exception with kafka streams application reset tool with --to-datetime
Bug · Open · Major · created 2022-02-17

When I try to run the the reset tool with {{{}--to-datetime{}}}, such as:
[code/log omitted]
{{I get the following exception}}
[code/log omitted]
Note when I run the above with --to-earliest or --to-offset instead of {{-to-datetime, the tool runs successfully.}}

- **Bruno Cadonna:** [~pcallahan] thank you for the report,
 This seems to be a duplicate of https://issues.apache.org/jira/browse/KAFKA-9527.
 Could you confirm that this is fixed in 3.0.0?

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
- **Luke Chen:** >  I get the same behavior with 2.2.0.
 Oh, really!
 > it probably makes more sense to update the quickstart.
 Maybe we can have a better definition about what we expected to be shown in the `configs` value. My understanding is it showed the overridden configs. If so, it should be a bug. If not, we…
- **Richard Joerger:** I'd love to help out on this particular Jira. I'm new to the project so I apologize for any silly questions. It seems that we as a community need to discuss what the output of the kafka-topics tooling should look like. When we're looking at the documentation, I don't see any documentation explicitly…
- **Deng Ziming:** Hello [~rjoerger] 
  # this issue is enough to track the problem so another issue is unnecessary
  # We are not intend to include default `segment.bytes` in the output but it was printed(due to an bug), but this bug has been around for a long time so [~mimaison] suggest we keep this bug in the futur…
- **Luke Chen:** Thanks for the answers, [~dengziming] !
 [~rjoerger] , as Ziming said, we are unsure the root cause of this issue. Maybe you can investigate it first, and see if you find anything. My thought is that, since we didn't provide any new configs during create topics:
 _> bin/kafka-topics.sh --create --to…
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

- **Dhirendra Singh:** Some more information
 split brain issue is happening with the controller.
 when brokers (including the active controller) lose connection with zookeeper, for few seconds 2 brokers are the active controller.
 following is the log of broker 1 and broker 0. At the time when connection to zookeeper was…
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

- **Matthias J. Sax:** We needed to revet one PR for 4.1 release, as it introduces a regression bug: [https://github.com/apache/kafka/pull/18292]
 Re-opening to make sure we complete this issue with 4.2 release – as we did only revert in 4.1 branch, but not in trunk, also filed https://issues.apache.org/jira/browse/KAFKA-…

## KAFKA-13723: max.compaction.lag.ms implemented incorrectly
Bug · Resolved (Not A Problem) · Major · components: core · created 2022-03-09 · resolved 2022-03-09

In https://issues.apache.org/jira/browse/KAFKA-7321, we introduced max.compaction.lag.ms to guarantee that a record be cleaned before a certain time. 
The implementation in LogCleanerManager has the following code. The path for earliestDirtySegmentTimestamp < cleanUntilTime seems incorrect. In that case, it seems that we should set the delay to 0 so that we could trigger cleaning immediately since the segment has been dirty for longer than max.compaction.lag.ms. 
[code/log omitted]

- **Jun Rao:** [~xiongqiwu] and [~jjkoshy]  : Could you check if this is a real issue? Thanks.
- **xiongqi wu:** [~junrao]  Hi Jun, this function is supposed to capture violation that pass-by the max compaction delay. 
 e.g, 
 if maxCompactionDelay > 0, which mean it has violated the policy (e.g, the log is not compacted within the maxCompaction config time), and the log should be compact immediately. 
 if max…
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
- **Colin McCabe:** As of 3.3, we now use {{config.brokerHeartbeatIntervalMs}} as the deadline
 It should be a good improvement for clusters under load

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

- **RivenSun:** Hi [~omkreddy]  [~guozhang] and  [~showuon] 
 Could you give some advice?
 Thanks.
- **RivenSun:** Hi [~dajac]  [~rsivaram]
 Could you give some suggestions for this issue?
 Thanks.

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

- **Sree Vaddi:** Work Around:
 - restart the broker node. ({*}tried and worked{*})
 - clear the lock file of offset / partition / consumer / consumer group in zk data.folder.

## KAFKA-13759: Disable producer idempotence by default in producers instantiated by Connect
Bug · Resolved (Fixed) · Major · components: connect · created 2022-03-22 · resolved 2022-03-23

https://issues.apache.org/jira/browse/KAFKA-7077 was merged recently referring to KIP-318. Before that in AK 3.0 idempotence was enabled by default across Kafka producers. 
However, some compatibility implications were missed in both cases. 
If idempotence is enabled by default Connect won't be able to communicate via its producers with Kafka brokers older than version 0.11. Perhaps more importantly, for brokers older than version 2.8 the {{IDEMPOTENT_WRITE}} ACL is required to be granted to t…

- **Konstantine Karantasis:** This issue has been now been merged on the 3.2 and 3.1 branches to avoid a breaking change when Connect contacts older brokers and idempotence is enabled in the producer by default. 
 [~cadonna] [~tombentley] fyi. 
 Hopefully this fix makes to the upcoming releases but please let me know if the targ…

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
- **Dongjin Lee:** Hi [~yyu1993] [~showuon],
 It seems like this issue is a counterpart of LOG4J2-3256, which disables logging from {{org.apache.kafka.common}} and {{org.apache.kafka.clients}} packages. How about add a similar logic to log4j-appender?
- **Ismael Juma:** I suggest we do the simplest change first (disable idempotence) and then follow up with more complicated change.
- _…1 more comments_

## KAFKA-13762: Kafka brokers are not coming up 
Bug · Open · Blocker · created 2022-03-23

Out of 9 brokers only 3 brokers coming up. Totally 3 VMs Each VM is having 3 brokers
We are getting below error 
Exception in thread "main" java.lang.reflect.InvocationTargetException

- **Jordan Moore:** [~kkameshm90] Please lower the priority as it is not a project blocker.
 Your error is caused by the JMX exporter from Prometheus you've custom added to your broker startup process, and so is really unrelated to any issues with Kafka project.
 You need to stop whatever other process has already boun…

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

- **Bruno Cadonna:** [~shivakumar] Are you referring to the following CVE?
 https://nvd.nist.gov/vuln/detail/CVE-2020-36518
 This CVE seems to affect 2.8.1, 3.0.1 but not 3.1.1 and 3.2.0 since the latter ones use 2.12.6.1 (see  KAFKA-13658).
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

- **Daniel Urban:** Connector configs are used for consumer/producer overrides, converter classes, etc.
 Not necessary to propagate all configs to tasks.
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

- **ASF GitHub Bot:** divijvaidya opened a new pull request, #420: URL: https://github.com/apache/kafka-site/pull/420    As per the [Apache privacy policy](https://privacy.apache.org/faq/committers.html), Google Fonts are recommended to be hosted along with the website.
    This change  adds the fonts locally in the code…
- **Divij Vaidya:** Fixed "It's using Google Fonts" -> [https://github.com/apache/kafka-site/pull/420] 
 [~mimaison] please review.
- **ASF GitHub Bot:** divijvaidya commented on PR #420: URL: https://github.com/apache/kafka-site/pull/420#issuecomment-1183179393    @ijuma @mimaison please review.
- **ASF GitHub Bot:** divijvaidya opened a new pull request, #421: URL: https://github.com/apache/kafka-site/pull/421    **Why**
    As per the [Apache branching policy](https://www.apache.org/foundation/marks/pmcs#navigation), every project website's main navigation system must feature certain text links back to key pag…
- **Divij Vaidya:** Addressed "It's missing a link to the privacy policy" -> [https://github.com/apache/kafka-site/pull/421]
 cc: [~mimaison] for review
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

- **Matthias J. Sax:** I think you mix up two concepts: windowing is about "grouping" records according to their timestamp. Thus, the _window-size_ you define via `TimeWindows.withSizeAndGrace()` (or similar) defines into which window a record falls into.
 On the other hand suppression has nothing to do with the definitio…

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
- **Jack Vanlightly:** I presume you would need to perform a broker decommissioning process to remove that broker from the cluster before adding a new empty broker with the same id?
 Is there documentation for how to decommission a dead broker safely?
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
- **Guozhang Wang:** I've re-tested this case locally with 5+ times, each with 50 runs, and identified it is a flakiness by itself, not a real bug. The fix is summarized in https://github.com/apache/kafka/pull/12468.
 On a side note, I think it's an overkill to really introduce the whole test class as an integration tes…

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

- **Matthias J. Sax:** > we see in the kafka UI 
 There is no "Kafka UI" – at least not as part of Apache Kafka. If you are using some other "external" UI, it's unclear how they compute/display the lag.
 Two thories:
  * The don't sum the lag over all partitions but take the max over all partitions?
  * They compute the l…
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
- **Colin McCabe:** I believe this is KAFKA-13649, which was fixed recently.
 The issue came about because we accidentally shared the same authorizer object between c-located controller and broker.

## KAFKA-13938: Jenkins builds are timing out after streams integration tests
Task · Open · Major · components: build · created 2022-05-25

Jenkins PR builder is sporadically failing with timeouts. A few examples:
https://ci-builds.apache.org/job/Kafka/job/kafka-pr/view/change-requests/job/PR-12136/5/execution/node/137/log/
https://ci-builds.apache.org/job/Kafka/job/kafka-pr/view/change-requests/job/PR-12207/1/execution/node/137/log/
https://ci-builds.apache.org/job/Kafka/job/kafka-pr/view/change-requests/job/PR-12062/7/execution/node/138/log/
In these examples, the timeout occurs after 
22:14:00  streams-5: SMOKE-TEST-CLIENT-C…

- **Jason Gustafson:** I looked at a few of the recent builds. It seems like one of the recently kraft-converted tests in `LogOffsetTest` is hanging. 
 For example: [https://ci-builds.apache.org/job/Kafka/job/kafka-pr/view/change-requests/job/PR-12062/7/execution/node/138/log/]
 We see this test started on jdk17:
 ```
 *1…
- **Jason Gustafson:** I posted a PR to add a timeout to `LogOffsetTest` here: https://github.com/apache/kafka/pull/12213.
- **João Pedro Fonseca:** Hi, [~mumrah]! Since Jenkins was disabled yesterday, could this taks be closed?

## KAFKA-13939: Memory Leak When Logging Is Disabled In InMemoryTimeOrderedKeyValueBuffer
Bug · Resolved (Fixed) · Blocker · components: streams · created 2022-05-25 · resolved 2022-06-16

If `loggingEnabled` is false, the `dirtyKeys` Set is not cleared within `flush()`, see [https://github.com/apache/kafka/blob/3.2/streams/src/main/java/org/apache/kafka/streams/state/internals/InMemoryTimeOrderedKeyValueBuffer.java#L262.] However, dirtyKeys is still written to in the loop within `evictWhile`. This causes dirtyKeys to continuously grow for the life of the buffer.

- **Jackson Newhouse:** One way to patch this would be something like
 [code/log omitted]
 Since `loggingEnabled` is final, we can just not track the dirty keys. The set is only read from if `loggingEnabled` is true.
- **Jackson Newhouse:** If you search Stack Overflow you'll find occasional instances of people running into this problem, such as [https://stackoverflow.com/questions/59239783/kafka-streams-suppressed-feature-causes-oom-heavy-gc] 
 and
 [https://stackoverflow.com/questions/70651437/kafka-stream-oom-out-of-memory|https://s…
- **Matthias J. Sax:** Thanks for reporting this issue – sound rather severs – I bumped the priority to blocker.
 As you already have a fix, would you like to open a PR on GitHub?
- **Guozhang Wang:** Thanks [~jnewhouse], I looked at the code you pointed it out and I agree it's a bug indeed, and should be fixed asap. Please let us know if you'd like to open a PR to fix it.
- **Jackson Newhouse:** I'll open a PR.
- _…3 more comments_

## KAFKA-13940: DescribeQuorum returns INVALID_REQUEST if not handled by leader
Bug · Resolved (Fixed) · Major · created 2022-05-25 · resolved 2022-08-17

In `KafkaRaftClient.handleDescribeQuorum`, we currently return INVALID_REQUEST if the node is not the current raft leader. This is surprising and doesn't work with our general approach for retrying forwarded APIs. In `BrokerToControllerChannelManager`, we only retry after `NOT_CONTROLLER` errors. It would be more consistent with the other Raft APIs if we returned NOT_LEADER_OR_FOLLOWER, but that also means we need additional logic in `BrokerToControllerChannelManager` to handle that error and re…


## KAFKA-13941: Re-enable ARM builds following INFRA-23305
Task · Resolved (Fixed) · Major · components: build · created 2022-05-26 · resolved 2022-05-27

Once https://issues.apache.org/jira/browse/INFRA-23305 is resolved, we should re-enable ARM builds in the Jenkinsfile.

- **Divij Vaidya:** [~mumrah] ARM build have been timing out consistently lately. The problem might have resurfaced. Could you please look into it or guide the community on how to debug the root cause? Note that the failing ARM build almost always causes the entire build to fail.
 Example: https://ci-builds.apache.org/…

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
- **Divij Vaidya:** I have fixed the bug which was causing a snapshot with LONG_MAX at [https://github.com/apache/kafka/pull/12224] 
 Also note that there are other tests such as QuorumControllerTest.testSnapshotOnlyAfterConfiguredMinBytes failing due to same bug
 [code/log omitted]

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

