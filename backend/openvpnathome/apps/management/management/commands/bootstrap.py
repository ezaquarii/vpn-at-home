from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.validators import EmailValidator

from . import ManagementCommand
from openvpnathome.utils import user_input
from openvpnathome.apps.openvpn.models import DhParams
from openvpnathome.apps.openvpn.utils import generate_dhparams, generate_tls_auth_key

User = get_user_model()


class Command(ManagementCommand):

    DEFAULT_ADMIN_USER_EMAIL = 'admin@openvpnathome.net'
    DEFAULT_ADMIN_PASSWORD = 'admin123'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('-d', '--development', action='store_true', help="Bootstrap for development")
        parser.add_argument('-m', '--disable-migrations', action='store_true', help="Do not run DB migrations")
        parser.add_argument('-a', '--admin-user', help='Admin account email')
        parser.add_argument('-p', '--admin-password', help='Admin account password')

    @property
    def option_disable_migrations(self):
        return self.options.get('disable_migrations', False)

    @property
    def option_development(self):
        return self.options.get('development', False)

    @property
    def option_create_server(self):
        return self.options.get('create_server', False)

    @property
    def option_admin_email(self):
        return self.options.get('admin_user', None)

    @property
    def options_admin_password(self):
        return self.options.get('admin_password', None)

    def run(self, *args, **options):
        if not self.option_disable_migrations:
            call_command('migrate')
        self._create_admin()
        self._create_settings()

    def _call_configure(self):
        args = ['--no-warnings']
        if self.option_development:
            args.append('--development')
        call_command('configure', *args)

    def _create_admin(self):
        if User.objects.filter(is_superuser=True, is_staff=True).count() != 0:
            return

        if self.option_admin_email:
            email = self.option_admin_email
            self.log('Admin user e-mail: {email}', email=email)
        else:
            email = user_input('Enter admin user e-mail', validator=EmailValidator())

        if self.options_admin_password:
            password = self.options_admin_password
            self.log('Admin user password supplied.')
        else:
            password = user_input('Enter admin user password [8 chars min]', validator=lambda x: len(x) >= 8)

        admin_user = User.objects.create(email=email, is_staff=True, is_superuser=True)
        admin_user.set_password(password)
        admin_user.save()
        self.log('Created admin user {email}', email=email)

    def _create_settings(self):
        if DhParams.objects.count() == 0:
            DhParams.objects.create()
            self.log('Created DH params table')

        dhparams = DhParams.objects.first()

        if len(dhparams.dhparams) == 0:
            self.log('Generating DH params. This will take 1 minute or longer on slower machines. Patience is a virtue...')
            dhparams.dhparams = generate_dhparams()
            self.log('Generated DH params')

        dhparams.save()
