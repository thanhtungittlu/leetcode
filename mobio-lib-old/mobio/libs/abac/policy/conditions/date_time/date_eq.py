"""
    Date equal conditions
"""

from marshmallow import post_load
from .base import DateCondition, DateConditionSchema


class DateEq(DateCondition):
    """
        Condition for number `what` equals `value`
    """

    def _is_satisfied(self) -> bool:
        timestamp_what = self.convert_timestamp_from_any(self.what)
        if self.qualifier == self.Qualifier.ForAnyValue:
            for i in self.values:
                # if self.value_is_none(i) and self.value_is_none(self.what):
                #     return True
                # elif self.value_is_none(i) or self.value_is_none(self.what):
                #     continue
                timestamp_i = self.convert_timestamp_from_any(i)
                # if not timestamp_i or not timestamp_what:
                #     return False
                if timestamp_what == timestamp_i:
                    return True
            return False
        else:
            for i in self.values:
                # if self.value_is_none(i) and self.value_is_none(self.what):
                #     continue
                # elif self.value_is_none(i) or self.value_is_none(self.what):
                #     return False
                timestamp_i = self.convert_timestamp_from_any(i)
                # if not timestamp_i or not timestamp_what:
                #     return False
                if timestamp_what != timestamp_i:
                    return False
            return True


class DateEqSchema(DateConditionSchema):
    """
        JSON schema for equals datetime condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return DateEq(**data)
