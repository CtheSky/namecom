# encoding=utf-8

import unittest

from namecom import DnssecApi
from . import test_env_auth
from sample_data import dnssec as dnssec_sample

api = DnssecApi(domainName=dnssec_sample.domainName, auth=test_env_auth)


class DnssecApiTestCase(unittest.TestCase):

    def test_create_delete_dnssec(self):
        create_dnssec_result = api.create_dnssec(
            keyTag=dnssec_sample.keyTag,
            algorithm=dnssec_sample.algorithm,
            digestType=dnssec_sample.digestType,
            digest=dnssec_sample.digest
        )

        dnssec = create_dnssec_result.dnssec
        self.assertEqual(dnssec, dnssec_sample)

        delete_dnssec_result = api.delete_dnssec(dnssec_sample.digest)
        self.assertEqual(delete_dnssec_result.status_code, 200)
