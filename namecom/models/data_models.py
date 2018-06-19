# encoding=utf-8

__all__ = ['Domain', 'Contacts', 'Contact', 'DomainSearchResult']


class DataModel(object):

    @classmethod
    def from_dict(cls, data):
        raise NotImplemented

    def to_dict(self):
        return {
            k: v.to_dict() if isinstance(v, DataModel) else v
            for k, v in self.__dict__.items()
        }


class Domain(DataModel):

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
    def from_dict(cls, data):
        if not data:
            return None

        domain = Domain(**data)
        domain.contacts = Contacts.from_dict(data.get('contacts'))

        return domain


class Contacts(DataModel):

    def __init__(self, registrant, admin, tech, billing):
        self.registrant = registrant
        self.admin = admin
        self.tech = tech
        self.billing = billing

    @classmethod
    def from_dict(cls, data):
        if not data:
            return None

        kwargs = {
            field: Contact(**data.get(field))
            for field in ['registrant', 'admin', 'tech', 'billing']
        }
        return Contacts(**kwargs)


class Contact(DataModel):

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


class DomainSearchResult(DataModel):

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

    @classmethod
    def from_dict(cls, data):
        if not data:
            return None

        return DomainSearchResult(**data)
