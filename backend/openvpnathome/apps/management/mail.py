from django.core.mail.backends.smtp import EmailBackend as _EmailBackend

from .models import Settings as _Settings


class EmailSender():
    """
    This class sends email using dynamically configured backend.
    SMTP client configuration is injected into constructor.

    :param settings: See management.Settings model or None. If no settings are provided, they are fetched from database at runtime.
    :param email_backend: Optional email backend class; by default it uses django.core.mail.backends.smtp.EmailBackend
    """
    def __init__(self, settings=None, email_backend=_EmailBackend):
        self.settings = settings if settings else _Settings.objects.first()
        if not self.settings:
            raise RuntimeError('EmailSender requires management.Settings, but no settings were provided and no settings are found in database.')
        self.backend = email_backend(host=self.settings.email_smtp_server,
                                     port=self.settings.email_smtp_port,
                                     username=self.settings.email_smtp_login,
                                     password=self.settings.email_smtp_password,
                                     use_tls=True,
                                     use_ssl=False,
                                     fail_silently=False,
                                     timeout=10)

    def send(self, email):
        if self.can_send_emails:
            email.from_email = self.settings.email_from
            email.connection = self.backend
            email.send()
            return True
        else:
            return False

    @property
    def can_send_emails(self):
        return self.settings.email_enabled and self.settings.email_from
