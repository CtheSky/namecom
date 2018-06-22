# encoding=utf-8

import unittest

from namecom import DnsApi
from . import test_env_auth
from sample_data import (
    domain as domain_sample,
    record as record_sample)

api = DnsApi(domainName=domain_sample.domainName, auth=test_env_auth)


class DnsApiTestCase(unittest.TestCase):

    def test_get_record(self):
        get_record_result = api.get_record(record_sample.id)

        record = get_record_result.record
        self.assertDictEqual(record.__dict__, record_sample.__dict__)

    def test_list_records(self):
        list_records_result = api.list_records()

        records = list_records_result.records
        self.assertIn(record_sample, records)
