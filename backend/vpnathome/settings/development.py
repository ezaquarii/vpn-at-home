from vpnathome.settings import USER_SETTINGS

DEVELOPMENT = USER_SETTINGS.development
DEBUG = USER_SETTINGS.development
DEBUG_TOOLBAR_ENABLED = USER_SETTINGS.debug_toolbar_enabled and USER_SETTINGS.development
