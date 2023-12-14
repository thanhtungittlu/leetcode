"""
    Others conditions base class
"""

import logging

from marshmallow import Schema, fields, EXCLUDE, validate

from ..base import ConditionBase, ABCMeta, abstractmethod

LOG = logging.getLogger(__name__)



class OthersCondition(ConditionBase, metaclass=ABCMeta):
    """
        Base class for numeric conditions
    """

    def __init__(self, values, what, **kwargs):
        self.values = values
        self.what = what


    @abstractmethod
    def _is_satisfied(self) -> bool:
        """
            Is numeric conditions satisfied

            :param what: numeric value to check
            :return: True if satisfied else False
        """
        raise NotImplementedError()


class OthersConditionSchema(Schema):
    """
        Base JSON schema for numeric conditions
    """
    values = fields.Dict(default={}, missing={}, allow_none=False)
    what = fields.String(required=True, allow_none=False)

    class Meta:
        unknown = EXCLUDE