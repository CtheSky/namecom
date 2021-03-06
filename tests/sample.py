from namecom import Domain, Contact, Contacts, Record, DNSSEC, EmailForwarding, URLForwarding, VanityNameserver, Auth

correct_auth = Auth('cthesky-test', '96414285232f77557662ba9be585ba926f04dc9b')
wrong_auth = Auth('cthesky-test', 'wrong token')

contact_sample1 = Contact(
    firstName='Tianhong', lastName='Chu', phone='+86.13818231324', email='cthesky@yeah.net',
    country='CN', city='Shanghai', state='Shanghai', zip='200090',
    address1='Room 501, Building 18, 3031 ChangYang Road, YangPu District, Shanghai City')

contacts_sample1 = Contacts(admin=contact_sample1, tech=contact_sample1, registrant=contact_sample1, billing=contact_sample1)

domain_sample1 = Domain(domainName='cthesky.band',
                        nameservers=['ns2fln.name.com', 'ns3cna.name.com'],
                        contacts=contacts_sample1)

domain_sample2 = Domain(domainName='cthesky.irish',
                        nameservers=['ns2fln.name.com', 'ns3cna.name.com'],
                        contacts=contacts_sample1)

record_sample1 = Record(id=357756, domainName='cthesky.band', host='test',
                        fqdn='test.cthesky.band.', type='A',
                        answer='10.0.0.1', ttl=300)

dnssec_sample1 = DNSSEC(domainName='cthesky.band', keyTag=30909, algorithm=8, digestType=2, digest='E2D3C916F6DEEAC73294E8268FB5885044A833FC5459588F4A9184CFC41A5766')
dnssec_sample2 = DNSSEC(domainName='cthesky.band', keyTag=33630, algorithm=5, digestType=2, digest='4177EAEC09A37178357871EBE3FB361CABB2861F12A1D51DDE18CBA2439BB5C1')

email_forwarding_sample1 = EmailForwarding(domainName='cthesky.band', emailBox='test1', emailTo='cthesky@yeah.net')
email_forwarding_sample2 = EmailForwarding(domainName='cthesky.band', emailBox='test2', emailTo='cthesky@yeah.net')
email_forwarding_sample3 = EmailForwarding(domainName='cthesky.band', emailBox='test2', emailTo='cthesky@gmail.com')

url_forwarding_sample1 = URLForwarding(domainName='cthesky.band', host='testurl.cthesky.band', forwardsTo='https://www.example.net', type='redirect')
url_forwarding_sample2 = URLForwarding(domainName='cthesky.band', host='testurl.cthesky.band', forwardsTo='https://www.example.com', type='redirect')

vanity_nameserver_sample1 = VanityNameserver(domainName='cthesky.band', hostname='ns1.cthesky.band',
                                             ips=["192.168.1.1", "fd01:4860:4860::8888"])
vanity_nameserver_sample2 = VanityNameserver(domainName='cthesky.band', hostname='ns1.cthesky.band',
                                             ips=["192.168.0.1", "fd01:4860:4860::8888"])
