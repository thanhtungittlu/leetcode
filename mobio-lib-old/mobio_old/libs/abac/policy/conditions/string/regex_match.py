"""
    String regex match conditions
"""

import re

from marshmallow import Schema, fields, post_load, ValidationError

from .base import StringCondition


class RegexMatch(StringCondition):
    """
        Condition for string `self.what` matches regex `value`
    """

    def _is_satisfied(self) -> bool:

        if self.qualifier == self.Qualifier.ForAnyValue:
            for i in self.values:
                if not self.is_string(i) and not self.is_string(self.what):
                    return True
                elif not self.is_string(i) or not self.is_string(self.what):
                    continue

                if re.search(i, self.what) is not None:
                    return True
            return False
        else:
            for i in self.values:
                if not self.is_string(i) and not self.is_string(self.what):
                    continue
                elif not self.is_string(i) or not self.is_string(self.what):
                    return False

                if re.search(i, self.what) is None:
                    return False
            return True


def validate_regex(value):
    """
        Validate given regex. Throws ValidationError exception
        for invalid regex expressions.
    """
    # noinspection PyBroadException
    try:
        if isinstance(value, str):
            re.compile(value)
        else:
            for i in value:
                re.compile(i)
    except Exception:
        raise ValidationError("Invalid regex expression '{}'.".format(value))


class RegexMatchSchema(Schema):
    """
        JSON schema for regex match string condition
    """
    values = fields.List(fields.String(required=True, allow_none=False), required=True, allow_none=False,
                         validate=validate_regex)

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return RegexMatch(**data)
