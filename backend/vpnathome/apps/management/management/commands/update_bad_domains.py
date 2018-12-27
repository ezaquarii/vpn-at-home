from datetime import datetime

from django.contrib.auth import get_user_model

from vpnathome.apps.management.badhosts import get_domains_from_bad_hosts_file
from vpnathome.apps.management.models import BlockedDomain, BlockListUrl
from . import ManagementCommand


User = get_user_model()


class Command(ManagementCommand):

    def run(self, *args, **options):

        unique_domains = set()

        for item in BlockListUrl.objects.filter(enabled=True):
            url = item.url
            try:
                domains = get_domains_from_bad_hosts_file(url)
                unique_domains.update(domains)
                item.count = len(domains)
                item.save()
                self.log(f"Donwloaded {len(domains)} bad domains from {url}")
            except Exception as e:
                self.log(f"Skipping {url} due to error {e}")

        self.log(f"Got {len(unique_domains)} unique bad domains")

        BlockedDomain.objects.all().delete()
        blocked = [BlockedDomain(domain=domain) for domain in unique_domains]
        BlockedDomain.objects.bulk_create(objs=blocked)
