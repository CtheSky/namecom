__all__ = ['Auth']


class Auth:

    def __init__(self, username, token):
        self.username = username
        self.token = token

    @property
    def auth_tuple(self):
        return self.username, self.token
