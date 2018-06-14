import json

from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.views import View
from django.template.response import TemplateResponse

from openvpnathome.apps.management.models import Settings
from openvpnathome.utils import is_database_migrated
from openvpnathome.settings import USER_SETTINGS


User = get_user_model()


class FrontendView(View):

    @property
    def is_bootstrapped(self):
        return True

    @property
    def has_active_admin(self):
        return User.objects.filter(is_superuser=True, is_staff=True, is_active=True).count() > 0

    @property
    def is_configured(self):
        return all((is_database_migrated(),
                    USER_SETTINGS.is_configured,
                    USER_SETTINGS.has_settings_file,
                    self.has_active_admin))

    def get(self, request):
        if self.is_configured:
            settings = Settings.objects.first()
            context = {
                'state': json.dumps({
                    'authenticated': self.request.user.is_authenticated,
                    'registration_enabled': settings.registration_enabled,
                    'email_enabled': settings.email_enabled,
                    'hydrated': False
                })
            }
            return TemplateResponse(request, 'index.html', context=context)
        else:
            context = {
                'has_settings_file': USER_SETTINGS.has_settings_file,
                'is_configured': USER_SETTINGS.is_configured,
                'is_migrated': is_database_migrated(),
                'is_bootstrapped': self.is_bootstrapped,
                'has_active_admin': self.has_active_admin
            }
            return TemplateResponse(request, 'not_configured.html', context=context)
