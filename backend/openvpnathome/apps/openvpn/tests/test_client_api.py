from django.urls import reverse

from rest_framework import status

from openvpnathome.apps.openvpn.models import Client
from openvpnathome.tests import APITestWithBaseFixture


class Fixture(APITestWithBaseFixture):

    servers_url = reverse('openvpn-api:servers')
    clients_url = reverse('openvpn-api:clients')

    def setUp(self):
        super().setUp()
        response = self.admin_client.post(self.servers_url, dict(name='Server', email='admin@emial.com', hostname='hostname'))
        self.assertStatus(response, status.HTTP_201_CREATED)


class CreateClientPermissions(Fixture):

    create_client_dto = dict(name='A Client')

    def test_create_client_requires_authentication(self):
        response = self.client.post(self.clients_url, self.create_client_dto)
        self.assertUnauthorized(response)

    def test_create_client(self):
        response = self.alpha_client.post(self.clients_url, self.create_client_dto)
        self.assertStatus(response, status.HTTP_201_CREATED)


class CreateClient(Fixture):

    create_client_dto_1 = dict(name='Client 1')
    create_client_dto_2 = dict(name='Client 2')

    def setUp(self):
        super().setUp()
        response_1 = self.alpha_client.post(self.clients_url, self.create_client_dto_1)
        self.assertResponseOk(response_1)
        self.client_1 = Client.objects.get(id=response_1.data['id'])

        response_2 = self.alpha_client.post(self.clients_url, self.create_client_dto_2)
        self.assertResponseOk(response_2)
        self.client_2 = Client.objects.get(id=response_2.data['id'])

    def test_created_client_has_proper_ower(self):
        self.assertEqual(self.client_1.owner, self.test_user_alpha)
        self.assertEqual(self.client_2.owner, self.test_user_alpha)

    def test_created_client_has_proper_name(self):
        self.assertEqual(self.client_1.name, self.create_client_dto_1['name'])
        self.assertEqual(self.client_2.name, self.create_client_dto_2['name'])


class ListClients(Fixture):

    def setUp(self):
        super().setUp()
        self.alpha_clients = []
        self.bravo_clients = []
        for index in range(1, 10):
            create_alpha_client_dto = dict(name='Alpha Client {index}'.format(index=index))
            alpha_response = self.alpha_client.post(self.clients_url, create_alpha_client_dto)
            self.assertResponseOk(alpha_response)
            alpha_client = Client.objects.get(id=alpha_response.data['id'])
            self.alpha_clients.append(alpha_client)

            create_bravo_client_dto = dict(name='Bravo Client {index}'.format(index=index))
            bravo_response = self.bravo_client.post(self.clients_url, create_bravo_client_dto)
            self.assertResponseOk(bravo_response)
            bravo_client = Client.objects.get(id=bravo_response.data['id'])
            self.bravo_clients.append(bravo_client)

    def test_list_requires_authentication(self):
        response = self.client.get(self.clients_url)
        self.assertUnauthorized(response)

    def test_list_contains_only_owned_clients(self):
        response = self.alpha_client.get(self.clients_url)
        self.assertResponseOk(response)
        ids = [item['id'] for item in response.data]
        clients = Client.objects.filter(id__in=ids)
        self.assertEqual(clients.count(), len(self.alpha_clients))
        for client in clients:
            self.assertTrue(client.name.startswith('Alpha'))
            self.assertEqual(client.owner, self.test_user_alpha)
