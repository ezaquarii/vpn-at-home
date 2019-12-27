from django.test.utils import override_settings
from django.urls import reverse

from dateutil.relativedelta import relativedelta
from datetime import datetime
from rest_framework import status

from vpnathome.apps.management.models import Settings
from vpnathome.apps.openvpn.models import Client, Server
from vpnathome.tests import APITestWithBaseFixture, skip_if_email_not_configured


class Fixture(APITestWithBaseFixture):
    """
    Fixture with created server.
    """

    servers_url = reverse('openvpn-api:servers')
    clients_url = reverse('openvpn-api:clients')

    def setUp(self):
        super().setUp()
        alpha_response = self.admin_client.post(self.servers_url, dict(name='Alpha Server', email='admin@email.com', hostname='alpha_hostname'))
        self.assertStatus(alpha_response, status.HTTP_201_CREATED)
        bravo_response = self.admin_client.post(self.servers_url, dict(name='Bravo Server', email='admin@email.com', hostname='bravo_hostname'))
        self.assertStatus(bravo_response, status.HTTP_201_CREATED)
        self.alpha_server = Server.objects.get(pk=alpha_response.data['id'])
        self.bravo_server = Server.objects.get(pk=bravo_response.data['id'])
        self.alpha_server_clients_url = reverse('openvpn-api:server-clients', kwargs={'server_id': self.alpha_server.pk})
        self.bravo_server_clients_url = reverse('openvpn-api:server-clients', kwargs={'server_id': self.bravo_server.pk})


class CreateClientPermissions(Fixture):

    create_client_dto = dict(name='A Client')

    def test_create_client_requires_authentication(self):
        response = self.client.post(self.alpha_server_clients_url, self.create_client_dto)
        self.assertUnauthorized(response)

    def test_create_client(self):
        response = self.alpha_client.post(self.alpha_server_clients_url, self.create_client_dto)
        self.assertStatus(response, status.HTTP_201_CREATED)


class CreateClient(Fixture):

    create_client_dto_1 = dict(name='Client 1', validity_time=7, validity_time_unit='days')
    create_client_dto_2 = dict(name='Client 2', validity_time=7, validity_time_unit='years')

    def setUp(self):
        super().setUp()
        response_1 = self.alpha_client.post(self.alpha_server_clients_url, self.create_client_dto_1)
        self.assertResponseOk(response_1)
        self.client_1 = Client.objects.get(id=response_1.data['id'])

        response_2 = self.alpha_client.post(self.alpha_server_clients_url, self.create_client_dto_2)
        self.assertResponseOk(response_2)
        self.client_2 = Client.objects.get(id=response_2.data['id'])

    def test_created_client_has_proper_ower(self):
        self.assertEqual(self.client_1.owner, self.test_user_alpha)
        self.assertEqual(self.client_2.owner, self.test_user_alpha)

    def test_created_client_has_proper_name(self):
        self.assertEqual(self.client_1.name, self.create_client_dto_1['name'])
        self.assertEqual(self.client_2.name, self.create_client_dto_2['name'])

    def test_created_client_with_valididty_time(self):
        self.assertEqual(self.client_1.name, self.create_client_dto_1['name'])
        self.assertEqual(self.client_2.name, self.create_client_dto_2['name'])

    def test_created_with_custom_validity_end(self):
        end = self.client_1.cert.validity_end
        start = self.client_1.cert.validity_start
        delta = end - start
        self.assertTrue(delta.days >= 7)
        self.assertTrue(delta.days <= 8)

        end = self.client_2.cert.validity_end
        start = self.client_2.cert.validity_start
        delta = end - start
        self.assertTrue(delta.days >= 7 * 365)

    def test_cannot_create_client_without_server(self):
        Server.objects.all().delete()
        self.assertEquals(0, Server.objects.count())
        response = self.alpha_client.post(self.alpha_server_clients_url, self.create_client_dto_1)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)


class ListClients(Fixture):

    def setUp(self):
        super().setUp()
        self.alpha_clients = []
        self.bravo_clients = []
        for index in range(1, 10):
            create_alpha_client_dto = dict(name='Alpha Client {index}'.format(index=index))
            alpha_response = self.alpha_client.post(self.alpha_server_clients_url, create_alpha_client_dto)
            self.assertResponseOk(alpha_response)
            alpha_client = Client.objects.get(id=alpha_response.data['id'])
            self.alpha_clients.append(alpha_client)

            create_bravo_client_dto = dict(name='Bravo Client {index}'.format(index=index))
            bravo_response = self.bravo_client.post(self.bravo_server_clients_url, create_bravo_client_dto)
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


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend', SERVER_EMAIL='server@email.com')
class SendClientConfig(Fixture):

    create_client_dto = dict(name='A Client')

    def setUp(self):
        super().setUp()
        settings = Settings.instance()
        settings.email_enabled = True
        settings.save()
        response = self.alpha_client.post(self.alpha_server_clients_url, self.create_client_dto)
        self.assertStatus(response, status.HTTP_201_CREATED)
        self.send_config_url = reverse('openvpn-api:send-client-config', kwargs={'id': response.data['id']})

    def test_send_owned_client_config(self):
        from django.core.mail import outbox
        self.assertFalse(outbox)
        response = self.alpha_client.post(self.send_config_url)
        self.assertResponseOk(response)
        self.assertEquals(1, len(outbox))
        message = outbox[0]
        self.assertEquals(1, len(message.attachments))

    def test_sending_client_config_requires_ownership(self):
        from django.core.mail import outbox
        self.assertFalse(outbox)
        response = self.bravo_client.post(self.send_config_url)
        self.assertNotFound(response)

    def test_admin_can_send_config_owner_by_other_users(self):
        from django.core.mail import outbox
        self.assertFalse(outbox)
        response = self.admin_client.post(self.send_config_url)
        self.assertResponseOk(response)
        self.assertEquals(1, len(outbox))

    def test_email_is_disabled(self):
        settings = Settings.instance()
        settings.email_enabled = False
        settings.save()
        from django.core.mail import outbox
        self.assertFalse(outbox)
        response = self.alpha_client.post(self.send_config_url)
        self.assertResponseOk(response)
        self.assertFalse(outbox)