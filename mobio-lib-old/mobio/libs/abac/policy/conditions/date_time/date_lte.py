"""
    Numeric less than equal conditions
"""

from marshmallow import post_load

from .base import DateCondition, DateConditionSchema


class DateLte(DateCondition):
    """
        Condition for number `what` less than equals `value`
    """

    def _is_satisfied(self) -> bool:
        timestamp_what = self.convert_timestamp_from_any(self.what)
        if self.qualifier == self.Qualifier.ForAnyValue:
            for i in self.values:
                timestamp_i = self.convert_timestamp_from_any(i)
                if not timestamp_i or not timestamp_what:
                    return False
                if timestamp_what <= timestamp_i:
                    return True
            return False
        else:
            for i in self.values:
                timestamp_i = self.convert_timestamp_from_any(i)
                if not timestamp_i or not timestamp_what:
                    return False
                if timestamp_what > timestamp_i:
                    return False
            return True


class DateLteSchema(DateConditionSchema):
    """
        JSON schema for less than equals numeric condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return DateLte(**data)
