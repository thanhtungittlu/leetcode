import unicodedata

from ..models.country_configs import CountryConfigModel, CountryConfigStructure, RankConfigStructure
from ..models.address_mapping import AddressMappingModel

FIELD_MAPPING_NORMALIZE = ["country", "state",
                           "county", "city", "district", "subdistrict"]


class MappingInput:
    COUNTRY = "country"


class CountryConfig:
    TYPE = "COUNTRY"
    FIELD_CODE = "country_code"


LOG_HEADER = '*** Location SDK:::'


class MobioLocationSDK:

    # co the cache neu can
    def get_location_by_mapping(self, merchant_id, mapping):
        try:
            print("="*20)
            log_fuction = f'{LOG_HEADER} get_location_by_mapping():::'
            print(f'{log_fuction} INFO: input merchant_id: {merchant_id}')
            print(f'{log_fuction} INFO: input mapping: {mapping}')

            mapping = self.normalize_unicode(mapping)
            print('{} INFO: normalize_unicode output mapping: {}'.format(
                log_fuction, mapping))
            country_input = mapping.get(MappingInput.COUNTRY)
            if not country_input:
                print(f'{log_fuction} ERROR: country_input is empty')
                return False, None

            # get country first
            mapping_value = self._build_mapping_value([], country_input)
            country_mapping = AddressMappingModel().find_mapping(
                merchant_id=merchant_id,
                mapping_value=mapping_value,
                location_type=CountryConfig.TYPE
            )
            if not country_mapping:
                print(
                    f'{log_fuction} ERROR: mapping_value: "{mapping_value}" - mess: country_mapping not found')
                return False, None

            country_code = country_mapping.get(CountryConfig.FIELD_CODE)

            country_config = CountryConfigModel().find_one_by_key(key=country_code)
            if not country_config:
                print(
                    f'{log_fuction} ERROR: country_code: "{country_code}" - mess: country_config not found')
                raise Exception("country_config not exists!")

            rank_configs = country_config.get(CountryConfigStructure.CONFIGS)
            rank_configs.sort(key=lambda x: x.get(RankConfigStructure.RANK))

            mapping_codes = [country_mapping.get(CountryConfig.FIELD_CODE)]
            last_result = country_mapping
            for rank_config in rank_configs:
                if rank_config.get(RankConfigStructure.RANK) > 1:
                    current_mapping_code, location = self._find_location(
                        merchant_id=merchant_id,
                        mapping=mapping,
                        rank_config=rank_config,
                        mapping_codes=mapping_codes
                    )
                    if not location:
                        break
                    mapping_codes.append(current_mapping_code)
                    last_result = location

            # check mapping_full
            mapping_full = self._check_mapping_full(
                mapping_input=mapping,
                len_mapping_codes=len(mapping_codes),
                rank_configs=rank_configs
            )
            print(f'{log_fuction} INFO: result mapping_full: {mapping_full}')
            print(f'{log_fuction} INFO: result last_result: {last_result}')
            return mapping_full, last_result
        except Exception as ex:
            raise
        finally:
            print("="*20)

    @staticmethod
    def _check_mapping_full(mapping_input, len_mapping_codes, rank_configs):
        mapping_full = False
        count_key_mapping = 0
        for key_mapping, value_mapping in mapping_input.items():
            for item_rank in rank_configs:
                if item_rank.get(RankConfigStructure.FIELD) == key_mapping:
                    count_key_mapping += 1
                    break
        if count_key_mapping == len_mapping_codes:
            mapping_full = True
        return mapping_full

    def _find_location(self, merchant_id, mapping, rank_config, mapping_codes):
        log_fuction = f'{LOG_HEADER} _find_location():::'
        location_field_code = rank_config.get(RankConfigStructure.FIELD_CODE)
        location_field = rank_config.get(RankConfigStructure.FIELD)
        mapping_value = mapping.get(location_field)
        if mapping_value:
            current_mapping_value = self._build_mapping_value(
                mapping_codes, mapping_value)
            location_type = rank_config.get(RankConfigStructure.KEY)
            print("{} mapping_value: {} - location_type: {}".format(
                log_fuction,
                current_mapping_value,
                location_type
            ))
            # find mapping
            address_mapping = AddressMappingModel().find_mapping(
                merchant_id=merchant_id,
                mapping_value=current_mapping_value,
                location_type=location_type
            )
            if address_mapping:
                return address_mapping.get(location_field_code), address_mapping
        return None, None

    @staticmethod
    def _build_mapping_value(mapping_codes, current_mapping_value):
        mapping_value = ""
        for item in mapping_codes:
            mapping_value = mapping_value + str(item) + "#"
        mapping_value = mapping_value + current_mapping_value + "#"
        return mapping_value

    def normalize_unicode(self, mapping):
        log_fuction = f'{LOG_HEADER} normalize_unicode():::'
        new_mapping = {}
        for key, value in mapping.items():
            if key in FIELD_MAPPING_NORMALIZE and value and isinstance(value, str):
                print("{} OLD: {} {}".format(
                    log_fuction, key, bytearray(value, "utf-8")))
                new_value = unicodedata.normalize("NFC", value)
                print("{} NEW: {} {}".format(log_fuction,
                      key, bytearray(new_value, "utf-8")))
                new_mapping[key] = new_value
            else:
                new_mapping[key] = value
        return new_mapping
