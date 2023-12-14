"""
    Operation base class
"""

from abc import ABCMeta, abstractmethod
import re

# from py_abac.context import EvaluationContext
# what is value of field, values is list value policy
MapAnyValue = ""

patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}


class ConditionBase(metaclass=ABCMeta):
    """
        Base class for conditions
    """

    # @abstractmethod
    # def is_satisfied(self, ctx: EvaluationContext) -> bool:
    #     """
    #         Is conditions satisfied?
    #
    #         :param ctx: evaluation context
    #         :return: True if satisfied else False
    #     """
    #     raise NotImplementedError()

    class Qualifier:
        ForAnyValue = "ForAnyValue"
        ForAllValues = "ForAllValues"
        ALL = [ForAnyValue, ForAllValues]

    @classmethod
    def value_is_none(cls, value):
        if not value and value not in [0, False]:
            return True
        return False

    @classmethod
    def utf8_to_ascii(cls, text):
        if not isinstance(text, str):
            return ''
        output = text
        for regex, replace in patterns.items():
            output = re.sub(regex, replace, output)
            output = re.sub(regex.upper(), replace.upper(), output)
        return output.lower()
