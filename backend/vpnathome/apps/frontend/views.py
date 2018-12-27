import json

from django.contrib.auth import get_user_model
from django.views import View
from django.template.response import TemplateResponse
from vpnathome import VERSION

from vpnathome.apps.management.models import Settings


User = get_user_model()


class FrontendView(View):

    def get(self, request):
        if not hasattr(request, 'app_not_ready'):
            settings = Settings.objects.first()
            context = {
                'version': VERSION,
                'state': json.dumps({
                    'authenticated': self.request.user.is_authenticated,
                    'registration_enabled': settings.registration_enabled,
                    'email_enabled': settings.email_enabled
                })
            }
            return TemplateResponse(request, 'index.html', context=context)
        else:
            context = {
                'version': VERSION,
                'state': json.dumps({
                    'authenticated': False,
                    'registration_enabled': False,
                    'email_enabled': False,
                    'app_not_ready': request.app_not_ready
                })
            }
            return TemplateResponse(request, 'index.html', context=context)
