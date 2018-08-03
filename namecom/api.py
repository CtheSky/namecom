"""
namecom: api.py

Implements several api classes for the name.com v4 api.

Tianhong Chu [https://github.com/CtheSky]
License: MIT
"""

__all__ = ['DnsApi', 'DnssecApi', 'DomainApi', 'EmailForwardingApi', 'TransferApi', 'URLForwardingApi',
           'VanityNameserverApi']

import requests

from . import exceptions
from .utils import *
from .result_models import *

PRODUCT_API_HOST = 'https://api.name.com'
TEST_API_HOST = 'https://api.dev.name.com'


class _ApiBase(object):
    """
    This is the base class for api.

    It provides common utilities for each api:
      1. http authentication
      2. send request
      3. parse result
      4. error handling
    """

    def __init__(self, auth, use_test_env):
        self.auth = auth
        self.api_host = PRODUCT_API_HOST if not use_test_env else TEST_API_HOST
        self.endpoint = ''

    def _do(self, method, relative_path=None, **kwargs):
        """
        Used to send the request.

        :param method: http method to use
        :param relative_path: additional url path after endpoint
        :param kwargs: keyword arguments that will be passed to request method from requests module
        :return: response from requests module
        """
        resp = requests.request(method,
                                self.api_host + self.endpoint + (relative_path if relative_path else ''),
                                auth=(self.auth.username, self.auth.token),
                                **kwargs)

        if resp.status_code // 100 != 2:
            raise exceptions.make_exception(resp)

        return resp

    def _parse_result(self, resp, parse_func, klass):
        """
        Used to parse response result.

        :param resp: http response from requests module
        :param parse_func: helper function from utils.parse_utils module, it parses response and fill the result fields
        :param klass: the class of parsed response result this method returns
        :return: an instance of klass with parsed response information
        """
        result = klass(resp)
        parse_func(result, resp.json())
        return result


class DnsApi(_ApiBase):
    """
    The api class for DNS. More details about each parameter :class:`here <namecom.Record>`.
    Official namecom documentation : https://www.name.com/api-docs/DNS
    """

    def __init__(self, domainName, auth, use_test_env=False):
        """
        Parameters
        ----------
        domainName : string
            domain that dns records belongs to

        auth : :class:`~namecom.Auth`
            http authentication to use

        use_test_env : bool
            whether runs in test environment
        """
        super(DnsApi, self).__init__(auth, use_test_env)
        self.endpoint = '/v4/domains/{domain_name}/records'.format(domain_name=domainName)

    def list_records(self, page=1, perPage=1000):
        """Returns all records for a zone.

        Parameters
        ----------
        page: int
            which page to return

        perPage : int
            the number of records to return per request

        Returns
        -------
        :class:`~namecom.result_models.ListRecordsResult`
            a response result instance with parsed response info
        """
        params = {
            'page': page,
            'perPage': perPage
        }

        resp = self._do('GET', params=params)
        return self._parse_result(resp, parse_list_records, ListRecordsResult)

    def get_record(self, id):
        """Returns details about an individual record.

        Parameters
        ----------
        id : int
            the server-assigned unique identifier for this record

        Returns
        -------
        :class:`~namecom.result_models.GetRecordResult`
            a response result instance with parsed response info
        """
        resp = self._do('GET', relative_path='/{id}'.format(id=id))
        return self._parse_result(resp, parse_get_record, GetRecordResult)

    def create_record(self, host, type, answer, ttl=300, priority=None):
        """Creates a new record in the zone.

        Parameters
        ----------
        host : string
            hostname relative to the zone
        type : string
            dns record type
        answer : string
            dns record answer
        ttl : int
            dns record ttl
        priority : int
            dns record priority

        Returns
        -------
        :class:`~namecom.result_models.CreateRecordResult`
            a response result instance with parsed response info
        """
        data = json_dumps({
            'host': host,
            'type': type,
            'answer': answer,
            'ttl': ttl,
            'priority': priority
        })

        resp = self._do('POST', data=data)
        return self._parse_result(resp, parse_create_record, CreateRecordResult)

    def update_record(self, id, host=None, type=None, answer=None, ttl=300, priority=None):
        """Replaces the record with the new record that is passed.

        Parameters
        ----------
        id : int
            the server-assigned unique identifier for this record
        host : string
            hostname relative to the zone
        type : string
            dns record type
        answer : string
            dns record answer
        ttl : int
            dns record ttl
        priority : int
            dns record priority

        Returns
        -------
        :class:`~namecom.result_models.UpdateRecordResult`
            a response result instance with parsed response info
        """
        data = json.dumps({
            'host': host,
            'type': type,
            'answer': answer,
            'ttl': ttl,
            'priority': priority
        })

        resp = self._do('PUT', relative_path='/{id}'.format(id=id), data=data)
        return self._parse_result(resp, parse_update_record, UpdateRecordResult)

    def delete_record(self, id):
        """Deletes a record from the zone.

        Parameters
        ----------
        id : int
            the server-assigned unique identifier for this record

        Returns
        -------
        :class:`~namecom.result_models.DeleteRecordResult`
            a response result instance with parsed response info
        """
        resp = self._do('DELETE', relative_path='/{id}'.format(id=id))
        return self._parse_result(resp, parse_delete_record, DeleteRecordResult)


class DnssecApi(_ApiBase):
    """
    The api class for Domain Name System Security Extensions (DNSSEC).
    More details about each parameter :class:`here <namecom.DNSSEC>`.
    Official namecom documentation : https://www.name.com/api-docs/DNSSECs
    """

    def __init__(self, domainName, auth, use_test_env=False):
        """
        Parameters
        ----------
        domainName : string
            domain to manipulate dnssec on

        auth : :class:`~namecom.Auth`
            http authentication to use

        use_test_env : bool
            whether runs in test environment
        """
        super(DnssecApi, self).__init__(auth, use_test_env)
        self.endpoint = '/v4/domains/{domainName}/dnssec'.format(domainName=domainName)

    def list_dnssecs(self, page=1, perPage=1000):
        """Lists all of the DNSSEC keys registered with the registry.

        Parameters
        ----------
        page: int
            which page to return

        perPage : int
            the number of records to return per request

        Returns
        -------
        :class:`~namecom.result_models.ListDnssecsResult`
            a response result instance with parsed response info
        """
        params = {
            'page': page,
            'perPage': perPage
        }

        resp = self._do('GET', params=params)
        return self._parse_result(resp, parse_list_dnssecs, ListDnssecsResult)

    def get_dnssec(self, digest):
        """Retrieves the details for a key registered with the registry.

        Parameters
        ----------
        digest : string
            Digest is the digest for the DNSKEY RR to retrieve.

        Returns
        -------
        :class:`~namecom.result_models.GetDnssecResult`
            a response result instance with parsed response info
        """
        resp = self._do('GET', relative_path='/{digest}'.format(digest=digest))
        return self._parse_result(resp, parse_get_dnssec, GetDnssecResult)

    def create_dnssec(self, keyTag, algorithm, digestType, digest):
        """Registers a DNSSEC key with the registry.

        Parameters
        ----------
        keyTag : int
             key tag value of the DNSKEY RR

        algorithm : int
            an integer identifying the algorithm used for signing

        digestType : int
            an integer identifying the algorithm used to create the digest

        digest : string
            a digest of the DNSKEY RR that is registered with the registry

        Returns
        -------
        :class:`~namecom.result_models.CreateDnssecResult`
            a response result instance with parsed response info
        """
        data = json_dumps({
            'keyTag': keyTag,
            'algorithm': algorithm,
            'digestType': digestType,
            'digest': digest
        })

        resp = self._do('POST', data=data)
        return self._parse_result(resp, parse_create_dnssec, CreateDnssecResult)

    def delete_dnssec(self, digest):
        """Removes a DNSSEC key from the registry.

        Parameters
        ----------
        digest : string
            a digest of the DNSKEY RR that is registered with the registry

        Returns
        -------
        :class:`~namecom.result_models.DeleteDnssecResult`
            a response result instance with parsed response info
        """
        resp = self._do('DELETE', relative_path='/{digest}'.format(digest=digest))
        return self._parse_result(resp, parse_delete_dnssec, DeleteDnssecResult)


class DomainApi(_ApiBase):
    """
    The api class for Domain.
    More details about each parameter :class:`here <namecom.Domain>`.
    Official namecom documentation : https://www.name.com/api-docs/domain
    """

    def __init__(self, auth, use_test_env=False):
        """
        Parameters
        ----------
        auth : :class:`~namecom.Auth`
            http authentication to use

        use_test_env : bool
            whether runs in test environment
       """
        super(DomainApi, self).__init__(auth, use_test_env)
        self.endpoint = '/v4/domains'

    def list_domains(self, page=1, perPage=1000):
        """Returns all domains in the account. It omits some information that can be retrieved from GetDomain.

        Parameters
        ----------
        page: int
            which page to return

        perPage : int
            the number of records to return per request

        Returns
        -------
        :class:`~namecom.result_models.ListDomainsResult`
            a response result instance with parsed response info
        """
        params = {
            'page': page,
            'perPage': perPage
        }

        resp = self._do('GET', params=params)
        return self._parse_result(resp, parse_list_domains, ListDomainsResult)

    def get_domain(self, domainName):
        """Returns details about a specific domain

        Parameters
        ----------
        domainName : string
            name of the domain to retrieve
        Returns
        -------
        :class:`~namecom.result_models.GetDomainResult`
            a response result instance with parsed response info
        """
        resp = self._do('GET', relative_path='/{domainName}'.format(domainName=domainName))
        return self._parse_result(resp, parse_get_domain, GetDomainResult)

    def create_domain(self, domain, purchasePrice, purchaseType='registration',
                      years=1, tldRequirements=None, promoCode=None):
        """

        Parameters
        ----------
        domain : :class:`~namecom.Domain`
            the domain object to create

        purchasePrice : float
            the amount to pay for the domain

        purchaseType : string
            PurchaseType defaults to "registration" but should be copied from the result of a search command otherwise

        years : int
            how many years to register the domain for.

        tldRequirements : dict[string -> string]
           TLDRequirements is a way to pass additional data that is required by some registries

        promoCode : string
            PromoCode is not yet implemented

        Returns
        -------
        :class:`~namecom.result_models.CreateDomainResult`
            a response result instance with parsed response info
        """
        data = json_dumps({
            'domain': domain,
            'purchasePrice': purchasePrice,
            'purchaseType': purchaseType,
            'years': years,
            'tldRequirements': tldRequirements if tldRequirements else [],
            'promoCode': promoCode
        })

        resp = self._do('POST', data=data)
        return self._parse_result(resp, parse_create_domain, CreateDomainResult)

    def enable_autorenew(self, domainName):
        """Enables the domain to be automatically renewed when it gets close to expiring.

        Parameters
        ----------
        domainName : string
            name of the domain to retrieve

        Returns
        -------
        :class:`~namecom.result_models.EnableAutorenewResult`
            a response result instance with parsed response info
        """
        resp = self._do('POST', relative_path='/{domainName}:enableAutorenew'.format(domainName=domainName))
        return self._parse_result(resp, parse_enable_autorenew, EnableAutorenewResult)

    def disable_autorenew(self, domainName):
        """Disables automatic renewals, thus requiring the domain to be renewed manually.

        Parameters
        ----------
        domainName : string
            name of the domain to retrieve

        Returns
        -------
        :class:`~namecom.result_models.DisableAutorenewResult`
            a response result instance with parsed response info
        """
        resp = self._do('POST', relative_path='/{domainName}:disableAutorenew'.format(domainName=domainName))
        return self._parse_result(resp, parse_disable_autorenew, DisableAutorenewResult)

    def renew_domain(self, domainName, purchasePrice, years=1, promoCode=None):
        """Renew a domain. Purchase_price is required if the renewal is not regularly priced.

        Parameters
        ----------
        domainName : string
            name of the domain to renew

        purchasePrice : float
            the amount to pay for the domain renewal

        years : int
            how many years to renew the domain for

        promoCode : string
            PromoCode is not yet implemented

        Returns
        -------
        :class:`~namecom.result_models.RenewDomainResult`
            a response result instance with parsed response info
        """
        data = json_dumps({
            'purchasePrice': purchasePrice,
            'years': years,
            'promoCode': promoCode
        })

        resp = self._do('POST', relative_path='/{domainName}:renew'.format(domainName=domainName), data=data)
        return self._parse_result(resp, parse_renew_domain, RenewDomainResult)

    def get_auth_code_for_domain(self, domainName):
        """Returns the Transfer Authorization Code for the domain.

        Parameters
        ----------
        domainName : string
            name of the domain to renew

        Returns
        -------
        :class:`~namecom.result_models.GetAuthCodeForDomainResult`
            a response result instance with parsed response info
        """
        resp = self._do('GET', relative_path='/{domainName}:getAuthCode'.format(domainName=domainName))
        return self._parse_result(resp, parse_get_authcode, GetAuthCodeForDomainResult)

    def purchase_privacy(self, domainName, purchasePrice, years=1, promoCode=None):
        """Add Whois Privacy protection to a domain or will an renew existing subscription.

        Parameters
        ----------
        domainName : string
            name of the domain to renew

        purchasePrice : float
            the amount to pay for the domain renewal

        years : int
            how many years to renew the domain for

        promoCode : string
            PromoCode is not yet implemented

        Returns
        -------
        :class:`~namecom.result_models.PurchasePrivacyResult`
            a response result instance with parsed response info
        """
        data = json_dumps({
            'purchasePrice': purchasePrice,
            'years': years,
            'promoCode': promoCode
        })

        resp = self._do('POST', relative_path='/{domainName}:purchasePrivacy'.format(domainName=domainName), data=data)
        return self._parse_result(resp, parse_purchase_privacy, PurchasePrivacyResult)

    def set_nameservers(self, domainName, nameservers):
        """Set the nameservers for the Domain.

        Parameters
        ----------
        domainName : string
            name of the domain to set the nameservers for

        nameservers : []string
            a list of the nameservers to set

        Returns
        -------
        :class:`~namecom.result_models.SetNameserversResult`
            a response result instance with parsed response info
        """
        data = json_dumps({
            'nameservers': nameservers
        })

        resp = self._do('POST', relative_path='/{domainName}:setNameservers'.format(domainName=domainName), data=data)
        return self._parse_result(resp, parse_set_nameservers, SetNameserversResult)

    def set_contacts(self, domainName, contacts):
        """"Set the contacts for the Domain.

        Parameters
        ----------
        domainName : string
            name of the domain to set the contacts for

        contacts : Contacts
            contacts to set

        Returns
        -------
        :class:`~namecom.result_models.SetContactsResult`
            a response result instance with parsed response info
        """
        data = json_dumps({
            'contacts': contacts
        })

        resp = self._do('POST', relative_path='/{domainName}:setContacts'.format(domainName=domainName), data=data)
        return self._parse_result(resp, parse_set_contacts, SetContactsResult)

    def lock_domain(self, domainName):
        """Lock a domain so that it cannot be transfered to another registrar.

        Parameters
        ----------
        domainName : string
            name of the domain to lock

        Returns
        -------
        :class:`~namecom.result_models.LockDomainResult`
            a response result instance with parsed response info
        """
        resp = self._do('POST', relative_path='/{domainName}:lock'.format(domainName=domainName))
        return self._parse_result(resp, parse_lock_domain, LockDomainResult)

    def unlock_domain(self, domainName):
        """Unlock a domain so that it can be transfered to another registrar.

        Parameters
        ----------
        domainName : string
            name of the domain to unlock

        Returns
        -------
        :class:`~namecom.result_models.UnlockDomainResult`
            a response result instance with parsed response info
        """
        resp = self._do('POST', relative_path='/{domainName}:unlock'.format(domainName=domainName))
        return self._parse_result(resp, parse_unlock_domain, UnlockDomainResult)

    def check_availability(self, domainNames, promoCode=None):
        """Check a list of domains to see if they are purchaseable. A Maximum of 50 domains can be specified.

        Parameters
        ----------
        domainNames : []string
            the list of domains to check if they are available

        promoCode : string
            PromoCode is not yet implemented

        Returns
        -------
        :class:`~namecom.result_models.CheckAvailabilityResult`
            a response result instance with parsed response info
        """
        data = json_dumps({
            'domainNames': domainNames,
            'promoCode': promoCode
        })

        resp = self._do('POST', relative_path=':checkAvailability', data=data)
        return self._parse_result(resp, parse_check_availability, CheckAvailabilityResult)

    def search(self, keyword, tldFilter=None, timeout=1000, promoCode=None):
        """Perform a search for specified keywords.

        Parameters
        ----------
        keyword : string
            the search term to search for

        tldFilter : []string
            TLDFilter will limit results to only contain the specified TLDs

        timeout : int
            Timeout is a value in milliseconds on how long to perform the search for

        promoCode : string
            PromoCode is not yet implemented

        Returns
        -------
        :class:`~namecom.result_models.SearchResult`
            a response result instance with parsed response info
        """
        data = json_dumps({
            'keyword': keyword,
            'tldFilter': tldFilter if tldFilter else [],
            'timeout': timeout,
            'promoCode': promoCode
        })

        resp = self._do('POST', relative_path=':search', data=data)
        return self._parse_result(resp, parse_search, SearchResult)

    def search_stream(self, keyword, tldFilter=None, timeout=1000, promoCode=None):
        """Return JSON encoded SearchResults as they are recieved from the registry

        Parameters
        ----------
        keyword : string
            the search term to search for

        tldFilter : []string
            TLDFilter will limit results to only contain the specified TLDs

        timeout : int
            Timeout is a value in milliseconds on how long to perform the search for

        promoCode : string
            PromoCode is not yet implemented

        Returns
        -------
        :class:`~namecom.result_models.SearchStreamResult`
            a response result instance with parsed response info
        """
        data = json_dumps({
            'keyword': keyword,
            'tldFilter': tldFilter if tldFilter else [],
            'timeout': timeout,
            'promoCode': promoCode
        })

        resp = self._do('POST', relative_path=':searchStream', data=data, stream=True)
        result = SearchStreamResult(resp)
        parse_search_stream(result, resp)

        return result


class EmailForwardingApi(_ApiBase):
    """
    The api class for name.com EmailForwarding.
    More details about each parameter :class:`here <namecom.EmailForwarding>`.
    Official namecom documentation : https://www.name.com/api-docs/EmailForwardings
    """

    def __init__(self, domainName, auth, use_test_env=False):
        """
        Parameters
        ----------
        domainName : string
            domain that dns records belongs to

        auth : :class:`~namecom.Auth`
            http authentication to use

        use_test_env : bool
            whether runs in test environment
        """
        super(EmailForwardingApi, self).__init__(auth, use_test_env)
        self.endpoint = '/v4/domains/{domain_name}/email/forwarding'.format(domain_name=domainName)

    def list_email_forwardings(self, perPage=1000, page=1):
        """Returns a pagenated list of email forwarding entries for a domain.

        Parameters
        ----------
        perPage : int
            the number of records to return per request

        page : int
            which page to return

        Returns
        -------
        :class:`~namecom.result_models.ListEmailForwardingsResult`
            a response result instance with parsed response info
        """
        params = {
            'page': page,
            'perPage': perPage
        }

        resp = self._do('GET', params=params)
        return self._parse_result(resp, parse_list_email_forwardings, ListEmailForwardingsResult)

    def get_mail_forwarding(self, emailBox):
        """Returns an email forwarding entry

        Parameters
        ----------
        emailBox : string
            which email box to retrieve

        Returns
        -------
        :class:`~namecom.result_models.GetEmailForwardingResult`
            a response result instance with parsed response info
        """
        resp = self._do('GET', relative_path='/{emailBox}'.format(emailBox=emailBox))
        return self._parse_result(resp, parse_get_email_forwarding, GetEmailForwardingResult)

    def create_email_forwarding(self, emailBox, emailTo):
        """Creates an email forwarding entry.

        If this is the first email forwarding entry, it may modify the MX records for the domain accordingly.

        Parameters
        ----------
        emailBox : string
            the user portion of the email address to forward

        emailTo : string
            the entire email address to forward email to

        Returns
        -------
        :class:`~namecom.result_models.GetEmailForwardingResult`
            a response result instance with parsed response info
        """
        data = json_dumps({
            'emailBox': emailBox,
            'emailTo': emailTo
        })

        resp = self._do('POST', data=data)
        return self._parse_result(resp, parse_create_email_forwarding, CreateEmailForwardingResult)

    def update_email_forwarding(self, emailBox, emailTo):
        """Updates which email address the email is being forwarded to.

        Parameters
        ----------
        emailBox : string
            the user portion of the email address to forward

        emailTo : string
            the entire email address to forward email to

        Returns
        -------
        :class:`~namecom.result_models.GetEmailForwardingResult`
            a response result instance with parsed response info
        """
        data = json_dumps({
            'emailTo': emailTo
        })

        resp = self._do('PUT', relative_path='/{emailBox}'.format(emailBox=emailBox), data=data)
        return self._parse_result(resp, parse_update_email_forwarding, UpdateEmailForwardingResult)

    def delete_email_forwarding(self, emailBox):
        """Deletes the email forwarding entry.

        Parameters
        ----------
        emailBox : string
            the user portion of the email address to forward

        Returns
        -------
        :class:`~namecom.result_models.DeleteEmailForwardingResult`
            a response result instance with parsed response info
        """
        resp = self._do('DELETE', relative_path='/{emailBox}'.format(emailBox=emailBox))
        return self._parse_result(resp, parse_delete_email_forwarding, DeleteEmailForwardingResult)


class TransferApi(_ApiBase):
    """
    The api class for Domain Transfer.
    More details about each parameter :class:`here <namecom.Transfer>`.
    Official namecom documentation : https://www.name.com/api-docs/Transfers
    """

    def __init__(self, auth, use_test_env=False):
        """
        Parameters
        ----------
        auth : :class:`~namecom.Auth`
            http authentication to use

        use_test_env : bool
            whether runs in test environment
        """
        super(TransferApi, self).__init__(auth, use_test_env)
        self.endpoint = '/v4/transfers'

    def list_transfers(self, page=1, perPage=1000):
        """Lists all pending transfer in requests.

        To get the information related to a non-pending transfer, you can use the GetTransfer function for that.

        Returns
        -------
        :class:`~namecom.result_models.ListTransferResult`
            a response result instance with parsed response info
        """
        params = {
            'page': page,
            'perPage': perPage
        }

        resp = self._do('GET', params=params)
        return self._parse_result(resp, parse_list_transfers, ListTransfersResult)

    def get_transfer(self, domainName):
        """Gets details for a transfer request.

        Parameters
        ----------
        domainName : str
            DomainName is the domain you want to get the transfer information for

        Returns
        -------
        :class:`~namecom.result_models.GetTransferResult`
            a response result instance with parsed response info
        """
        resp = self._do('GET', relative_path='/{domainName}'.format(domainName=domainName))
        return self._parse_result(resp, parse_get_transfer, GetTransferResult)

    def create_transfer(self, domainName, authCode, purchasePrice, privacyEnabled=False, promoCode=None):
        """Purchases a new domain transfer request.

        Parameters
        ----------
        domainName : str
            DomainName is the domain you want to transfer to Name.com

        authCode : str
            AuthCode is the authorization code for the transfer

        purchasePrice : float
            the amount to pay for the transfer of the domain

        privacyEnabled : bool
            a flag on whether to purchase Whois Privacy with the transfer

        promoCode : str
            PromoCode is not implemented yet

        Returns
        -------
        :class:`~namecom.result_models.CreateTransferResult`
            a response result instance with parsed response info
        """
        data = json_dumps({
            'domainName': domainName,
            'authCode': authCode,
            'purchasePrice': purchasePrice,
            'privacyEnabled': privacyEnabled,
            'promoCode': promoCode
        })

        resp = self._do('POST', data=data)
        return self._parse_result(resp, parse_create_transfer, CreateTransferResult)

    def cancel_transfer(self, domainName):
        """Cancels a pending transfer request and refunds the amount to account credit.

        Parameters
        ----------
        domainName : str
            DomainName is the domain to be transfered to Name.com

        Returns
        -------
        :class:`~namecom.result_models.CancelTransferResult`
            a response result instance with parsed response info
        """
        resp = self._do('POST', relative_path='/{domainName}:cancel'.format(domainName=domainName))
        return self._parse_result(resp, parse_cancel_tranfer, CancelTransferResult)


class URLForwardingApi(_ApiBase):

    def __init__(self, domainName, auth, use_test_env=False):
        """
        Parameters
        ----------
        domainName : str
            domain name to manipulate url forwarding for

        auth : :class:`~namecom.Auth`
            http authentication to use

        use_test_env : bool
            whether runs in test environment
        """
        super(URLForwardingApi, self).__init__(auth, use_test_env)
        self.endpoint = '/v4/domains/{domainName}/url/forwarding'.format(domainName=domainName)

    def list_url_forwardings(self, page=1, perPage=1000):
        """Returns a pagenated list of URL forwarding entries for a domain.

        Parameters
        ----------
        page: int
            which page to return

        perPage : int
            the number of records to return per request

        Returns
        -------
        :class:`~namecom.result_models.ListURLForwardingsResult`
            a response result instance with parsed response info
        """
        params = {
            'page': page,
            'perPage': perPage
        }

        resp = self._do('GET', params=params)
        return self._parse_result(resp, parse_list_url_forwardings, ListURLForwardingsResult)

    def get_url_forwarding(self, host):
        """Returns an URL forwarding entry.

        Parameters
        ----------
        host : str
            the part of the domain name before the domain

        Returns
        -------
        :class:`~namecom.result_models.GetURLForwardingResult`
            a response result instance with parsed response info
        """
        resp = self._do('GET', relative_path='/{host}'.format(host=host))
        return self._parse_result(resp, parse_get_url_forwarding, GetURLForwardingResult)

    def create_url_forwarding(self, host, forwardsTo, type=None, title=None, meta=None):
        """Creates an URL forwarding entry.

        If this is the first URL forwarding entry, it may modify the A records for the domain accordingly.

        Parameters
        ----------
        host : str
            the entirety of the hostname. i.e. www.example.org

        forwardsTo : str
            the URL this host will be forwarded to

        type : str
            the type of forwarding

        title : str
            the title for the html page to use if the type is masked

        meta : str
            the meta tags to add to the html page if the type is masked

        Returns
        -------
        :class:`~namecom.result_models.CreateURLForwardingResult`
            a response result instance with parsed response info
        """
        data = json_dumps({
            'host': host,
            'forwardsTo': forwardsTo,
            'type': type,
            'title': title,
            'meta': meta
        })

        resp = self._do('POST', data=data)
        return self._parse_result(resp, parse_create_url_forwarding, CreateURLForwardingResult)

    def update_url_forwarding(self, host, forwardsTo, type=None, title=None, meta=None):
        """Updates which URL the host is being forwarded to.

        Parameters
        ----------
        host : str
            the entirety of the hostname. i.e. www.example.org

        forwardsTo : str
            the URL this host will be forwarded to

        type : str
            the type of forwarding

        title : str
            the title for the html page to use if the type is masked

        meta : str
            the meta tags to add to the html page if the type is masked

        Returns
        -------
        :class:`~namecom.result_models.UpdateURLForwardingResult`
            a response result instance with parsed response info
        """
        data = json_dumps({
            'forwardsTo': forwardsTo,
            'type': type,
            'title': title,
            'meta': meta
        })

        resp = self._do('PUT', relative_path='/{host}'.format(host=host), data=data)
        return self._parse_result(resp, parse_update_url_forwarding, UpdateURLForwardingResult)

    def delete_url_forwarding(self, host):
        """Deletes the URL forwarding entry.

        Parameters
        ----------
        host : str
            the entirety of the hostname. i.e. www.example.org

        Returns
        -------
        :class:`~namecom.result_models.DeleteURLForwardingResult`
            a response result instance with parsed response info
        """
        resp = self._do('DELETE', relative_path='/{host}'.format(host=host))
        return self._parse_result(resp, parse_delete_url_forwarding, DeleteURLForwardingResult)


class VanityNameserverApi(_ApiBase):

    def __init__(self, domainName, auth, use_test_env=False):
        """
        Parameters
        ----------
        domainName : str
            domain name to manipulate nameserver for

        auth : :class:`~namecom.Auth`
            http authentication to use

        use_test_env : bool
            whether runs in test environment
        """
        super(VanityNameserverApi, self).__init__(auth, use_test_env)
        self.endpoint = '/v4/domains/{domainName}/vanity_nameservers'.format(domainName=domainName)

    def list_vanity_nameservers(self, page=1, perPage=1000):
        """Lists all nameservers registered with the registry.

        It omits the IP addresses from the response. Those can be found from calling GetVanityNameserver.

        Parameters
        ----------
        page: int
            which page to return

        perPage : int
            the number of records to return per request

        Returns
        -------
        :class:`~namecom.result_models.ListVanityNameserversResult`
            a response result instance with parsed response info
        """
        params = {
            'page': page,
            'perPage': perPage
        }

        resp = self._do('GET', params=params)
        return self._parse_result(resp, parse_list_vanity_nameservers, ListVanityNameserversResult)

    def get_vanity_nameserver(self, hostname):
        """GetVanityNameserver gets the details for a vanity nameserver registered with the registry.

        Parameters
        ----------
        hostname: str
            the hostname of the nameserver

        Returns
        -------
        :class:`~namecom.result_models.GetVanityNameserverResult`
            a response result instance with parsed response info
        """
        resp = self._do('GET', relative_path='/{hostname}'.format(hostname=hostname))
        return self._parse_result(resp, parse_get_vanity_nameserver, GetVanityNameserverResult)

    def create_vanity_nameserver(self, hostname, ips):
        """Registers a nameserver with the registry.

        Parameters
        ----------
        hostname: str
            the hostname of the nameserver

        ips: []str
            a list of IP addresses that are used for glue records for this nameserver

        Returns
        -------
        :class:`~namecom.result_models.CreateVanityNameserverResult`
            a response result instance with parsed response info
        """
        data = json_dumps({
            'hostname': hostname,
            'ips': ips
        })

        resp = self._do('POST', data=data)
        return self._parse_result(resp, parse_create_vanity_nameserver, CreateVanityNameserverResult)

    def update_vanity_nameserver(self, hostname, ips):
        """Update the glue record IP addresses at the registry.

        Parameters
        ----------
        hostname: str
            the domain to for the vanity nameserver

        ips: []str
            a list of IP addresses that are used for glue records for this nameserver

        Returns
        -------
        :class:`~namecom.result_models.UpdateVanityNameserverResult`
            a response result instance with parsed response info
        """
        data = json_dumps({
            'ips': ips
        })

        resp = self._do('PUT', relative_path='/{hostname}'.format(hostname=hostname), data=data)
        return self._parse_result(resp, parse_update_vanity_nameserver, UpdateVanityNameserverResult)

    def delete_vanity_nameserver(self, hostname):
        """Unregisteres the nameserver at the registry.

        This might fail if the registry believes the nameserver is in use.

        Parameters
        ----------
        hostname : str
            the domain of the vanity nameserver to delete

        Returns
        -------
        :class:`~namecom.result_models.DeleteVanityNameserverResult`
            a response result instance with parsed response info
        """
        resp = self._do('DELETE', relative_path='/{hostname}'.format(hostname=hostname))
        return self._parse_result(resp, parse_delete_vanity_nameserver, DeleteVanityNameserverResult)

