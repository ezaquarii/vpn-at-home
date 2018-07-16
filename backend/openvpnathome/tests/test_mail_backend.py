from unittest import mock, skipIf
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.utils import timezone

from openvpnathome.apps.management.models import Settings
from openvpnathome.mail import ConfigurableEmailBackend
from openvpnathome.tests import APITestWithBaseFixture, skip_if_email_not_configured


def create_default_mock_settings():
    from django.conf import settings
    backend_settings = mock.MagicMock()
    backend_settings.email_enabled = settings.EMAIL_ENABLED
    backend_settings.email_smtp_server = settings.EMAIL_HOST
    backend_settings.email_smtp_port = settings.EMAIL_PORT
    backend_settings.email_smtp_login = settings.EMAIL_HOST_USER
    backend_settings.email_smtp_password = settings.EMAIL_HOST_PASSWORD
    return backend_settings


def create_test_email(connection=None):

    email = EmailMessage(subject='OpenVPN@Home Test Email %s' % timezone.now(),
                         body='This is a test e-mail',
                         from_email=settings.SERVER_EMAIL,
                         to=settings.ADMINS,
                         connection=connection)
    return email


@skip_if_email_not_configured()
class TestBackendSendsEmail(APITestWithBaseFixture):

    def setUp(self):
        self.settings = create_default_mock_settings()
        self.connection = ConfigurableEmailBackend(settings=self.settings)

    def test_send_email(self):
        email = create_test_email(self.connection)
        count = email.send()
        self.assertEqual(1, count, 'Expected 1 message to be sent')

    def test_send_multiple_messages(self):
        self.connection.open()
        emails = [
            create_test_email(),
            create_test_email()
        ]
        count = self.connection.send_messages(emails)
        self.connection.close()
        self.assertEqual(len(emails), count)


@skip_if_email_not_configured()
class TestBackendCanBeDisabled(APITestWithBaseFixture):

    def setUp(self):
        self.settings = create_default_mock_settings()
        self.settings.email_enabled = False

    def test_backend_disabled(self):
        connection = ConfigurableEmailBackend(settings=self.settings)
        email = create_test_email(connection)
        count = email.send()
        self.assertIsNone(count, 'Backend should be disabled')


@skip_if_email_not_configured()
class TestBackendFallsBackToDjangoSettings(APITestWithBaseFixture):

    def setUp(self):
        self.settings = mock.MagicMock()
        self.settings.email_smtp_server = ''
        self.settings.email_smtp_port = 0
        self.settings.email_smtp_login = ''
        self.settings.email_smtp_password = ''
        self.connection = ConfigurableEmailBackend(settings=self.settings)

    def test_backend_falls_back_to_django_settings_when_settings_are_falsy(self):
        self.assertEqual(self.connection.host, settings.EMAIL_HOST)
        self.assertEqual(self.connection.port, settings.EMAIL_PORT)
        self.assertEqual(self.connection.username, settings.EMAIL_HOST_USER)
        self.assertEqual(self.connection.password, settings.EMAIL_HOST_PASSWORD)


@skip_if_email_not_configured()
class TestBackendReadsSettingsFromDb(APITestWithBaseFixture):

    def setUp(self):
        self.settings = Settings.instance()
        self.settings.email_smtp_server = 'testserver.com'
        self.settings.email_smtp_port = 999
        self.settings.email_smtp_login = 'test-login'
        self.settings.email_smtp_password = 'test-password'
        self.settings.save()
        self.connection = ConfigurableEmailBackend()

    def test_settings_from_database(self):
        self.assertEqual(self.connection.host,     self.settings.email_smtp_server)
        self.assertEqual(self.connection.port,     self.settings.email_smtp_port)
        self.assertEqual(self.connection.username, self.settings.email_smtp_login)
        self.assertEqual(self.connection.password, self.settings.email_smtp_password)
