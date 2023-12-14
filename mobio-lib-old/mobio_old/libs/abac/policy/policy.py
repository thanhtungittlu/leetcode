"""
    Policy class
"""
import json
from marshmallow import Schema, fields, post_load, ValidationError, validate, EXCLUDE
from .conditions.schema import ConditionSchema
from .utils import Utils
from .conditions.base import ConditionBase
from .exceptions import *


class AccessType:
    DENY_ACCESS = "deny"
    ALLOW_ACCESS = "allow"


class Policy(object):
    """
        Policy class containing rules and targets
    """

    def __init__(
            self,
            effect: str,
            # action: list,
            # resource: list,
            condition: dict,
            request_access: dict, **kwargs
    ):
        self.effect = effect
        # self.action = action
        # self.resource = resource
        self.condition = condition
        self.condition_convert = None
        self.request_access = request_access

    def is_allowed(self):
        conditions = self.convert_condition()
        self.condition_convert = conditions
        for condition in conditions:
            # print("abac_sdk condition: ", condition)
            if condition.get("operator") == "Null":
                what_check = self.get_value_from_field(condition.get("field"))
                if what_check is not None:
                    return False
            else:
                cond_schema = ConditionSchema().load(condition)
                if not cond_schema._is_satisfied():
                    return False
        return True

    def get_condition_convert(self):
        return self.condition_convert

    def convert_condition(self):
        """
            {
                "operator": "StringEquals",
                "field": "user:staff_code",
                "values": ["A123456"],
                "qualifier": "ForAnyValue",
                "if_exists": false,
                "ignore_case": false,
            }
        :return:
        """
        list_condition = []
        have_condition_exclude = False
        for item in self.condition:
            cond_schema = self.validate_item_condition(item)
            # print("abac_sdk cond_schema: {}".format(json.dumps(cond_schema)))
            if cond_schema.get("operator") == "Null":
                list_condition.append({**item})
            elif cond_schema.get("operator") in ["Exists", "NotExists"]:
                if_exists = cond_schema.get("if_exists")
                what_check = self.get_value_from_field(cond_schema.get("field"))
                if if_exists:
                    if not what_check and what_check not in [0, False]:
                        continue
                resource_name, resource_key = Utils.split_delemiter_resource(cond_schema.get("field"))
                data_resource = {}
                if resource_name:
                    if self.request_access.get(resource_name) and isinstance(
                            self.request_access.get(resource_name), dict):
                        data_resource = self.request_access.get(resource_name)
                list_condition.append({
                    **item,
                    "values": data_resource,
                    "what": resource_key,
                })
            else:
                if_exists = cond_schema.get("if_exists")
                what_check = self.get_value_from_field(cond_schema.get("field"))
                if if_exists:
                    if not what_check and what_check not in [0, False]:
                        continue
                # if what_check is None:
                #     raise GetValueNoneException("{} get value is None".format(cond_schema.get("field")))
                if not what_check and isinstance(what_check, str):
                    what_check = None
                values = []
                for v in cond_schema.get("values"):
                    value_from_variable = self.get_value_from_variable(v)
                    if not value_from_variable and isinstance(value_from_variable, str):
                        value_from_variable = None
                    if isinstance(value_from_variable, list):
                        values.extend(value_from_variable)
                    else:
                        values.append(value_from_variable)
                list_condition.append({
                    **item,
                    "values": values,
                    "what": what_check,
                })
        # if len(list_condition) == 0 and not have_condition_exclude:
        #     raise EmptyConditionException("no condition found")
        return list_condition

    def get_value_from_variable(self, str_variable):
        if isinstance(str_variable, str) and Utils.check_field_is_variable(str_variable):
            variables = Utils.get_field_key_from_variable(str_variable)
            if variables:
                if len(variables) == 1:
                    field_value = self.get_value_from_field(variables[0])
                    if field_value is None:
                        # raise GetValueNoneException("{} get value is None".format(variables[0]))
                        return field_value
                    if isinstance(field_value, str):
                        field_value_format = Utils.replace_variable_to_value(variables[0], field_value, str_variable)
                        return field_value_format
                    return field_value
                for field_key in variables:
                    field_value = self.get_value_from_field(field_key)
                    if field_value is None:
                        # raise GetValueNoneException("{} get value is None".format(field_key))
                        field_value = ""
                    field_value = str(field_value)
                    str_variable = Utils.replace_variable_to_value(field_key, field_value, str_variable)
        return str_variable

    def get_value_from_field(self, field_key):
        resource_name, resource_key = Utils.split_delemiter_resource(field_key)
        if resource_name and resource_key:
            if self.request_access.get(resource_name) and isinstance(self.request_access.get(resource_name), dict):
                data_resource = self.request_access.get(resource_name)
                value = Utils.get_nested_value(data_resource, resource_key)
                return value
        return None

    def validate_item_condition(self, obj):
        try:
            return ConditionValidateSchema().load(obj)
        except Exception as err:
            raise InvalidConditionException("validate_item_condition: {}".format(err))


class ConditionValidateSchema(Schema):
    operator = fields.String(required=True, allow_none=False)
    field = fields.String(required=True, allow_none=False)
    values = fields.List(fields.Raw(required=True, allow_none=False), required=True, allow_none=False)
    qualifier = fields.String(default=ConditionBase.Qualifier.ForAnyValue,
                              validate=validate.OneOf(ConditionBase.Qualifier.ALL))
    if_exists = fields.Boolean(default=False)
    ignore_case = fields.Boolean(default=False)

    class Meta:
        unknown = EXCLUDE


class PolicySchema(Schema):
    """
        JSON schema for policy
    """
    effect = fields.String(required=True, validate=validate.OneOf([AccessType.DENY_ACCESS, AccessType.ALLOW_ACCESS]))
    # action = fields.List(fields.String(required=True, allow_none=False),required=True, allow_none=False)
    # resource = fields.List(fields.String(required=True, allow_none=False),required=True, allow_none=False)
    condition = fields.List(fields.Raw(required=True, allow_none=False), required=True, allow_none=False)
    request_access = fields.Dict(default={}, missing={}, allow_none=False)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return Policy(**data)
