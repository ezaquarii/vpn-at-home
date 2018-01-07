INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'constance',
    'constance.backends.database',

    'openvpnathome.apps.frontend',
    'openvpnathome.apps.accounts',
    'openvpnathome.apps.x509',
    'openvpnathome.apps.management',
    'openvpnathome.apps.openvpn'
]

from django.conf import settings as _settings
if _settings.DEBUG_TOOLBAR_ENABLED:
    INSTALLED_APPS.append('debug_toolbar')
