# Django refuses to boot with empty key, so we place dummy
SECRET_KEY = 'dummy-secret-key-overwritten-in-private-config'

try:
    from openvpnathome.config import SECRET_KEY
except:
    pass
