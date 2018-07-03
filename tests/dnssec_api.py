import unittest

from namecom import DnssecApi
from sample_data import (
    correct_auth,
    dnssec_sample1,
    dnssec_sample2
)

api = DnssecApi(domainName=dnssec_sample1.domainName, auth=correct_auth, use_test_env=True)


class DnssecApiTestCase(unittest.TestCase):

    def test_list_dnssec(self):
        list_dnssecs_result = api.list_dnssecs()

        dnssecs = list_dnssecs_result.dnssecs
        self.assertIn(dnssec_sample2, dnssecs)

    def test_get_dnssec(self):
        get_dnssec_result = api.get_dnssec(dnssec_sample2.digest)

        dnssec = get_dnssec_result.dnssec
        self.assertEqual(dnssec, dnssec_sample2)

    def test_create_delete_dnssec(self):
        create_dnssec_result = api.create_dnssec(
            keyTag=dnssec_sample1.keyTag,
            algorithm=dnssec_sample1.algorithm,
            digestType=dnssec_sample1.digestType,
            digest=dnssec_sample1.digest
        )

        dnssec = create_dnssec_result.dnssec
        self.assertEqual(dnssec, dnssec_sample1)

        delete_dnssec_result = api.delete_dnssec(dnssec_sample1.digest)
        self.assertEqual(delete_dnssec_result.status_code, 200)
