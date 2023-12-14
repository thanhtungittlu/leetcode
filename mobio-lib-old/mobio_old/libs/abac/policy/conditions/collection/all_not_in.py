"""
    All of the values not in collection conditions
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class AllNotIn(CollectionCondition):
    """
        Condition for all values of `what` not in `values`
    """

    def _is_satisfied(self) -> bool:
        if not self.what:
            return False
        return not set(self.values).issubset(self.what)


class AllNotInSchema(CollectionConditionSchema):
    """
        JSON schema for all not in collection condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return AllNotIn(**data)
