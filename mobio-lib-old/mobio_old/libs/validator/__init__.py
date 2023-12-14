#!/usr/bin/python
# -*- coding: utf8 -*-

"""
validator.py

A library for validating that dictionary
values fit inside of certain sets of parameters.
"""
import json
import os
import re
from abc import ABCMeta, abstractmethod
from collections import defaultdict
from collections import namedtuple

# from flask import request, abort, json

basestring = str

__version__ = "1.2.5"

RESOURCE_OF_HTTP_VALIDATE = None
try:
    RESOURCE_OF_HTTP_VALIDATE, _ = os.path.split(os.path.abspath(__file__))
except Exception as ex:
    print(ex)
    pass


def __open_file(path):
    try:
        return open(path, encoding='UTF-8', mode='r')
    except UnicodeDecodeError:
        return open(path, encoding='ASCII', mode='r')


def __load_lang_json(param):
    if RESOURCE_OF_HTTP_VALIDATE:
        path = '%s/message_vi.json' % RESOURCE_OF_HTTP_VALIDATE

        if param == 'en':
            path = '%s/message_en.json' % RESOURCE_OF_HTTP_VALIDATE

        with __open_file(path) as data_file:
            return json.loads(data_file.read())

    return None


__lang_dict_vi = __load_lang_json('vi')
__lang_dict_en = __load_lang_json('en')


def _get_lang():
    param = 'en'
    try:
        from flask import request
        param = request.args.get('lang')
        if param and param not in ('vi', 'en'):
            param = 'en'
    except Exception as lex:
        print(lex)
        pass

    return __lang_dict_en if param == 'en' else __lang_dict_vi


class VALIDATION_RESULT:
    CLASS_NAME = 'ValidationResult'
    VALID = 0
    ERRORS = 1


ValidationResult = namedtuple('ValidationResult', ['valid', 'errors'])


def _isstr(s):
    """
    Python 2/3 compatible check to see
    if an object is a string type.

    """

    try:
        return isinstance(s, basestring)
    except NameError:
        return isinstance(s, str)


class Validator(object):
    """
    Abstract class that advanced
    validators can inherit from in order
    to set custom error messages and such.

    """

    __metaclass__ = ABCMeta

    err_message = "failed validation"
    not_message = "failed validation"

    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    _lang_dict = None

    def set_lang_message(self, message_name):
        lang_dict = _get_lang()
        if lang_dict:
            self.err_message = lang_dict[message_name]['err_message']
            self.not_message = lang_dict[message_name]['not_message']
            return True
        return False


class In(Validator):
    """
    Use to specify that the
    value of the key being
    validated must exist
    within the collection
    passed to this validator.

    """

    def __init__(self, collection):
        self.collection = collection
        self.err_message = "must be one of %r" % collection
        self.not_message = "must not be one of %r" % collection
        if self.set_lang_message('in'):
            self.err_message %= collection
            self.not_message %= collection

    def __call__(self, a_value):
        return a_value in self.collection


class Not(Validator):
    """
    Use to negate the requirement
    of another validator. Does not
    work with Required.

    """

    def __init__(self, validator):
        self.validator = validator
        self.err_message = getattr(validator, "not_message", "failed validation")
        self.not_message = getattr(validator, "err_message", "failed validation")
        lang_dict = _get_lang()
        if lang_dict:
            self.err_message = getattr(validator, "not_message", lang_dict['validator']["not_message"])
            self.not_message = getattr(validator, "err_message", lang_dict['validator']["err_message"])

    def __call__(self, a_value):
        return not self.validator(a_value)


class Range(Validator):
    """
    Use to specify that the value of the
    key being validated must fall between
    the start and end values. By default
    the range is inclusive, though the
    range can be made excusive by setting
    inclusive to false.

    """

    def __init__(self, start, end, inclusive=True):
        self.start = start
        self.end = end
        self.inclusive = inclusive
        self.err_message = "must fall between %s and %s" % (start, end)
        self.not_message = "must not fall between %s and %s" % (start, end)
        if self.set_lang_message('range'):
            self.err_message %= (start, end)
            self.not_message %= (start, end)

    def __call__(self, a_value):
        if self.inclusive:
            return self.start <= a_value <= self.end
        else:
            return self.start < a_value < self.end


class Equals(Validator):
    """
    Use to specify that the
    value of the key being
    validated must be equal to
    the value that was passed
    to this validator.

    """

    def __init__(self, obj):
        self.obj = obj
        self.err_message = "must be equal to %r" % obj
        self.not_message = "must not be equal to %r" % obj
        if self.set_lang_message('equals'):
            self.err_message %= obj
            self.not_message %= obj

    def __call__(self, a_value):
        return a_value == self.obj


class Blank(Validator):
    """
    Use to specify that the
    value of the key being
    validated must be equal to
    the empty string.

    This is a shortcut for saying
    Equals("").

    """

    def __init__(self):
        self.err_message = "must be an empty string"
        self.not_message = "must not be an empty string"
        self.set_lang_message('blank')

    def __call__(self, a_value):
        return a_value == ""


class Truthy(Validator):
    """
    Use to specify that the
    value of the key being
    validated must be truthy,
    i.e. would cause an if statement
    to evaluate to True.

    """

    def __init__(self):
        self.err_message = "must be True-equivalent value"
        self.not_message = "must be False-equivalent value"
        self.set_lang_message('truthy')

    def __call__(self, a_value):
        if a_value:
            return True
        else:
            return False


def Required(field, dictionary):
    """
    When added to a list of validations
    for a dictionary key indicates that
    the key must be present. This
    should not be called, just inserted
    into the list of validations.

    # Example:
        validations = {
            "field": [Required, Equals(2)]
        }

    By default, keys are considered
    optional and their validations
    will just be ignored if the field
    is not present in the dictionary
    in question.

    """

    return field in dictionary


class InstanceOf(Validator):
    """
    Use to specify that the
    value of the key being
    validated must be an instance
    of the passed in base class
    or its subclasses.

    """

    def __init__(self, base_class):
        self.base_class = base_class
        self.err_message = "must be an instance of %s or its subclasses" % base_class.__name__
        self.not_message = "must not be an instance of %s or its subclasses" % base_class.__name__
        if self.set_lang_message('instance_of'):
            self.err_message %= base_class.__name__
            self.not_message %= base_class.__name__

    def __call__(self, a_value):
        return isinstance(a_value, self.base_class)


class InstanceOfAllowNull(Validator):
    """
    Use to specify that the
    value of the key being
    validated must be an instance
    of the passed in base class
    or its subclasses.
    """

    def __init__(self, base_class):
        self.base_class = base_class
        self.err_message = "must be an instance of %s or its subclasses" % base_class.__name__
        self.not_message = "must not be an instance of %s or its subclasses" % base_class.__name__
        if self.set_lang_message('instance_of'):
            self.err_message %= base_class.__name__
            self.not_message %= base_class.__name__

    def __call__(self, a_value):
        # return isinstance(a_value, self.base_class)
        return isinstance(a_value, (self.base_class, type(None)))


class SubclassOf(Validator):
    """
    Use to specify that the
    value of the key being
    validated must be a subclass
    of the passed in base class.
    """

    def __init__(self, base_class):
        self.base_class = base_class
        self.err_message = "must be a subclass of %s" % base_class.__name__
        self.not_message = "must not be a subclass of %s" % base_class.__name__
        if self.set_lang_message('subclass_of'):
            self.err_message %= base_class.__name__
            self.not_message %= base_class.__name__

    def __call__(self, class_):
        return issubclass(class_, self.base_class)


class Pattern(Validator):
    """
    Use to specify that the
    value of the key being
    validated must match the
    pattern provided to the
    validator.
    """

    def __init__(self, pattern):
        self.pattern = pattern
        self.err_message = "must match regex pattern %s" % pattern
        self.not_message = "must not match regex pattern %s" % pattern
        self.compiled = re.compile(pattern)
        if self.set_lang_message('pattern'):
            self.err_message %= pattern
            self.not_message %= pattern

    def __call__(self, a_value):
        return self.compiled.match(a_value)


class Then(Validator):
    """
    Special validator for use as
    part of the If rule.
    If the conditional part of the validation
    passes, then this is used to apply another
    set of dependent rules.
    """

    def __init__(self, validation):
        self.validation = validation

    def __call__(self, dictionary):
        return validate(self.validation, dictionary)


class If(Validator):
    """
    Special conditional validator.
    If the validator passed as the first
    parameter to this function passes,
    then a second set of rules will be
    applied to the dictionary.
    """

    def __init__(self, validator, then_clause):
        self.validator = validator
        self.then_clause = then_clause

    def __call__(self, a_value, dictionary):
        conditional = False
        dependent = None
        if self.validator(a_value):
            conditional = True
            dependent = self.then_clause(dictionary)
        return conditional, dependent


class Length(Validator):
    """
    Use to specify that the
    value of the key being
    validated must have at least
    `minimum` elements and optionally
    at most `maximum` elements.

    At least one of the parameters
    to this validator must be non-zero,
    and neither may be negative.
    """

    err_messages = {
        "maximum": "must be at most {0} elements in length",
        "minimum": "must be at least {0} elements in length",
        "range": "must{0}be between {1} and {2} elements in length"
    }

    def __init__(self, minimum, maximum=0):
        if not minimum and not maximum:
            raise ValueError("Length must have a non-zero minimum or maximum parameter.")
        if minimum < 0 or maximum < 0:
            raise ValueError("Length cannot have negative parameters.")

        lang_dict = _get_lang()
        if lang_dict:
            self.err_messages = lang_dict['length']

        self.minimum = minimum
        self.maximum = maximum
        if minimum and maximum:
            self.err_message = self.err_messages["range"].format(' ', minimum, maximum)
            self.not_message = self.err_messages["range"].format(' not ', minimum, maximum)
        elif minimum:
            self.err_message = self.err_messages["minimum"].format(minimum)
            self.not_message = self.err_messages["maximum"].format(minimum - 1)
        elif maximum:
            self.err_message = self.err_messages["maximum"].format(maximum)
            self.not_message = self.err_messages["minimum"].format(maximum + 1)

    def __call__(self, a_value):
        if self.maximum:
            return self.minimum <= len(a_value) <= self.maximum
        else:
            return self.minimum <= len(a_value)


class Contains(Validator):
    """
    Use to ensure that the value of the key
    being validated contains the value passed
    into the Contains validator. Works with
    any type that supports the 'in' syntax.
    """

    def __init__(self, contained):
        self.contained = contained
        self.err_message = "must contain {0}".format(contained)
        self.not_message = "must not contain {0}".format(contained)
        if self.set_lang_message('contains'):
            self.err_message = self.err_message.format(contained)
            self.not_message = self.not_message.format(contained)

    def __call__(self, container):
        return self.contained in container


class Each(Validator):
    """
    Use to ensure that

    If Each is passed a list of validators, it
    just applies each of them to each element in
    the list.

    If it's instead passed a *dictionary*, it treats
    it as a validation to be applied to each element in
    the dictionary.

    """

    def __init__(self, validations):
        assert isinstance(validations, (list, tuple, set, dict))
        self.validations = validations

    def __call__(self, container):
        assert isinstance(container, (list, tuple, set))
        errors = []
        # handle the "apply simple validation to each in list"
        # use case
        if isinstance(self.validations, (list, tuple, set)):
            for item in container:
                for valid in self.validations:
                    valid = valid(item)
                    if not valid:
                        errors.append("all values " + valid.err_message)

        # handle the somewhat messier list of dicts case
        if isinstance(self.validations, dict):
            errors = defaultdict(list)
            for index, item in enumerate(container):
                valid, err = validate(self.validations, item)
                if not valid:
                    errors[index] = err
            errors = dict(errors)
        return len(errors) == 0, errors


def validate(validation, dictionary):
    """
    Validate that a dictionary passes a set of
    key-based validators. If all of the keys
    in the dictionary are within the parameters
    specified by the validation mapping, then
    the validation passes.

    :param validation: a mapping of keys to validators
    :type validation: dict

    :param dictionary: dictionary to be validated
    :type dictionary: dict

    :return: a tuple containing a bool indicating
    success or failure and a mapping of fields
    to error messages.

    """

    errors = defaultdict(list)
    for a_key in validation:
        if isinstance(validation[a_key], (list, tuple)):
            if Required in validation[a_key]:
                if not Required(a_key, dictionary):
                    errors[a_key] = "must be present"
                    continue
            _validate_list_helper(validation, dictionary, a_key, errors)
        else:
            valid = validation[a_key]
            if valid == Required:
                if not Required(a_key, dictionary):
                    errors[a_key] = "must be present"
            else:
                _validate_and_store_errs(valid, dictionary, a_key, errors)
    if len(errors) > 0:
        # `errors` gets downgraded from default dict to dict
        # because it makes for prettier output
        return ValidationResult(valid=False, errors=dict(errors))
    else:
        return ValidationResult(valid=True, errors={})


def _validate_and_store_errs(validator, dictionary, a_key, errors):
    # Validations shouldn't throw exceptions because of
    # type mismatches and the like. If the rule is 'Length(5)' and
    # the value in the field is 5, that should be a validation failure,
    # not a TypeError because you can't call len() on an int.
    # It's not ideal to have to hide exceptions like this because
    # there could be actual problems with a validator, but we're just going
    # to have to rely on tests preventing broken things.
    try:
        valid = validator(dictionary[a_key])
    except Exception as ex:
        print("http_validator/_validate_and_store_errs", ex)
        # Since we caught an exception while trying to validate,
        # treat it as a failure and return the normal error message
        # for that validator.
        valid = (False, validator.err_message)
    if isinstance(valid, tuple):
        valid, errs = valid
        if errs and isinstance(errs, list):
            errors[a_key] += errs
        elif errs:
            errors[a_key].append(errs)
    elif not valid:
        # set a default error message for things like lambdas
        # and other callable that won't have an err_message set.
        msg = getattr(validator, "err_message", "failed validation")
        errors[a_key].append(msg)


def _validate_list_helper(validation, dictionary, a_key, errors):
    for valid in validation[a_key]:
        # don't break on optional keys
        if a_key in dictionary:
            # Ok, need to deal with nested
            # validations.
            if isinstance(valid, dict):
                _, nested_errors = validate(valid, dictionary[a_key])
                if nested_errors:
                    errors[a_key].append(nested_errors)
                continue
            # Done with that, on to the actual
            # validating bit.
            # Skip Required, since it was already
            # handled before this point.
            if not valid == Required:
                # special handling for the
                # If(Then()) form
                if isinstance(valid, If):
                    conditional, dependent = valid(dictionary[a_key], dictionary)
                    # if the If() condition passed and there were errors
                    # in the second set of rules, then add them to the
                    # list of errors for the key with the condtional
                    # as a nested dictionary of errors.
                    if conditional and dependent[1]:
                        errors[a_key].append(dependent[1])
                # handling for normal validators
                else:
                    _validate_and_store_errs(valid, dictionary, a_key, errors)


def get_field(obj, field_name, default_value):
    if obj[field_name] is None:
        return default_value
    else:
        return obj[field_name]


class HttpValidator(object):
    def __init__(self, rules):
        self.rules = rules

    def validate_object(self, obj):
        for field in obj:
            if field not in self.rules:
                return ValidationResult(valid=False, errors={field: 'field have not in Rules'})

        return validate(self.rules, obj)

    def validate_optional(self, obj):
        for field in obj:
            if field not in self.rules:
                self.rules[field] = []
        return validate(self.rules, obj)

    def validate_field(self, obj, field_name):
        if field_name not in self.rules:
            return ValidationResult(valid=False, errors={field_name: 'field have not in Rules'})

        rul = {field_name: self.rules[field_name]}
        dic = {field_name: obj[field_name]}
        return validate(rul, dic)


class PhoneNumber(Validator):
    """
    Use to specify that the
    value of the key being
    validated must match the
    pattern provided to the
    validator.
    """

    def __init__(self):
        pattern = r'\(?([0-9]{3})\)?([ .-]?)([0-9]{3})\2([0-9]{4})'
        self.err_message = "must match regex pattern example (098) 883 0588 or " \
                           "(098).883.0588 or (098)-883-0588 or 098-883-0588 or 098 883 0588 or 0988830588"
        self.not_message = "must not match regex pattern %s" % pattern

        if self.set_lang_message('phone_number'):
            self.not_message %= pattern

        self.compiled = re.compile(pattern)

    def __call__(self, a_value):
        return self.compiled.match(a_value)


class Email(Validator):
    """
    Use to specify that the
    value of the key being
    validated must match the
    pattern provided to the
    validator.
    """

    def __init__(self):
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        self.err_message = "must match regex pattern example lytuananh2003@gmail.com"
        self.not_message = "must not match regex pattern %s" % pattern
        self.compiled = re.compile(pattern)

        if self.set_lang_message('email'):
            self.not_message %= pattern

    def __call__(self, a_value):
        return self.compiled.match(a_value)


class Password(Validator):
    """
    Use to specify that the
    value of the key being
    validated must match the
    pattern provided to the
    validator.
    password requires:
        - contains at least 8 characters,
        - contains least 1 number,
        - contains least one alphabet 1 (a-z)
        - contain at least 1 capital letter (A-Z),
        - contains only 0-9a-zA-Z
    """

    def __init__(self):
        pattern = r"(^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$)"
        self.err_message = "Invalid new password, password needed:contains at least 8 characters," \
                           "contains at least one number,Contains at least 1 lowercase letter (a-z), " \
                           "contain at least 1 capital letter (A-Z),contains only 0-9a-zA-Z. pattern: %s"
        self.not_message = "Invalid new password, password not needed:contains at least 8 characters," \
                           "contains at least one number,Contains at least 1 lowercase letter (a-z), " \
                           "contain at least 1 capital letter (A-Z),contains only 0-9a-zA-Z. pattern: %s"
        self.compiled = re.compile(pattern)

        if self.set_lang_message('password'):
            self.err_message %= pattern
            self.not_message %= pattern

    def __call__(self, a_value):
        return self.compiled.match(a_value)


class DateTime(Validator):
    """
    Use to specify that the
    value of the key being
    validated must match the
    pattern provided to the
    validator.
    """

    def __init__(self):
        pattern = r"^([0-9]{2,4})-([0-1][0-9])-([0-3][0-9])(?:( [0-2][0-9]):([0-5][0-9]):([0-5][0-9]))?$"
        self.err_message = "must match regex pattern example: 2017-04-30 19:59:00"
        self.not_message = "must not match regex pattern %s" % pattern
        self.compiled = re.compile(pattern)

        if self.set_lang_message('date_time'):
            self.not_message %= pattern

    def __call__(self, a_value):
        return self.compiled.match(a_value)


class Unicode(Validator):
    """
    Use to specify that the
    value of the key being
    validated must be unicode,
    i.e. would cause an if statement
    to evaluate to True.
    """

    def __init__(self):
        self.err_message = "must be unicode value"
        self.not_message = "must be not unicode value"
        self.set_lang_message('unicode')

    def __call__(self, a_value):
        try:
            a_value.encode('utf-8')
            # field is unicode
            return True
        except TypeError:
            # field is not unicode
            return False
