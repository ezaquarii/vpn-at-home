from vpnathome.settings import USER_SETTINGS

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',

    'rest_framework',
    'rest_framework.authtoken',

    'vpnathome.apps.frontend',
    'vpnathome.apps.accounts',
    'vpnathome.apps.x509',
    'vpnathome.apps.management',
    'vpnathome.apps.openvpn'
]

if USER_SETTINGS.debug_toolbar_enabled and USER_SETTINGS.development:
    INSTALLED_APPS.append('debug_toolbar')
