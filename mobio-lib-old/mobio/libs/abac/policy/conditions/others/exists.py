"""
    Attribute exists conditions
"""
from marshmallow import post_load

from .base import OthersCondition, OthersConditionSchema


class Exists(OthersCondition):
    """
        Condition for attribute value exists
    """

    def _is_satisfied(self) -> bool:
        if self.values.get(self.what) or self.values.get(self.what) in [0, False]:
            return True
        else:
            return False


class ExistsSchema(OthersConditionSchema):
    """
        JSON schema for attribute value exists conditions
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return Exists(**data)
