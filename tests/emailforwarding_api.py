import unittest

from namecom import EmailForwardingApi
from sample_data import (
    correct_auth,
    dnssec_sample1,
    email_forwarding_sample1,
    email_forwarding_sample2,
    email_forwarding_sample3
)

api = EmailForwardingApi(domainName=dnssec_sample1.domainName, auth=correct_auth, use_test_env=True)


class EmailForwordingApiTestCase(unittest.TestCase):

    def test_list_dnssec(self):
        list_email_forwardings_result = api.list_email_forwardings()

        email_forwardings = list_email_forwardings_result.email_forwardings
        self.assertIn(email_forwarding_sample1, email_forwardings)

    def test_get_email_forwarding(self):
        get_email_forwarding_result = api.get_mail_forwarding(email_forwarding_sample1.emailBox)

        email_forwarding = get_email_forwarding_result.email_forwarding
        self.assertEqual(email_forwarding, email_forwarding_sample1)

    def test_create_update_delete_email_forwarding(self):
        create_result = api.create_email_forwarding(emailBox=email_forwarding_sample2.emailBox,
                                                    emailTo=email_forwarding_sample2.emailTo)
        email_forwarding = create_result.email_forwarding
        self.assertEqual(email_forwarding, email_forwarding_sample2)

        update_result = api.update_email_forwarding(emailBox=email_forwarding_sample3.emailBox,
                                                    emailTo=email_forwarding_sample3.emailTo)
        email_forwarding = update_result.email_forwarding
        self.assertEqual(email_forwarding, email_forwarding_sample3)

        delete_result = api.delete_email_forwarding(emailBox=email_forwarding_sample3.emailBox)
        self.assertEqual(delete_result.status_code, 200)






