from django.urls import path
from .api import SettingsApi, Test500Error, BlockListUrlApi, SshKeysApi

api_urlpatterns = [
    path('settings/', SettingsApi.as_view(), name='settings'),
    path('block_lists/', BlockListUrlApi.as_view({'get': 'list', 'put': 'update'}), name='block_lists'),
    path('ssh/public/', SshKeysApi.as_view({'get': 'get_public_key'}), name='ssh_public_key'),
    path('test500/', Test500Error.as_view(), name='test500error')
]
