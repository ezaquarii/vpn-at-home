from datetime import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model

from vpnathome.apps.management.badhosts import get_domains_from_bad_hosts_file
from vpnathome.apps.management.models import BlockedDomain, BlockListUrl
from . import ManagementCommand


User = get_user_model()


class Command(ManagementCommand):

    help = "Update DNS block list, fetching list of domains from enabled sources."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('-l', '--list', action='store_true', help='List all sources')
        parser.add_argument('sources', type=int, nargs='*', metavar='id', help="Enabled sources (ids)")

    def run(self, *args, **options):

        if options.get('list', False):
            return self._run_list()
        else:
            self._run_update(**options)

    @staticmethod
    def _run_list():
        lines = [f"id: {item.id}, enabled: {item.enabled}, url: {item.url}" for item in BlockListUrl.objects.all()]
        return "\n".join(lines)

    def _run_update(self, **options):
        sources = options['sources']
        if len(sources) > 0:
            BlockListUrl.objects.filter(id__in=sources).update(enabled=True)
            BlockListUrl.objects.exclude(id__in=sources).update(enabled=False, count=None, last_updated=None)

        unique_domains = set()
        timestamp = timezone.now()
        for item in BlockListUrl.objects.filter(enabled=True):
            url = item.url
            try:
                domains = self._download_bad_hosts(url)
                unique_domains.update(domains)
                item.enabled = True
                item.count = len(domains)
                item.last_updated = timestamp
                item.save()
                self.log(f"Downloaded {len(domains)} domains from {url}")
            except Exception as e:
                self.log(f"Skipping {url} due to error '{e}'")

        self.log(f"Got {len(unique_domains)} unique domains")

        BlockedDomain.objects.all().delete()
        blocked = [BlockedDomain(domain=domain) for domain in unique_domains]
        BlockedDomain.objects.bulk_create(objs=blocked)

    def _download_bad_hosts(self, url):
        return get_domains_from_bad_hosts_file(url)
