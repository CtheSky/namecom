# encoding=utf-8

import os
import unittest

from namecom import DomainApi, Domain, Contact, Contacts
from . import test_env_auth

TEST_ALL = os.environ.get('TEST_ALL')

api = DomainApi(test_env_auth)

contact = Contact(
    firstName='Tianhong', lastName='Chu', phone='+86.13818231324', email='cthesky@yeah.net',
    country='CN', city='Shanghai', state='Shanghai', zip='200090',
    address1='Room 501, Building 18, 3031 ChangYang Road, YangPu District, Shanghai City')
contacts = Contacts(admin=contact, tech=contact, registrant=contact, billing=contact)
existing_domain = Domain(domainName='cthesky.band',
                         contacts=contacts,
                         nameservers=['ns2fln.name.com', 'ns3cna.name.com'])


class DomainApiTestCase(unittest.TestCase):

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
        set_nameservers_result = api.set_nameservers(existing_domain.domainName, existing_domain.nameservers)

        domain = set_nameservers_result.domain
        self.assertListEqual(domain.nameservers, existing_domain.nameservers)

    def test_set_contacts(self):
        set_contacts_result = api.set_contacts(existing_domain.domainName, existing_domain.contacts)

        domain = set_contacts_result.domain
        self.assertDictEqual(domain.contacts.to_dict(), existing_domain.contacts.to_dict())

    def test_get_auth_code_for_domain(self):
        get_auth_code_result = api.get_auth_code_for_domain(existing_domain.domainName)

        authCode = get_auth_code_result.authCode
        self.assertTrue(authCode)

    def test_lock_domain(self):
        lock_domain_result = api.lock_domain(existing_domain.domainName)

        domain = lock_domain_result.domain
        self.assertTrue(domain.locked)

    def test_unlock_domain(self):
        unlock_domain_result = api.unlock_domain(existing_domain.domainName)

        domain = unlock_domain_result.domain
        self.assertFalse(domain.locked)

    def test_check_availability(self):
        check_availability_result = api.check_availability(domainNames=[existing_domain.domainName])

        results = check_availability_result.results
        self.assertTrue(len(results) == 1)

        search_result = results[0]
        self.assertTrue(search_result.domainName, existing_domain.domainName)

    def test_search(self):
        search_result = api.search(keyword='cthesky', timeout=5000)

        results = search_result.results
        self.assertTrue(len(results))
        self.assertTrue(all([_.domainName for _ in results]))
        self.assertTrue(all([_.sld for _ in results]))
        self.assertTrue(all([_.tld for _ in results]))
        self.assertIn('cthesky', [_.sld for _ in results])

    def test_search_stream(self):
        search_stream_result = api.search_stream(keyword='cthesky', timeout=5000)

        results = search_stream_result.results
        self.assertTrue(len(results))
        self.assertTrue(all([_.domainName for _ in results]))
        self.assertTrue(all([_.sld for _ in results]))
        self.assertTrue(all([_.tld for _ in results]))
        self.assertIn('cthesky', [_.sld for _ in results])
