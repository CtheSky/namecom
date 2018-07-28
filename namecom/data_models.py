"""
namecom: data_models.py

Defines data models for the api.

Tianhong Chu [https://github.com/CtheSky]
License: MIT
"""


class DataModel(object):
    """
    This is base class for data models.

    It provides following utilities:
      1. class method `from_dict` to construct model from a dict
      2. instance method `to_dict` to transfer model to a dict
      3. overrides equality test using __dict__
    """
    @classmethod
    def from_dict(cls, dct):
        """Create DataModel object from dict."""
        if not dct:
            return None
        return cls(**dct)

    def to_dict(self):
        """Returns a dict representation of DataModel object."""
        return {
            k: v.to_dict() if isinstance(v, DataModel) else v
            for k, v in self.__dict__.items()
        }

    def __repr__(self):
        cls_name = self.__class__.__name__
        params = ', '.join(['{}={!r}'.format(k, v) for k, v in self.__dict__.items()])
        return '{}({})'.format(cls_name, params)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self is other or self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))


class Record(DataModel):
    """
    This is a class for an individual DNS resource record.

    Attributes
    ----------
    id : int
        Unique record id. Value is ignored on Create, and must match the URI on Update.

    domainName : string
        DomainName is the zone that the record belongs to.

    host : string
        Host is the hostname relative to the zone: e.g. for a record for blog.example.org,
        domain would be "example.org" and host would be "blog".
        An apex record would be specified by either an empty host "" or "@".
        A SRV record would be specified by "_{service}._{protocal}.{host}":
        e.g. "_sip._tcp.phone" for _sip._tcp.phone.example.org.

    fqdn : string
        FQDN is the Fully Qualified Domain Name. It is the combination of the host and the domain name.
        It always ends in a ".". FQDN is ignored in CreateRecord, specify via the Host field instead.

    type : string
        Type is one of the following: A, AAAA, ANAME, CNAME, MX, NS, SRV, or TXT.

    answer : string
        Answer is either the IP address for A or AAAA records; the target for ANAME, CNAME, MX, or NS records;
        the text for TXT records. For SRV records, answer has the following format:
        "{weight} {port} {target}" e.g. "1 5061 sip.example.org".

    ttl : int
        TTL is the time this record can be cached for in seconds. Name.com allows a minimum TTL of 300,
        or 5 minutes.

    priority : int
        Priority is only required for MX and SRV records, it is ignored for all others.
    """

    def __init__(self, id, domainName, fqdn, type, answer, host=None, ttl=300, priority=None):
        self.id = id
        self.domainName = domainName
        self.host = host
        self.fqdn = fqdn
        self.type = type
        self.answer = answer
        self.ttl = ttl
        self.priority = priority

    def __str__(self):
        return 'Record: id[%s] host[%s] type[%s] answer[%s]' % (self.id, self.host, self.type, self.answer)


class DNSSEC(DataModel):
    """
    This is a class for Domain Name System Security Extensions (DNSSEC).
    It contains all the data required to create a DS record at the registry.

    Attributes
    ----------
    domainName : string
        DomainName is the domain name.

    keyTag : int
        KeyTag contains the key tag value of the DNSKEY RR that validates this signature.
        The algorithm to generate it is here: https://tools.ietf.org/html/rfc4034#appendix-B

    algorithm : int
        Algorithm is an integer identifying the algorithm used for signing. Valid values can be found here:
        https://www.iana.org/assignments/dns-sec-alg-numbers/dns-sec-alg-numbers.xhtml

    digestType : int
        DigestType is an integer identifying the algorithm used to create the digest. Valid values can be found
        here: https://www.iana.org/assignments/ds-rr-types/ds-rr-types.xhtml

    digest : string
        Digest is a digest of the DNSKEY RR that is registered with the registry.
    """

    def __init__(self, domainName, keyTag, algorithm, digestType, digest):
        self.domainName = domainName
        self.keyTag = keyTag
        self.algorithm = algorithm
        self.digestType = digestType
        self.digest = digest


class Domain(DataModel):
    """
    This class lists all the data for a domain.

    Attributes
    ----------
    domainName : string
        DomainName is the punycode encoded value of the domain name.

    nameservers : []string
        Nameservers is the list of nameservers for this domain. If unspecified it defaults to your account
        default nameservers.

    contacts : :class:`~namecom.Contacts`
        Contacts for the domain.

    privacyEnabled : bool
        PrivacyEnabled reflects if Whois Privacy is enabled for this domain.

    locked : bool
        Locked indicates that the domain cannot be transfered to another registrar.

    autorenewEnabled : bool
        AutorenewEnabled indicates if the domain will attempt to renew automatically before expiration.

    expireDate : string
        ExpireDate is the date the domain will expire.

    createDate : string
        CreateDate is the date the domain was created at the registry.

    renewalPrice : float
        RenewalPrice is the price to renew the domain. It may be required for the RenewDomain command.
    """

    def __init__(self, domainName, locked=None, expireDate=None, createDate=None, contacts=None,
                 nameservers=None, privacyEnabled=None, autorenewEnabled=None, renewalPrice=None):
        self.domainName = domainName
        self.nameservers = nameservers
        self.contacts = contacts
        self.privacyEnabled = privacyEnabled
        self.locked = locked
        self.autorenewEnabled = autorenewEnabled
        self.expireDate = expireDate
        self.createDate = createDate
        self.renewalPrice = renewalPrice

    def __str__(self):
        return 'Domain: domainName[%s]' % self.domainName

    @classmethod
    def from_dict(cls, dct):
        if not dct:
            return None

        domain = Domain(**dct)
        domain.contacts = Contacts.from_dict(dct.get('contacts'))

        return domain


class Contacts(DataModel):
    """
    This class stores the contact information for the roles related to domains.

    Attributes
    ----------
    registrant : :class:`~namecom.Contact`
        Registrant is the rightful owner of the account and has the right to use and/or sell the domain name.
        They are able to make changes to all account, domain, and product settings. This information should be
        reviewed and updated regularly to ensure accuracy.

    admin : :class:`~namecom.Contact`
        Registrants often designate an administrative contact to manage their domain name(s). They primarily deal
        with business information such as the name on record, postal address, and contact information for the
        official registrant.

    tech : :class:`~namecom.Contact`
        The technical contact manages and maintains a domain's nameservers. If you're working with a web designer
        or someone in a similar role, you many want to assign them as a technical contact.

    billing : :class:`~namecom.Contact`
        The billing contact is the party responsible for paying bills for the account and taking care of renewals.
    """

    def __init__(self, registrant, admin, tech, billing):
        self.registrant = registrant
        self.admin = admin
        self.tech = tech
        self.billing = billing

    @classmethod
    def from_dict(cls, dct):
        if not dct:
            return None

        kwargs = {
            field: Contact.from_dict(dct.get(field))
            for field in ['registrant', 'admin', 'tech', 'billing']
        }
        return Contacts(**kwargs)


class Contact(DataModel):
    """
    This class contains all the contact data.

    Attributes
    ----------
    firstName : string
        First name of the contact.

    lastName : string
        Last name of the contact.

    companyName : string
        Company name of the contact. Leave blank if the contact is an individual as some registries will assume
        it is a corporate entity otherwise.

    address1 : string
        Address1 is the first line of the contact's address.

    address2 : string
        Address2 is the second line of the contact's address.

    city : string
        City of the contact's address.

    state : string
        State or Province for the contact's address.

    zip : string
        Zip or Postal Code for the contact's address.

    country : string
        Country code for the contact's address. Required to be a ISO 3166-1 alpha-2 code.

    phone : string
        Phone number of the contact. Should be specified in the following format: "+cc.llllllll" where cc
        is the country code and llllllll is the local number.

    fax : string
        Fax number of the contact. Should be specified in the following format: "+cc.llllllll" where cc
        is the country code and llllllll is the local number.

    email : string
        Email of the contact. Should be a complete and valid email address.
    """

    def __init__(self, firstName, lastName, companyName=None, address1=None, address2=None, city=None,
                 state=None, zip=None, country=None, phone=None, fax=None, email=None):
        self.firstName = firstName
        self.lastName = lastName
        self.companyName = companyName
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
    """
    SearchResult is returned by the CheckAvailability, Search, and SearchStream functions.

    Attributes
    ----------
    domainName : string
        DomainName is the punycode encoded value of the domain name.

    sld : string
        SLD is first portion of the domain_name.

    tld : string
        TLD is the rest of the domain_name after the SLD.

    purchasable : bool
        Purchaseable indicates whether the search result is available for purchase.

    premium : bool
        Premium indicates that this search result is a premium result and the purchase_price needs to be passed to
        the DomainCreate command.

    purchasePrice : float
        PurchasePrice is the price for purchasing this domain for 1 year. Purchase_price is always in USD.

    purchaseType : string
        PurchaseType indicates what kind of purchase this result is for. It should be passed to the DomainCreate
        command.

    renewalPrice : float
        RenewalPrice is the annual renewal price for this domain as it may be different then the purchase_price.
    """

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


class EmailForwarding(DataModel):
    """
    EmailForwarding contains all the information for an email forwarding entry.

    Attributes
    ----------
    domainName : string
        DomainName is the domain part of the email address to forward

    emailBox : string
        DomainName is the domain part of the email address to forward

    emailTo : string
        EmailTo is the entire email address to forward email to
    """
    def __init__(self, domainName, emailBox, emailTo):
        self.domainName = domainName
        self.emailBox = emailBox
        self.emailTo = emailTo


class Transfer(DataModel):
    """
    Transfer contains the information related to a transfer of a domain name to Name.com.

    Attributes
    ----------
    domainName : string
        DomainName is the domain to be transfered to Name.com.

    email : string
        Email is the email address that the approval email was sent to. Not every TLD requries an approval email.
        This is usaully pulled from Whois.

    status : string
        Status is the current status of the transfer. Details about statuses can be found in the following
        Knowledge Base article: https://www.name.com/support/articles/115012519688-Transfer-status-FAQ.
    """
    def __init__(self, domainName, email, status):
        self.domainName = domainName
        self.email = email
        self.status = status


class URLForwarding(DataModel):
    """
    URLForwarding is the model for URL forwarding entries.

    Attributes
    ----------
    domainName : string
        DomainName is the domain part of the hostname to forward.

    host : string
        Host is the entirety of the hostname. i.e. www.example.org

    forwardsTo : string
        ForwardsTo is the URL this host will be forwarded to.

    type : string
        Type is the type of forwarding. Valid types are:
        Masked - This retains the original domain in the address bar and will not reveal or display the actual
        destination URL. If you are forwarding knowledgebase.ninja to Name.com, the address bar will say
        knowledgebase.ninja. This is sometimes called iframe forwarding. And: Redirect - This does not retain
        the original domain in the address bar, so the user will see it change and realize they were forwarded
        from the URL they originally entered. If you are forwarding knowledgebase.ninja to Name.com, the address
        bar will say Name.com. This is also called 301 forwarding.

    title : string
        Title is the title for the html page to use if the type is masked. Values are ignored for types other
        then "masked".

    meta : string
        Meta is the meta tags to add to the html page if the type is masked.
        ex: "meta name='keywords' content='fish, denver, platte'". Values are ignored for types other then "masked".
    """
    def __init__(self, domainName, host, forwardsTo, type, title=None, meta=None):
        self.domainName = domainName
        self.host = host
        self.forwardsTo = forwardsTo
        self.type = type
        self.title = title
        self.meta = meta


class VanityNameserver(DataModel):
    """
    VanityNameserver contains the hostname as well as the list of IP addresses for nameservers.

    Attributes
    ----------
    domainName : string
        DomainName is the domain the nameserver is a subdomain of.

    hostname : string
        Hostname is the hostname of the nameserver.

    ips : []string
        IPs is a list of IP addresses that are used for glue records for this nameserver.
    """
    def __init__(self, domainName, hostname, ips=None):
        self.domainName = domainName
        self.hostname = hostname
        self.ips = ips
