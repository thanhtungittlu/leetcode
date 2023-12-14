"""
    Any of the values not contains collection conditions
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class AnyNotContains(CollectionCondition):
    """
        Condition for any value of `what` in `values`
    """

    def _is_satisfied(self) -> bool:
        for i in self.values:
            for w in self.what:
                if i is None and w is None:
                    continue
                elif i is None or w is None:
                    return True
                if i in w:
                    return False
        return True


class AnyNotContainsSchema(CollectionConditionSchema):
    """
        JSON schema for any in collection condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return AnyNotContains(**data)
