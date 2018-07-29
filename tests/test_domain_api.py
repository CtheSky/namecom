import os
import unittest

from namecom import DomainApi, Domain
from .sample import (
    correct_auth,
    domain_sample1 as sample1,
    domain_sample2 as sample2
)

TEST_ALL = os.environ.get('TEST_ALL')
api = DomainApi(auth=correct_auth, use_test_env=True)


class DomainApiTestCase(unittest.TestCase):

    def test_list_domains(self):
        result = api.list_domains()

        domains = result.domains
        self.assertTrue(len(domains))

        domain_names = [domain.domainName for domain in domains]
        self.assertIn(sample1.domainName, domain_names)

    def test_get_domain(self):
        result = api.get_domain(sample1.domainName)

        domain = result.domain
        self.assertTrue(domain.domainName, sample1.domainName)

    def test_enable_autorenew(self):
        result = api.enable_autorenew(sample1.domainName)

        domain = result.domain
        self.assertTrue(domain.autorenewEnabled)

    def test_disable_autorenew(self):
        result = api.disable_autorenew(sample1.domainName)

        domain = result.domain
        self.assertFalse(domain.autorenewEnabled)

    def test_set_nameservers(self):
        result = api.set_nameservers(sample1.domainName, sample1.nameservers)

        domain = result.domain
        self.assertListEqual(domain.nameservers, sample1.nameservers)

    def test_set_contacts(self):
        result = api.set_contacts(sample1.domainName, sample1.contacts)

        domain = result.domain
        self.assertDictEqual(domain.contacts.to_dict(), sample1.contacts.to_dict())

    def test_get_auth_code_for_domain(self):
        result = api.get_auth_code_for_domain(sample1.domainName)

        authCode = result.authCode
        self.assertTrue(authCode)

    def test_lock_domain(self):
        result = api.lock_domain(sample1.domainName)

        domain = result.domain
        self.assertTrue(domain.locked)

    def test_check_availability(self):
        result = api.check_availability(domainNames=[sample1.domainName])

        results = result.results
        self.assertTrue(len(results) == 1)

        search_result = results[0]
        self.assertTrue(search_result.domainName, sample1.domainName)

    def test_search(self):
        search_result = api.search(keyword='cthesky', timeout=5000)

        results = search_result.results
        if results:
            self.assertTrue(all([_.domainName for _ in results]))
            self.assertTrue(all([_.sld for _ in results]))
            self.assertTrue(all([_.tld for _ in results]))
            self.assertIn('cthesky', [_.sld for _ in results])

    def test_search_stream(self):
        search_stream_result = api.search_stream(keyword='cthesky', timeout=5000)

        results = search_stream_result.results
        if results:
            self.assertTrue(all([_.domainName for _ in results]))
            self.assertTrue(all([_.sld for _ in results]))
            self.assertTrue(all([_.tld for _ in results]))
            self.assertIn('cthesky', [_.sld for _ in results])

    @unittest.skipUnless(TEST_ALL, "save credit on testing account")
    def test_create_domain(self):
        """Search the domain, buy the cheapest available one."""
        search_result = api.search(keyword='cthesky', timeout=5000)

        results = search_result.results
        if not results:
            return
        cheapest_result = sorted([_ for _ in results if _.purchasable], key=lambda x: x.purchasePrice)[0]
        domain_to_buy = Domain(domainName=cheapest_result.domainName)

        create_domain_result = api.create_domain(domain_to_buy, cheapest_result.purchasePrice)

        self.assertIsNotNone(create_domain_result.domain)
        self.assertIsNotNone(create_domain_result.order)
        self.assertIsNotNone(create_domain_result.totalPaid)

    @unittest.skipUnless(TEST_ALL, "save credit on testing account")
    def test_renew_domain(self):
        result = api.enable_autorenew(sample1.domainName)
        domain = result.domain

        result = api.renew_domain(domainName=domain.domainName, purchasePrice=domain.renewalPrice)

        self.assertIsNotNone(result.domain)
        self.assertIsNotNone(result.order)
        self.assertIsNotNone(result.totalPaid)

    @unittest.skip("not sure about the correct purchasePrice")
    def test_purchase_privacy(self):
        result = api.purchase_privacy(sample2.domainName, purchasePrice=19.99)

        self.assertIsNotNone(result.domain)
        self.assertIsNotNone(result.order)
        self.assertIsNotNone(result.totalPaid)

    @unittest.skip('domain should in a state that requires this operation')
    def test_unlock_domain(self):
        result = api.unlock_domain(sample1.domainName)

        domain = result.domain
        self.assertFalse(domain.locked)
