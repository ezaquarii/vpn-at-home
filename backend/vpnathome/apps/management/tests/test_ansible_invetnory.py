from vpnathome.tests import APITestWithBaseFixture
from vpnathome.apps.management.models import BlockedDomain
from vpnathome.apps.management.management.commands.ansible_inventory import Command


class TestGetDomainsInventory(APITestWithBaseFixture):

    def setUp(self):
        domains = ['alpha.com', 'bravo.com', 'charlie.net', 'delta.net']
        BlockedDomain.objects.bulk_create([BlockedDomain(domain=domain) for domain in domains])
        self.assertEquals(len(domains), BlockedDomain.objects.count())

    def test_get_domains_inventory(self):
        domains = Command().get_blocked_domains()
        self.assertTrue(len(domains.keys()), 2)
        self.assertTrue('alpha.com' in domains['com'])
        self.assertTrue('bravo.com' in domains['com'])
        self.assertTrue('charlie.net' in domains['net'])
        self.assertTrue('delta.net' in domains['net'])
