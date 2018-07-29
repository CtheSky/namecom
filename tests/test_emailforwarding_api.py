import unittest

from namecom import EmailForwardingApi
from .sample import (
    correct_auth,
    dnssec_sample1,
    email_forwarding_sample1 as sample1,
    email_forwarding_sample2 as sample2,
    email_forwarding_sample3 as sample3
)

api = EmailForwardingApi(domainName=dnssec_sample1.domainName, auth=correct_auth, use_test_env=True)


class EmailForwordingApiTestCase(unittest.TestCase):

    def test_list_email_forwardins(self):
        result = api.list_email_forwardings()

        email_forwardings = result.email_forwardings
        self.assertIn(sample1, email_forwardings)

    def test_get_email_forwarding(self):
        result = api.get_mail_forwarding(sample1.emailBox)

        email_forwarding = result.email_forwarding
        self.assertEqual(email_forwarding, sample1)

    def test_create_update_delete_email_forwarding(self):
        result = api.create_email_forwarding(emailBox=sample2.emailBox, emailTo=sample2.emailTo)
        email_forwarding = result.email_forwarding
        self.assertEqual(email_forwarding, sample2)

        result = api.update_email_forwarding(emailBox=sample3.emailBox,
                                                    emailTo=sample3.emailTo)
        email_forwarding = result.email_forwarding
        self.assertEqual(email_forwarding, sample3)

        result = api.delete_email_forwarding(emailBox=sample3.emailBox)
        self.assertEqual(result.status_code, 200)






