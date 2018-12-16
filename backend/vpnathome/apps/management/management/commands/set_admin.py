from django.contrib.auth import get_user_model

from vpnathome.apps.management import is_database_migrated
from . import ManagementCommand


User = get_user_model()


class Command(ManagementCommand):

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("admin_email", help="Admin user e-mail")
        parser.add_argument("admin_password", help="Admin user password")
        parser.add_argument('-f', '--first-name', help="Admin first name")
        parser.add_argument('-l', '--last-name', help="Admin last name")

    @property
    def option_admin_email(self):
        return self.options.get('admin_email')

    @property
    def option_admin_password(self):
        return self.options.get('admin_password')

    @property
    def option_admin_first_name(self):
        return self.options.get('admin_first_name', None)

    @property
    def option_admin_last_name(self):
        return self.options.get('admin_last_name', None)

    def run(self, *args, **options):
        if not is_database_migrated():
            self.log('Database not migrated. Cannot set admin user.')
            return

        created = False
        user = User.objects.filter(is_superuser=True, is_staff=True).first()
        if not user:
            created = True
            user = User.objects.create(email=self.option_admin_email, is_superuser=True, is_staff=True)

        user.is_active = True
        user.email = self.option_admin_email
        if self.option_admin_first_name:
            user.first_name = self.option_admin_first_name
        if self.option_admin_last_name:
            user.last_name = self.option_admin_last_name
        user.set_password(self.option_admin_password)
        user.save()

        if created:
            self.log('Created admin with email {email}', email=user.email)
        else:
            self.log('Set admin email to {email}', email=user.email)
