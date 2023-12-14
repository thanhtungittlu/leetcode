class COMMON(object):
    DATE_TIME_FORMAT = '%Y-%m-%dT%TZ'
    DATE_TIME_FORMAT_2 = '%Y%m%d%H%M%S'
    DATE_TIME_FORMAT_3 = '%Y-%m-%dT%H:%M:%S.%fZ'
    DATE_TIME_FORMAT_4 = '%Y-%m-%dT%H:%M:%S.%f%Z'
    DATE_TIME_FORMAT_5 = '%Y-%m-%d %H:%M:%S'
    DATE_TIME_FORMAT_6 = '%Y-%m-%dT%H:%M:%S.%f'
    DATE_TIME_FORMAT_7 = '%Y-%m-%dT%T.%fZ'
    DATE_FORMAT = '%Y%m%d'
    BIRTHDAY_FORMAT = '%d/%m/%Y'


class Elastic:
    HOSTS = 'hosts'
    PORT = 'port'
    INDEX = 'index'
    DOC_TYPE = 'doc_type'


class MerchantParams:
    CREATED_TIME = 'created_time'
    UPDATED_TIME = 'updated_time'
    AUTO_MERGE = 'auto_merge'
    MERCHANT_ID = 'merchant_id'
    RULES = 'rules'

    # RULE_NAME = 'rule_name'
    DYNAMIC_FIELDS = 'dynamic_fields'
    PARENTS = 'parents'
    TIMEZONE = 'timezone'
    ENRICH_FIELDS = 'enrich_fields'
    VERSION = 'version'


class AUDIENCE_STRUCTURE:
    CRITERIA_KEY = 'criteria_key'
    OPERATOR_KEY = 'operator_key'
    VALUES = 'values'


class OPERATOR_KEY:
    OP_IS_BETWEEN = 'op_is_between'
    OP_IS_EQUAL = 'op_is_equal'
    OP_IS_NOT_EQUAL = 'op_is_not_equal'
    OP_IS_GREATER = 'op_is_greater'
    OP_IS_GREATER_EQUAL = 'op_is_greater_equal'
    OP_IS_HAS = 'op_is_has'
    OP_IS_HAS_NOT = 'op_is_has_not'
    OP_IS_IN = 'op_is_in'
    OP_IS_LESS = 'op_is_less'
    OP_IS_LESS_EQUAL = 'op_is_less_equal'
    OP_IS_REGEX = 'op_is_regex'
    OP_IS_EMPTY = 'op_is_empty'
    OP_IS_NOT_EMPTY = 'op_is_not_empty'
    OP_IS_NOT_IN = 'op_is_not_in'
