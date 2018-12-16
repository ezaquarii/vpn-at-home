from django.shortcuts import get_object_or_404

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from vpnathome.apps.management.models import Settings

from .models import Server, Client, DhParams
from .serializers import CreateServerSerializer, ServerSerializer, AdminServerSerializer, CreateClientSerializer, ClientSerializer
from .utils import send_client_config


class ServerApi(ViewSet):

    def get_permissions(self):
        if self.action in ['create', 'delete']:
            return [permissions.IsAdminUser()]
        else:
            return [permissions.IsAuthenticated()]

    def create(self, request):
        dhparams = DhParams.objects.first()
        context = dict(owner=self.request.user, dhparams=dhparams)
        create_serializer = CreateServerSerializer(data=request.data, context=context)
        create_serializer.is_valid(raise_exception=True)
        server = create_serializer.save()

        server_serializer = ServerSerializer(instance=server)
        return Response(data=server_serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        servers = Server.objects.filter(deleted=False)
        if request.user.is_superuser:
            serializer = AdminServerSerializer(instance=servers, many=True)
        else:
            serializer = ServerSerializer(instance=servers, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, server_id):
        server = get_object_or_404(Server, id=server_id, owner=request.user, deleted=False)
        server.deleted = True
        server.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientApi(ViewSet):

    permission_classes = [permissions.IsAuthenticated]

    def get_clients(self, **kwargs):
        return Client.objects.filter(server__deleted=False, **kwargs)

    def get_client_or_404(self, **kwargs):
        return get_object_or_404(Client, server__deleted=False, **kwargs)


    def create(self, request, server_id):
        server = get_object_or_404(Server, pk=server_id, deleted=False)
        if server is None:
            return Response(data='Server not found', status=status.HTTP_404_NOT_FOUND)
        context = dict(owner=request.user, server=server)
        create_serializer = CreateClientSerializer(data=request.data, context=context)
        create_serializer.is_valid(raise_exception=True)
        client = create_serializer.save()

        client_serializer = ClientSerializer(instance=client)
        return Response(data=client_serializer.data, status=status.HTTP_201_CREATED)

    def list_all_clients(self, request):
        if request.user.is_superuser:
            clients = self.get_clients()
        else:
            clients = self.get_clients(owner=request.user)
        serializer = ClientSerializer(instance=clients, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def list_server_clients(self, request, server_id):
        if request.user.is_superuser:
            clients = self.get_clients(server_id=server_id)
        else:
            clients = self.get_clients(owner=request.user, server_id=server_id)
        serializer = ClientSerializer(instance=clients, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def send_email(self, request, id):
        settings = Settings.instance()
        if not settings.email_enabled:
            return Response(status=status.HTTP_200_OK)

        if request.user.is_superuser:
            client = self.get_client_or_404(id=id)
        else:
            client = self.get_client_or_404(id=id, owner=request.user)

        send_client_config(config=client)
        return Response(status=status.HTTP_200_OK)
