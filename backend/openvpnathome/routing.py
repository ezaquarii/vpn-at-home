from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.staticfiles import StaticFilesHandler
from channels.http import AsgiHandler
from django.conf.urls import url

from openvpnathome.consumers import ProcessRunnerConsumer

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^ws/$", ProcessRunnerConsumer),
        ])
    ),
    "http": AuthMiddlewareStack(
        URLRouter([
            url(r"/static/", StaticFilesHandler),
            url(r"", AsgiHandler)
        ])
    ),
})

