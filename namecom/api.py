# encoding=utf-8

__all__ = ['DomainApi']

import requests
import json

from parse_utils import *
from .models import *

PRODUCT_API_HOST = 'https://api.name.com'
TEST_API_HOST = 'https://api.dev.name.com'


class _ApiBase(object):
    def __init__(self, auth):
        self.auth = auth
        self.api_host = PRODUCT_API_HOST if not auth.use_test_env else TEST_API_HOST
        self.endpoint = ''

    def _do(self, method, relative_path=None, **kwargs):
        resp = requests.request(method,
                                self.api_host + self.endpoint + (relative_path if relative_path else ''),
                                auth=self.auth.auth_tuple,
                                **kwargs)
        return resp

    def _parse_result(self, resp, parse_func, klass):
        result = klass(resp)
        parse_func(result, resp.json())
        return result


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
        data = json.dumps({
            'domain': domain.to_dict(),
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
        data = json.dumps({
            'nameservers': nameservers
        })

        resp = self._do('POST', relative_path='/{domainName}:setNameservers'.format(domainName=domainName), data=data)
        return self._parse_result(resp, parse_set_nameservers, SetNameserversResult)

    def set_contacts(self, domainName, contacts):
        data = json.dumps({
            'contacts': contacts.to_dict()
        })

        resp = self._do('POST', relative_path='/{domainName}:setContacts'.format(domainName=domainName), data=data)
        return self._parse_result(resp, parse_set_contacts, SetContactsResult)

    def renew_domain(self, domainName, purchasePrice, years=1, promoCode=None):
        data = json.dumps({
            'purchasePrice': purchasePrice,
            'years': years,
            'promoCode': promoCode
        })

        resp = self._do('POST', relative_path='/{domainName}:renew'.format(domainName=domainName), data=data)
        return self._parse_result(resp, parse_renew_domain, RenewDomainResult)

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
        data = json.dumps({
            'domainNames': domainNames,
            'promoCode': promoCode
        })

        resp = self._do('POST', relative_path=':checkAvailability', data=data)
        return self._parse_result(resp, parse_check_availability, CheckAvailabilityResult)

    def search(self, keyword, tldFilter=None, timeout=1000, promoCode=None):
        data = json.dumps({
            'keyword': keyword,
            'tldFilter': tldFilter if tldFilter else [],
            'timeout': timeout,
            'promoCode': promoCode
        })

        resp = self._do('POST', relative_path=':search', data=data)
        return self._parse_result(resp, parse_search, SearchResult)

    def search_stream(self, keyword, tldFilter=None, timeout=1000, promoCode=None):
        data = json.dumps({
            'keyword': keyword,
            'tldFilter': tldFilter if tldFilter else [],
            'timeout': timeout,
            'promoCode': promoCode
        })

        resp = self._do('POST', relative_path=':searchStream', data=data)
        result = SearchStreamResult(resp)
        parse_search_stream(result, [json.loads(obj) for obj in resp.content.strip().split('\n')])

        return result
