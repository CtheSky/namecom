class DataModel(object):

    @classmethod
    def from_dict(cls, data):
        raise NotImplemented

    def to_dict(self):
        return {
            k: v.to_dict() if isinstance(v, DataModel) else v
            for k, v in self.__dict__.items()
        }

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self is other or self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))


class Record(DataModel):

    def __init__(self, id, domainName, host, fqdn, type, answer, ttl=300, priority=None):
        self.id = int(id)
        self.domainName = domainName
        self.host = host
        self.fqdn = fqdn
        self.type = type
        self.answer = answer
        self.ttl = ttl
        self.priority = int(priority) if priority else None

    def __str__(self):
        return 'Record: id[%s] host[%s] type[%s] answer[%s]' % (self.id, self.host, self.type, self.answer)

    @classmethod
    def from_dict(cls, data):
        if not data:
            return None
        return Record(**data)


class DNSSEC(DataModel):

    def __init__(self, domainName, keyTag, algorithm, digestType, digest):

        self.domainName = domainName

        # KeyTag contains the key tag value of the DNSKEY RR that validates this signature.
        # The algorithm to generate it is here: https://tools.ietf.org/html/rfc4034#appendix-B
        self.keyTag = keyTag

        # Algorithm is an integer identifying the algorithm used for signing.
        # Valid values can be found here: https://www.iana.org/assignments/dns-sec-alg-numbers/dns-sec-alg-numbers.xhtml
        self.algorithm = algorithm

        # DigestType is an integer identifying the algorithm used to create the digest.
        # Valid values can be found here: https://www.iana.org/assignments/ds-rr-types/ds-rr-types.xhtml
        self.digestType = digestType

        # Digest is a digest of the DNSKEY RR that is registered with the registry.
        self.digest = digest

    @classmethod
    def from_dict(cls, data):
        if not data:
            return None
        return DNSSEC(**data)


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
