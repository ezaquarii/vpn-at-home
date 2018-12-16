from ipaddress import IPv4Network

from rest_framework import exceptions

from vpnathome.tests import APITestWithBaseFixture

from ..models import Server
from ..serializers import ServerSerializer, CreateServerSerializer


class TestServerSerializer(APITestWithBaseFixture):

    @classmethod
    def setUpClass(cls):
        super(TestServerSerializer, cls).setUpClass()
        cls.builder.server()

    def setUp(self):
        super().setUp()
        self.assertEqual(1, Server.objects.count())
        self.server = Server.objects.first()
        self.server_data = ServerSerializer(instance=self.server).data

    def test_serialize_network(self):
        """Test custom fields serialization only"""
        self.assertTrue('network' in self.server_data)
        network = IPv4Network(self.server_data.get('network'))
        self.assertEqual(network, self.server.network)

    def test_serialization_update_network(self):
        new_network = IPv4Network('192.168.1.0/24')
        self.assertNotEqual(new_network, self.server.network)
        new_server_data = {'network': str(new_network)}
        serializer = ServerSerializer(instance=self.server, data=new_server_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        updated_server = Server.objects.get(id=self.server.id)
        self.assertEqual(new_network, updated_server.network)


class TestCreateServerSerializer(APITestWithBaseFixture):

    NON_DEFAULT_NETWORK = IPv4Network('192.168.1.0/24')

    def setUp(self):
        super().setUp()
        self.context = {
            'owner': self.test_user_admin,
            'dhparams': self.dhparams
        }
        self.assertNotEquals(self.NON_DEFAULT_NETWORK, Server.DEFAULT_NETWORK)

    def test_create_server_with_custom_network(self):
        dto = {
            'name': 'Server Name',
            'hostname': 'test.hostname',
            'protocol': 'tcp',
            'network': self.NON_DEFAULT_NETWORK
        }
        serializer = CreateServerSerializer(data=dto, context=self.context)
        serializer.is_valid(raise_exception=True)
        server = serializer.save()
        self.assertEquals(self.context['owner'], server.owner)
        self.assertEquals(dto['name'], server.name)
        self.assertEquals(dto['hostname'], server.hostname)
        self.assertEquals(self.context['owner'].email, server.email)
        self.assertEquals(dto['protocol'], server.protocol)
        self.assertEquals(dto['network'], server.network)

    def test_create_server_with_default_network(self):
        dto = {
            'name': 'Server Name',
            'hostname': 'test.hostname',
        }
        serializer = CreateServerSerializer(data=dto, context=self.context)
        serializer.is_valid(raise_exception=True)
        server = serializer.save()
        self.assertEquals(self.context['owner'], server.owner)
        self.assertEquals(dto['name'], server.name)
        self.assertEquals(dto['hostname'], server.hostname)
        self.assertEquals(self.context['owner'].email, server.email)
        self.assertEquals(Server.DEFAULT_PROTOCOL, server.protocol)
        self.assertEquals(Server.DEFAULT_NETWORK, server.network)

    def test_create_server_with_invalid_network(self):
        dto = {
            'name': 'Server Name',
            'hostname': 'test.hostname',
            'network': '172.17.0.1/16'
        }
        serializer = CreateServerSerializer(data=dto, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('network' in serializer.errors)
