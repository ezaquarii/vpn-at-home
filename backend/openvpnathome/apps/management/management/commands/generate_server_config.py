from os.path import abspath
from django.contrib.auth import get_user_model
from django.core.management.base import CommandError
from openvpnathome.apps.openvpn.models import Server
from . import ManagementCommand


User = get_user_model()


class Command(ManagementCommand):

    help = "Generate and write or print OpenVPN server config file."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('-s', '--server', help="Server name")
        parser.add_argument('-o', '--output-file', help="Output file")

    @property
    def option_server(self):
        return self.options.get('server')

    @property
    def option_output_file(self):
        return self.options.get('output_file')

    def get_server(self):
        if self.option_server:
            try:
                return Server.objects.get(name=self.option_server)
            except Server.DoesNotExist:
                raise CommandError('Server [{server}] not found'.format(server=self.option_server))
        else:
            server = Server.objects.first()
            if server is None:
                raise CommandError('Default server not found')
            return server

    def write_to_file(self, config):
        absolute_path = abspath(self.option_output_file)
        self.log('Writing file to {file}'.format(file=absolute_path))
        with open(absolute_path, 'w') as f:
            f.write(config)

    def run(self, *args, **options):
        server = self.get_server()
        config = server.render_to_string()
        if self.option_output_file is None:
            print(config)
        else:
            self.write_to_file(config)
