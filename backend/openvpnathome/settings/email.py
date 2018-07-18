from openvpnathome.settings import USER_SETTINGS

EMAIL_BACKEND = 'openvpnathome.mail.ConfigurableEmailBackend'
EMAIL_ENABLED = USER_SETTINGS.email_enabled
SERVER_EMAIL = USER_SETTINGS.email_server_from
ADMINS = [('', email) for email in USER_SETTINGS.email_admin_emails]

#
# Configured dynamically via management.Settings:
#
# EMAIL_HOST
# EMAIL_PORT
# EMAIL_HOST_USER
# EMAIL_HOST_PASSWORD
#
