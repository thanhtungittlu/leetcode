"""
    Date equal conditions
"""

from marshmallow import post_load
from .base import MonthDayCondition, MonthDayConditionSchema


class MonthDayEq(MonthDayCondition):

    def _is_satisfied(self) -> bool:
        day_what = self.convert_day_format_from_any(self.what)
        if self.qualifier == self.Qualifier.ForAnyValue:
            for i in self.values:
                day_i = self.convert_day_format_from_any(i)
                if day_what == day_i:
                    return True
            return False
        else:
            for i in self.values:
                day_i = self.convert_day_format_from_any(i)
                if day_what != day_i:
                    return False
            return True


class MonthDayEqSchema(MonthDayConditionSchema):
    """
        JSON schema for equals datetime condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return MonthDayEq(**data)
