import os

from mobio.libs.caching import LruCache, StoreType


class ConsumerGroup:
    DEFAULT_CONSUMER_GROUP_ID = "mobio-consumers"


class RequeueStatus:
    ENABLE = 0
    DISABLE = -1


class MobioEnvironment:
    HOST = 'HOST'
    ADMIN_HOST = 'ADMIN_HOST'
    REDIS_URI = 'REDIS_URI'
    REDIS_HOST = 'REDIS_HOST'
    REDIS_PORT = 'REDIS_PORT'
    KAFKA_BROKER = 'KAFKA_BROKER'
    KAFKA_REPLICATION_FACTOR = 'KAFKA_REPLICATION_FACTOR'
    YEK_REWOP = 'YEK_REWOP'
    DEFAULT_BROKER_ID_ASSIGN = "DEFAULT_BROKER_ID_ASSIGN"
    SALE_BROKER_ID_ASSIGN = "SALE_BROKER_ID_ASSIGN"
    PROFILING_BROKER_ID_ASSIGN = "PROFILING_BROKER_ID_ASSIGN"
    JB_BROKER_ID_ASSIGN = "JB_BROKER_ID_ASSIGN"


KAFKA_BOOTSTRAP = os.getenv(MobioEnvironment.KAFKA_BROKER)

lru_cache_kafka = LruCache(
    store_type=StoreType.REDIS,
    # config_file_name=APP_CONFIG_FILE_PATH,
    cache_prefix="kafka_lib_",
    redis_uri=os.getenv(MobioEnvironment.REDIS_URI),
)
