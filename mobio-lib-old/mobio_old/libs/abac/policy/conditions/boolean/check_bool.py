"""
    All of the values in collection conditions
"""

from marshmallow import post_load

from .base import BooleanCondition, BooleanConditionSchema

truthy = {
    "t",
    "T",
    "true",
    "True",
    "TRUE",
    "on",
    "On",
    "ON",
    "y",
    "Y",
    "yes",
    "Yes",
    "YES",
    "1",
    1,
    True,
}
falsy = {
    "f",
    "F",
    "false",
    "False",
    "FALSE",
    "off",
    "Off",
    "OFF",
    "n",
    "N",
    "no",
    "No",
    "NO",
    "0",
    0,
    0.0,
    False,
}


class CheckBool(BooleanCondition):
    """
        Condition for all values of `what` in `values`
    """

    def _is_satisfied(self) -> bool:
        for i in self.values:
            if (i in truthy and self.what in truthy) or (i in falsy and self.what in falsy):
                return True
        return False


class CheckBoolSchema(BooleanConditionSchema):
    """
        JSON schema for all in collection condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return CheckBool(**data)
