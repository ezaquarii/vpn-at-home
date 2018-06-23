import uuid

from django.urls import reverse
from django.utils.text import slugify

from rest_framework import serializers

from openvpnathome.apps.x509.models import Ca, Cert
from .models import Server, Client
from .utils import generate_tls_auth_key


class ServerSerializer(serializers.ModelSerializer):

    email = serializers.SerializerMethodField()
    validity_end = serializers.SerializerMethodField()

    class Meta:
        model = Server
        fields = ['id', 'created', 'name', 'email', 'validity_end']

    def get_email(self, instance):
        return instance.ca.email

    def get_validity_end(self, instance):
        return instance.cert.validity_end


class AdminServerSerializer(ServerSerializer):

    download_url = serializers.SerializerMethodField()

    class Meta(ServerSerializer.Meta):
        fields = ServerSerializer.Meta.fields + ['download_url']

    def get_download_url(self, instance):
        kwargs={'server_id': instance.id, 'filename': slugify(instance.name) + '.conf'}
        return reverse('openvpn:download-server-config', kwargs=kwargs)


class CreateServerSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=Server.MAX_NAME_LENGTH)
    hostname = serializers.CharField(max_length=Server.MAX_HOSTNAME_LENGTH, allow_blank=False)
    email = serializers.EmailField(required=False)
    protocol = serializers.RegexField(regex="tcp|udp", required=False, default="udp")

    def create(self, validated_data):
        owner = self.context['owner']
        ca_name = '{name} CA'.format(name=validated_data['name'])

        ca = Ca.objects.create(owner=owner,
                               name=ca_name,
                               email=owner.email,
                               common_name=slugify(ca_name))

        cert_name = '{name} Server Certificate'.format(name=validated_data['name'])
        common_name = uuid.uuid4().hex
        cert = Cert.objects.create(owner=owner,
                                   ca=ca,
                                   name=cert_name,
                                   type=Cert.TYPE_SERVER,
                                   email=owner.email,
                                   common_name=common_name)

        tls_auth_key = generate_tls_auth_key()
        dhparams = self.context['dhparams']
        server = Server.objects.create(name=validated_data['name'],
                                       hostname=validated_data['hostname'],
                                       owner=owner,
                                       ca=ca,
                                       cert=cert,
                                       tls_auth_key=tls_auth_key,
                                       dhparams=dhparams,
                                       protocol=validated_data['protocol'])

        return server


class ClientSerializer(serializers.ModelSerializer):

    email = serializers.SerializerMethodField()
    validity_end = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'created', 'name', 'email', 'validity_end', 'download_url']

    def get_email(self, instance):
        return instance.cert.email

    def get_validity_end(self, instance):
        return instance.cert.validity_end

    def get_download_url(self, instance):
        kwargs={'client_id': instance.id, 'filename': instance.filename}
        return reverse('openvpn:download-client-config', kwargs=kwargs)


class CreateClientSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=Client.MAX_NAME_LENGTH)

    def create(self, validated_data):
        owner = self.context['owner']
        server = self.context['server']
        cert_name = '{name} Client Certificate'.format(name=validated_data['name'])
        common_name = uuid.uuid4().hex

        cert = Cert.objects.create(owner=owner,
                                   ca=server.ca,
                                   name=cert_name,
                                   type=Cert.TYPE_CLIENT,
                                   email=owner.email,
                                   common_name=common_name)

        client = Client.objects.create(name=validated_data['name'],
                                       owner=owner,
                                       server=server,
                                       cert=cert)

        return client
