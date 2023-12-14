"""
    Numeric greater than conditions
"""

from marshmallow import post_load

from .base_list import NumericListCondition, NumericListConditionSchema


class ListGt(NumericListCondition):
    """
        Condition for number `what` greater than `value`
    """

    def _is_satisfied(self) -> bool:
        if self.qualifier == self.Qualifier.ForAnyValue:
            for w in self.what:
                for v in self.values:
                    if w > v:
                        return True
            return False
        else:
            for w in self.what:
                for v in self.values:
                    if w <= v:
                        return False
            return True


class ListGtSchema(NumericListConditionSchema):
    """
        JSON schema for greater than numeric condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return ListGt(**data)
