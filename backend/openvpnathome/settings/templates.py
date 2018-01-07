from django.conf import settings as _settings
from openvpnathome import get_frontend_path


def extra_template_dirs():
    if _settings.DEVELOPMENT:
        return [get_frontend_path('dist')]
    else:
        return []


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': extra_template_dirs(),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
