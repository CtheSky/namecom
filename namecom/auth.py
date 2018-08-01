"""
namecom: auth.py

Contains Auth class which stores username & token
for api class to access the name.com service.

Tianhong Chu [https://github.com/CtheSky]
License: MIT
"""

__all__ = ['Auth']


class Auth(object):
    """
    The class for http basic authentication.
    Used by api class to do authenticate request.
    Could be found at token manage page: https://www.name.com/account/settings/api
    """

    def __init__(self, username, token):
        """
        Parameters
        ----------
        username : string
            username from token manage page
        token : string
            token value from token manage page
        """
        self.username = username
        self.token = token
