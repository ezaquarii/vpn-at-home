from django.contrib.auth import get_user_model
from django.urls import reverse

from vpnathome.tests import APITestWithBaseFixture

from ..models import Settings


class GetSettings(APITestWithBaseFixture):

    url = reverse('management-api:settings')

    def setUp(self):
        self.assertTrue(Settings.objects.exists(), "Settings entry must exist")
        self.settings = Settings.objects.first()
        self.update = {'email_enabled': not self.settings.email_enabled}

    def test_requires_authorization(self):
        response_anonymous = self.client.get(self.url)
        self.assertUnauthorized(response_anonymous)

        response_normal_user = self.alpha_client.get(self.url)
        self.assertForbidden(response_normal_user)

    def test_superuser_can_retrieve(self):
        response = self.admin_client.get(self.url)
        self.assertResponseOk(response)

    def test_superuser_can_set(self):
        response = self.admin_client.put(self.url, self.update)
        self.assertResponseOk(response)
        self.assertNotEqual(self.settings.email_enabled, response.data['email_enabled'])

    def test_user_cannot_set(self):
        response = self.alpha_client.put(self.url, self.update)
        self.assertForbidden(response)

    def test_user_cannot_update(self):
        response = self.alpha_client.patch(self.url, self.update)
        self.assertForbidden(response)
