# encoding=utf-8

__all__ = ['ListDomainsResult', 'GetDomainResult', 'SearchResult', 'CreateDomainResult',
           'EnableAutorenewResult', 'DisableAutorenewResult', 'SetNameserversResult']


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


class EnableAutorenewResult(RequestResult):

    def __init__(self, resp):
        super(EnableAutorenewResult, self).__init__(resp)

        self. domain = None


class DisableAutorenewResult(RequestResult):

    def __init__(self, resp):
        super(DisableAutorenewResult, self).__init__(resp)

        self. domain = None


class SetNameserversResult(RequestResult):

    def __init__(self, resp):
        super(SetNameserversResult, self).__init__(resp)

        self. domain = None

