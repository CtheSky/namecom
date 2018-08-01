"""
namecom: exceptions.py

Defines exception classes

Tianhong Chu [https://github.com/CtheSky]
License: MIT
"""

_CODE_MSG_2_EXCEPTION = {}  # map (status_code, message) tuple to Exception class


def make_exception(resp):
    """Parse response content and return a NamecomError instance."""
    data = resp.json()

    status_code = resp.status_code
    headers = resp.headers
    message = data.get('message')
    details = data.get('details')

    try:
        klass = _CODE_MSG_2_EXCEPTION[(status_code, message)]
        return klass(status_code, headers, message, details)
    except KeyError:
        return NamecomError(status_code, headers, message, details)


class NamecomError(Exception):
    """Base Exception class for namecom api."""

    def __init__(self, status_code, headers, message, details):
        """

        Parameters
        ----------
        status_code : int
            http response status code

        headers : MutableMapping
            http response headers from requests.Response

        message : str
            a general error message

        details : str
            an optional "details" key which contains a string with additional
            information about the error
        """
        super(NamecomError, self).__init__()
        self.status_code = status_code
        self.headers = headers
        self.message = message
        self.details = details

    def __str__(self):
        return 'Namecom Error: status code [%s], message [%s], details [%s]' % \
               (self.status_code, self.message, self.details)


def _add_to_mapping(cls):
    """Decorator that register exceptions to _CODE_MSG_2_EXCEPTION mapping."""
    status_code = getattr(cls, 'status_code', None)
    message = getattr(cls, 'message', None)

    if status_code is not None and message is not None:
        _CODE_MSG_2_EXCEPTION[(status_code, message)] = cls

    return cls


@_add_to_mapping
class PermissionDeniedError(NamecomError):
    """Fixed params: status_code -> 403, message -> Permission Denied"""
    status_code = 403
    message = 'Permission Denied'


@_add_to_mapping
class InvalidArgumentError(NamecomError):
    """Fixed params: status_code -> 400, message -> Invalid Argument"""
    status_code = 400
    message = 'Invalid Argument'


@_add_to_mapping
class NotFoundError(NamecomError):
    """Fixed params: status_code -> 404, message -> Not Found"""
    status_code = 404
    message = 'Not Found'


@_add_to_mapping
class ServerError(NamecomError):
    """Fixed params: status_code -> 500, message -> Internal Error"""
    status_code = 500
    message = 'Internal Error'
