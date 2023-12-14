"""
    String conditions base class
"""

import logging

from marshmallow import Schema, fields, EXCLUDE, validate

from ..base import ConditionBase, ABCMeta, abstractmethod

LOG = logging.getLogger(__name__)


class StringCondition(ConditionBase, metaclass=ABCMeta):
    """
        Base class for string conditions
    """

    def __init__(self, values, what, qualifier=ConditionBase.Qualifier.ForAnyValue, ignore_case=False,
                 delimiter="", **kwargs):
        # xử lý ignore case
        self.case_insensitive = ignore_case
        if ignore_case:
            self.values = [self.utf8_to_ascii(i) if isinstance(i, str) else i for i in values]
            self.what = self.utf8_to_ascii(what) if isinstance(what, str) else what
            self.delimiter = self.utf8_to_ascii(delimiter) if isinstance(delimiter, str) else delimiter
        else:
            self.values = [i for i in values]
            self.what = what
            self.delimiter = delimiter
        self.qualifier = qualifier

    @abstractmethod
    def _is_satisfied(self) -> bool:
        """
            Is string conditions satisfied

            :param what: string value to check
            :return: True if satisfied else False
        """
        raise NotImplementedError()

    @classmethod
    def is_string(cls, value) -> bool:
        """
            Check if value is string
        """
        return isinstance(value, str)


class StringConditionSchema(Schema):
    """
        Base JSON schema for string conditions
    """
    values = fields.List(fields.String(required=True, allow_none=True), required=True, allow_none=False)
    ignore_case = fields.Bool(default=False, missing=False)
    what = fields.String(required=True, allow_none=True)
    qualifier = fields.String(allow_none=False, load_default=ConditionBase.Qualifier.ForAnyValue,
                              validate=validate.OneOf(ConditionBase.Qualifier.ALL))
    delimiter = fields.String(required=False, default="", missing="")

    class Meta:
        unknown = EXCLUDE
