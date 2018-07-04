__all__ = ['DnsApi', 'DnssecApi', 'DomainApi']

import requests

from . import exceptions
from .utils import *
from .models import *

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

    def list_records(self):
        """Returns all records for a zone.

        Returns
        -------
        :class:`~namecom.ListRecordsResult`
            a response result instance with parsed response info
        """
        resp = self._do('GET')
        return self._parse_result(resp, parse_list_records, ListRecordsResult)

    def get_record(self, id):
        """Returns details about an individual record.

        Parameters
        ----------
        id : int
            the server-assigned unique identifier for this record

        Returns
        -------
        :class:`~namecom.GetRecordResult`
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
        :class:`~namecom.CreateRecordResult`
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
        :class:`~namecom.UpdateRecordResult`
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
        :class:`~namecom.DeleteRecordResult`
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

    def list_dnssecs(self):
        """Lists all of the DNSSEC keys registered with the registry.

        Returns
        -------
        :class:`~namecom.ListDnssecsResult`
            a response result instance with parsed response info
        """
        resp = self._do('GET')
        return self._parse_result(resp, parse_list_dnssecs, ListDnssecsResult)

    def get_dnssec(self, digest):
        """Retrieves the details for a key registered with the registry.

        Parameters
        ----------
        digest : string
            Digest is the digest for the DNSKEY RR to retrieve.

        Returns
        -------
        :class:`~namecom.GetDnssecResult`
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
        :class:`~namecom.CreateDnssecResult`
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
        :class:`~namecom.DeleteDnssecResult`
            a response result instance with parsed response info
        """
        resp = self._do('DELETE', relative_path='/{digest}'.format(digest=digest))
        return self._parse_result(resp, parse_delete_dnssec, DeleteDnssecResult)


class DomainApi(_ApiBase):

    def __init__(self, auth, use_test_env=False):
        super(DomainApi, self).__init__(auth, use_test_env)
        self.endpoint = '/v4/domains'

    def list_domains(self):
        resp = self._do('GET')
        return self._parse_result(resp, parse_list_domains, ListDomainsResult)

    def get_domain(self, domainName):
        resp = self._do('GET', relative_path='/{domainName}'.format(domainName=domainName))
        return self._parse_result(resp, parse_get_domain, GetDomainResult)

    def create_domain(self, domain, purchasePrice, purchaseType='registration',
                      years=1, tldRequirements=None, promoCode=None):
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
        resp = self._do('POST', relative_path='/{domainName}:enableAutorenew'.format(domainName=domainName))
        return self._parse_result(resp, parse_enable_autorenew, EnableAutorenewResult)

    def disable_autorenew(self, domainName):
        resp = self._do('POST', relative_path='/{domainName}:disableAutorenew'.format(domainName=domainName))
        return self._parse_result(resp, parse_disable_autorenew, DisableAutorenewResult)

    def set_nameservers(self, domainName, nameservers):
        data = json_dumps({
            'nameservers': nameservers
        })

        resp = self._do('POST', relative_path='/{domainName}:setNameservers'.format(domainName=domainName), data=data)
        return self._parse_result(resp, parse_set_nameservers, SetNameserversResult)

    def set_contacts(self, domainName, contacts):
        data = json_dumps({
            'contacts': contacts
        })

        resp = self._do('POST', relative_path='/{domainName}:setContacts'.format(domainName=domainName), data=data)
        return self._parse_result(resp, parse_set_contacts, SetContactsResult)

    def renew_domain(self, domainName, purchasePrice, years=1, promoCode=None):
        data = json_dumps({
            'purchasePrice': purchasePrice,
            'years': years,
            'promoCode': promoCode
        })

        resp = self._do('POST', relative_path='/{domainName}:renew'.format(domainName=domainName), data=data)
        return self._parse_result(resp, parse_renew_domain, RenewDomainResult)

    def purchase_privacy(self, domainName, purchasePrice, years=1, promoCode=None):
        data = json_dumps({
            'purchasePrice': purchasePrice,
            'years': years,
            'promoCode': promoCode
        })

        resp = self._do('POST', relative_path='/{domainName}:purchasePrivacy'.format(domainName=domainName), data=data)
        return self._parse_result(resp, parse_purchase_privacy, PurchasePrivacyResult)

    def get_auth_code_for_domain(self, domainName):
        resp = self._do('GET',  relative_path='/{domainName}:getAuthCode'.format(domainName=domainName))
        return self._parse_result(resp, parse_get_authcode, GetAuthCodeForDomainResult)

    def lock_domain(self, domainName):
        resp = self._do('POST', relative_path='/{domainName}:lock'.format(domainName=domainName))
        return self._parse_result(resp, parse_lock_domain, LockDomainResult)

    def unlock_domain(self, domainName):
        resp = self._do('POST', relative_path='/{domainName}:unlock'.format(domainName=domainName))
        return self._parse_result(resp, parse_unlock_domain, UnlockDomainResult)

    def check_availability(self, domainNames, promoCode=None):
        data = json_dumps({
            'domainNames': domainNames,
            'promoCode': promoCode
        })

        resp = self._do('POST', relative_path=':checkAvailability', data=data)
        return self._parse_result(resp, parse_check_availability, CheckAvailabilityResult)

    def search(self, keyword, tldFilter=None, timeout=1000, promoCode=None):
        data = json_dumps({
            'keyword': keyword,
            'tldFilter': tldFilter if tldFilter else [],
            'timeout': timeout,
            'promoCode': promoCode
        })

        resp = self._do('POST', relative_path=':search', data=data)
        return self._parse_result(resp, parse_search, SearchResult)

    def search_stream(self, keyword, tldFilter=None, timeout=1000, promoCode=None):
        data = json_dumps({
            'keyword': keyword,
            'tldFilter': tldFilter if tldFilter else [],
            'timeout': timeout,
            'promoCode': promoCode
        })

        resp = self._do('POST', relative_path=':searchStream', data=data)
        result = SearchStreamResult(resp)
        parse_search_stream(result, [json.loads(obj) for obj in resp.content.strip().split('\n')])

        return result
