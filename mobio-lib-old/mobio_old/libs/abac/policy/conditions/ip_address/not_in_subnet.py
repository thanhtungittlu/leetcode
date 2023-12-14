"""
    String contains conditions
"""

from marshmallow import post_load
import ipaddress
from .base import IpAddressCondition, IpAddressConditionSchema


class NotInSubnet(IpAddressCondition):
    """
        Condition for string `self.what` contains `value`
    """

    def _is_satisfied(self) -> bool:
        for i in self.values:
            if ipaddress.ip_address(self.what) in ipaddress.ip_network(i):
                return False
        return True

class NotInSubnetSchema(IpAddressConditionSchema):
    """
        JSON schema for contains string conditions
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return NotInSubnet(**data)
