import unittest

from namecom import DnsApi, TransferApi, exceptions
from .sample import (
    correct_auth,
    wrong_auth,
    record_sample1 as sample1
)


class ExceptionTestCase(unittest.TestCase):

    def test_permission_denied(self):
        api = DnsApi(sample1.domainName, auth=wrong_auth, use_test_env=True)

        def should_raise():
            api.get_record(sample1.id)

        self.assertRaises(exceptions.PermissionDenied, should_raise)

    def test_server_error(self):
        api = TransferApi(auth=correct_auth, use_test_env=True)

        def should_raise():
            api.create_transfer('example.org', authCode='wrong_auth', purchasePrice=10.99)

        self.assertRaises(exceptions.ServerError, should_raise)

    def test_not_found(self):
        api = TransferApi(auth=correct_auth, use_test_env=True)

        def should_raise():
            api.get_transfer('notexist.org')

        self.assertRaises(exceptions.NotFoundError, should_raise)
