from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View

from .models import Client, Server


@method_decorator(login_required, name='dispatch')
class DownloadServerConfig(View):

    def get(self, request, server_id, **kwargs):
        server = get_object_or_404(Server, owner=self.request.user, id=server_id)
        return HttpResponse(content=server.render_to_string(), content_type=server.mimetype)


@method_decorator(login_required, name='dispatch')
class DownloadClientConfig(View):

    def get(self, request, client_id, **kwargs):
        if self.request.user.is_superuser:
            client = get_object_or_404(Client, id=client_id)
        else:
            client = get_object_or_404(Client, owner=self.request.user, id=client_id)

        return HttpResponse(content=client.render_to_string(), content_type=client.mimetype)
