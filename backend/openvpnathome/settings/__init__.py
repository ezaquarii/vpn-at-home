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
from os import access, R_OK
from os.path import isfile
from openvpnathome import get_root_path as _get_root_path
from openvpnathome.utils import get_nested_item

SETTINGS_FILE_PATH = _get_root_path("settings.json")

DEFAULT_USER_SETTINGS = {
    '__version__': 1,
    '__doc__': 'This is the application settings file. Do not modify Python files. '
               'Review it and change configured to True.',
    'configured': False,
    'development': False,
    'debug_toolbar_enabled': False,
    'secret_key': 'secret-key-not-set',
    'allowed_hosts': ['*'],
    'internal_ips': ['127.0.0.1'],
    'email': {
        '__doc__': 'server_email will be visible in From: for outgoing e-mails.',
        'enabled': False,
        'smtp_server': None,
        'smtp_server_port': 0,
        'smtp_user': '',
        'smtp_password': '',
        'server_from': None,
        'admin_emails': [],
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
            self._settings = DEFAULT_USER_SETTINGS.copy()

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
        return isfile(self.settings_file_path) and access(self.settings_file_path, R_OK)

    @property
    def email_enabled(self):
        return self.get('email.enabled')

    @property
    def email_smtp_server(self):
        return self.get('email.smtp_server')

    @property
    def email_smtp_server_port(self):
        return self.get('email.smtp_server_port')

    @property
    def email_smtp_user(self):
        return self.get('email.smtp_user')
    
    @property
    def email_smtp_password(self):
        return self.get('email.smtp_password')

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

USER_SETTINGS = UserSettings()
