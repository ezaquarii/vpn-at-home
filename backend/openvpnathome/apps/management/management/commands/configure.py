import json
from random import SystemRandom

from django.contrib.auth import get_user_model

from . import ManagementCommand

from openvpnathome import get_root_path
from openvpnathome.settings import UserSettings, DEFAULT_USER_SETTINGS
from openvpnathome.utils import get_object_or_none


User = get_user_model()


class Command(ManagementCommand):

    # important, as db is not available before generating config;
    # don't run command under db transaction
    uses_db = False

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('-d', '--development', action='store_true', help="Configure for development")
        parser.add_argument('-p', '--preview', action='store_true', help="Dump generated config to stdout, do not write.")
        parser.add_argument('-f', '--force', action='store_true', help="Force overwriting config if it already exists")
        parser.add_argument('-a', '--accept', action='store_true', help="Accept configuration (sets 'configured' flag to true)")

    @property
    def option_development(self):
        return self.options.get('development', False)

    @property
    def option_no_warnings(self):
        return self.options.get('development', False)

    @property
    def option_preview(self):
        return self.options.get('preview', False)

    @property
    def option_force(self):
        return self.options.get('force', False)

    @property
    def option_accept(self):
        return self.options.get('accept', False)

    def run(self, *args, **options):
        user_settings = UserSettings()
        if user_settings.has_settings_file and not self.option_preview and not self.option_force:
            self.warn('Config file already exist. Skipping.')
        else:
            admin = get_object_or_none(User, is_superuser=True)
            new_settings = DEFAULT_USER_SETTINGS.copy()
            new_settings['secret_key'] = self.create_secret_key()
            new_settings['development'] = self.option_development
            new_settings['email']['server_from'] = admin.email if admin is not None else ''
            new_settings['email']['admin_emails'] = [admin.email] if admin is not None else []
            new_settings['database'].update(**{
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': get_root_path('db/db.sqlite3'),
            })
            if self.option_development:
                new_settings['configured'] = True
                new_settings['debug_toolbar_enabled'] = True

            if self.option_accept:
                self.log('Automatically accepting default configuration.')
                new_settings['configured'] = True

            if self.option_preview:
                settings_json =json.dumps(new_settings, indent=4)
                print(settings_json)
            else:
                user_settings = UserSettings(settings=new_settings)
                user_settings.write()

            if self.option_development:
                self.log('Created configuration file {file} (development)'.format(file=user_settings.settings_file_path))
            else:
                self.log('Created configuration file {file}'.format(file=user_settings.settings_file_path))

    @staticmethod
    def create_secret_key():
        import string
        available_chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join([SystemRandom().choice(available_chars) for i in range(50)])
