"""
    Numeric less than conditions
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class Lt(NumericCondition):
    """
        Condition for number `what` less than `value`
    """

    def _is_satisfied(self) -> bool:
        if self.qualifier == self.Qualifier.ForAnyValue:
            for i in self.values:
                if self.what < i:
                    return True
            return False
        else:
            for i in self.values:
                if self.what >= i:
                    return False
            return True


class LtSchema(NumericConditionSchema):
    """
        JSON schema for less than numeric condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return Lt(**data)
