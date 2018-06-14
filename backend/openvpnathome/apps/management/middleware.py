from django.contrib.auth import get_user_model
from django.db import OperationalError
from openvpnathome.settings import USER_SETTINGS

from . import is_database_migrated
from openvpnathome.apps.openvpn.models import DhParams

User = get_user_model()


class CheckIsAppReadyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self.is_configured:
            context = {
                'has_settings_file': USER_SETTINGS.has_settings_file,
                'is_configured': USER_SETTINGS.is_configured,
                'is_migrated': is_database_migrated(),
                'has_active_admin': self.has_active_admin
            }
            setattr(request, 'app_not_ready', context)
        return self.get_response(request)

    @property
    def has_active_admin(self):
        try:
            return User.objects.filter(is_superuser=True, is_staff=True, is_active=True).count() > 0
        except OperationalError:
            return False

    @property
    def is_configured(self):
        return all((is_database_migrated(),
                    USER_SETTINGS.is_configured,
                    USER_SETTINGS.has_settings_file,
                    self.has_active_admin))
