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
        list_domains_result = api.list_domains()

        domains = list_domains_result.domains
        self.assertTrue(len(domains))

        domain_names = [domain.domainName for domain in domains]
        self.assertIn(sample1.domainName, domain_names)

    def test_get_domain(self):
        get_domain_result = api.get_domain(sample1.domainName)

        domain = get_domain_result.domain
        self.assertTrue(domain.domainName, sample1.domainName)

    def test_enable_autorenew(self):
        enable_autorenew_result = api.enable_autorenew(sample1.domainName)

        domain = enable_autorenew_result.domain
        self.assertTrue(domain.autorenewEnabled)

    def test_disable_autorenew(self):
        disable_autorenew_result = api.disable_autorenew(sample1.domainName)

        domain = disable_autorenew_result.domain
        self.assertFalse(domain.autorenewEnabled)

    def test_set_nameservers(self):
        set_nameservers_result = api.set_nameservers(sample1.domainName, sample1.nameservers)

        domain = set_nameservers_result.domain
        self.assertListEqual(domain.nameservers, sample1.nameservers)

    def test_set_contacts(self):
        set_contacts_result = api.set_contacts(sample1.domainName, sample1.contacts)

        domain = set_contacts_result.domain
        self.assertDictEqual(domain.contacts.to_dict(), sample1.contacts.to_dict())

    def test_get_auth_code_for_domain(self):
        get_auth_code_result = api.get_auth_code_for_domain(sample1.domainName)

        authCode = get_auth_code_result.authCode
        self.assertTrue(authCode)

    def test_lock_domain(self):
        lock_domain_result = api.lock_domain(sample1.domainName)

        domain = lock_domain_result.domain
        self.assertTrue(domain.locked)

    def test_check_availability(self):
        check_availability_result = api.check_availability(domainNames=[sample1.domainName])

        results = check_availability_result.results
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

        print create_domain_result.domain, create_domain_result.order, create_domain_result.totalPaid
        self.assertIsNotNone(create_domain_result.domain)
        self.assertIsNotNone(create_domain_result.order)
        self.assertIsNotNone(create_domain_result.totalPaid)

    @unittest.skipUnless(TEST_ALL, "save credit on testing account")
    def test_renew_domain(self):
        enable_autorenew_result = api.enable_autorenew(sample1.domainName)
        domain = enable_autorenew_result.domain

        renew_domain_result = api.renew_domain(domainName=domain.domainName, purchasePrice=domain.renewalPrice)

        print renew_domain_result.domain, renew_domain_result.order, renew_domain_result.totalPaid
        self.assertIsNotNone(renew_domain_result.domain)
        self.assertIsNotNone(renew_domain_result.order)
        self.assertIsNotNone(renew_domain_result.totalPaid)

    @unittest.skip("not sure about the correct purchasePrice")
    def test_purchase_privacy(self):
        purchase_privacy_result = api.purchase_privacy(sample2.domainName, purchasePrice=19.99)

        print purchase_privacy_result.domain, purchase_privacy_result.order, purchase_privacy_result.totalPaid
        self.assertIsNotNone(purchase_privacy_result.domain)
        self.assertIsNotNone(purchase_privacy_result.order)
        self.assertIsNotNone(purchase_privacy_result.totalPaid)

    @unittest.skip('domain should in a state that requires this operation')
    def test_unlock_domain(self):
        unlock_domain_result = api.unlock_domain(sample1.domainName)

        domain = unlock_domain_result.domain
        self.assertFalse(domain.locked)
