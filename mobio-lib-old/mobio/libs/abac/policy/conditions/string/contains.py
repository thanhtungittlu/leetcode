"""
    String contains conditions
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class Contains(StringCondition):
    """
        Condition for string `self.what` contains `value`
        delimiter kiem tra cho field dac biet scope_code
    """

    def _is_satisfied(self) -> bool:
        if self.qualifier == self.Qualifier.ForAnyValue:
            # chua bat ky gia tri nao deu se dung
            for i in self.values:
                if not self.is_string(i) and not self.is_string(self.what):
                    return True
                elif not self.is_string(i) or not self.is_string(self.what):
                    continue

                if self.delimiter:
                    if i + self.delimiter in self.what or i == self.what:
                        return True
                else:
                    if i in self.what:
                        return True
            return False
        else:
            # chua bat ky gia tri nao deu se dung
            for i in self.values:
                if not self.is_string(i) and not self.is_string(self.what):
                    continue
                elif not self.is_string(i) or not self.is_string(self.what):
                    return False

                if self.delimiter:
                    if i + self.delimiter in self.what or i == self.what:
                        pass
                    else:
                        return False
                else:
                    if i not in self.what:
                        return False
            return True


class ContainsSchema(StringConditionSchema):
    """
        JSON schema for contains string conditions
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return Contains(**data)
