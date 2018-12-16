import sys
from django.core.management.base import BaseCommand
from vpnathome.apps.management import is_database_migrated


class Command(BaseCommand):

    help = "Checks if database is migrated. To be used in shell scripts. Returns 0 if DB is migrated, 1 otherwise."

    def handle(self, *args, **options):
        if is_database_migrated():
            sys.exit(0)
        else:
            sys.exit(1)
