from vpnathome import get_frontend_path, get_root_path
from vpnathome.settings import USER_SETTINGS

STATIC_URL = '/static/'
STATIC_ROOT = get_root_path('static')

if USER_SETTINGS.development:
    STATICFILES_DIRS = [
        get_frontend_path('dist/static')
    ]
