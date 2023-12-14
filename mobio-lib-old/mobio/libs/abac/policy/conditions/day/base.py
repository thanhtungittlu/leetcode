"""
    String conditions base class
"""

import datetime
import logging

from dateutil.parser import parse
from marshmallow import Schema, fields, EXCLUDE, validate

from ..base import ConditionBase, ABCMeta, abstractmethod

LOG = logging.getLogger(__name__)


class DayCondition(ConditionBase, metaclass=ABCMeta):
    """
        Base class for string conditions
    """

    class DateFormat:
        DAY_FORMAT = "%Y-%m-%d"
        ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

    def __init__(self, values, what, date_format=DateFormat.ISO_FORMAT, qualifier=ConditionBase.Qualifier.ForAnyValue,
                 **kwargs):
        self.values = values
        self.what = what
        self.qualifier = qualifier
        self.date_format = date_format

    @abstractmethod
    def _is_satisfied(self) -> bool:
        """
            Is string conditions satisfied

            :param what: string value to check
            :return: True if satisfied else False
        """
        raise NotImplementedError()

    def convert_str_to_date(self, d_str):
        try:
            return datetime.datetime.strptime(d_str, self.DateFormat.ISO_FORMAT)
        except:
            return None

    def check_format_input_day(self, i):
        if isinstance(i, str):
            if self.convert_str_to_date(i):
                return True
        return False

    def convert_string_to_day_format(self, date_str):
        return datetime.datetime.strptime(date_str, self.date_format).strftime(self.DateFormat.DAY_FORMAT)

    def convert_date_to_day_format(self, d):
        return d.strftime(self.DateFormat.DAY_FORMAT)

    def convert_timestamp_to_day_format(self, timestamp):
        # try:
        return datetime.datetime.fromtimestamp(timestamp).strftime(self.DateFormat.DAY_FORMAT)
        # except:
        #     return None

    def convert_string_to_day_format_from_parse(self, date_str):
        try:
            return parse(date_str).strftime(self.DateFormat.DAY_FORMAT)
        except:
            return None

    def convert_day_format_from_any(self, i):
        if isinstance(i, (int, float)):
            day_format = self.convert_timestamp_to_day_format(i)
        elif isinstance(i, str):
            day_format = self.convert_string_to_day_format_from_parse(i)
            if day_format is None:
                day_format = self.convert_string_to_day_format(i)
        elif isinstance(i, datetime.datetime):
            day_format = self.convert_date_to_day_format(i)
        else:
            return False
        return day_format


class DayConditionSchema(Schema):
    """
        Base JSON schema for string conditions
    """
    values = fields.List(fields.Raw(required=True, allow_none=True), required=True, allow_none=False)
    what = fields.Raw(required=True, allow_none=True)
    qualifier = fields.String(allow_none=False, load_default=ConditionBase.Qualifier.ForAnyValue,
                              validate=validate.OneOf(ConditionBase.Qualifier.ALL))
    date_format = fields.String(allow_none=False, load_default=DayCondition.DateFormat.ISO_FORMAT, )

    class Meta:
        unknown = EXCLUDE
