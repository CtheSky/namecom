from ..models import *


def parse_list_records(result, dct):
    result.records = [Record.from_dict(obj) for obj in dct.get('records', [])]


def parse_get_record(result, dct):
    result.record = Record.from_dict(dct)


def parse_create_record(result, dct):
    result.record = Record.from_dict(dct)


def parse_update_record(result, dct):
    result.record = Record.from_dict(dct)


def parse_delete_record(result, dct):
    pass


def parse_list_dnssecs(result, dct):
    result.dnssecs = [DNSSEC.from_dict(obj) for obj in dct.get('dnssec')]
    result.nextPage = dct.get('nextPage')
    result.lastPage = dct.get('lastPage')


def parse_get_dnssec(result, dct):
    result.dnssec = DNSSEC.from_dict(dct)


def parse_create_dnssec(result, dct):
    result.dnssec = DNSSEC.from_dict(dct)


def parse_delete_dnssec(result, dct):
    pass


def parse_list_domains(result, dct):
    result.domains = [Domain.from_dict(obj) for obj in dct.get('domains', [])]
    result.nextPage = dct.get('nextPage')
    result.lastPage = dct.get('lastPage')


def parse_get_domain(result, dct):
    result.domain = Domain.from_dict(dct)


def parse_create_domain(result, dct):
    result.domain = Domain.from_dict(dct.get('domain'))
    result.order = dct.get('order')
    result.totalPaid = dct.get('totalPaid')


def parse_enable_autorenew(result, dct):
    result.domain = Domain.from_dict(dct)


def parse_disable_autorenew(result, dct):
    result.domain = Domain.from_dict(dct)


def parse_set_nameservers(result, dct):
    result.domain = Domain.from_dict(dct)


def parse_set_contacts(result, dct):
    result.domain = Domain.from_dict(dct)


def parse_renew_domain(result, dct):
    result.domain = Domain.from_dict(dct.get('domain'))
    result.order = dct.get('order')
    result.totalPaid = dct.get('totalPaid')


def parse_purchase_privacy(result, dct):
    result.domain = Domain.from_dict(dct.get('domain'))
    result.order = dct.get('order')
    result.totalPaid = dct.get('totalPaid')


def parse_get_authcode(result, dct):
    result.authCode = dct.get('authCode')


def parse_lock_domain(result, dct):
    result.domain = Domain.from_dict(dct)


def parse_unlock_domain(result, dct):
    result.domain = Domain.from_dict(dct)


def parse_check_availability(result, dct):
    result.results = [DomainSearchResult.from_dict(obj) for obj in dct.get('results', [])]


def parse_search(result, dct):
    result.results = [DomainSearchResult.from_dict(obj) for obj in dct.get('results', [])]


def parse_search_stream(result, dct):
    result.results = [DomainSearchResult.from_dict(obj) for obj in dct]


def parse_list_email_forwardings(result, dct):
    result.email_forwardings = [EmailForwarding.from_dict(obj) for obj in dct.get('emailForwarding', [])]
    result.nextPage = dct.get('nextPage')
    result.lastPage = dct.get('lastPage')


def parse_get_email_forwarding(result, dct):
    result.email_forwarding = EmailForwarding.from_dict(dct)


def parse_create_email_forwarding(result, dct):
    result.email_forwarding = EmailForwarding.from_dict(dct)


def parse_update_email_forwarding(result, dct):
    result.email_forwarding = EmailForwarding.from_dict(dct)


def parse_delete_email_forwarding(result, dct):
    pass


def parse_list_transfers(result, dct):
    result.transfers = [Transfer.from_dict(obj) for obj in dct.get('transfers', [])]
    result.nextPage = dct.get('nextPage')
    result.lastPage = dct.get('lastPage')


def parse_get_transfer(result, dct):
    result.transfer = Transfer.from_dict(dct)


def parse_create_transfer(result, dct):
    result.transfer = Transfer.from_dict(dct.get('transfer'))
    result.order = dct.get('order')
    result.totalPaid = dct.get('totalPaid')


def parse_cancel_tranfer(result, dct):
    result.transfer = Transfer.from_dict(dct)