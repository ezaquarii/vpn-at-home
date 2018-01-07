from unittest import mock, skipIf
from django.core.mail import EmailMessage
from django.conf import settings
from openvpnathome.tests import APITestWithBaseFixture

from ..mail import EmailSender

@skipIf(not settings.EMAIL_ENABLED, "This test require private email configuration. Provide settings.private and re-run test.")
class TestEmailSender(APITestWithBaseFixture):

    def setUp(self):
        self.settings = mock.MagicMock()
        self.settings.email_enabled = settings.EMAIL_ENABLED
        self.settings.email_from = settings.EMAIL_FROM
        self.settings.email_smtp_server = settings.EMAIL_HOST
        self.settings.email_smtp_port = settings.EMAIL_PORT
        self.settings.email_smtp_login = settings.EMAIL_HOST_USER
        self.settings.email_smtp_password = settings.EMAIL_HOST_PASSWORD

        self.sender = EmailSender(self.settings)
        self.message = EmailMessage(to=['hello@ezaquarii.com'],
                                    subject='Test subject',
                                    body='Test body')

    def test_send_email(self):
        self.assertTrue(self.sender.send(self.message), 'Email should be enabled')
        self.assertIsNotNone(self.message.connection, 'Backend connection should be set by sender')
        self.assertEqual(self.message.from_email, self.settings.email_from, 'From email should be set by sender')

    def test_email_is_disabled(self):
        self.settings.email_enabled = False
        self.assertFalse(self.sender.send(self.message), 'Email should be disabled')
