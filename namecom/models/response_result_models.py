class RequestResult(object):
    def __init__(self, resp):
        self.resp = resp
        self.status_code = resp.status_code
        self.headers = resp.headers


class ListRecordsResult(RequestResult):

    def __init__(self, resp):
        super(ListRecordsResult, self).__init__(resp)

        self.records = []

    def __iter__(self):
        return iter(self.records)


class GetRecordResult(RequestResult):

    def __init__(self, resp):
        super(GetRecordResult, self).__init__(resp)

        self.record = None


class CreateRecordResult(RequestResult):

    def __init__(self, resp):
        super(CreateRecordResult, self).__init__(resp)

        self.record = None


class UpdateRecordResult(RequestResult):

    def __init__(self, resp):
        super(UpdateRecordResult, self).__init__(resp)

        self.record = None


class DeleteRecordResult(RequestResult):
    pass


class ListDnssecsResult(RequestResult):

    def __init__(self, resp):
        super(ListDnssecsResult, self).__init__(resp)

        self.dnssecs = []
        self.nextPage = None
        self.lastPage = None


class GetDnssecResult(RequestResult):

    def __init__(self, resp):
        super(GetDnssecResult, self).__init__(resp)

        self.dnssec = None


class CreateDnssecResult(RequestResult):

    def __init__(self, resp):
        super(CreateDnssecResult, self).__init__(resp)

        self.dnssec = None


class DeleteDnssecResult(RequestResult):
    pass


class ListDomainsResult(RequestResult):

    def __init__(self, resp):
        super(ListDomainsResult, self).__init__(resp)

        self.domains = []
        self.nextPage = None
        self.lastPage = None


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
        self.order = None
        self.totalPaid = None


class EnableAutorenewResult(RequestResult):

    def __init__(self, resp):
        super(EnableAutorenewResult, self).__init__(resp)

        self.domain = None


class DisableAutorenewResult(RequestResult):

    def __init__(self, resp):
        super(DisableAutorenewResult, self).__init__(resp)

        self.domain = None


class SetNameserversResult(RequestResult):

    def __init__(self, resp):
        super(SetNameserversResult, self).__init__(resp)

        self.domain = None


class SetContactsResult(RequestResult):

    def __init__(self, resp):
        super(SetContactsResult, self).__init__(resp)

        self.domain = None


class RenewDomainResult(RequestResult):

    def __init__(self, resp):
        super(RenewDomainResult, self).__init__(resp)

        self.domain = None
        self.order = None
        self.totalPaid = None


class PurchasePrivacyResult(RequestResult):

    def __init__(self, resp):
        super(PurchasePrivacyResult, self).__init__(resp)

        self.domain = None
        self.order = None
        self.totalPaid = None


class GetAuthCodeForDomainResult(RequestResult):

    def __init__(self, resp):
        super(GetAuthCodeForDomainResult, self).__init__(resp)

        self.authCode = ''


class LockDomainResult(RequestResult):

    def __init__(self, resp):
        super(LockDomainResult, self).__init__(resp)

        self. domain = None


class UnlockDomainResult(RequestResult):

    def __init__(self, resp):
        super(UnlockDomainResult, self).__init__(resp)

        self. domain = None


class CheckAvailabilityResult(RequestResult):

    def __init__(self, resp):
        super(CheckAvailabilityResult, self).__init__(resp)

        self.results = []


class SearchStreamResult(RequestResult):

    def __init__(self, resp):
        super(SearchStreamResult, self).__init__(resp)

        self.results = []


class ListEmailForwardingsResult(RequestResult):

    def __init__(self, resp):
        super(ListEmailForwardingsResult, self).__init__(resp)

        self.email_forwardings = []
        self.nextPage = None
        self.lastPage = None


class GetEmailForwardingResult(RequestResult):

    def __init__(self, resp):
        super(GetEmailForwardingResult, self).__init__(resp)

        self.email_forwarding = None


class CreateEmailForwardingResult(RequestResult):

    def __init__(self, resp):
        super(CreateEmailForwardingResult, self).__init__(resp)

        self.email_forwarding = None


class UpdateEmailForwardingResult(RequestResult):

    def __init__(self, resp):
        super(UpdateEmailForwardingResult, self).__init__(resp)

        self.email_forwarding = None


class DeleteEmailForwardingResult(RequestResult):
    pass


class ListTransfersResult(RequestResult):

    def __init__(self, resp):
        super(ListTransfersResult, self).__init__(resp)

        self.transfers = []


class GetTransferResult(RequestResult):

    def __init__(self, resp):
        super(GetTransferResult, self).__init__(resp)

        self.transfer = None


class CreateTransferResult(RequestResult):

    def __init__(self, resp):
        super(CreateTransferResult, self).__init__(resp)

        self.transfer = None
        self.order = None
        self.totalPaid = None


class CancelTransferResult(RequestResult):

    def __init__(self, resp):
        super(CancelTransferResult, self).__init__(resp)

        self.transfer = None


class ListURLForwardinsResult(RequestResult):

    def __init__(self, resp):
        super(ListURLForwardinsResult, self).__init__(resp)

        self.url_forwardings = []


class GetURLForwardingResult(RequestResult):

    def __init__(self, resp):
        super(GetURLForwardingResult, self).__init__(resp)

        self.url_forwarding = None


class CreateURLForwardingResult(RequestResult):

    def __init__(self, resp):
        super(CreateURLForwardingResult, self).__init__(resp)

        self.url_forwarding = None


class UpdateURLForwardingResult(RequestResult):

    def __init__(self, resp):
        super(UpdateURLForwardingResult, self).__init__(resp)

        self.url_forwarding = None


class DeleteURLForwardingResult(RequestResult):
    pass


class ListVanityNameserversResult(RequestResult):

    def __init__(self, resp):
        super(ListVanityNameserversResult, self).__init__(resp)

        self.vanityNameservers = []
        self.nextPage = None
        self.lastPage = None


class GetVanityNameserverResult(RequestResult):

    def __init__(self, resp):
        super(GetVanityNameserverResult, self).__init__(resp)

        self.vanityNameserver = None


class CreateVanityNameserverResult(RequestResult):

    def __init__(self, resp):
        super(CreateVanityNameserverResult, self).__init__(resp)

        self.vanityNameserver = None


class UpdateVanityNameserverResult(RequestResult):

    def __init__(self, resp):
        super(UpdateVanityNameserverResult, self).__init__(resp)

        self.vanityNameserver = None


class DeleteVanityNameserverResult(RequestResult):
    pass
