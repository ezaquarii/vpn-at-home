DEVELOPMENT = False

try:
    from openvpnathome.config import DEVELOPMENT
except:
    pass

DEBUG = DEVELOPMENT
DEBUG_TOOLBAR_ENABLED = DEVELOPMENT
