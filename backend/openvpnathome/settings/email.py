from openvpnathome.settings import USER_SETTINGS

EMAIL_ENABLED = USER_SETTINGS.email_enabled
EMAIL_HOST = USER_SETTINGS.email_smtp_server
EMAIL_PORT = USER_SETTINGS.email_smtp_server_port
EMAIL_HOST_USER = USER_SETTINGS.email_smtp_user
EMAIL_HOST_PASSWORD = USER_SETTINGS.email_smtp_password
EMAIL_FROM = USER_SETTINGS.email_from
EMAIL_TO_ADMIN = USER_SETTINGS.email_to
