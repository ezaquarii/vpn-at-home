from openvpnathome.settings import USER_SETTINGS

EMAIL_BACKEND = 'openvpnathome.mail.ConfigurableEmailBackend'
EMAIL_ENABLED = USER_SETTINGS.email_enabled
EMAIL_HOST = USER_SETTINGS.email_smtp_server
EMAIL_PORT = USER_SETTINGS.email_smtp_server_port
EMAIL_HOST_USER = USER_SETTINGS.email_smtp_user
EMAIL_HOST_PASSWORD = USER_SETTINGS.email_smtp_password
SERVER_EMAIL = USER_SETTINGS.email_server_from
ADMINS = [('', email) for email in USER_SETTINGS.email_admin_emails]
