"""
namecom: __init__.py

This package file exports data models and api classes
for interacting with name.com v4 api.

Tianhong Chu [https://github.com/CtheSky]
License: MIT
"""

from . import exceptions
from .auth import Auth
from . import result_models
from .data_models import (
    Contact,
    Contacts,
    DNSSEC,
    Domain,
    DomainSearchResult,
    EmailForwarding,
    Record,
    Transfer,
    URLForwarding,
    VanityNameserver
)
from .api import (
    DnsApi,
    DnssecApi,
    DomainApi,
    EmailForwardingApi,
    TransferApi,
    URLForwardingApi,
    VanityNameserverApi,
)
