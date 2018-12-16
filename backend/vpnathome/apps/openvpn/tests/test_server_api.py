from ipaddress import IPv4Network

from django.urls import reverse

from rest_framework import status

from vpnathome.apps.openvpn.models import Server
from vpnathome.apps.x509.models import Ca, Cert
from vpnathome.tests import APITestWithBaseFixture

from ..serializers import CreateServerSerializer


class CreateServerPermissions(APITestWithBaseFixture):

    url = reverse('openvpn-api:servers')
    request_dto = {'name': 'Server Name', 'email': 'admin@domain.com', 'hostname': 'host.net'}

    def test_admin_user_can_access_api(self):
        response = self.admin_client.post(self.url, self.request_dto)
        self.assertStatus(response, status=status.HTTP_201_CREATED)

    def test_anonymous_user_cant_create_server(self):
        response = self.client.post(self.url, self.request_dto)
        self.assertUnauthorized(response)

    def test_normal_authenticated_cant_create_server(self):
        response = self.alpha_client.post(self.url, self.request_dto)
        self.assertForbidden(response)


class CreateServerFixture(object):
    url = reverse('openvpn-api:servers')
    name = 'Server Name'
    email = 'admin@email.com'
    hostname = 'localhost.localdomain.net'
    non_default_protocol = Server.PROTOCOL_TCP # non-default protocol
    non_default_network = IPv4Network('192.168.1.0/24')

    def create_request_dto(self, **kwargs):
        return {'name': self.name,
                'email': self.email,
                'hostname': self.hostname,
                'protocol': self.non_default_protocol,
                **kwargs}


class CreateServer(APITestWithBaseFixture, CreateServerFixture):

    def setUp(self):
        request_dto = self.create_request_dto()
        response = self.admin_client.post(self.url, request_dto)
        self.assertStatus(response, status.HTTP_201_CREATED)
        self.server = Server.objects.get(id=response.data['id'])

    def test_ca_is_created(self):
        Ca.objects.get(id=self.server.ca_id)

    def test_certs_is_created(self):
        Cert.objects.get(id=self.server.cert_id)

    def test_ca_name_is_derived_from_server_name(self):
        ca = self.server.ca
        self.assertTrue(self.server.name in ca.name)

    def test_cert_name_is_derived_from_server_name(self):
        cert = self.server.cert
        self.assertTrue(self.server.name in cert.name)

    def test_protocol_is_set_to_tcp(self):
        self.assertEquals(self.server.protocol, self.non_default_protocol)

    def test_default_network_is_set(self):
        self.assertEquals(self.server.network, Server.DEFAULT_NETWORK)

    def test_default_port_is_set(self):
        self.assertEqual(self.server.port, Server.DEFAULT_PORT)


class CreateServerWithNetwork(APITestWithBaseFixture, CreateServerFixture):

    def test_create_server_with_valid_network(self):
        request_dto = self.create_request_dto(network=str(self.non_default_network))
        response = self.admin_client.post(self.url, request_dto)
        self.assertStatus(response, status.HTTP_201_CREATED)
        server = Server.objects.get(id=response.data['id'])
        self.assertEquals(self.non_default_network, server.network)

    def test_create_server_with_invalid_network(self):
        for invalid_network in ['192.168.1.1/24', 'some random string', '01010101']:
            request_dto = self.create_request_dto(network=invalid_network)
            response = self.admin_client.post(self.url, request_dto)
            self.assertStatus(response, status.HTTP_400_BAD_REQUEST)

    def test_create_server_with_network_with_unsupported_netmask(self):
        invalid_network = '192.168.1.0/4'
        request_dto = self.create_request_dto(network=invalid_network)
        response = self.admin_client.post(self.url, request_dto)
        self.assertStatus(response, status.HTTP_400_BAD_REQUEST)


class CreateServerWithPort(APITestWithBaseFixture, CreateServerFixture):

    CUSTOM_PORT = 10000

    def test_create_server_with_cusom_port(self):
        request_dto = self.create_request_dto(port=self.CUSTOM_PORT)
        response = self.admin_client.post(self.url, request_dto)
        self.assertStatus(response, status.HTTP_201_CREATED)
        server = Server.objects.get(id=response.data['id'])
        self.assertEquals(server.port, self.CUSTOM_PORT)


class ListServers(APITestWithBaseFixture):

    url = reverse('openvpn-api:servers')
    servers = [
        {'name': 'Server 1', 'hostname': 'host1'},
        {'name': 'Server 2', 'hostname': 'host2'},
        {'name': 'Server 3', 'hostname': 'host3'}
    ]

    def setUp(self):
        context = {'owner': self.test_user_admin, 'dhparams': self.dhparams}
        serializer = CreateServerSerializer(data=self.servers, many=True, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(len(self.servers), Server.objects.count())

    def test_list_requires_authorization(self):
        response = self.client.get(self.url)
        self.assertUnauthorized(response)

    def test_admin_list_contains_download_url(self):
        response = self.admin_client.get(self.url)
        self.assertResponseOk(response)
        self.assertEqual(len(self.servers), len(response.data))
        for server in response.data:
            self.assertTrue(server['download_url'])

    def test_user_list_doesnt_contain_download_url(self):
        response = self.alpha_client.get(self.url)
        self.assertResponseOk(response)
        self.assertEqual(len(self.servers), len(response.data))
        for server in response.data:
            self.assertFalse('download_url' in server)
