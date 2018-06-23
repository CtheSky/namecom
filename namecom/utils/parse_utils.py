# encoding=utf-8

from ..models import *


def parse_list_records(result, data):
    result.records = [Record.from_dict(obj) for obj in data.get('records', [])]


def parse_get_record(result, data):
    result.record = Record.from_dict(data)


def parse_create_record(result, data):
    result.record = Record.from_dict(data)


def parse_update_record(result, data):
    result.record = Record.from_dict(data)


def parse_delete_record(result, data):
    pass


def parse_create_dnssec(result, data):
    result.dnssec = DNSSEC.from_dict(data)


def parse_delete_dnssec(result, data):
    pass

def parse_list_domains(result, data):
    result.domains = [Domain.from_dict(obj) for obj in data.get('domains', [])]
    result.nextPage = data.get('nextPage')
    result.lastPage = data.get('lastPage')


def parse_get_domain(result, data):
    result.domain = Domain.from_dict(data)


def parse_create_domain(result, data):
    result.domain = Domain.from_dict(data.get('domain'))
    result.order = data.get('order')
    result.totalPaid = data.get('totalPaid')


def parse_enable_autorenew(result, data):
    result.domain = Domain.from_dict(data)


def parse_disable_autorenew(result, data):
    result.domain = Domain.from_dict(data)


def parse_set_nameservers(result, data):
    result.domain = Domain.from_dict(data)


def parse_set_contacts(result, data):
    result.domain = Domain.from_dict(data)


def parse_renew_domain(result, data):
    result.domain = Domain.from_dict(data.get('domain'))
    result.order = data.get('order')
    result.totalPaid = data.get('totalPaid')


def parse_purchase_privacy(result, data):
    result.domain = Domain.from_dict(data.get('domain'))
    result.order = data.get('order')
    result.totalPaid = data.get('totalPaid')


def parse_get_authcode(result, data):
    result.authCode = data.get('authCode')


def parse_lock_domain(result, data):
    result.domain = Domain.from_dict(data)


def parse_unlock_domain(result, data):
    result.domain = Domain.from_dict(data)


def parse_check_availability(result, data):
    result.results = [DomainSearchResult.from_dict(obj) for obj in data.get('results', [])]


def parse_search(result, data):
    result.results = [DomainSearchResult.from_dict(obj) for obj in data.get('results', [])]


def parse_search_stream(result, data):
    result.results = [DomainSearchResult.from_dict(obj) for obj in data]
