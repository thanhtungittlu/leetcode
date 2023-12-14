"""
    Collection conditions base class
"""

import logging

from marshmallow import Schema, fields, EXCLUDE

from ..base import ConditionBase, ABCMeta, abstractmethod

LOG = logging.getLogger(__name__)


def is_collection(value) -> bool:
    """
        Check if value is a collection
    """
    return any([isinstance(value, list), isinstance(value, set), isinstance(value, tuple)])


class CollectionCondition(ConditionBase, metaclass=ABCMeta):
    """
        Base class for collection conditions

        :param values: collection of values to compare during policy evaluation
    """

    def __init__(self, values, what, ignore_case=False, **kwargs):
        values = values if not self.value_is_none(values) else [None]
        what = what if not self.value_is_none(what) else [None]
        if ignore_case:
            values = [self.utf8_to_ascii(i) if isinstance(i, str) else i for i in values]
            what = [self.utf8_to_ascii(i) if isinstance(i, str) else i for i in what]
        self.values = values
        self.what = what

    @abstractmethod
    def _is_satisfied(self) -> bool:
        """
            Is collection conditions satisfied

            :param what: collection to check
            :return: True if satisfied else False
        """
        raise NotImplementedError()


class CollectionConditionSchema(Schema):
    """
        Base JSON schema class for collection conditions
    """
    values = fields.List(
        fields.Raw(required=True, allow_none=True),
        required=True,
        allow_none=True
    )
    what = fields.List(
        fields.Raw(allow_none=True),
        required=True,
        allow_none=True
    )
    ignore_case = fields.Bool(default=False, missing=False)

    class Meta:
        unknown = EXCLUDE
