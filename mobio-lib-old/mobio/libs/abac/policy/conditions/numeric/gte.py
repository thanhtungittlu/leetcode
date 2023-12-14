"""
    Numeric greater than equal conditions
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class Gte(NumericCondition):
    """
        Condition for number `what` greater than equals `value`
    """

    def _is_satisfied(self) -> bool:
        if self.qualifier == self.Qualifier.ForAnyValue:
            for i in self.values:
                if self.what >= i:
                    return True
            return False
        else:
            for i in self.values:
                if self.what < i:
                    return False
            return True


class GteSchema(NumericConditionSchema):
    """
        JSON schema for greater than equals numeric condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return Gte(**data)
