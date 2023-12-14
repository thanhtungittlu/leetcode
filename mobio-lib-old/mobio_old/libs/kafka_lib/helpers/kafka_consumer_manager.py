import json
from abc import abstractmethod
from copy import deepcopy
from datetime import datetime, timedelta
from confluent_kafka.cimpl import KafkaError, KafkaException, Consumer
from mobio.libs.kafka_lib import RequeueStatus, KAFKA_BOOTSTRAP
from mobio.libs.kafka_lib.helpers import consumer_warning_slack
from mobio.libs.kafka_lib.models.mongo.requeue_consumer_model import (
    RequeueConsumerModel,
)
from time import time, sleep
from uuid import uuid4
from os.path import exists
import os


class BaseKafkaConsumer:
    def __init__(
            self,
            topic_name: object,
            group_id: object,
            client_mongo,
            retryable=True,
            session_timeout_ms=15000,
            bootstrap_server=None,
            consumer_config=None
    ):
        self.client_id = str(uuid4())
        self.group_id = group_id
        config = {
            "bootstrap.servers": KAFKA_BOOTSTRAP if not bootstrap_server else bootstrap_server,
            "group.id": group_id,
            "auto.offset.reset": "latest",
            "session.timeout.ms": session_timeout_ms,
            "client.id": self.client_id,
            'error_cb': self.error_cb,
        }
        if consumer_config:
            config.update(consumer_config)
        c = Consumer(
            config
        )
        self.client_mongo = client_mongo
        self.retryable = retryable

        self.topic_name = topic_name
        try:
            c.subscribe([self.topic_name])
            print("consumer %s is started" % self.topic_name)

            # Add mapping client-id kafka and pod name
            # Lưu file consumer theo group
            DATA_DIR = os.environ.get("APPLICATION_DATA_DIR")
            folder_path = "{}/{}/{}".format(DATA_DIR, 'kafka-liveness-consumer', group_id)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            # Add mapping client-id kafka and pod name
            file_path = "{folder_path}/{client_id}".format(folder_path=folder_path, client_id=self.client_id)
            # Save relationship pods and topic
            host_name = os.environ.get("HOSTNAME")
            f = open(file_path, "w")
            pod_data_info = "{host_name}".format(host_name=host_name)
            f.write(pod_data_info)
            f.close()

            while True:
                msg = c.poll(1.0)

                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        print(
                            "%% %s [%d] reached end at offset %d\n"
                            % (msg.topic(), msg.partition(), msg.offset())
                        )
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    try:
                        key = msg.key()
                        message = msg.value().decode("utf-8")
                        payload = json.loads(message)

                        start_time = time()

                        self.process(payload, key)
                        end_time = time()
                        print(
                            "end: {} with total time: '[{:.3f}s]".format(
                                self.topic_name, end_time - start_time
                            )
                        )
                    except Exception as e:
                        print(
                            "MessageQueue::run - topic: {} ERR: {}".format(
                                self.topic_name, e
                            )
                        )
        except RuntimeError as e:
            print("something unexpected happened: {}: {}".format(self.topic_name, e))
        except KafkaException as e:
            print("KafkaException: {}: {}".format(self.topic_name, e))
        finally:
            print("consumer is stopped")
            c.close()
            consumer_warning_slack(pod_name=os.environ.get("HOSTNAME"), group_id=self.group_id,
                                   pretext="Consumer closed")
            sleep(30)
            raise Exception("Consumer closed")

    def error_cb(self, err):
        print("Client error: {}".format(err))
        consumer_warning_slack(pod_name=os.environ.get("HOSTNAME"), group_id=self.group_id,
                               pretext="client error: {}".find(err))

    def process(self, data, key=None):
        count_err = 0
        if self.retryable:
            recall_data = deepcopy(data)
        else:
            recall_data = None
        try:
            if "count_err" in data:
                count_err = int(data.pop("count_err"))
            self.message_handle(data=data)
        except Exception as e:
            print("consumer::run - topic: {} ERR: {}".format(self.topic_name, e))
            if recall_data and self.retryable:
                count_err += 1
                data_error = {
                    "topic": self.topic_name,
                    "key": key.decode("ascii") if key else key,
                    "data": recall_data,
                    "error": str(e),
                    "count_err": count_err,
                    "next_run": datetime.utcnow() + timedelta(minutes=5 + count_err),
                    "status": RequeueStatus.ENABLE
                    if count_err <= 10
                    else RequeueStatus.DISABLE,
                }
                result = RequeueConsumerModel(self.client_mongo).insert(data=data_error)
                print("RequeueConsumerModel result: {}".format(result))

    @abstractmethod
    def message_handle(self, data):
        pass
