from openvpnathome.settings import USER_SETTINGS

EMAIL_BACKEND = 'openvpnathome.mail.ConfigurableEmailBackend'
EMAIL_ENABLED = USER_SETTINGS.email_enabled
SERVER_EMAIL = USER_SETTINGS.email_server_from
ADMINS = [('', email) for email in USER_SETTINGS.email_admin_emails]

#
# Configurable backend is ignoring those settings; SMTP config is
# taken from DB, but those values will be used during db migration
#
EMAIL_HOST = USER_SETTINGS.email_smtp_server
EMAIL_PORT = USER_SETTINGS.email_smtp_port
EMAIL_HOST_USER = USER_SETTINGS.email_smtp_login
EMAIL_HOST_PASSWORD = USER_SETTINGS.email_smtp_password

