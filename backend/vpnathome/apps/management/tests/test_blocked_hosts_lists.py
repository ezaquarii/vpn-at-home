import random

from django.urls import reverse

from vpnathome.tests import APITestWithBaseFixture

from ..serializers import BlockListUrlSerializer
from ..models import BlockListUrl


class GetBlockedHostsLists(APITestWithBaseFixture):

    url = reverse('management-api:block_lists')

    def setUp(self):
        self.assertTrue(BlockListUrl.objects.exists(), "Blocked hosts lists should be loaded")

    def test_requires_authorization(self):
        response_anonymous = self.client.get(self.url)
        self.assertUnauthorized(response_anonymous, "API requires authorization")

    def test_requires_admin_permissions(self):
        response_normal_user = self.alpha_client.get(self.url)
        self.assertForbidden(response_normal_user, "Normal users should not have access to sources")

    def test_superuser_can_retrieve(self):
        response = self.admin_client.get(self.url)
        self.assertResponseOk(response)
        self.assertEquals(BlockListUrl.objects.count(), len(response.data), "Not all sources are retrieved")


class EnableHostsSource(APITestWithBaseFixture):

    url = reverse('management-api:block_lists')

    def setUp(self):
        self.serializer = BlockListUrlSerializer(instance=BlockListUrl.objects.all(), many=True)
        self.update_data = self.serializer.data
        for item in self.update_data:
            item['enabled'] = random.choice((True, False))

    def test_enable_and_disable_sources(self):
        response = self.admin_client.put(self.url, self.update_data)
        self.assertResponseOk(response)
        for reference_item in self.update_data:
            database_item = BlockListUrl.objects.get(id=reference_item['id'])
            self.assertEquals(reference_item['enabled'], database_item.enabled)
