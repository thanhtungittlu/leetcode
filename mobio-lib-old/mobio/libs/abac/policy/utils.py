from copy import deepcopy
import re, json
from datetime import datetime
from user_agents import parse
from flask import request
import base64
from dateutil.parser import parse


class Utils:
    ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

    @classmethod
    def convert_string_to_format(cls, date_str, date_format):
        try:
            return datetime.strptime(date_str, cls.ISO_FORMAT).strftime(date_format)
        except:
            return date_str

    @staticmethod
    def split_delemiter_resource(str_value):
        resource_name, resource_key = None, None
        if ":" in str_value:
            values = str_value.split(":")
            resource_name, resource_key = values[0], values[1]
        else:
            resource_name = str_value
        return resource_name, resource_key

    @staticmethod
    def split_delemiter_field(str_value):
        return str_value.split(":")

    @staticmethod
    def get_nested_value(obj, field):
        obj_value = deepcopy(obj)
        fields = field.split('.')
        for f in fields:
            obj_value = obj_value.get(f)
            if obj_value is None:
                return None
        return obj_value

    @staticmethod
    def get_field_key_from_variable(str_text) -> list:
        key_regex = "\${(.*?)}"
        try:
            if isinstance(str_text, int):
                return []
            return re.findall(key_regex, str_text)
        except Exception as er:
            print("abac_sdk get_field_key_from_variable key: {}, err: {}".format(key_regex, er))
            return []

    @staticmethod
    def replace_variable_to_value(field_key, field_value, str_origin):
        key_regex = "\${" + field_key + "}"
        return re.sub(fr'{key_regex}', field_value, str_origin)

    @staticmethod
    def check_field_is_variable(field_key):
        # if field_key.startswith("${") and field_key.endswith("}"):
        #     return True
        # return False
        if Utils.get_field_key_from_variable(field_key):
            return True
        return False

    @staticmethod
    def get_date_utcnow():
        return datetime.utcnow()

    @staticmethod
    def parse_user_agent(ua_string):
        try:
            user_agent = parse(ua_string)
            # if user_agent.is_pc:
            #     device = "web"
            # else:
            #     device = "mobile"
            agent_info = {
                "env:browser": user_agent.browser,
                "env:os": user_agent.os,
                # "env:device_type": device,
            }
            return agent_info
        except:
            return {}

    @staticmethod
    def get_info_from_header_request():
        try:
            header_data = request.headers
            user_agent = header_data.get('User-Agent')
            current_ip = request.remote_addr
            if header_data.get("X-Real-Ip"):
                current_ip = header_data.get("X-Real-Ip")
            device_type = header_data.get('mobio-device-type')
            return {
                "source_ip": current_ip,
                "user_agent": user_agent,
                "device_type": device_type if device_type else "web"
            }
        except:
            return {}

    @staticmethod
    def get_fields_of_resource(full_resource):
        fields = {}
        if "/" not in full_resource:
            return fields
        split_resource = full_resource.split("/")
        service_resource, field_multi = split_resource[0], split_resource[1]
        resource = service_resource.split(":")[-1]
        return {resource: field_multi.split(",")}

    @staticmethod
    def field_in_body_request(list_field, body_request):
        if list_field and body_request:
            for field in list_field:
                if field in body_request:
                    return True
        return False

    @staticmethod
    def add_field_in_body_request(list_field, body_request):
        if list_field and body_request:
            for field in list_field:
                # if isinstance(body_request.get(field), bool) or isinstance(body_request.get(field), int) \
                #         or isinstance(body_request.get(field), float):
                #     return True
                # if not body_request.get(field):
                #     continue
                # return True
                if Utils.check_value_valid_check_action_add(body_request.get(field)):
                    return True
        return False

    @staticmethod
    def check_value_valid_check_action_add(value_check):
        if isinstance(value_check, bool) or isinstance(value_check, int) \
                or isinstance(value_check, float):
            return True
        if not value_check:
            return False
        return True

    @staticmethod
    def base64_encode(data):
        try:
            byte_string = data.encode('utf-8')
            encoded_data = base64.b64encode(byte_string)
            return encoded_data.decode(encoding='UTF-8')
        except:
            return ""

    @staticmethod
    def base64_decode(encoded_data):
        try:
            if isinstance(encoded_data, bytes):
                encoded_data = encoded_data.decode('UTF-8')
            decoded_data = base64.urlsafe_b64decode(encoded_data + '=' * (-len(encoded_data) % 4))
            return decoded_data.decode(encoding='UTF-8')
        except:
            return encoded_data

    @staticmethod
    def get_info_jwt():
        try:
            data_author = request.headers['Authorization']
            if not data_author:
                raise ValueError("Authorization not found")
            auth_type, jwt_token = data_author.split(None, 1)
            auth_type = auth_type.lower()
            if auth_type not in ['basic', 'bearer', 'digest']:
                raise ValueError("Authorization invalid")
            json_token = {}
            if auth_type == 'bearer':
                arr_token = jwt_token.split(".")
                data = Utils.base64_decode(arr_token[1].replace('_', '/') + '===')
                body_token = json.loads(data.decode('utf8'))
                merchant_id = body_token.get('merchant_id', None)
                account_id = body_token.get('id', None)
                json_token.update({
                    "merchant_id": merchant_id,
                    "account_id": account_id,
                })
            return auth_type, json_token
        except:
            raise ValueError("Authorization invalid")
