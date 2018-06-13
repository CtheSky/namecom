# encoding=utf-8

import os
import unittest

from namecom import DomainApi, Domain
from . import test_env_auth

api = DomainApi(test_env_auth)
existing_domain = Domain(domainName='cthesky.band')
TEST_ALL = os.environ.get('TEST_ALL')


class DomainApiTestCase(unittest.TestCase):

    def test_search(self):
        search_result = api.search(keyword='cthesky', timeout=5000)

        results = search_result.results
        self.assertTrue(len(results))
        self.assertTrue(all([_.domainName for _ in results]))
        self.assertTrue(all([_.sld for _ in results]))
        self.assertTrue(all([_.tld for _ in results]))

    def test_list_domains(self):
        list_domains_result = api.list_domains()

        domains = list_domains_result.domains
        self.assertTrue(len(domains))

        domain_names = [domain.domainName for domain in domains]
        self.assertIn(existing_domain.domainName, domain_names)

    def test_get_domain(self):
        get_domain_result = api.get_domain(existing_domain.domainName)

        domain = get_domain_result.domain
        self.assertTrue(domain.domainName, existing_domain.domainName)

    @unittest.skipUnless(TEST_ALL, "don't buy domain everytime due to potential credit limit on testing account")
    def test_create_domain(self):
        """Search the domain, buy the cheapest available one."""
        search_result = api.search(keyword='cthesky', timeout=5000)

        results = search_result.results
        if not results:
            return
        cheapest_result = sorted([_ for _ in results if _.purchasable], key=lambda x: x.purchasePrice)[0]
        domain_to_buy = Domain(domainName=cheapest_result.domainName)

        create_domain_result = api.create_domain(domain_to_buy, cheapest_result.purchasePrice)

        print create_domain_result.domain, create_domain_result.order, create_domain_result.totalPaid
        self.assertIsNotNone(create_domain_result.domain)
        self.assertIsNotNone(create_domain_result.order)
        self.assertIsNotNone(create_domain_result.totalPaid)

    def test_enable_autorenew(self):
        enable_autorenew_result = api.enable_autorenew(existing_domain.domainName)

        domain = enable_autorenew_result.domain
        self.assertTrue(domain.autorenewEnabled)

    def test_disable_autorenew(self):
        disable_autorenew_result = api.disable_autorenew(existing_domain.domainName)

        domain = disable_autorenew_result.domain
        self.assertFalse(domain.autorenewEnabled)

    def test_set_nameservers(self):
        nameservers = ['ns1.name.com', 'ns2.name.com']
        set_nameservers_result = api.set_nameservers(existing_domain.domainName, nameservers)

        domain = set_nameservers_result.domain
        self.assertEqual(domain.domainName, existing_domain.domainName)
