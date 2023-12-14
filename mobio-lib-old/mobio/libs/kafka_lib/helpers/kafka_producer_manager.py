import json
from confluent_kafka.cimpl import Producer, KafkaException, KafkaError
from mobio.libs.Singleton import Singleton

from mobio.libs.kafka_lib import KAFKA_BOOTSTRAP


def error_cb(err):
    print("Client error: {}".format(err))
    if err.code() == KafkaError._ALL_BROKERS_DOWN or \
       err.code() == KafkaError._AUTHENTICATION:
        # Any exception raised from this callback will be re-raised from the
        # triggering flush() or poll() call.
        raise KafkaException(err)


@Singleton
class KafkaProducerManager:
    producer = Producer(
                {
                    "request.timeout.ms": 20000,
                    "bootstrap.servers": KAFKA_BOOTSTRAP,
                    "compression.type": "zstd",
                    "linger.ms": 10,
                    # 'error_cb': error_cb,
                })

    def flush_message(self, topic: str, key: str, value):
        self.producer.produce(
            topic=topic,
            key=key,
            value=json.dumps(value).encode("utf-8"),
            on_delivery=self.kafka_delivery_report,
        )
        self.producer.poll(0)

    def kafka_delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print("Message delivery failed: {}".format(err))
        else:
            print('message delivery to: {}, {}'.format(msg.topic(), msg.partition()))
