# encoding=utf-8


class Domain:

    def __init__(self, domainName, locked=None, expireDate=None, createDate=None, contacts=None,
                 nameservers=None, privacyEnabled=None, autorenewEnabled=None, renewalPrice=None):
        self.domainName = domainName
        self.nameservers = nameservers
        self.privacyEnabled = privacyEnabled
        self.locked = locked
        self.autorenewEnabled = autorenewEnabled
        self.expireDate = expireDate
        self.createDate = createDate
        self.renewalPrice = renewalPrice
        self.contacts = contacts

    def __str__(self):
        return 'Domain: domainName[%s]' % self.domainName

    @classmethod
    def from_json(cls, data):
        if not data:
            return None

        domain = Domain(**data)
        domain.contacts = Contacts.from_json(data.get('contacts'))

        return domain


class Contacts:

    def __init__(self, registrant, admin, tech, billing):
        self.registrant = registrant
        self.admin = admin
        self.tech = tech
        self.billing = billing

    @classmethod
    def from_json(cls, data):
        if not data:
            return None

        kwargs = {
            field: Contact(**data.get(field))
            for field in ['registrant', 'admin', 'tech', 'billing']
        }
        return Contacts(**kwargs)


class Contact:

    def __init__(self, firstName, lastName, companyName=None, address1=None, address2=None, city=None,
                 state=None, zip=None, country=None, phone=None, fax=None, email=None):
        self.firstName = firstName
        self.lastName = lastName
        self.compayName = companyName
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.zip = zip
        self.country = country
        self.phone = phone
        self.fax = fax
        self.email = email


class DomainSearchResult:

    def __init__(self, domainName, sld, tld, purchasable=None,
                 premium=None, purchasePrice=None, purchaseType=None, renewalPrice=None):
        self.domainName = domainName
        self.sld = sld
        self.tld = tld
        self.purchasable = purchasable
        self.premium = premium
        self.purchasePrice = purchasePrice
        self.purchaseType = purchaseType
        self.renewalPrice = renewalPrice


class RequestResult(object):
    def __init__(self, resp):
        self.resp = resp
        self.status_code = resp.status_code
        self.headers = resp.headers


class ListDomainsResult(RequestResult):

    def __init__(self, resp):
        super(ListDomainsResult, self).__init__(resp)

        self.domains = []
        self.nextPage = 0
        self.lastPage = 0


class GetDomainResult(RequestResult):

    def __init__(self, resp):
        super(GetDomainResult, self).__init__(resp)

        self.domain = None
        self.contacts = None


class SearchResult(RequestResult):

    def __init__(self, resp):
        super(SearchResult, self).__init__(resp)

        self.results = []


class CreateDomainResult(RequestResult):

    def __init__(self, resp):
        super(CreateDomainResult, self).__init__(resp)

        self.domain = None
        self.order = 0
        self.totalPaid = 0


__all__ = ['Domain', 'DomainSearchResult', 'Contacts', 'Contact', 'DomainSearchResult',
           'ListDomainsResult', 'GetDomainResult', 'SearchResult', 'CreateDomainResult']
