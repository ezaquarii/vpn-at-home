from django.urls import path
from .api import SettingsApi, Test500Error

api_urlpatterns = [
    path('settings/', SettingsApi.as_view(), name='settings'),
    path('test500/', Test500Error.as_view(), name='test500error')
]
