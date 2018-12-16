"""vpnathome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

from vpnathome.apps.accounts.urls import api_urlpatterns as account_api_urls
from vpnathome.apps.management.urls import api_urlpatterns as management_api_urls
from vpnathome.apps.openvpn.urls import api_urlpatterns as openvpn_api_urls
from vpnathome.apps.openvpn.urls import views_urlpatterns as openvpn_views_urls
from vpnathome.apps.frontend.views import FrontendView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('openvpn/', include((openvpn_views_urls, 'openvpn'))),
    path('api/management/', include((management_api_urls, 'management-api'))),
    path('api/accounts/', include((account_api_urls, 'accounts-api'))),
    path('api/openvpn/', include((openvpn_api_urls, 'openvpn-api'))),
    re_path('^.*', FrontendView.as_view())
]

if settings.DEBUG_TOOLBAR_ENABLED:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
