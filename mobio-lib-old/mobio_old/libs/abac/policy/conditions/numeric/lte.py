"""
    Numeric less than equal conditions
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class Lte(NumericCondition):
    """
        Condition for number `what` less than equals `value`
    """

    def _is_satisfied(self) -> bool:
        if self.qualifier == self.Qualifier.ForAnyValue:
            for i in self.values:
                if self.what <= i:
                    return True
            return False
        else:
            for i in self.values:
                if self.what > i:
                    return False
            return True


class LteSchema(NumericConditionSchema):
    """
        JSON schema for less than equals numeric condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return Lte(**data)
