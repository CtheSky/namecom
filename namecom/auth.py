# encoding=utf-8


class Auth:

    def __init__(self, username, token, use_test_env=False):
        self.username = username
        self.token = token
        self.use_test_env = use_test_env

    @property
    def auth_tuple(self):
        return self.username, self.token
