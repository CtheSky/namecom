# encoding=utf-8

__all__ = ['ListDomainsResult', 'GetDomainResult', 'SearchResult', 'CreateDomainResult']


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