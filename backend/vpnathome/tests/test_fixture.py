from django.contrib.auth import get_user_model
from django.test import testcases

from . import APITestWithBaseFixture
from .fixture import FixtureBuilder, APITestCase, BaseFixtureMixin

User = get_user_model()


class TestFixtureBuilder(testcases.TestCase):

    ADMIN_EMAIL = 'admin@vpnathome.com'
    USER_EMAIL = 'user@vpnathome.com'

    def setUp(self):
        self.builder = FixtureBuilder()

    def test_create_admin(self):
        self.builder.admin(self.ADMIN_EMAIL)
        user = User.objects.get(email=self.ADMIN_EMAIL)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user(self):
        self.builder.user(self.USER_EMAIL)
        user = User.objects.get(email=self.USER_EMAIL)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_server_without_admin(self):
        with self.assertRaises(AssertionError):
            self.builder.server('name', 'host')

    def test_server_requires_dhparams(self):
        self.builder.admin(self.ADMIN_EMAIL)
        with self.assertRaises(AssertionError):
            self.builder.server('Server', 'hostname')

    def test_server(self):
        self.builder.admin(self.ADMIN_EMAIL)
        self.builder.dhparams()
        self.builder.server('Server', 'hostname')

    def test_client_requires_server(self):
        with self.assertRaises(AssertionError):
            self.builder.user(self.USER_EMAIL)
            self.builder.client('Client', self.USER_EMAIL)

    def test_client_requires_user(self):
        self.builder.admin(self.ADMIN_EMAIL)
        self.builder.dhparams()
        self.builder.server('Server', 'hostname')
        with self.assertRaises(AssertionError):
            self.builder.client('Client', 'nonexisting@user.com')

    def test_client_owned_by_admin(self):
        self.builder.admin(self.ADMIN_EMAIL)
        self.builder.dhparams()
        self.builder.server('Server', 'hostname')
        self.builder.client('Client', self.ADMIN_EMAIL)


class TestAPITestWithBaseFixture(APITestWithBaseFixture):

    def test_user_is_created(self):
        self.assertIsNotNone(self.test_user_admin)
        self.assertIsNotNone(self.test_user_alpha)
        self.assertIsNotNone(self.test_user_bravo)
        self.assertIsNotNone(self.test_user_charlie)

    def test_token_is_created(self):
        self.assertIsNotNone(self.test_user_admin_token)
        self.assertIsNotNone(self.test_user_alpha_token)
        self.assertIsNotNone(self.test_user_bravo_token)
        self.assertIsNotNone(self.test_user_charlie_token)
