from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Permission
from django.urls import reverse

from vpnathome.tests import APITestWithBaseFixture

User = get_user_model()


class GetUser(APITestWithBaseFixture):

    url = reverse('accounts-api:user')

    def setUp(self):
        permission = Permission.objects.get(codename='download_server_config')
        self.test_user_admin.user_permissions.add(permission)
        self.test_user_alpha.user_permissions.add(permission)

    def test_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertUnauthorized(response)

    def test_superuser_permissions(self):
        response = self.admin_client.get(self.url)
        self.assertResponseOk(response)
        self.assertTrue('superuser' in response.data['permissions'])
        self.assertTrue('download_server_config' in response.data['permissions'])

    def test_normal_user_permissions(self):
        response = self.alpha_client.get(self.url)
        self.assertResponseOk(response)
        self.assertFalse('superuser' in response.data['permissions'])
        self.assertTrue('download_server_config' in response.data['permissions'])

    def test_user_email(self):
        response = self.alpha_client.get(self.url)
        self.assertResponseOk(response)
        self.assertEqual(self.test_user_alpha.email, response.data['email'])
