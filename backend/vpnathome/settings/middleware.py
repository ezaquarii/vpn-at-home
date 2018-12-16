from vpnathome.settings import USER_SETTINGS
from vpnathome.utils import is_database_migrated

MIDDLEWARE = list(filter(lambda m: m is not None, [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'vpnathome.apps.management.middleware.CheckIsAppReadyMiddleware',
]))

if USER_SETTINGS.debug_toolbar_enabled and USER_SETTINGS.development:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
