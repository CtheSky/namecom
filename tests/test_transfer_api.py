import unittest

from namecom import TransferApi
from sample import correct_auth

api = TransferApi(auth=correct_auth, use_test_env=True)

domainName = 'example.org'
authCode = 'Authc0de'
price = 10.99


class TransferApiTestCase(unittest.TestCase):

    @unittest.skip('should use correct auth code and price')
    def test_create_get_list_cancel_transfer(self):
        result = api.create_transfer(domainName=domainName, authCode=authCode, purchasePrice=price)
        self.assertIsNotNone(result.order)
        self.assertEqual(result.totalPaid, price)
        self.assertEqual(result.transfer.domainName, domainName)

        result = api.get_transfer(domainName)
        self.assertIsNotNone(result.transfer.domainName)
        self.assertIsNotNone(result.transfer.email)
        self.assertIsNotNone(result.transfer.status)

        result = api.list_transfers()
        self.assertIn(domainName, [_.domainName for _ in result.transfers])

        result = api.cancel_transfer(domainName)
        self.assertEqual(result.transfer.domainName, domainName)



