from django.shortcuts import get_object_or_404

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from openvpnathome.apps.management.models import Settings

from .models import Server, Client, DhParams
from .serializers import CreateServerSerializer, ServerSerializer, AdminServerSerializer, CreateClientSerializer, ClientSerializer
from .utils import send_client_config


class ServerApi(ViewSet):

    def create(self, request):
        dhparams = DhParams.objects.first()
        context = dict(owner=self.request.user, dhparams=dhparams)
        create_serializer = CreateServerSerializer(data=request.data, context=context)
        create_serializer.is_valid(raise_exception=True)
        server = create_serializer.save()

        server_serializer = ServerSerializer(instance=server)
        return Response(data=server_serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        servers = Server.objects.all()

        # TODO: refactor it using dynamic serializer fields
        if request.user.is_superuser:
            serializer = AdminServerSerializer(instance=servers, many=True)
        else:
            serializer = ServerSerializer(instance=servers, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAdminUser()]
        else:
            return [permissions.IsAuthenticated()]


class ClientApi(ViewSet):

    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, server_id):
        server = get_object_or_404(Server, pk=server_id)
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
            clients = Client.objects.all()
        else:
            clients = Client.objects.filter(owner=request.user)
        serializer = ClientSerializer(instance=clients, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def list_server_clients(self, request, server_id):
        if request.user.is_superuser:
            clients = Client.objects.filter(server_id=server_id)
        else:
            clients = Client.objects.filter(owner=request.user, server_id=server_id)
        serializer = ClientSerializer(instance=clients, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def send_email(self, request, id):
        settings = Settings.instance()
        if not settings.email_enabled:
            return Response(status=status.HTTP_200_OK)

        if request.user.is_superuser:
            client = get_object_or_404(Client, id=id)
        else:
            client = get_object_or_404(Client, id=id, owner=request.user)

        send_client_config(config=client)
        return Response(status=status.HTTP_200_OK)
