import unittest

from namecom import VanityNameserverApi, exceptions
from .sample import (
    correct_auth,
    vanity_nameserver_sample1 as sample1,
    vanity_nameserver_sample2 as sample2
)

api = VanityNameserverApi(domainName=sample1.domainName, auth=correct_auth, use_test_env=True)


class VanityNameserverApiTestCase(unittest.TestCase):

    def test_create_get_list_update_delete(self):
        # clean existing data
        try:
            api.delete_vanity_nameserver(sample1.hostname)
        except exceptions.NamecomError:
            pass

        result = api.create_vanity_nameserver(hostname=sample1.hostname, ips=sample1.ips)
        self.assertEqual(result.vanityNameserver, sample1)

        result = api.get_vanity_nameserver(sample1.hostname)
        self.assertEqual(result.vanityNameserver, sample1)

        result = api.list_vanity_nameservers()
        self.assertIn(sample1.hostname, [_.hostname for _ in result.vanityNameservers])

        result = api.update_vanity_nameserver(sample2.hostname, sample2.ips)
        self.assertEqual(sample2, result.vanityNameserver)

        result = api.delete_vanity_nameserver(sample2.hostname)
        self.assertEqual(result.status_code, 200)
