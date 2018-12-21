import ipaddress
import re

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django import forms
from vpnathome import get_bin_path


User = get_user_model()


def filter_empty_config_lines(input):
    """Filter out comments and empty lines from OpenVPN config file"""
    if input is not None:
        return re.sub(r'(?m)^(#.*\n+|;.*\n+|\s+\n+|\n+)', '', input)
    else:
        return None


class NetworkAddressField(models.Field):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def parse_ipv4_network(value):
        if isinstance(value, ipaddress.IPv4Network):
            address = value
        else:
            try:
                address = ipaddress.IPv4Network(value)
            except ValueError as e:
                raise ValidationError(_('Enter a valid IPv4 network address.'), code='invalid')

        if address.netmask.compressed not in ['255.0.0.0', '255.255.0.0', '255.255.255.0']:
            raise ValidationError(_('Only 8/16/24 networks are supported'), code='invalid')

        return address

    def get_internal_type(self):
        return "CharField"

    def from_db_value(self, value, expression, connection):
        if value is None or value is '':
            return None
        else:
            return self.parse_ipv4_network(value)

    def to_python(self, value):
        if isinstance(value, ipaddress.IPv4Network):
            return value
        elif isinstance(value, str):
            return self.parse_ipv4_network(value)
        elif value is None:
            return value
        else:
            raise ValidationError('Unknown type {type}'.format(type=type(value)))

    def get_prep_value(self, value):
        if value is None:
            return None
        elif isinstance(value, str):
            self.parse_ipv4_network(value)
            return value
        elif isinstance(value, ipaddress.IPv4Network):
            self.parse_ipv4_network(value)  # ok for parsed value, will check value only
            return str(value)
        else:
            raise ValidationError('Value {value} of unexpected type {type}'.format(value=str(value), type=type(value)))


class DhParams(models.Model):
    dhparams = models.TextField(max_length=4096, blank=True, default='')


class Server(models.Model):

    MAX_NAME_LENGTH = 64
    MAX_HOSTNAME_LENGTH = 128

    PROTOCOL_UDP = 'udp'
    PROTOCOL_TCP = 'tcp'
    PROTOCOL_CHOICES = (
        (PROTOCOL_UDP, 'UDP'),
        (PROTOCOL_TCP, 'TCP'),
    )

    DEFAULT_NETWORK = ipaddress.IPv4Network('172.30.0.0/16')
    DEFAULT_PROTOCOL = PROTOCOL_UDP
    DEFAULT_PORT = 1194

    class Meta:
        permissions = (
            ('download_server_config', 'Download server config'),
        )

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    hostname = models.CharField(max_length=MAX_HOSTNAME_LENGTH, blank=False)
    port = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(65535)], default=DEFAULT_PORT)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    ca = models.ForeignKey('x509.Ca', on_delete=models.CASCADE, related_name='+')
    cert = models.ForeignKey('x509.Cert', on_delete=models.CASCADE, related_name='+')
    tls_auth_key = models.TextField(max_length=8192)
    dhparams = models.ForeignKey(DhParams, on_delete=models.CASCADE)
    protocol = models.CharField(choices=PROTOCOL_CHOICES, default=DEFAULT_PROTOCOL, max_length=10)
    network = NetworkAddressField(max_length=100, default=str(DEFAULT_NETWORK), null=True)
    deleted = models.BooleanField(default=False)
    deploy_dns = models.BooleanField(default=False)

    def __str__(self):
        if self.deleted:
            return 'Server {name}, {hostname}, {owner}, deleted'.format(name=self.name, hostname=self.hostname, owner=self.email)
        else:
            return 'Server {name}, {hostname}, {owner}'.format(name=self.name, hostname=self.hostname, owner=self.email)

    @property
    def email(self):
        return self.owner.email

    @property
    def filename(self):
        return 'server-' + slugify(self.name) + '.conf'

    @property
    def mimetype(self):
        return 'application/x-openvpn-profile'

    @property
    def protocol_server_option(self):
        return 'udp' if self.protocol == 'udp' else 'tcp-server'

    @property
    def protocol_client_option(self):
        return 'udp' if self.protocol == 'udp' else 'tcp-client'

    @property
    def client_connect_script(self):
        return get_bin_path('connect.sh')

    @property
    def gateway(self):
        return str(next(self.network.hosts()))

    def render_to_string(self):
        """
        Render server's configuration to string, using OpenVPN configuration template.
        Resulting config contains deployment-specific paths, so you should make
        sure to re-generate server config when app deployment path changes.

        :return: Rendered configuration file contents.
        """
        context = {
            'ca': self.ca.certificate.strip(),
            'cert': self.cert.certificate.strip(),
            'key': self.cert.private_key.strip(),
            'dh': self.dhparams.dhparams.strip(),
            'tls_auth': self.tls_auth_key.strip(),
            'protocol': self.protocol_server_option,
            'client_connect_script': self.client_connect_script,
            'network': self.network.network_address,
            'netmask': self.network.netmask,
            'port': self.port,
            'deploy_dns': self.deploy_dns,
            'gateway': self.gateway
        }
        config = render_to_string('server.ovpn', context=context)
        return filter_empty_config_lines(config)


class Client(models.Model):

    MAX_NAME_LENGTH = 64

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='+')
    cert = models.ForeignKey('x509.Cert', on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return 'Client {id}, {owner}'.format(id=self.id, owner=self.email)

    @property
    def email(self):
        return self.owner.email

    @property
    def filename(self):
        return "{client}--at--{server}.conf".format(client=slugify(self.name), server=slugify(self.server.name))

    @property
    def mimetype(self):
        return 'application/x-openvpn-profile'

    def render_to_string(self):
        """
        Render client's configuration to string, using OpenVPN configuration template.

        :return: Rendered configuration file contents.
        """
        context = {
            'ca': self.server.ca.certificate.strip(),
            'cert': self.cert.certificate.strip(),
            'key': self.cert.private_key.strip(),
            'tls_auth': self.server.tls_auth_key.strip(),
            'server_hostname': self.server.hostname,
            'server_port': self.server.port,
            'protocol': self.server.protocol_client_option
        }
        config = render_to_string('client.ovpn', context=context)
        return filter_empty_config_lines(config)
