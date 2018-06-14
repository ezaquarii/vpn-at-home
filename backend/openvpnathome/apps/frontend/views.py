import json

from django.contrib.auth import get_user_model
from django.views import View
from django.template.response import TemplateResponse

from openvpnathome.apps.management.models import Settings


User = get_user_model()


class FrontendView(View):

    def get(self, request):
        if not hasattr(request, 'app_not_ready'):
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
            return TemplateResponse(request, 'not_configured.html', context=request.app_not_ready)
