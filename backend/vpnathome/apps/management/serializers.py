from django.conf import settings
from rest_framework import serializers

from .models import Settings


class SettingsSerializer(serializers.ModelSerializer):

    email_from = serializers.SerializerMethodField()
    email_smtp_server = serializers.SerializerMethodField()
    email_smtp_port = serializers.SerializerMethodField()
    email_smtp_login = serializers.SerializerMethodField()
    email_smtp_password = serializers.SerializerMethodField()

    class Meta:
        model = Settings
        fields = ('email_enabled',
                  'registration_enabled',
                  'email_from',
                  'email_smtp_server',
                  'email_smtp_port',
                  'email_smtp_login',
                  'email_smtp_password')

    def get_email_from(self, instance):
        return settings.SERVER_EMAIL

    def get_email_smtp_server(self, instance):
        return settings.EMAIL_HOST

    def get_email_smtp_port(self, instance):
        return settings.EMAIL_PORT

    def get_email_smtp_login(self, instance):
        return settings.EMAIL_HOST_USER

    def get_email_smtp_password(self, instance):
        return 'hidden'
