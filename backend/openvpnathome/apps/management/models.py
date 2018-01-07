from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Settings(models.Model):

    EMAIL_MAX_LENGTH = 128

    email_enabled = models.BooleanField(default=False)
    email_from = models.EmailField(max_length=EMAIL_MAX_LENGTH, blank=True, default='')
    email_smtp_server = models.CharField(max_length=EMAIL_MAX_LENGTH, blank=True, default='')
    email_smtp_port = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(65535)], default=465)
    email_smtp_login = models.CharField(max_length=EMAIL_MAX_LENGTH, blank=True, default='')
    email_smtp_password = models.CharField(max_length=EMAIL_MAX_LENGTH, blank=True, default='')

    registration_enabled = models.BooleanField(default=True)

    class Meta():
        verbose_name = 'settings'
        verbose_name_plural = 'settings'

    def __str__(self):
        return 'Settings pk={id}'.format(id=self.id)

    @staticmethod
    def instance():
        return Settings.objects.first()
