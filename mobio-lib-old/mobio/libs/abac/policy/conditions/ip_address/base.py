"""
    String conditions base class
"""

import logging
import ipaddress
from marshmallow import Schema, fields, EXCLUDE, ValidationError

from ..base import ConditionBase, ABCMeta, abstractmethod

LOG = logging.getLogger(__name__)

def validate_ip_address(address):
    try:
        if isinstance(address, str):
            ipaddress.ip_address(address)
        else:
            for i in address:
                ipaddress.ip_address(i)
    except Exception:
        raise ValidationError("Invalid ip_address '{}'.".format(address))

def validate_ip_network(address):
    try:
        if isinstance(address, str):
            ipaddress.ip_network(address)
        else:
            for i in address:
                ipaddress.ip_network(i)
    except Exception:
        raise ValidationError("Invalid ip_network '{}'.".format(address))

class IpAddressCondition(ConditionBase, metaclass=ABCMeta):
    """
        Base class for string conditions
    """

    def __init__(self, values, what, **kwargs):
        self.values = values
        self.what = what


    @abstractmethod
    def _is_satisfied(self) -> bool:
        """
            Is string conditions satisfied

            :param what: string value to check
            :return: True if satisfied else False
        """
        raise NotImplementedError()


class IpAddressConditionSchema(Schema):
    """
        Base JSON schema for string conditions
    """
    values = fields.List(fields.String(required=True, allow_none=False), required=True, allow_none=False, validate=validate_ip_network)
    what = fields.String(required=True, allow_none=False, validate=validate_ip_address)

    class Meta:
        unknown = EXCLUDE