"""
    Value is in collection conditions
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class IsIn(CollectionCondition):
    """
        Condition for `what` is a member of `values`
    """

    def _is_satisfied(self) -> bool:
        return self.what in self.values


class IsInSchema(CollectionConditionSchema):
    """
        JSON schema for is in collection condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return IsIn(**data)
