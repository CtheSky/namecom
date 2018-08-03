"""
namecom: result_models.py

Defines response result models for the api.

Tianhong Chu [https://github.com/CtheSky]
License: MIT
"""


class RequestResult(object):
    """Base class for Response class.

    Attributes
    ----------
    resp :
        http response from requests.Response

    status_code : int
        http status code

    headers : MutableMapping)
        http response headers from requests.Response
    """
    def __init__(self, resp):
        self.resp = resp
        self.status_code = resp.status_code
        self.headers = resp.headers


class ListRecordsResult(RequestResult):
    """Response class for ListRecords method.

    Attributes
    ----------
    records : [] :class:`~namecom.Record`
        list of Records

    nextPage : int
        NextPage is the identifier for the next page of results. 
        It is only populated if there is another page of results after the current page.

    lastPage : int
        LastPage is the identifier for the final page of results. 
        It is only populated if there is another page of results after the current page.
    """
    def __init__(self, resp):
        super(ListRecordsResult, self).__init__(resp)

        self.records = []
        self.nextPage = None
        self.lastPage = None


class GetRecordResult(RequestResult):
    """Response class for GetRecord method.

    Attributes
    ----------
    record : :class:`~namecom.Record`
        instance of Record
    """
    def __init__(self, resp):
        super(GetRecordResult, self).__init__(resp)

        self.record = None


class CreateRecordResult(RequestResult):
    """Response class for CreateRecord method.

    Attributes
    ----------
    record : :class:`~namecom.Record`
        instance of Record
    """
    def __init__(self, resp):
        super(CreateRecordResult, self).__init__(resp)

        self.record = None


class UpdateRecordResult(RequestResult):
    """Response class for UpdateRecord method.

    Attributes
    ----------
    record : :class:`~namecom.Record`
        instance of Record
    """
    def __init__(self, resp):
        super(UpdateRecordResult, self).__init__(resp)

        self.record = None


class DeleteRecordResult(RequestResult):
    """Response class for DeleteRecord method."""


class ListDnssecsResult(RequestResult):
    """Response class for ListDnssecs method.

    Attributes
    ----------
    dnssecs : [] :class:`~namecom.DNSSEC`
        list of DNSSEC

    nextPage : int
        NextPage is the identifier for the next page of results. 
        It is only populated if there is another page of results after the current page.

    lastPage : int
        LastPage is the identifier for the final page of results. 
        It is only populated if there is another page of results after the current page.
    """
    
    def __init__(self, resp):
        super(ListDnssecsResult, self).__init__(resp)

        self.dnssecs = []
        self.nextPage = None
        self.lastPage = None


class GetDnssecResult(RequestResult):
    """Response class for GetDnssec method.

    Attributes
    ----------
    dnssec : :class:`~namecom.DNSSEC`
        instance of DNSSEC
    """
    def __init__(self, resp):
        super(GetDnssecResult, self).__init__(resp)

        self.dnssec = None


class CreateDnssecResult(RequestResult):
    """Response class for CreateDnssec method.

    Attributes
    ----------
    dnssec : :class:`~namecom.DNSSEC`
        instance of DNSSEC
    """
    def __init__(self, resp):
        super(CreateDnssecResult, self).__init__(resp)

        self.dnssec = None


class DeleteDnssecResult(RequestResult):
    """Response class for DeleteDnssec method."""


class ListDomainsResult(RequestResult):
    """Response class for ListDomains method.

    Attributes
    ----------
    domains : [] :class:`~namecom.Domain`
        list of Domains

    nextPage : int
        NextPage is the identifier for the next page of results. 
        It is only populated if there is another page of results after the current page.

    lastPage : int
        LastPage is the identifier for the final page of results. 
        It is only populated if there is another page of results after the current page.
    """
    def __init__(self, resp):
        super(ListDomainsResult, self).__init__(resp)

        self.domains = []
        self.nextPage = None
        self.lastPage = None


class GetDomainResult(RequestResult):
    """Response class for GetDomain method.

    Attributes
    ----------
    domain : :class:`~namecom.Domain`
        instance of Domain
    """
    def __init__(self, resp):
        super(GetDomainResult, self).__init__(resp)

        self.domain = None


class SearchResult(RequestResult):
    """Response class for Search method.

    Attributes
    ----------
    results : [] :class:`~namecom.DomainSearchResult`
        instance of DomainSearchResult
    """
    def __init__(self, resp):
        super(SearchResult, self).__init__(resp)

        self.results = []


class CreateDomainResult(RequestResult):
    """Response class for CreateDomain method.

    Attributes
    ----------
    domain : :class:`~namecom.Domain`
        instance of Domain

    order : int
        Order is an identifier for this purchase.
    
    totalPaid : float
        TotalPaid is the total amount paid
    """
    def __init__(self, resp):
        super(CreateDomainResult, self).__init__(resp)

        self.domain = None
        self.order = None
        self.totalPaid = None


class EnableAutorenewResult(RequestResult):
    """Response class for EnableAutorenew method.

    Attributes
    ----------
    domain : :class:`~namecom.Domain`
        instance of Domain
    """
    def __init__(self, resp):
        super(EnableAutorenewResult, self).__init__(resp)

        self.domain = None


class DisableAutorenewResult(RequestResult):
    """Response class for DisableAutorenew method.

    Attributes
    ----------
    domain : :class:`~namecom.Domain`
        instance of Domain
    """
    def __init__(self, resp):
        super(DisableAutorenewResult, self).__init__(resp)

        self.domain = None


class SetNameserversResult(RequestResult):
    """Response class for SetNameservers method.

    Attributes
    ----------
    domain : :class:`~namecom.Domain`
        instance of Domain
    """
    def __init__(self, resp):
        super(SetNameserversResult, self).__init__(resp)

        self.domain = None


class SetContactsResult(RequestResult):
    """Response class for SetContacts method.

    Attributes
    ----------
    domain : :class:`~namecom.Domain`
        instance of Domain
    """
    def __init__(self, resp):
        super(SetContactsResult, self).__init__(resp)

        self.domain = None


class RenewDomainResult(RequestResult):
    """Response class for RenewDomain method.

    Attributes
    ----------
    domain : :class:`~namecom.Domain`
        instance of Domain

    order : int
        Order is an identifier for this purchase.
    
    totalPaid : float
        TotalPaid is the total amount paid
    """
    def __init__(self, resp):
        super(RenewDomainResult, self).__init__(resp)

        self.domain = None
        self.order = None
        self.totalPaid = None


class PurchasePrivacyResult(RequestResult):
    """Response class for PurchasePrivacy method.

    Attributes
    ----------
    domain : :class:`~namecom.Domain`
        instance of Domain

    order : int
        Order is an identifier for this purchase.
    
    totalPaid : float
        TotalPaid is the total amount paid
    """
    def __init__(self, resp):
        super(PurchasePrivacyResult, self).__init__(resp)

        self.domain = None
        self.order = None
        self.totalPaid = None


class GetAuthCodeForDomainResult(RequestResult):
    """Response class for GetAuthCodeForDomain method.

    Attributes
    ----------
    authCode : str
        AuthCode is the authorization code needed to transfer a domain to another registrar
    """
    def __init__(self, resp):
        super(GetAuthCodeForDomainResult, self).__init__(resp)

        self.authCode = None


class LockDomainResult(RequestResult):
    """Response class for LockDomain method.

    Attributes
    ----------
    domain : :class:`~namecom.Domain`
        instance of Domain
    """
    def __init__(self, resp):
        super(LockDomainResult, self).__init__(resp)

        self.domain = None


class UnlockDomainResult(RequestResult):
    """Response class for UnlockDomain method.

    Attributes
    ----------
    domain : :class:`~namecom.Domain`
        instance of Domain
    """
    def __init__(self, resp):
        super(UnlockDomainResult, self).__init__(resp)

        self.domain = None


class CheckAvailabilityResult(RequestResult):
    """Response class for CheckAvailability method.

    Attributes
    ----------
    results : [] :class:`~namecom.DomainSearchResult`
        instance of DomainSearchResult
    """
    def __init__(self, resp):
        super(CheckAvailabilityResult, self).__init__(resp)

        self.results = []


class SearchStreamResult(RequestResult):
    """Response class for SearchStream method.

    Attributes
    ----------
    results : [] :class:`~namecom.DomainSearchResult`
        a generator yielding of DomainSearchResult
    """
    def __init__(self, resp):
        super(SearchStreamResult, self).__init__(resp)

        self.results = []


class ListEmailForwardingsResult(RequestResult):
    """Response class for ListEmailForwardings method.

    Attributes
    ----------
    email_forwardings : [] :class:`~namecom.EmailForwarding`
        list of EmailForwarding

    nextPage : int
        NextPage is the identifier for the next page of results. 
        It is only populated if there is another page of results after the current page.

    lastPage : int
        LastPage is the identifier for the final page of results. 
        It is only populated if there is another page of results after the current page.
    """
    def __init__(self, resp):
        super(ListEmailForwardingsResult, self).__init__(resp)

        self.email_forwardings = []
        self.nextPage = None
        self.lastPage = None


class GetEmailForwardingResult(RequestResult):
    """Response class for GetEmailForwarding method.

    Attributes
    ----------
    email_forwarding : :class:`~namecom.EmailForwarding`
        instance of EmailForwarding
    """
    def __init__(self, resp):
        super(GetEmailForwardingResult, self).__init__(resp)

        self.email_forwarding = None


class CreateEmailForwardingResult(RequestResult):
    """Response class for CreateEmailForwarding method.

    Attributes
    ----------
    email_forwarding : :class:`~namecom.EmailForwarding`
        instance of EmailForwarding
    """
    def __init__(self, resp):
        super(CreateEmailForwardingResult, self).__init__(resp)

        self.email_forwarding = None


class UpdateEmailForwardingResult(RequestResult):
    """Response class for UpdateEmailForwarding method.

    Attributes
    ----------
    email_forwarding : :class:`~namecom.EmailForwarding`
        instance of EmailForwarding
    """
    def __init__(self, resp):
        super(UpdateEmailForwardingResult, self).__init__(resp)

        self.email_forwarding = None


class DeleteEmailForwardingResult(RequestResult):
    """Response class for DeleteEmailForwarding method."""


class ListTransfersResult(RequestResult):
    """Response class for ListTransfers method.

    Attributes
    ----------
    transfers : [] :class:`~namecom.Transfer`
        list of Transfer

    nextPage : int
        NextPage is the identifier for the next page of results. 
        It is only populated if there is another page of results after the current page.

    lastPage : int
        LastPage is the identifier for the final page of results. 
        It is only populated if there is another page of results after the current page.
    """
    def __init__(self, resp):
        super(ListTransfersResult, self).__init__(resp)

        self.transfers = []
        self.nextPage = None
        self.lastPage = None


class GetTransferResult(RequestResult):
    """Response class for GetTransfer method.

    Attributes
    ----------
    transfer : :class:`~namecom.Transfer`
        instance of Transfer
    """
    def __init__(self, resp):
        super(GetTransferResult, self).__init__(resp)

        self.transfer = None


class CreateTransferResult(RequestResult):
    """Response class for CreateTransfer method.

    Attributes
    ----------
    transfer : :class:`~namecom.Transfer`
        instance of Transfer

    order : int
        Order is an identifier for this purchase.
    
    totalPaid : float
        TotalPaid is the total amount paid
    """
    def __init__(self, resp):
        super(CreateTransferResult, self).__init__(resp)

        self.transfer = None
        self.order = None
        self.totalPaid = None


class CancelTransferResult(RequestResult):
    """Response class for CancelTransfer method.

    Attributes
    ----------
    transfer : :class:`~namecom.Transfer`
        instance of Transfer
    """
    def __init__(self, resp):
        super(CancelTransferResult, self).__init__(resp)

        self.transfer = None


class ListURLForwardingsResult(RequestResult):
    """Response class for ListURLForwardins method.

    Attributes
    ----------
    url_forwardings : [] :class:`~namecom.URLForwarding`
        list of URLForwarding

    nextPage : int
        NextPage is the identifier for the next page of results. 
        It is only populated if there is another page of results after the current page.

    lastPage : int
        LastPage is the identifier for the final page of results. 
        It is only populated if there is another page of results after the current page.
    """
    def __init__(self, resp):
        super(ListURLForwardingsResult, self).__init__(resp)

        self.url_forwardings = []
        self.nextPage = None
        self.lastPage = None


class GetURLForwardingResult(RequestResult):
    """Response class for GetURLForwarding method.

    Attributes
    ----------
    url_forwarding : :class:`~namecom.URLForwarding`
        instance of URLForwarding
    """
    def __init__(self, resp):
        super(GetURLForwardingResult, self).__init__(resp)

        self.url_forwarding = None


class CreateURLForwardingResult(RequestResult):
    """Response class for CreateURLForwarding method.

    Attributes
    ----------
    url_forwarding : :class:`~namecom.URLForwarding`
        instance of URLForwarding
    """
    def __init__(self, resp):
        super(CreateURLForwardingResult, self).__init__(resp)

        self.url_forwarding = None


class UpdateURLForwardingResult(RequestResult):
    """Response class for UpdateURLForwarding method.

    Attributes
    ----------
    url_forwarding : :class:`~namecom.URLForwarding`
        instance of URLForwarding
    """
    def __init__(self, resp):
        super(UpdateURLForwardingResult, self).__init__(resp)

        self.url_forwarding = None


class DeleteURLForwardingResult(RequestResult):
    """Response class for DeleteURLForwarding method."""


class ListVanityNameserversResult(RequestResult):
    """Response class for ListVanityNameservers method.

    Attributes
    ----------
    vanityNameservers : [] :class:`~namecom.VanityNameserver`
        list of VanityNameserver

    nextPage : int
        NextPage is the identifier for the next page of results. 
        It is only populated if there is another page of results after the current page.

    lastPage : int
        LastPage is the identifier for the final page of results. 
        It is only populated if there is another page of results after the current page.
    """
    def __init__(self, resp):
        super(ListVanityNameserversResult, self).__init__(resp)

        self.vanityNameservers = []
        self.nextPage = None
        self.lastPage = None


class GetVanityNameserverResult(RequestResult):
    """Response class for GetVanityNameserver method.

    Attributes
    ----------
    vanityNameserver : :class:`~namecom.VanityNameserver`
        instance of VanityNameserver
    """
    def __init__(self, resp):
        super(GetVanityNameserverResult, self).__init__(resp)

        self.vanityNameserver = None


class CreateVanityNameserverResult(RequestResult):
    """Response class for CreateVanityNameserver method.

    Attributes
    ----------
    vanityNameserver : :class:`~namecom.VanityNameserver`
        instance of VanityNameserver
    """
    def __init__(self, resp):
        super(CreateVanityNameserverResult, self).__init__(resp)

        self.vanityNameserver = None


class UpdateVanityNameserverResult(RequestResult):
    """Response class for UpdateVanityNameserver method.

    Attributes
    ----------
    vanityNameserver : :class:`~namecom.VanityNameserver`
        instance of VanityNameserver
    """
    def __init__(self, resp):
        super(UpdateVanityNameserverResult, self).__init__(resp)

        self.vanityNameserver = None
        
        
class DeleteVanityNameserverResult(RequestResult):
    """Response class for DeleteVanityNameserver method."""
