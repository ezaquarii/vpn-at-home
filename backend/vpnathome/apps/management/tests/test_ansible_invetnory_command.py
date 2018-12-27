import json

from vpnathome.tests import APITestWithBaseFixture
from vpnathome.apps.management.models import BlockedDomain
from vpnathome.apps.management.management.commands.ansible_inventory import Command
from vpnathome.apps.openvpn.models import Server


class TestGetBlockedDomainsInventory(APITestWithBaseFixture):

    def setUp(self):
        domains = ['alpha.com', 'bravo.com', 'charlie.net', 'delta.net']
        BlockedDomain.objects.bulk_create([BlockedDomain(domain=domain) for domain in domains])
        self.assertEquals(len(domains), BlockedDomain.objects.count())

    def test_get_blocked_domains_variable(self):
        domains = Command.get_blocked_domains()
        self.assertTrue(len(domains.keys()), 2)
        self.assertTrue('alpha.com' in domains['com'])
        self.assertTrue('bravo.com' in domains['com'])
        self.assertTrue('charlie.net' in domains['net'])
        self.assertTrue('delta.net' in domains['net'])


class TestGenerateInventory(APITestWithBaseFixture):

    def setUp(self):
        super().setUp()
        self.vpn_nodes = [
            dict(name='alpha', hostname='vpn.alpha.net', deploy_dns=True),
            dict(name='bravo', hostname='vpn.bravo.net', deploy_dns=False)
        ]
        for vpn in self.vpn_nodes:
            self.builder.server(vpn['name'], vpn['hostname'], vpn['deploy_dns'])
        self.assertEquals(len(self.vpn_nodes), Server.objects.count())

        self.dns_blocked_domains = [
            'domain1.com',
            'domain2.com',
            'domain3.net',
            'domain4.net'
        ]
        for domain in self.dns_blocked_domains:
            self.builder.dns_blocked_domain(domain=domain)
        self.assertEquals(len(self.dns_blocked_domains), BlockedDomain.objects.count())

    def test_list_hosts(self):
        inventory_str = Command().run_list()
        inventory = json.loads(inventory_str)
        for expected in self.vpn_nodes:
            self.assertTrue(expected['hostname'] in inventory['vpns']['hosts'])
        self.assertEquals(inventory['vpns']['vars'], {}, "Variables should be empty in list ")
        self.assertEquals(inventory['vpns']['children'], [], "Children should be empty in list mode")

    def test_list_hosts_for_local_inventory(self):
        inventory_str = Command().run_list(local=True)
        inventory = json.loads(inventory_str)
        self.assertEquals(inventory['vpns']['hosts'], ['localhost'])

    def test_inventory_for_nonexisting_host(self):
        inventory = json.loads(Command().run_host(hostname=None))
        self.assertEquals(inventory, {})

    def test_inventory_for_localhost(self):
        server = Server.objects.first()
        for localhost in ['localhost', 'localhost.localdomain', '127.0.0.1']:
            inventory = json.loads(Command().run_host(hostname=localhost))
            self.assertEquals(inventory['vpn_name'], server.name)

    def test_inventory_for_hostname(self):
        servers = Server.objects.all()
        for server in servers:
            inventory = json.loads(Command().run_host(hostname=server.hostname))
            self.assertEquals(inventory['ansible_user'], 'root')
            self.assertEquals(inventory['vpn_name'], server.name)
            self.assertEquals(inventory['vpn_port'], server.port)
            if server.deploy_dns:
                self.assertEquals(2, len(inventory['blocked_domains']['com']))
                self.assertEquals(2, len(inventory['blocked_domains']['net']))
            else:
                self.assertEquals(inventory['blocked_domains'], {})
