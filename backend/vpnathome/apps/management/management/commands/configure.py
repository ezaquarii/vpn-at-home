import json
from random import SystemRandom

from django.contrib.auth import get_user_model
from django.db.utils import DatabaseError

from . import ManagementCommand

from vpnathome import get_data_path
from vpnathome.settings import UserSettings, DEFAULT_USER_SETTINGS
from vpnathome.apps.management.models import Settings
from vpnathome.utils import get_object_or_none


User = get_user_model()


class Command(ManagementCommand):

    help = 'Generate settings.json file with application settings. '\
           'Existing e-mail settings from db will be reused.'

    # important, as db is not available before generating config;
    # don't run command under db transaction
    uses_db = False
    migrations_required = False

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('-d', '--development', action='store_true', help="Configure for development")
        parser.add_argument('-p', '--preview', action='store_true', help="Dump generated config to stdout, do not write.")
        parser.add_argument('-f', '--force', action='store_true', help="Force overwriting config if it already exists")
        parser.add_argument('-a', '--accept', action='store_true', help="Accept configuration (sets 'configured' flag to true)")
        parser.add_argument('--no-smtp', action='store_true', help='Disable e-mail')
        parser.add_argument('--admin-email', type=str, help='Admin e-mail (used as server From too)')
        parser.add_argument('--smtp-server', type=str, help='SMTP server address')
        parser.add_argument('--smtp-port', type=str, help='SMTP server TLS port')
        parser.add_argument('--smtp-login', type=str, help='SMTP login')
        parser.add_argument('--smtp-password', type=str, help='SMTP password')

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

    @property
    def option_admin_email(self):
        return self.options.get('admin_email', None)

    @property
    def option_no_smtp(self):
        return self.options.get('no_smtp', False)

    @property
    def option_smtp_server(self):
        return self.options.get('smtp_server', None)

    @property
    def option_smtp_port(self):
        return self.options.get('smtp_port', 0)

    @property
    def option_smtp_login(self):
        return self.options.get('smtp_login', None)

    @property
    def option_smtp_password(self):
        return self.options.get('smtp_password', None)

    def run(self, *args, **options):
        user_settings = UserSettings()
        if user_settings.has_settings_file and not self.option_preview and not self.option_force:
            self.warn('Config file already exist. Skipping.')
        else:
            admin = get_object_or_none(User, is_superuser=True)
            new_settings = DEFAULT_USER_SETTINGS.copy()
            new_settings['secret_key'] = self.create_secret_key()
            new_settings['development'] = self.option_development
            new_settings['email']['enabled'] = not self.option_no_smtp
            new_settings['email']['server_from'] = admin.email if admin is not None else ''
            new_settings['email']['admin_emails'] = [admin.email] if admin is not None else []
            new_settings['database'].update(**{
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': get_data_path('db/db.sqlite3'),
            })

            existing_email_settings = self._get_existing_email_settings()
            new_settings['email'].update(existing_email_settings)

            options_email_settings = self._get_options_email_settings()
            new_settings['email'].update(options_email_settings)

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

    def _get_existing_email_settings(self):
        try:
            db_settings = Settings.instance()
            from django.conf import settings as django_settings
            email = {
                'enabled': db_settings.email_enabled,
                'server_email': django_settings.SERVER_EMAIL,
                'admin_emails': django_settings.ADMINS,
                'smtp': {
                    'server': db_settings.email_smtp_server,
                    'port': db_settings.email_smtp_port,
                    'login': db_settings.email_smtp_login,
                    'password': db_settings.email_smtp_password
                }
            }
            return email
        except DatabaseError:
            return {}

    def _get_options_email_settings(self):
        smtp = {}
        if self.option_smtp_server:
            smtp['server'] = self.option_smtp_server

        if self.option_smtp_server:
            smtp['port'] = self.option_smtp_port

        if self.option_smtp_server:
            smtp['login'] = self.option_smtp_login

        if self.option_smtp_server:
            smtp['password'] = self.option_smtp_password

        django_email_settings = {}
        if self.option_admin_email:
            django_email_settings['server_from'] = self.option_admin_email
            django_email_settings['admin_emails'] = [self.option_admin_email]

        email = {}
        if django_email_settings:
            email.update(django_email_settings)
        if smtp:
            email['smtp'] = smtp
        return email
