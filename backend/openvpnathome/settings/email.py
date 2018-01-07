EMAIL_ENABLED = False
EMAIL_HOST = 'localhost'
EMAIL_PORT = '25'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_FROM = ''
EMAIL_TO_ADMIN = ''

try:
    from openvpnathome.config import EMAIL_ENABLED
    from openvpnathome.config import EMAIL_HOST
    from openvpnathome.config import EMAIL_PORT
    from openvpnathome.config import EMAIL_HOST_USER
    from openvpnathome.config import EMAIL_HOST_PASSWORD
    from openvpnathome.config import EMAIL_FROM
    from openvpnathome.config import EMAIL_TO_ADMIN
except:
    pass
