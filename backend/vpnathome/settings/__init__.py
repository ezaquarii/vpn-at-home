"""
This module contains all app configuration.

Configuration is split into individual, topic files.
Some settings can be overwritten by private configuration file
located in main app directory ('settings.json')

You should not edit this file (usually). If you want to alter
configuration, check private ``settings.json`` file first.
"""

import copy
import json
from os import access, R_OK, getcwd
from os.path import isfile
from vpnathome import get_data_path as _get_data_path
from vpnathome.utils import get_nested_item

SETTINGS_FILE_PATH = _get_data_path("settings.json")

DEFAULT_USER_SETTINGS = {
    '__version__': 1,
    '__doc__': 'This is the application settings file. Do not modify Python files. '
               'Review it and change configured to True.',
    'configured': False,
    'development': True,
    'debug_toolbar_enabled': False,
    'secret_key': 'secret-key-not-set',
    'allowed_hosts': ['*'],
    'internal_ips': ['127.0.0.1'],
    'email': {
        '__doc__': 'Django e-mail backend configuration. '
                   'Make sure you set server_from and admin_emails to correct values.',
        'enabled': True,
        'server_from': "no-reply@vpnathome.localdomain",
        'admin_emails': [],
        'smtp': {
            'server': None,
            'port': 587,
            'login': None,
            'password': None,
        },
    },
    'database': {
        '__doc__': "This object will be put verbatim into Django DATABASES['default'] setting. See Django DATABASES documentation.",
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}


class UserSettings(object):

    def __init__(self, settings_file_path=SETTINGS_FILE_PATH, settings=None):
        self.settings_file_path = settings_file_path
        if settings:
            self._settings = settings
        elif self.has_settings_file:
            with open(self.settings_file_path) as settings_file:
                self._settings = json.load(settings_file)
        else:
            self._settings = copy.deepcopy(DEFAULT_USER_SETTINGS)

    def get(self, path):
        try:
            result = get_nested_item(self._settings, path)
        except KeyError:
            result = get_nested_item(DEFAULT_USER_SETTINGS, path)
        # returned object must be safely added to django settings; django modifies settings dictionaries,
        # so it must have a private, non-shared copy
        return copy.deepcopy(result)

    def write(self):
        with open(self.settings_file_path, 'w') as of:
            json.dump(self._settings, of, indent=4)

    @property
    def is_configured(self):
        return self.get('configured')

    @property
    def has_settings_file(self):
        return self.settings_file_path is not None\
               and isfile(self.settings_file_path)\
               and access(self.settings_file_path, R_OK)

    @property
    def email_enabled(self):
        return self.get('email.enabled')

    @property
    def email_smtp_server(self):
        return self.get('email.smtp.server')

    @property
    def email_smtp_port(self):
        return self.get('email.smtp.port')

    @property
    def email_smtp_login(self):
        return self.get('email.smtp.login')

    @property
    def email_smtp_password(self):
        return self.get('email.smtp.password')

    @property
    def email_server_from(self):
        return self.get('email.server_from')

    @property
    def email_admin_emails(self):
        return self.get('email.admin_emails')

    @property
    def database(self):
        return self.get('database')

    @property
    def secret_key(self):
        return self.get('secret_key')

    @property
    def allowed_hosts(self):
        return self.get('allowed_hosts')

    @property
    def internal_ips(self):
        return self.get('internal_ips')

    @property
    def development(self):
        return self.get('development')

    @property
    def debug_toolbar_enabled(self):
        return self.get('debug_toolbar_enabled')

    @property
    def database_file_path(self):
        if 'sqlite3' in self.database['ENGINE'] and ':memory:' not in self.database['NAME']:
            return self.database['NAME']
        else:
            return None


USER_SETTINGS = UserSettings(settings_file_path=SETTINGS_FILE_PATH)
