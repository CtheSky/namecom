__all__ = ['DnsApi', 'DnssecApi', 'DomainApi']

import requests

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

    def __init__(self, auth):
        self.auth = auth
        self.api_host = PRODUCT_API_HOST if not auth.use_test_env else TEST_API_HOST
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
                                auth=self.auth.auth_tuple,
                                **kwargs)
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
    The api class for DNS.
    More details at: https://www.name.com/api-docs/DNS
    """

    def __init__(self, domainName, auth):
        super(DnsApi, self).__init__(auth)
        self.endpoint = '/v4/domains/{domain_name}/records'.format(domain_name=domainName)

    def list_records(self):
        """
        Returns all records for a zone.
        :return: an instance of ListRecordsResult class with parsed response info
        """
        resp = self._do('GET')
        return self._parse_result(resp, parse_list_records, ListRecordsResult)

    def get_record(self, id):
        """
        Returns details about an individual record.
        :param id: the server-assigned unique identifier for this record
        :return: an instance of GetRecordResult class with parsed response info
        """
        resp = self._do('GET', relative_path='/{id}'.format(id=id))
        return self._parse_result(resp, parse_get_record, GetRecordResult)

    def create_record(self, host, type, answer, ttl=300, priority=None):
        """
        Creates a new record in the zone.

        More details about each param could be found in docstring of Record class.
        :param host: hostname relative to the zone
        :param type: dns record type
        :param answer: dns record answer
        :param ttl: dns record ttl
        :param priority: dns record priority
        :return:
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
        """
        Replaces the record with the new record that is passed.

        More details about each param could be found in docstring of Record class.
        :param id: the server-assigned unique identifier for this record
        :param host: hostname relative to the zone
        :param type: dns record type
        :param answer: dns record answer
        :param ttl: dns record ttl
        :param priority: dns record priority
        :return:
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
        """
        Deletes a record from the zone.
        :param id: the server-assigned unique identifier for this record
        :return: an instance of DeleteRecordResult class with parsed response info
        """
        resp = self._do('DELETE', relative_path='/{id}'.format(id=id))
        return self._parse_result(resp, parse_delete_record, DeleteRecordResult)


class DnssecApi(_ApiBase):

    def __init__(self, domainName, auth):
        super(DnssecApi, self).__init__(auth)
        self.endpoint = '/v4/domains/{domainName}/dnssec'.format(domainName=domainName)

    def list_dnssecs(self):
        resp = self._do('GET')
        return self._parse_result(resp, parse_list_dnssecs, ListDnssecsResult)

    def get_dnssec(self, digest):
        resp = self._do('GET', relative_path='/{digest}'.format(digest=digest))
        return self._parse_result(resp, parse_get_dnssec, GetDnssecResult)

    def create_dnssec(self, keyTag, algorithm, digestType, digest):
        data = json_dumps({
            'keyTag': keyTag,
            'algorithm': algorithm,
            'digestType': digestType,
            'digest': digest
        })

        resp = self._do('POST', data=data)
        return self._parse_result(resp, parse_create_dnssec, CreateDnssecResult)

    def delete_dnssec(self, digest):
        resp = self._do('DELETE', relative_path='/{digest}'.format(digest=digest))
        return self._parse_result(resp, parse_delete_dnssec, DeleteDnssecResult)


class DomainApi(_ApiBase):

    def __init__(self, auth):
        super(DomainApi, self).__init__(auth)
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
