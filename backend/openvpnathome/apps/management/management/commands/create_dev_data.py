from django.contrib.auth import get_user_model

from openvpnathome.apps.openvpn.models import Server, Client
from openvpnathome.apps.openvpn.serializers import CreateServerSerializer, CreateClientSerializer
from openvpnathome.apps.x509.models import Ca, Cert

from . import ManagementCommand

User = get_user_model()


class Command(ManagementCommand):

    help = 'Create data useful for development'

    def run(self, *args, **options):
        pass
        #self._create_server()
        #self._create_admin_clients()

    def _create_server(self):
        if not self.has_server:
            admin = User.objects.get(is_superuser=True)
            context = {'owner': admin}
            create_server_serializer = CreateServerSerializer(data=dict(name='Server', email=admin.email), context=context)
            create_server_serializer.is_valid(raise_exception=True)
            server = create_server_serializer.save()
            self.log('Created server: {}'.format(server))

    def _create_admin_clients(self):
        if not self.has_clients:
            admin = User.objects.get(is_superuser=True)
            server = Server.objects.filter(owner=admin).first()
            context = {'owner': admin, 'server': server}
            for id in range(1, 4):
                create_client_dto = dict(name='Client {}'.format(id))
                create_client_serializer = CreateClientSerializer(data=create_client_dto, context=context)
                create_client_serializer.is_valid(raise_exception=True)
                client = create_client_serializer.save()
                self.log('Created client: {}'.format(client))

    @property
    def has_server(self):
        return Server.objects.count() > 0

    @property
    def has_clients(self):
        return Client.objects.count() > 0
