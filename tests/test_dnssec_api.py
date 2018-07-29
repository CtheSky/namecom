import unittest

from namecom import DnssecApi, exceptions
from .sample import (
    correct_auth,
    dnssec_sample1 as sample1,
    dnssec_sample2 as sample2
)

api = DnssecApi(domainName=sample1.domainName, auth=correct_auth, use_test_env=True)


class DnssecApiTestCase(unittest.TestCase):

    def test_list_dnssec(self):
        result = api.list_dnssecs()

        dnssecs = result.dnssecs
        self.assertIn(sample2, dnssecs)

    def test_get_dnssec(self):
        result = api.get_dnssec(sample2.digest)

        dnssec = result.dnssec
        self.assertEqual(dnssec, sample2)

    def test_create_delete_dnssec(self):
        # cleanup existing data
        try:
            api.delete_dnssec(sample1.digest)
        except exceptions.NamecomError:
            pass

        result = api.create_dnssec(
            keyTag=sample1.keyTag,
            algorithm=sample1.algorithm,
            digestType=sample1.digestType,
            digest=sample1.digest
        )

        dnssec = result.dnssec
        self.assertEqual(dnssec, sample1)

        result = api.delete_dnssec(sample1.digest)
        self.assertEqual(result.status_code, 200)
