import unittest

from namecom import DnsApi
from . import test_env_auth
from sample_data import (
    domain_sample1 as domain_sample,
    record_sample1 as record_sample
)

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

    def test_create_update_delete_records(self):
        create_domain_result = api.create_record(host='dummy', type='A', answer='10.0.0.1')
        record = create_domain_result.record
        self.assertEqual(record.host, 'dummy')
        self.assertEqual(record.type, 'A')
        self.assertEqual(record.answer, '10.0.0.1')

        update_domain_result = api.update_record(id=record.id, answer='10.0.0.2')
        record = update_domain_result.record
        self.assertEqual(record.host, 'dummy')
        self.assertEqual(record.type, 'A')
        self.assertEqual(record.answer, '10.0.0.2')

        delete_domain_result = api.delete_record(id=record.id)
        self.assertEqual(delete_domain_result.status_code, 200)
