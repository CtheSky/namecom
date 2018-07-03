import unittest

from namecom import DnsApi, exceptions
from sample_data import (
    wrong_auth,
    record_sample1 as record_sample
)


class ExceptionTestCase(unittest.TestCase):

    def test_permission_denied(self):
        api = DnsApi(record_sample.domainName, auth=wrong_auth)

        def should_raise():
            api.get_record(record_sample.id)
            pass

        self.assertRaises(exceptions.PermissionDenied, should_raise)

