import os
from copy import deepcopy

from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic
import random
from mobio.libs.kafka_lib import MobioEnvironment, KAFKA_BOOTSTRAP
import inspect


class EnsureKafkaTopic:
    TOPIC_NAME = "topic"
    NUM_PARTITIONS = "num_partitions"
    REPLICATION_FACTOR = "replication_factor"
    CONFIG = "config"
    REPLICATION_ASSIGNMENT = "replica_assignment"

    @classmethod
    def get_all_property(cls):
        attributes = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
        values = [
            a[1]
            for a in attributes
            if not (a[0].startswith("__") and a[0].endswith("__"))
        ]
        return values

    def create_kafka_topics(self, lst_topic: list):
        all_property = self.get_all_property()
        new_topics = []
        admin_client = AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP})
        existing_topics = list(admin_client.list_topics().topics.keys())
        for topic in lst_topic:
            if topic.get(self.TOPIC_NAME) not in existing_topics:
                if not topic.get(self.REPLICATION_FACTOR):
                    topic[self.REPLICATION_FACTOR] = int(
                        os.getenv(MobioEnvironment.KAFKA_REPLICATION_FACTOR)
                    )
                if not topic.get(self.NUM_PARTITIONS):
                    topic[self.NUM_PARTITIONS] = 8
                if not topic.get(self.REPLICATION_ASSIGNMENT) and os.getenv(
                    MobioEnvironment.DEFAULT_BROKER_ID_ASSIGN
                ):
                    topic[self.REPLICATION_ASSIGNMENT] = os.getenv(
                        MobioEnvironment.DEFAULT_BROKER_ID_ASSIGN
                    )
                if topic.get(self.REPLICATION_ASSIGNMENT):
                    lst_assignment = []
                    lst_broker = [
                        int(x.split(":")[0])
                        for x in topic.get(self.REPLICATION_ASSIGNMENT).split(",")
                    ]
                    for i in range(topic.get(self.NUM_PARTITIONS)):
                        random.shuffle(lst_broker)
                        lst_assignment.append(
                            deepcopy(lst_broker)[: topic.get(self.REPLICATION_FACTOR)]
                        )
                    topic[self.REPLICATION_ASSIGNMENT] = lst_assignment
                    topic[self.REPLICATION_FACTOR] = None
                conf = {x: topic.get(x) for x in all_property if topic.get(x)}
                new_topics.append(NewTopic(**conf))
        if new_topics:
            fs = admin_client.create_topics(new_topics, operation_timeout=30)

            # Wait for each operation to finish.
            for topic, f in fs.items():
                try:
                    f.result()  # The result itself is None
                    print("New Topic {} created".format(topic))
                except Exception as e:
                    print("Failed to create new topic {}: {}".format(topic, e))

    def delete_kafka_topics(self, lst_topic: list):
        admin_client = AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP})
        fs = admin_client.delete_topics(lst_topic, operation_timeout=30)

        # Wait for each operation to finish.
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                print("Topic {} deleted".format(topic))
            except Exception as e:
                print("Failed to delete topic {}: {}".format(topic, e))


def create_kafka_topics(lst_topic):
    admin_client = AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP})
    existing_topics = list(admin_client.list_topics().topics.keys())
    new_topics = []
    for required_topic in lst_topic:
        if required_topic not in existing_topics:
            new_topics.append(
                NewTopic(
                    required_topic,
                    num_partitions=4,
                    replication_factor=int(
                        os.getenv(MobioEnvironment.KAFKA_REPLICATION_FACTOR)
                    ),
                )
            )
        else:
            print("Topic {} existed".format(required_topic))

    if new_topics:
        fs = admin_client.create_topics(new_topics)

        # Wait for each operation to finish.
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                print("New Topic {} created".format(topic))
            except Exception as e:
                print("Failed to create new topic {}: {}".format(topic, e))


def create_kafka_topics_v2(lst_topic):
    admin_client = AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP})
    existing_topics = list(admin_client.list_topics().topics.keys())
    new_topics = []
    for required_topic in lst_topic:
        if (
            type(required_topic) != tuple
            or len(required_topic) < 2
            or type(required_topic[1]) != int
            or type(required_topic[0]) != str
            or required_topic[1] < 1
        ):
            raise Exception("{} is not valid".format(required_topic))
        if required_topic[0] not in existing_topics:
            new_topics.append(
                NewTopic(
                    required_topic[0],
                    num_partitions=required_topic[1],
                    replication_factor=int(
                        os.getenv(MobioEnvironment.KAFKA_REPLICATION_FACTOR)
                    ),
                    config=required_topic[2]
                    if len(required_topic) == 3 and type(required_topic[2]) is dict
                    else {},
                )
            )
        else:
            print("Topic {} existed".format(required_topic[0]))

    if new_topics:
        fs = admin_client.create_topics(new_topics)

        # Wait for each operation to finish.
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                print("New Topic {} created".format(topic))
            except Exception as e:
                print("Failed to create new topic {}: {}".format(topic, e))


if __name__ == "__main__":
    EnsureKafkaTopic().create_kafka_topics(
        [
            # TEST WITH SET replica_assignment
            {
                EnsureKafkaTopic.TOPIC_NAME: "giang-test1",
                EnsureKafkaTopic.NUM_PARTITIONS: 8,
                EnsureKafkaTopic.CONFIG: {"compression.type": "snappy"},
                EnsureKafkaTopic.REPLICATION_ASSIGNMENT: os.getenv(
                    MobioEnvironment.SALE_BROKER_ID_ASSIGN  # SALE_BROKER_ID_ASSIGN
                )  # danh sách các broker_ids "10,20,30" ,
            },
            # TEST WITH SET replica_factor
            {
                EnsureKafkaTopic.TOPIC_NAME: "giang-test2",
                EnsureKafkaTopic.REPLICATION_ASSIGNMENT: os.getenv(
                    MobioEnvironment.PROFILING_BROKER_ID_ASSIGN
                )
            },
            # TEST WITH SET config
            {
                EnsureKafkaTopic.TOPIC_NAME: "giang-test3",
                EnsureKafkaTopic.NUM_PARTITIONS: 1,
                EnsureKafkaTopic.CONFIG: {"compression.type": "snappy"},
                EnsureKafkaTopic.REPLICATION_ASSIGNMENT: os.getenv(
                    MobioEnvironment.JB_BROKER_ID_ASSIGN
                )
            },
            # TEST WITHOUT manual config
            {
                EnsureKafkaTopic.TOPIC_NAME: "giang-test4",
                EnsureKafkaTopic.NUM_PARTITIONS: 1,
            },
        ]
    )
    # EnsureKafkaTopic().delete_kafka_topics(lst_topic=["giang-test{}".format(x) for x in range(10)])
