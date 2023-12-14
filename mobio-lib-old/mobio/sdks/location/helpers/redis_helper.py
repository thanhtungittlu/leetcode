import os
from datetime import timedelta
import datetime

import redis
import uuid
from bson import ObjectId, Decimal128
import json

from mobio.libs.Singleton import Singleton

ENV_REDIS_URI = os.getenv("REDIS_URI")

# 1 hour
REDIS_EXPIRE_DEFAULT = 3600


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif type(o) == datetime.date:
            a = datetime.datetime.combine(o, datetime.datetime.min.time())
            return a.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        elif type(o) == datetime.datetime:
            return o.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        elif isinstance(o, uuid.UUID):
            return str(o)
        elif isinstance(o, (bytes, bytearray)):
            return str(o, "utf-8")
        elif isinstance(o, Decimal128):
            return str(o)
        return json.JSONEncoder.default(self, o)


@Singleton
class RedisClient:
    redis_client = redis.from_url(ENV_REDIS_URI, decode_responses=True)

    def getConnection(self):
        if self.redis_client is None:
            self.redis_client = redis.from_url(ENV_REDIS_URI, decode_responses=True)
        return redis.Redis(connection_pool=self.redis_client)

    def set(self, key, value, expire_time=REDIS_EXPIRE_DEFAULT):
        value = JSONEncoder().encode(value)
        self.redis_client.set(key, value, ex=expire_time)
        result = json.loads(value)
        return result

    def get(self, key):
        data_cache = self.redis_client.get(key)
        if isinstance(data_cache, str):
            data_cache = json.loads(data_cache)
        return data_cache

    def delete(self, key):
        self.redis_client.delete(key)
        return True

    def delete_by_prefix(self, prefix):
        for key in self.redis_client.scan_iter(prefix + "*"):
            self.redis_client.delete(key)

    def increase(self, name, key="count", amount=1):
        result = self.redis_client.hincrby(name=name, key=key, amount=amount)
        if result == 1:
            self.redis_client.pexpire(name=name, time=timedelta(days=3))
        return result
