from .config import JSONEncoder, KafkaHelper
from .policy.utils import Utils


class ResultAccess:
    def __init__(self):
        self.allow_access = False
        self.display_config = []
        self.filter_config = []
        self.log_statement_deny = []
        self.log_statement_allow = []
        self.log_error = []
        self.data_allow = []
        self.code_error = 403
        self.data_log = {}

    def get_allow_access(self):
        # if self.allow_access:
        #     print("abac_sdk statement_allow: {}".format(self.log_statement_allow))
        # else:
        #     print("abac_sdk statement_deny: {}".format(self.log_statement_deny))
        # print("abac_sdk log_error: {}".format(self.log_error))
        self.push_kafka_log()
        print("abac_sdk log_full: {}".format(self.get_log()))
        return self.allow_access

    def set_allow_access(self, value: bool):
        self.allow_access = value

    def get_filter_config(self):
        """
        filter: [{'effect': 'allow', 'condition': [{'operator': 'StringEquals', 'field': 'deal:block',
        'values': ['KHDN'], 'qualifier': 'ForAnyValue', 'if_exists': False, 'ignore_case': False},
        {'operator': 'StringStartsWith', 'field': 'deal:scope_code', 'values': ['MB##HN'],
        'qualifier': 'ForAnyValue', 'if_exists': False, 'ignore_case': False}]}]
        :return:
        """
        # print(self.filter_config)
        return self.filter_config

    def add_filter_config(self, value):
        value_format = value
        for item in value_format.get("condition", []):
            if item.get("date_format"):
                v_format = []
                for v in item.get("values"):
                    v_format.append(Utils.convert_string_to_format(v, item.get("date_format")))
                item["values"] = v_format
        self.filter_config.append(value_format)

    def get_display_config(self):
        return self.display_config

    def add_display_config(self, value):
        self.display_config.append(value)

    @classmethod
    def build_key_filter_config(cls, effect, operator, field, qualifier):
        return effect + "#" + operator + "#" + field + "#" + qualifier

    @classmethod
    def extract_key_filter_config(cls, key_filter):
        items = key_filter.split("#")
        return {
            "effect": items[0],
            "operator": items[1],
            "field": items[2],
            "qualifier": items[3],
        }

    @classmethod
    def convert_data_save_log(cls, value):
        # return {
        #     'merchant_id': value.get('merchant_id'),
        #     'policy_code': value.get('policy_code'),
        #     'statement_id': value.get('statement_id'),
        #     'effect': value.get('effect'),
        #     'action': value.get('action'),
        #     'resource': value.get('resource'),
        # }
        return JSONEncoder().json_loads(value)

    def add_log_deny(self, value):
        self.log_statement_deny.append(self.convert_data_save_log(value))

    def add_log_allow(self, value):
        self.log_statement_allow.append(self.convert_data_save_log(value))

    def add_log_error(self, value):
        self.log_error.append(value)

    def get_log(self):
        output_engine = {
            "allow_access": self.allow_access,
            "display_config": self.display_config,
            "filter_config": self.filter_config,
            "log_statement_deny": self.log_statement_deny,
            "log_statement_allow": self.log_statement_allow,
            "log_error": self.log_error,
        }
        self.data_log.get("other", {}).update(output_engine)
        self.data_log = JSONEncoder().json_loads(self.data_log)
        return self.data_log

    # gom các condition cùng key ở các statement lại thành 1 condition,
    # nhưng logic chạy list statement thay đổi thành statement or với nhau, các condition trong statement and,
    # như vậy gom sẽ thành sai logic, kể cả gom trong 1 statement cũng là sai logic,
    # ví dụ user nào xem dữ liệu theo mã cấp user đó hoặc 2 mã cấp khác, policy sẽ tạo 2 statment để thỏa mãn logic trên
    def group_condition_key(self):
        """
        filter: [{'effect': 'allow', 'condition': [{'operator': 'StringEquals', 'field': 'deal:block',
        'values': ['KHDN'], 'qualifier': 'ForAnyValue', 'if_exists': False, 'ignore_case': False},
        {'operator': 'StringStartsWith', 'field': 'deal:scope_code', 'values': ['MB##HN'],
        'qualifier': 'ForAnyValue', 'if_exists': False, 'ignore_case': False}]}]
        :return:
        """
        # print(self.filter_config)
        dict_field = {}
        dict_exists = {}
        list_filter_config = []
        index_statement = 0
        for statement in self.filter_config:
            item_condition = []
            index_condition = 0
            effect = statement.get("effect")
            for condition in statement.get("condition"):
                operator = condition.get("operator")
                field = condition.get("field")
                qualifier = condition.get("qualifier")
                key_filter = self.build_key_filter_config(effect, operator, field, qualifier)
                if key_filter not in dict_field:
                    dict_field[key_filter] = [index_statement, index_condition]
                    item_condition.append(condition)
                else:
                    dict_exists[key_filter] = condition
                index_condition += 1
            if item_condition:
                list_filter_config.append({
                    'effect': effect,
                    'condition': item_condition
                })
            index_statement += 1
        for k, v in dict_exists.items():
            if k in dict_field:
                list_filter_config[dict_field.get(k)[0]].get("condition")[dict_field.get(k)[1]].get("values").extend(
                    v.get("values"))
        return list_filter_config

    def get_data_allow(self):
        return self.data_allow

    def add_data_allow(self, value):
        self.data_allow.append(value)

    def get_code_error(self):
        # code 403 ko co quyen do policy merchant tao
        # code 413 ko co quyen do ko co license
        return self.code_error

    def push_kafka_log(self):
        try:
            KafkaHelper.push_message_kafka(topic=KafkaHelper.TOPIC_ABAC_LOG,
                                           data=self.get_log())
        except Exception as err:
            print("push_kafka_log: {}".format(err))
