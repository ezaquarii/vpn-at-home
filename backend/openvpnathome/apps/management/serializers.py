from rest_framework import serializers

from .models import Settings


class SettingsSerializer(serializers.ModelSerializer):

    class Meta():
        model = Settings
        fields = '__all__'
        read_only_fields = ['id']
