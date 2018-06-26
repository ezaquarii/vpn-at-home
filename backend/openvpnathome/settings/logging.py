from openvpnathome import get_root_path

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },

    'handlers': {
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': get_root_path('logs/django.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },

    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'django': {
            'handlers': ['logfile', 'mail_admins'],
            'level': 'INFO'
        },
        'django.server': {
            'handlers': ['logfile'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
