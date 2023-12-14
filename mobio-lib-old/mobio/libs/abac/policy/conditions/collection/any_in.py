"""
    Any of the values in collection conditions
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class AnyIn(CollectionCondition):
    """
        Condition for any value of `what` in `values`
    """

    def _is_satisfied(self) -> bool:
        if not self.what:
            return False
        return bool(set(self.what).intersection(self.values))


class AnyInSchema(CollectionConditionSchema):
    """
        JSON schema for any in collection condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return AnyIn(**data)
