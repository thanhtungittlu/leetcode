"""
    String not contains conditions
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class NotContains(StringCondition):
    """
        Condition for string `self.what` not contains `value`
    """

    def _is_satisfied(self) -> bool:
        if self.qualifier == self.Qualifier.ForAnyValue:
            for i in self.values:
                if not self.is_string(i) and not self.is_string(self.what):
                    continue
                elif not self.is_string(i) or not self.is_string(self.what):
                    return True

                if self.delimiter:
                    if i + self.delimiter in self.what or i == self.what:
                        return False
                else:
                    if i in self.what:
                        return False
            return True
        else:
            for i in self.values:
                if not self.is_string(i) and not self.is_string(self.what):
                    return False
                elif not self.is_string(i) or not self.is_string(self.what):
                    continue

                if self.delimiter:
                    if i + self.delimiter in self.what or i == self.what:
                        return False
                else:
                    if i in self.what:
                        return False
            return True


class NotContainsSchema(StringConditionSchema):
    """
        JSON schema for not contains string condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return NotContains(**data)
