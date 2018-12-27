import json
from unittest import mock

from vpnathome.tests import APITestWithBaseFixture
from vpnathome.apps.management.models import BlockListUrl, BlockedDomain
from vpnathome.apps.management.management.commands.update_block_list import Command


class TestBlockListUpdate(APITestWithBaseFixture):

    @staticmethod
    def mock_download_bad_hosts(url):
        return ['1.bad.domain.com', '2.bad.domain.com']

    def setUp(self):
        BlockListUrl.objects.update(enabled=False)
        self.assertEquals(0, BlockedDomain.objects.count(), "No blocked domains should be present in DB during this test.")
        self.assertEquals(0, BlockListUrl.objects.filter(enabled=True).count(), "All block lists must be disabled")
        self.bad_hosts = ['1.bad.host.com', '2.bad.host.com', '3.bad.host.com']
        self.command = Command()
        self.command._download_bad_hosts = mock.MagicMock(return_value=self.bad_hosts)

    def test_list(self):
        result = self.command._run_list()
        lines = result.split('\n')
        self.assertEquals(BlockListUrl.objects.count(), len(lines), "Expected all items to be printed out")

    def test_update(self):
        BlockListUrl.objects.update(enabled=False)
        all_ids = {item.id for item in BlockListUrl.objects.all()}
        self.command._run_update(sources=all_ids)
        enabled_ids = {item.id for item in BlockListUrl.objects.filter(enabled=True)}
        self.assertEquals(all_ids, enabled_ids)
        self.assertEquals(len(self.bad_hosts), BlockedDomain.objects.count())

    def test_update_from_non_existing_sources(self):
        non_existing_id = 10000
        self.assertEquals(0, BlockListUrl.objects.filter(id=non_existing_id).count(), "Choose a non-existing ID")
        self.command._run_update(sources=[non_existing_id])
        self.assertEquals(0, BlockListUrl.objects.filter(enabled=True).count(), "Nothing should be enabled")
        self.assertEquals(0, BlockedDomain.objects.count(), "No domains should be retrieved")
