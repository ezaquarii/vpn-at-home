from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend as _EmailBackend
from openvpnathome.apps.management.models import Settings


class ConfigurableEmailBackend(_EmailBackend):
    """
    This is a wrapper around standard Django SMTP e-mail backend
    that takes configuration from database instead of Django settings.
    """

    def __init__(self, *args, settings=None, **kwargs):
        """
        Pass settings to base class.
        """
        self.settings = Settings.instance() if settings is None else settings
        kwargs_override = self.get_backend_config(**kwargs)
        super().__init__(*args, **kwargs, **kwargs_override)

    def get_backend_config(self, **kwargs):
        """
        Get backend config from provided settings. Empty values must be converted to None,
        to respect base class behavior.

        It will honor kwargs first, then settings from DB and it will fallback to Django settings.

        :return: kwargs with SMTP configuration compatible with base class constructor
        """
        return {
            'host': self._first_true_or_none(kwargs.get('host', None), self.settings.email_smtp_server, settings.EMAIL_HOST),
            'port': self._first_true_or_none(kwargs.get('port', None), self.settings.email_smtp_port, settings.EMAIL_PORT),
            'username': self._first_true_or_none(kwargs.get('username', None), self.settings.email_smtp_login, settings.EMAIL_HOST_USER),
            'password': self._first_true_or_none(kwargs.get('password', None), self.settings.email_smtp_password, settings.EMAIL_HOST_PASSWORD),
            'use_tls': self._first_true_or_none(kwargs.get('use_tls'), True),
        }

    @staticmethod
    def _first_true_or_none(*args):
        for item in args:
            if item:
                return item
        return None

    def open(self):
        if self.settings.email_enabled:
            return super().open()
        else:
            return False

    def close(self):
        if self.settings.email_enabled:
            return super().close()
        else:
            return None

    def send_messages(self, email_messages):
        if self.settings.email_enabled:
            return super().send_messages(email_messages)
        else:
            return None
