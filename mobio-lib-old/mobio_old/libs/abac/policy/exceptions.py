
class ErrorCodeException:
    GET_VALUE_NONE = 1001
    CONDITION_INVALID = 1002
    CONDITION_EMPTY = 1003
    CHECK_POLICY = 1004
    REQUEST_ACCESS_CREATE = 1005

class BaseException(Exception):
    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = message
        super().__init__(self.message)

class GetValueNoneException(BaseException):
    def __init__(self, message):
        error_code = ErrorCodeException.GET_VALUE_NONE
        message = " - " + str(error_code) + ": {}".format(message)
        super().__init__(error_code, message)

class InvalidConditionException(BaseException):
    def __init__(self, message):
        error_code = ErrorCodeException.CONDITION_INVALID
        message = " - " + str(error_code) + ": {}".format(message)
        super().__init__(error_code, message)

class EmptyConditionException(BaseException):
    def __init__(self, message):
        error_code = ErrorCodeException.CONDITION_EMPTY
        message = " - " + str(error_code) + ": {}".format(message)
        super().__init__(error_code, message)

class CheckPolicyException(BaseException):
    def __init__(self, message):
        error_code = ErrorCodeException.CHECK_POLICY
        message = " - " + str(error_code) + ": {}".format(message)
        super().__init__(error_code, message)

class RequestAccessCreateException(BaseException):
    def __init__(self, message):
        error_code = ErrorCodeException.REQUEST_ACCESS_CREATE
        message = " - " + str(error_code) + ": {}".format(message)
        super().__init__(error_code, message)