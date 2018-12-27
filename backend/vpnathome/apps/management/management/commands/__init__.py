import sys

from django.core.management.base import BaseCommand
from django.db import transaction
from vpnathome.utils import is_database_migrated


class ManagementCommand(BaseCommand):
    """
    Base management command that implements some common boilerplate.

    You should re-implement run() method instead of handle(). Run method
    will run under db transaction, which guarantee that failed operation won't
    leave db in inconsistent state.
    """

    uses_db = True
    migrations_required = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = None

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('-q', '--quiet', action='store_true', help="Suppress diagnostic messages")
        parser.add_argument('--no-warnings', action='store_true', help="Suppress warnings")

    def handle(self, *args, **options):

        if self.migrations_required and not is_database_migrated():
            raise RuntimeError("Database is not migrated. Backup your database and run ./manage.py migrate first.")

        self.options = options

        if self.uses_db:
            with transaction.atomic():
                return self.run(*args, **options)
        else:
            return self.run(*args, **options)

    def run(self, *args, **options):
        raise NotImplementedError("run() is not implemented")

    @property
    def is_quiet(self):
        return self.options.get('quiet', False)

    def log(self, message, **kwargs):
        """
        Prints formatted message to stdout. It can be suppressed with -q option.
        """
        if self.options is not None and not self.options.get('quiet', False):
            lines = message.format(**kwargs).split('\n')
            print(lines[0], file=sys.stderr)
            for l in lines[1:]:
                print('  ' + l, file=sys.stderr)

    def warn(self, message, **kwargs):
        if not self.options.get('no_warnings', False):
            self.log(message, **kwargs)

