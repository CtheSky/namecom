import unittest

from namecom import Transfer, Domain


class DataModelTestCase(unittest.TestCase):

    def test_repr_hash(self):
        transfer = Transfer(domainName='example.org', email='cthesky@yeah.net', status='Completed')
        repr_str = repr(transfer)

        got_transfer = eval(repr_str)
        self.assertEqual(transfer, got_transfer)
        self.assertEqual(hash(transfer), hash(got_transfer))
        self.assertFalse(transfer == 'transfer')
        self.assertTrue(transfer != 'transfer')

    def test_from_dict(self):
        result = Domain.from_dict(None)
        self.assertIsNone(result)

        transfer = Transfer(domainName='example.org', email='cthesky@yeah.net', status='Completed')
        got_transfer = Transfer.from_dict(dict(
            domainName='example.org',
            email='cthesky@yeah.net',
            status='Completed'
        ))
        self.assertEqual(transfer, got_transfer)