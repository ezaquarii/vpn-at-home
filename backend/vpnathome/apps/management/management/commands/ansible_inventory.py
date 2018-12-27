import json
from django.contrib.auth import get_user_model
from vpnathome.apps.management.models import BlockedDomain
from vpnathome.apps.openvpn.models import Server
from vpnathome.utils import get_object_or_none
from . import ManagementCommand


User = get_user_model()


class Command(ManagementCommand):

    help = "Generate Ansible inventory from configured servers."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--local', action='store_true', help="List groups in JSON format")
        parser.add_argument('--list', action='store_true', help="List groups in JSON format")
        parser.add_argument('--host', nargs=1, type=str, help="Print host variables in JSON format")

    @property
    def option_list(self):
        return self.options.get('list')

    @property
    def option_host(self):
        host = self.options.get('host')
        return host[0] if host else None

    @property
    def option_local(self):
        return self.options.get('local')

    def run_list(self, local=False):
        inventory = {
            'vpns': {
                'hosts': [],
                'vars': {},
                'children': []
            }
        }

        if local:
            inventory['vpns']['hosts'] = ['localhost']
        else:
            servers = Server.objects.all()
            for server in servers:
                inventory['vpns']['hosts'].append(server.hostname)

        json_inventory = json.dumps(inventory, indent=4)
        print(json_inventory)

    def run_host(self, hostname):
        if hostname in ['127.0.0.1', 'localhost', 'localhost.localdomain']:
            server = Server.objects.first()
        else:
            server = get_object_or_none(Server, hostname=hostname)
        vars = {}
        if server:
            vars['ansible_user'] = 'root'
            vars['vpn_network'] = str(server.network)
            vars['vpn_gateway'] = str(server.gateway)
            vars['vpn_name'] = server.name
            vars['vpn_port'] = server.port
            vars['vpn_config'] = server.render_to_string()
            vars['deploy_dns'] = server.deploy_dns
            vars['blocked_domains'] = self.get_blocked_domains() if server.deploy_dns else []
        vars_json = json.dumps(vars, indent=4)
        print(vars_json)

    def get_blocked_domains(self):
        return list(BlockedDomain.objects.values_list('domain', flat=True))

    def run(self, *args, **options):
        if self.option_list:
            self.run_list(local=self.option_local)
        elif self.option_host:
            self.run_host(hostname=self.option_host)
