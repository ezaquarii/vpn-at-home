from rest_framework import serializers

from .models import Settings


class SettingsSerializer(serializers.ModelSerializer):

    class Meta():
        model = Settings
        fields = ('email_enabled',
                  'email_from',
                  'email_smtp_server',
                  'email_smtp_port',
                  'email_smtp_login',
                  'email_smtp_password',
                  'registration_enabled')
