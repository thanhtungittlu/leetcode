"""
    String equals conditions
"""

from marshmallow import post_load, EXCLUDE

from .base import StringCondition, StringConditionSchema


class Equals(StringCondition):
    """
        Condition for string `self.what` equals `value`
    """

    def _is_satisfied(self) -> bool:
        if self.qualifier == self.Qualifier.ForAnyValue:
            for i in self.values:
                if not self.is_string(i) and not self.is_string(self.what):
                    return True
                elif not self.is_string(i) or not self.is_string(self.what):
                    continue

                if self.what == i:
                    return True
            return False
        else:
            for i in self.values:
                if not self.is_string(i) and not self.is_string(self.what):
                    continue
                elif not self.is_string(i) or not self.is_string(self.what):
                    return False

                if self.what != i:
                    return False
            return True


class EqualsSchema(StringConditionSchema):
    """
        JSON schema for equals string condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return Equals(**data)

