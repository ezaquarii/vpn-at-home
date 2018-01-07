from openvpnathome import get_root_path

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': get_root_path('db.sqlite3'),
    }
}

try:
    from openvpnathome.config import DATABASES
except:
    pass
