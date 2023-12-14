"""
    Attribute does not exists conditions
"""

from marshmallow import post_load

from .base import OthersCondition, OthersConditionSchema


class NotExists(OthersCondition):
    """
        Condition for attribute value not exists
    """

    def _is_satisfied(self) -> bool:
        if self.values.get(self.what) or self.values.get(self.what) in [0, False]:
            return False
        else:
            return True


class NotExistsSchema(OthersConditionSchema):
    """
        JSON schema for attribute value not exists condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use,unused-argument
        return NotExists(**data)
