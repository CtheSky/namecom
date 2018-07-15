import unittest

from namecom import URLForwardingApi
from sample_data import (
    correct_auth,
    url_forwarding_sample1,
    url_forwarding_sample2
)

api = URLForwardingApi(domainName=url_forwarding_sample1.domainName, auth=correct_auth, use_test_env=True)


class URLForwardingApiTestCase(unittest.TestCase):

    def test_create_get_list_update_delete(self):
        result = api.create_url_forwarding(host=url_forwarding_sample1.host,
                                           forwardsTo=url_forwarding_sample1.forwardsTo,
                                           type=url_forwarding_sample1.type)
        self.assertEqual(result.url_forwarding, url_forwarding_sample1)

        result = api.get_url_forwarding(url_forwarding_sample1.host)
        self.assertEqual(result.url_forwarding, url_forwarding_sample1)

        result = api.list_url_forwardings()
        self.assertIn(url_forwarding_sample1, result.url_forwardings)

        result = api.update_url_forwarding(host=url_forwarding_sample2.host,
                                           forwardsTo=url_forwarding_sample2.forwardsTo,
                                           type=url_forwarding_sample2.type)
        self.assertEqual(result.url_forwarding, url_forwarding_sample2)

        result = api.delete_url_forwarding(host=url_forwarding_sample2.host)
        self.assertEqual(result.status_code, 200)
