from namecom import Domain, Contact, Contacts

contact = Contact(
    firstName='Tianhong', lastName='Chu', phone='+86.13818231324', email='cthesky@yeah.net',
    country='CN', city='Shanghai', state='Shanghai', zip='200090',
    address1='Room 501, Building 18, 3031 ChangYang Road, YangPu District, Shanghai City')

contacts = Contacts(admin=contact, tech=contact, registrant=contact, billing=contact)

domain = Domain(domainName='cthesky.band',
                nameservers=['ns2fln.name.com', 'ns3cna.name.com'],
                contacts=contacts)
