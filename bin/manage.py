#!/usr/bin/env python3
import os
import sys

import warnings
warnings.filterwarnings(u'ignore',
        message=u'DateTimeField .* received a naive datetime',
        category=RuntimeWarning)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vpnathome.settings.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
    execute_from_command_line(sys.argv)
