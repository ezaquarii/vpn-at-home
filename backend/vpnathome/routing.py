from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.staticfiles import StaticFilesHandler
from channels.http import AsgiHandler
from django.conf.urls import url

from vpnathome.consumers import ProcessRunnerConsumer
from vpnathome.utils import is_database_migrated


__ws_router = URLRouter([
    url(r"^ws/$", ProcessRunnerConsumer),
])

__http_router = URLRouter([
    url(r"/static/", StaticFilesHandler),
    url(r"", AsgiHandler)
])

if is_database_migrated():
    application = ProtocolTypeRouter({
        "websocket": AuthMiddlewareStack(__ws_router),
        "http": AuthMiddlewareStack(__http_router),
    })
else:
    application = ProtocolTypeRouter({
        "http": __http_router
    })
