# -*- coding: utf-8 -*-

from namecom import Domain, Contact, Contacts, Record, DNSSEC

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

record = Record(id=357756, domainName='cthesky.band', host='test',
                fqdn='test.cthesky.band.', type='A',
                answer='10.0.0.1', ttl=300)

dnssec = DNSSEC(domainName='cthesky.band', keyTag=30909, algorithm=8, digestType=2,
                digest='E2D3C916F6DEEAC73294E8268FB5885044A833FC5459588F4A9184CFC41A5766')
