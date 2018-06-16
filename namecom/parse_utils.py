# encoding=utf-8

from .models import *


def parse_list_domains(result, data):
    result.domains = [Domain.from_json(obj) for obj in data.get('domains', [])]
    result.nextPage = data.get('nextPage', 0)
    result.lastPage = data.get('lastPage', 0)


def parse_get_domain(result, data):
    result.domain = Domain.from_json(data)


def parse_create_domain(result, data):
    result.domain = Domain.from_json(data.get('domain'))
    result.order = data.get('order')
    result.totalPaid = data.get('totalPaid')


def parse_enable_autorenew(result, data):
    result.domain = Domain.from_json(data)


def parse_disable_autorenew(result, data):
    result.domain = Domain.from_json(data)


def parse_set_nameservers(result, data):
    result.domain = Domain.from_json(data)


def parse_get_authcode(result, data):
    result.authCode = data.get('authCode')


def parse_lock_domain(result, data):
    result.domain = Domain.from_json(data)


def parse_unlock_domain(result, data):
    result.domain = Domain.from_json(data)


def parse_check_availability(result, data):
    result.results = [DomainSearchResult.from_json(obj) for obj in data.get('results', [])]


def parse_search(result, data):
    result.results = [DomainSearchResult.from_json(obj) for obj in data.get('results', [])]


def parse_search_stream(result, data):
    result.results = [DomainSearchResult.from_json(obj) for obj in data]
