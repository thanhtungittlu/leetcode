"""
    All of the values in collection conditions
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class AllIn(CollectionCondition):
    """
        Condition for all values of `what` in `values`
    """

    def _is_satisfied(self) -> bool:
        if not self.what:
            return False
        return set(self.values).issubset(self.what)


class AllInSchema(CollectionConditionSchema):
    """
        JSON schema for all in collection condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return AllIn(**data)
