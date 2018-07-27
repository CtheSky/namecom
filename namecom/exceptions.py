"""
namecom: exceptions.py

Defines exception classes

Tianhong Chu [https://github.com/CtheSky]
License: MIT
"""


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
            an optional "details" key which contains a string with additional information about the error
        """
        self.status_code = status_code
        self.headers = headers
        self.message = message
        self.details = details

    def __str__(self):
        return 'Namecom Error: status code [%s], message [%s], details [%s]' % \
               (self.status_code, self.message, self.details)


_error2exception = {}  # map (status_code, message) tuple to Exception class


def make_exception(resp):
    """Parse response content and return a NamecomError instance."""
    data = resp.json()

    status_code = resp.status_code
    headers = resp.headers
    message = data.get('message')
    details = data.get('details')

    try:
        klass = _error2exception[(status_code, message)]
        return klass(status_code, headers, message, details)
    except KeyError:
        return NamecomError(status_code, headers, message, details)


def add_to_mapping(cls):
    """Decorator that register exceptions to _error2exception."""
    status_code = getattr(cls, 'status_code', None)
    message = getattr(cls, 'message', None)

    if status_code is not None and message is not None:
        _error2exception[(status_code, message)] = cls

    return cls


@add_to_mapping
class PermissionDenied(NamecomError):
    status_code = 403
    message = 'Permission Denied'


@add_to_mapping
class InvalidArgument(NamecomError):
    status_code = 400
    message = 'Invalid Argument'


@add_to_mapping
class ServerError(NamecomError):
    status_code = 500
    message = 'Internal Error'
