from .base_model import BaseModel
from ..helpers import RedisCacheConfig
from ..helpers.redis_helper import RedisClient


class CountryConfigStructure:
    ID = "_id"
    KEY = "key"
    CONFIGS = "configs"


class RankConfigStructure:
    RANK = "rank"
    KEY = "key"
    FIELD = "field"
    FIELD_CODE = "field_code"


class CountryConfigModel(BaseModel):

    def __init__(self):
        super().__init__()
        self.collection = "country_configs"

    def find_one_by_key(self, key):
        key_cache = RedisCacheConfig.COUNTRY_CONFIG_KEY.format(key=key)
        value_cache = RedisClient().get(key=key_cache)
        if value_cache:
            return value_cache
        data = self.find_one(
            query={
                CountryConfigStructure.KEY: key
            }
        )
        if data:
            data = RedisClient().set(key=key_cache, value=data)
        return data


if __name__ == '__main__':
    data = CountryConfigModel().find_one({})
    print(data)
