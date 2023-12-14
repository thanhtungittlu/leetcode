
class RedisCacheConfig:
    PREFIX = "location_"

    COUNTRY_CONFIG_KEY = PREFIX+"country_config_{key}"
    MERCHANT_ADDRESS_MAPPING_KEY = PREFIX+"mapping_{merchant_id}_{mapping_value}_{location_type}"
