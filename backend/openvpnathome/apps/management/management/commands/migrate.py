from django.contrib.auth import get_user_model

from django.core.management.commands import migrate
from openvpnathome.settings import USER_SETTINGS
from openvpnathome.tests import is_running_under_test
from openvpnathome import ensure_path_dirs


class Command(migrate.Command):

    not_configured_hint = "Application is not configured yet and I don't know how to connect to the database.\n" \
                          "You must run 'manage.py configure' and accept 'settings.json' file before proceeding."

    def handle(self, *args, **options):
        if self.check_configuration():
            self.ensure_database_dir()
            super().handle(*args, **options)

    def check_configuration(self):
        if is_running_under_test():
            print("Running 'migrate' under test - skipping configuration check.")
            return True
        elif not USER_SETTINGS.is_configured:
            print("Running 'migrate' without settings.json - aborting migration.")
            print("")
            print(self.not_configured_hint)
            return False
        else:
            return True

    @staticmethod
    def ensure_database_dir():
        db = USER_SETTINGS.database
        if 'sqlite3' in db['ENGINE'] and db['NAME'] != ':memory:':
            ensure_path_dirs(db['NAME'])
