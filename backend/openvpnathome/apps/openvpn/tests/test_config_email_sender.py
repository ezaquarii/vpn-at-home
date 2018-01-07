from django.conf import settings
from unittest.mock import MagicMock
from openvpnathome.apps.openvpn.models import Server, Client
from openvpnathome.apps.openvpn.utils import ConfigEmailSender
from openvpnathome.tests import configRequired, APITestWithBaseFixture

@configRequired(settings.EMAIL_ENABLED, 'This test sends e-mail and e-mail support must be enabled.')
@configRequired(settings.EMAIL_TO_ADMIN, 'This test sends e-mail and valid admin e-mail must be configured.')
class TestConfigEmailSender(APITestWithBaseFixture):

    TEST_USER_ADMIN = settings.EMAIL_TO_ADMIN

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.builder.server()
        cls.builder.client(name='Client', owner_email=cls.TEST_USER_ADMIN)

    def setUp(self):
        mock_settings = MagicMock()
        mock_settings.email_enabled = settings.EMAIL_ENABLED
        mock_settings.email_from = settings.EMAIL_TO_ADMIN
        mock_settings.email_smtp_server = settings.EMAIL_HOST
        mock_settings.email_smtp_port = settings.EMAIL_PORT
        mock_settings.email_smtp_login = settings.EMAIL_HOST_USER
        mock_settings.email_smtp_password = settings.EMAIL_HOST_PASSWORD
        self.sender = ConfigEmailSender(mock_settings)

    def test_send(self):
        client = self.fixture.clients[0]
        self.assertEqual(client.owner, self.test_user_admin)
        self.sender.send_client_config(client)
