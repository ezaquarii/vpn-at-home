import json

from django.views.generic import TemplateView

from openvpnathome.apps.management.models import Settings


class FrontendView(TemplateView):

    template_name = 'index.html'

    def get_initial_state(self, **kwargs):
        settings = Settings.objects.first()
        return {
            'authenticated': self.request.user.is_authenticated,
            'registration_enabled': settings.registration_enabled,
            'email_enabled': settings.email_enabled,
            'hydrated': False
        }

    def get_context_data(self, **kwargs):
        state = self.get_initial_state(**kwargs)
        return {
            'state': json.dumps(state)
        }
