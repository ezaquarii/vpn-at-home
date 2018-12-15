import subprocess

from django.conf import settings
from django.core.mail import EmailMessage


def generate_dhparams(bits=2048):
    """
    Generate dhparams for OpenVPN. It calls openssl binary.

    :return: dhparams, 2048 bits
    """

    cmd = ['openssl', 'dhparam', str(bits)]
    completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if completed_process.returncode == 0:
        return completed_process.stdout.decode('utf8')
    else:
        raise subprocess.CalledProcessError(returncode=completed_process.returncode,
                                            cmd=cmd,
                                            output=completed_process.stdout,
                                            stderr=completed_process.stderr)


def generate_tls_auth_key():
    """
    Generate pre-shared secret key. It calls openvpn binary to generate it.

    :return: OpenVPN pre-shared secret key.
    """
    cmd = ['openvpn', '--genkey', '--secret', '/dev/stdout']
    completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if completed_process.returncode == 0:
        key_with_comments = completed_process.stdout.decode('utf8')
        key_lines = key_with_comments.split('\n')
        key_filtered_lines = list(filter(lambda x: not x.startswith('#'), key_lines))
        return '\n'.join(key_filtered_lines)
    else:
        raise subprocess.CalledProcessError(returncode=completed_process.returncode,
                                            cmd=cmd,
                                            output=completed_process.stdout,
                                            stderr=completed_process.stderr)


def send_client_config(config):
    email = EmailMessage(
        subject='OpenVPN configuration file',
        body='Please find attached OpenVPN configuration file',
        from_email=settings.SERVER_EMAIL if settings.SERVER_EMAIL else "no-reply@set_server_email_in_settings.json",
        to=[config.owner.email]
    )
    email.attach(config.filename, config.render_to_string(), config.mimetype)
    email.send(fail_silently=False) # default backend will be used internally
