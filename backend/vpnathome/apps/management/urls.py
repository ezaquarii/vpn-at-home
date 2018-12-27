from django.urls import path
from .api import SettingsApi, Test500Error, BlockListUrlApi

api_urlpatterns = [
    path('settings/', SettingsApi.as_view(), name='settings'),
    path('block_lists/', BlockListUrlApi.as_view({'get': 'list', 'put': 'update'}), name='block_lists'),
    path('test500/', Test500Error.as_view(), name='test500error')
]
