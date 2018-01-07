from django.conf import settings as _settings
from openvpnathome import get_frontend_path, get_root_path


STATIC_URL = '/static/'
STATIC_ROOT = get_root_path('static')

if _settings.DEVELOPMENT:
    STATICFILES_DIRS = [
        get_frontend_path('dist/static')
    ]
