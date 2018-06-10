# encoding=utf-8

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
        parse_func(result, resp)
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

    def search(self, keyword, tldFilter=None, timeout=1000, promoCode=None):
        data = json.dumps({
            'keyword': keyword,
            'tldFilter': tldFilter if tldFilter else [],
            'timeout': timeout,
            'promoCode': promoCode
        })

        resp = self._do('POST', relative_path=':search', data=data)
        return self._parse_result(resp, parse_search, SearchResult)

    def create_domain(self, domain, purchasePrice, purchaseType='registration',
                      years=1, tldRequirements=None, promoCode=None):
        data = json.dumps({
            'domain': vars(domain),
            'purchasePrice': purchasePrice,
            'purchaseType': purchaseType,
            'years': years,
            'tldRequirements': tldRequirements if tldRequirements else [],
            'promoCode': promoCode
        })

        resp = self._do('POST', data=data)
        return self._parse_result(resp, parse_create_domain, CreateDomainResult)


__all__ = ['DomainApi']