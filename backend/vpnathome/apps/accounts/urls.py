from django.urls import path
from .api import AuthenticationApi, UserApi

api_urlpatterns = [
    path('register/', AuthenticationApi.as_view({'post': 'register'}), name='register'),
    path('login/', AuthenticationApi.as_view({'post': 'login'}), name='login'),
    path('logout/', AuthenticationApi.as_view({'get': 'logout'}), name='logout'),
    path('user/', UserApi.as_view(), name='user'),
]
