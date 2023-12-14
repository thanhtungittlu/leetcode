"""
    Boolean conditions base class
"""

import logging

from marshmallow import Schema, fields, EXCLUDE

from ..base import ConditionBase, ABCMeta, abstractmethod

LOG = logging.getLogger(__name__)


class BooleanCondition(ConditionBase, metaclass=ABCMeta):
    """
        Base class for Boolean conditions

        :param values: Boolean of values to compare during policy evaluation
    """

    def __init__(self, values, what, **kwargs):
        self.values = values
        self.what = what

    @abstractmethod
    def _is_satisfied(self) -> bool:
        """
            Is Boolean conditions satisfied

            :param what: Boolean to check
            :return: True if satisfied else False
        """
        raise NotImplementedError()


class BooleanConditionSchema(Schema):
    """
        Base JSON schema class for Boolean conditions
    """
    values = fields.List(fields.Boolean(
        required=True,
        allow_none=False
    ), required=True,
        allow_none=False)
    what = fields.Boolean(
        required=True,
        allow_none=False
    )

    class Meta:
        unknown = EXCLUDE
