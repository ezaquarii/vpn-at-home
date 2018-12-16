from django.urls import path, re_path
from .api import ServerApi, ClientApi
from .views import DownloadServerConfig, DownloadClientConfig

api_urlpatterns = [
    path('servers/', ServerApi.as_view({'get': 'list',
                                        'post': 'create'}), name='servers'),
    path('servers/<int:server_id>/', ServerApi.as_view({'delete': 'delete'}), name='server'),
    path('servers/<int:server_id>/clients/', ClientApi.as_view({'get': 'list_server_clients',
                                                                'post': 'create'}), name='server-clients'),
    path('clients/', ClientApi.as_view({'get': 'list_all_clients'}), name='clients'),
    path('clients/<int:id>/send/', ClientApi.as_view({'post': 'send_email'}), name='send-client-config'),
]

views_urlpatterns = [
    re_path('download/server/(?P<server_id>\d+)/(?P<filename>\w+)', DownloadServerConfig.as_view(), name='download-server-config'),
    re_path('download/client/(?P<client_id>\d+)/(?P<filename>\w+)', DownloadClientConfig.as_view(), name='download-client-config')
]
