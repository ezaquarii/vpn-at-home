"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django
from channels.routing import get_default_application
from channels.staticfiles import StaticFilesWrapper

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vpnathome.settings.settings")
django.setup()
application = StaticFilesWrapper(get_default_application())
