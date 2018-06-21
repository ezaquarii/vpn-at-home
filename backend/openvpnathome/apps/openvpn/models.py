from django.db import models
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.text import slugify

User = get_user_model()
from django.contrib.auth.models import Permission


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

    class Meta:
        permissions = (
            ('download_server_config', 'Download server config'),
        )

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    hostname = models.CharField(max_length=MAX_HOSTNAME_LENGTH, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    ca = models.ForeignKey('x509.Ca', on_delete=models.CASCADE, related_name='+')
    cert = models.ForeignKey('x509.Cert', on_delete=models.CASCADE, related_name='+')
    tls_auth_key = models.CharField(max_length=8192)
    dhparams = models.ForeignKey(DhParams, on_delete=models.CASCADE)
    protocol = models.CharField(choices=PROTOCOL_CHOICES, default=PROTOCOL_UDP, max_length=10)

    def __str__(self):
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

    def render_to_string(self):
        """
        Render server's configuration to string, using OpenVPN configuration template.

        :return: Rendered configuration file contents.
        """
        context = {
            'ca': self.ca.certificate.strip(),
            'cert': self.cert.certificate.strip(),
            'key': self.cert.private_key.strip(),
            'dh': self.dhparams.dhparams.strip(),
            'tls_auth': self.tls_auth_key.strip(),
            'protocol': self.protocol_server_option
        }
        return render_to_string('server.ovpn', context=context)
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
        return self.cert.email

    @property
    def filename(self):
        return slugify(self.name) + '.conf'

    @property
    def mimetype(self):
        return 'application/x-openvpn-profile'
        #return 'text/plain'

    def render_to_string(self):
        """
        Render client's configuration to string, using OpenVPN configuration template.

        :return: Rendered configuration file contents.
        """
        context = {
            'ca': self.server.ca.certificate.strip(),
            'cert': self.cert.certificate.strip(),
            'key': self.cert.private_key.strip(),
            'tls_auth': self.server.tls_auth_key,
            'server_hostname': self.server.hostname,
            'protocol': self.server.protocol_client_option
        }
        return render_to_string('client.ovpn', context=context)
