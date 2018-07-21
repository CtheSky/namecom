import unittest

from namecom import DnsApi, exceptions
from sample import (
    wrong_auth,
    record_sample1 as sample1
)


class ExceptionTestCase(unittest.TestCase):

    def test_permission_denied(self):
        api = DnsApi(sample1.domainName, auth=wrong_auth)

        def should_raise():
            api.get_record(sample1.id)
            pass

        self.assertRaises(exceptions.PermissionDenied, should_raise)

