from vpnathome.tests import APITestWithBaseFixture, TestCase
from django.core.exceptions import ValidationError
from ipaddress import IPv4Network
from ..models import Server, filter_empty_config_lines


class TestServerModelNetwork(APITestWithBaseFixture):

    @classmethod
    def setUpClass(cls):
        super(TestServerModelNetwork, cls).setUpClass()
        cls.builder.server()

    def setUp(self):
        super().setUp()
        self.assertEqual(1, Server.objects.count())
        self.server = Server.objects.first()

    def test_default_network_is_set(self):
        self.assertEquals(type(self.server.network), IPv4Network)

    def test_cant_save_invalid_network(self):
        with self.assertRaises(ValidationError):
            self.server.network = '172.17.0.1/16'
            self.server.save()

    def test_cant_save_network_with_unsupported_netmask(self):
        with self.assertRaises(ValidationError):
            self.server.network = '172.17.0.0/22'
            self.server.save()

        with self.assertRaises(ValidationError):
            self.server.network = '172.17.0.1'
            self.server.save()

    def test_8_16_24_bit_netmasks_are_supported(self):
        for netmask in ['8', '16', '24']:
            self.server.network = '10.0.0.0/{netmask}'.format(netmask=netmask)
            self.server.save()


class TestServerModelConfigRender(APITestWithBaseFixture):

    CUSTOM_PORT = 10000

    @classmethod
    def setUpClass(cls):
        super(TestServerModelConfigRender, cls).setUpClass()
        cls.builder.server()

    def assertEntryPresent(self, entry):
        self.assertTrue(entry in self.config, 'Entry [{entry}] not found'.format(entry=entry))

    def setUp(self):
        self.server = Server.objects.first()
        self.server.port = self.CUSTOM_PORT
        self.config = self.server.render_to_string()

    def test_config_contains_server_network_entry(self):
        entry = 'server {network} {netmask}'.format(network=self.server.network.network_address,
                                                     netmask=self.server.network.netmask)
        self.assertEntryPresent(entry)

    def test_config_contains_port_entry(self):
        entry = 'port {}'.format(self.CUSTOM_PORT)
        self.assertEntryPresent(entry)


class TestFilterEmptyConfigLines(TestCase):

    input = "# commented line\n" \
            "valid option 1\n"\
            "; commented option\n"\
            "    \n"\
            "valid option 2\n"

    def test_comments_filtered_out(self):
        output = filter_empty_config_lines(self.input)
        expected =  "valid option 1\nvalid option 2\n"
        self.assertEquals(expected, output)

    def test_filter_handles_none(self):
        output = filter_empty_config_lines(None)
        self.assertIsNone(output)

    def test_filter_handles_empty_string(self):
        output = filter_empty_config_lines('')
        self.assertEquals('', output)
