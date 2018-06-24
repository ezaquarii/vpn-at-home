from os.path import abspath
from django.contrib.auth import get_user_model
from django.core.management.base import CommandError

from openvpnathome.apps.openvpn.models import Client
from openvpnathome.utils import get_object_or_none

from . import ManagementCommand

User = get_user_model()


class Command(ManagementCommand):

    help = "Generate and write or print OpenVPN client specific config options.\n"\
           "Output from this script should be pushed to the remote client on connection."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('-c', '--common-name', help="Client X509 CN (common name) value")
        parser.add_argument('-o', '--output-file', help="Output file")

    @property
    def option_common_name(self):
        return self.options.get('common_name')

    @property
    def option_output_file(self):
        return self.options.get('output_file')

    def write_to_file(self, config):
        absolute_path = abspath(self.option_output_file)
        self.log('Writing file to {file}'.format(file=absolute_path))
        with open(absolute_path, 'w') as f:
            f.write(config)

    def run(self, *args, **options):
        client = get_object_or_none(Client, cert__common_name=self.option_common_name)
        if not client:
            raise CommandError("Client with CN={common_name} does not exist".format(common_name=self.option_common_name))

        options = 'ifconfig-push 172.30.0.199 255.255.0.0\n'

        if self.option_output_file:
            self.write_to_file(options)
        else:
            print(options)
