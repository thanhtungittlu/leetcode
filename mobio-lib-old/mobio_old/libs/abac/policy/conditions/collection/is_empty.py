"""
    Collection is empty conditions
"""

from marshmallow import Schema, post_load

from .base import CollectionCondition


class IsEmpty(CollectionCondition):
    """
        Condition for `what` being an empty collection
    """

    def _is_satisfied(self) -> bool:
        """
            Is collection conditions satisfied

            :param what: collection to check
            :return: True if satisfied else False
        """
        if len(self.what) > 0:
            if self.what[0] is None:
                return True
            else:
                return False
        else:
            return True


class IsEmptySchema(Schema):
    """
        JSON schema for is empty collection condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use,unused-argument
        # self.validate(data)
        return IsEmpty(**data)
