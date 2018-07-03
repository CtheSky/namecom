class NamecomError(Exception):
    """
    Base Exception class for namecom api.

    Attributes:
         status_code (int):
             http response status code

         headers (MutableMapping):
             http response headers from requests.Response

         message (string):
             a general error message

         details (string):
             an optional "details" key which contains a string with additional information about the error.
    """

    def __init__(self, status_code, headers, message, details):
        self.status_code = status_code
        self.headers = headers
        self.message = message
        self.details = details


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