# encoding=utf-8

from .models import *


def parse_list_domains(result, response):
    data = response.json()

    result.domains = [Domain(**domain_data) for domain_data in data.get('domains', [])]
    result.nextPage = data.get('nextPage', 0)
    result.lastPage = data.get('lastPage', 0)


def parse_get_domain(result, response):
    data = response.json()

    result.domain = data.get('contacts')
    result.domain = data


def parse_search(result, response):
    data = response.json()

    result.results = [DomainSearchResult(**obj) for obj in data.get('results', [])]
