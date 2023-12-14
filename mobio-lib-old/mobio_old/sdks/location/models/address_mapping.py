from .base_model import BaseModel
from ..helpers import RedisCacheConfig
from ..helpers.redis_helper import RedisClient


class AddressMappingStructure:
    ID = "_id"
    MERCHANT_ID = "merchant_id"
    ADDRESS_ID = "address_id"
    MAPPING_VALUE = "mapping_value"
    RANK = "rank"
    TYPE = "type"


class AddressMappingModel(BaseModel):
    MERCHANT_DEFAULT = "SYSTEM_CONFIG"

    def __init__(self):
        super().__init__()
        self.collection = "address_mapping"

    def find_mapping(self, merchant_id, mapping_value, location_type):
        # cache redis
        key_cache = RedisCacheConfig.MERCHANT_ADDRESS_MAPPING_KEY.format(
            merchant_id=merchant_id, mapping_value=mapping_value, location_type=location_type
        )
        value_cache = RedisClient().get(key=key_cache)
        if value_cache:
            return value_cache 
        data = self.find_all(
            query={
                AddressMappingStructure.MERCHANT_ID: {
                    "$in": [merchant_id, self.MERCHANT_DEFAULT]
                },
                AddressMappingStructure.MAPPING_VALUE: mapping_value,
                AddressMappingStructure.TYPE: location_type
            },
            per_page=2
        )
        if not data:
            return None
        
        data_selected = None
        if len(data) == 1:
            data_selected = data[0]
        else:
            for item in data:
                if item.get(AddressMappingStructure.MERCHANT_ID) == self.MERCHANT_DEFAULT:
                    data_selected = item
                    break

        if data_selected:
            data_selected = RedisClient().set(key=key_cache, value=data_selected)
        return data_selected

