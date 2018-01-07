from django.urls import path
from .api import SettingsApi

api_urlpatterns = [
    path('settings/', SettingsApi.as_view(), name='settings'),
]
