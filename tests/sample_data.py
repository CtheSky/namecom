# -*- coding: utf-8 -*-

from namecom import Domain, Contact, Contacts, Record

contact = Contact(
    firstName='Tianhong', lastName='Chu', phone='+86.13818231324', email='cthesky@yeah.net',
    country='CN', city='Shanghai', state='Shanghai', zip='200090',
    address1='Room 501, Building 18, 3031 ChangYang Road, YangPu District, Shanghai City')

contacts = Contacts(admin=contact, tech=contact, registrant=contact, billing=contact)

domain = Domain(domainName='cthesky.band',
                nameservers=['ns2fln.name.com', 'ns3cna.name.com'],
                contacts=contacts)

domain2 = Domain(domainName='cthesky.irish',
                 nameservers=['ns2fln.name.com', 'ns3cna.name.com'],
                 contacts=contacts)

record = Record(id=357756, domainName=u'cthesky.band', host=u'test',
                fqdn=u'test.cthesky.band.', type=u'A',
                answer=u'10.0.0.1', ttl=300)
