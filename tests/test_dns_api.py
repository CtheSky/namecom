import unittest

from namecom import DnsApi, exceptions
from .sample import (
    correct_auth,
    record_sample1 as sample
)

api = DnsApi(domainName=sample.domainName, auth=correct_auth, use_test_env=True)


class DnsApiTestCase(unittest.TestCase):

    def test_get_record(self):
        result = api.get_record(sample.id)

        record = result.record
        self.assertDictEqual(record.__dict__, sample.__dict__)

    def test_list_records(self):
        result = api.list_records()

        records = result.records
        self.assertIn(sample, records)

    def test_create_update_delete_records(self):
        result = api.create_record(host='dummy', type='A', answer='10.0.0.1')

        record = result.record
        self.assertEqual(record.host, 'dummy')
        self.assertEqual(record.type, 'A')
        self.assertEqual(record.answer, '10.0.0.1')

        result = api.update_record(id=record.id, answer='10.0.0.2')

        record = result.record
        self.assertEqual(record.host, 'dummy')
        self.assertEqual(record.type, 'A')
        self.assertEqual(record.answer, '10.0.0.2')

        result = api.delete_record(id=record.id)
        self.assertEqual(result.status_code, 200)
