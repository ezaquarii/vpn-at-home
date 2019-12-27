from datetime import datetime
import uuid
from django.urls import reverse
from django.utils.text import slugify
from rest_framework import serializers

from vpnathome.apps.x509.models import Ca, Cert

from . import models
from .utils import generate_tls_auth_key


class NetworkAddressSerializerField(serializers.Field):

    def to_internal_value(self, data):
        return models.NetworkAddressField.parse_ipv4_network(data)

    def to_representation(self, value):
        return value.compressed


class ServerSerializer(serializers.ModelSerializer):

    serializer_field_mapping = {
        **serializers.ModelSerializer.serializer_field_mapping,
        models.NetworkAddressField: NetworkAddressSerializerField
    }

    email = serializers.SerializerMethodField()
    validity_end = serializers.SerializerMethodField()

    class Meta:
        model = models.Server
        fields = ['id', 'created', 'name', 'email', 'validity_end', 'network', 'hostname']

    def get_email(self, instance):
        return instance.owner.email

    def get_validity_end(self, instance):
        return instance.cert.validity_end


class AdminServerSerializer(ServerSerializer):

    download_url = serializers.SerializerMethodField()

    class Meta(ServerSerializer.Meta):
        fields = ServerSerializer.Meta.fields + ['download_url']

    def get_download_url(self, instance):
        kwargs={'server_id': instance.id, 'filename': slugify(instance.name) + '.conf'}
        return reverse('openvpn:download-server-config', kwargs=kwargs)


def validity_end_from_time(now, count, unit):
    from dateutil.relativedelta import relativedelta
    t = now
    t.replace(hour=0, minute=0, second=0, microsecond=0)
    if unit == 'days':
        t += relativedelta(days=count)
    elif unit == 'months':
        t += relativedelta(months=count)
    elif unit == 'years':
        t += relativedelta(years=count)
    return t


class CreateServerSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=models.Server.MAX_NAME_LENGTH)
    hostname = serializers.CharField(max_length=models.Server.MAX_HOSTNAME_LENGTH, allow_blank=False)
    port = serializers.IntegerField(required=False, default=models.Server.DEFAULT_PORT)
    email = serializers.EmailField(required=False)
    protocol = serializers.RegexField(regex="tcp|udp", required=False, default="udp")
    network = NetworkAddressSerializerField(required=False, default=models.Server.DEFAULT_NETWORK)
    deploy_dns = serializers.BooleanField(required=False, default=False)
    validity_time = serializers.IntegerField(required=False, default=1, min_value=1, max_value=1000)
    validity_time_unit = serializers.ChoiceField(required=False, default="years", choices=["days", "months", "years"])

    def create(self, validated_data):
        owner = self.context['owner']
        ca_name = '{name} CA'.format(name=validated_data['name'])

        validity_end = validity_end_from_time(now=datetime.now(),
                                              count=validated_data['validity_time'],
                                              unit=validated_data['validity_time_unit'])
        ca = Ca.objects.create(owner=owner,
                               name=ca_name,
                               email=owner.email,
                               common_name=slugify(ca_name),
                               validity_end=validity_end)

        cert_name = '{name} Server Certificate'.format(name=validated_data['name'])
        common_name = uuid.uuid4().hex
        cert = Cert.objects.create(owner=owner,
                                   ca=ca,
                                   name=cert_name,
                                   type=Cert.TYPE_SERVER,
                                   email=owner.email,
                                   common_name=common_name,
                                   validity_end=validity_end)

        tls_auth_key = generate_tls_auth_key()
        dhparams = self.context['dhparams']
        server = models.Server.objects.create(name=validated_data['name'],
                                              hostname=validated_data['hostname'],
                                              port=validated_data['port'],
                                              owner=owner,
                                              ca=ca,
                                              cert=cert,
                                              tls_auth_key=tls_auth_key,
                                              dhparams=dhparams,
                                              protocol=validated_data['protocol'],
                                              network=validated_data['network'],
                                              deploy_dns=validated_data['deploy_dns'])

        return server


class ClientSerializer(serializers.ModelSerializer):

    email = serializers.SerializerMethodField()
    validity_end = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
    server_name = serializers.SerializerMethodField()

    class Meta:
        model = models.Client
        fields = ['id', 'created', 'name', 'email', 'validity_end', 'download_url', 'server_name']

    def get_email(self, instance):
        return instance.owner.email

    def get_validity_end(self, instance):
        return instance.cert.validity_end

    def get_download_url(self, instance):
        kwargs={'client_id': instance.id, 'filename': instance.filename}
        return reverse('openvpn:download-client-config', kwargs=kwargs)

    def get_server_name(self, instance):
        return instance.server.name


class CreateClientSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=models.Client.MAX_NAME_LENGTH)
    validity_time = serializers.IntegerField(required=False, default=1, min_value=1, max_value=1000)
    validity_time_unit = serializers.ChoiceField(required=False, default="years", choices=["days", "months", "years"])

    def create(self, validated_data):
        owner = self.context['owner']
        server = self.context['server']
        cert_name = '{name} Client Certificate'.format(name=validated_data['name'])
        common_name = uuid.uuid4().hex

        validity_end = validity_end_from_time(now=datetime.now(),
                                              count=validated_data['validity_time'],
                                              unit=validated_data['validity_time_unit'])

        cert = Cert.objects.create(owner=owner,
                                   ca=server.ca,
                                   name=cert_name,
                                   type=Cert.TYPE_CLIENT,
                                   email=owner.email,
                                   common_name=common_name,
                                   validity_end=validity_end)

        client = models.Client.objects.create(name=validated_data['name'],
                                              owner=owner,
                                              server=server,
                                              cert=cert)

        return client
