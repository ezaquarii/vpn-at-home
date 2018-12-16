from vpnathome.settings import USER_SETTINGS
from vpnathome import get_frontend_path


def extra_template_dirs():
    if USER_SETTINGS.development:
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
