#!/bin/sh
#
# Starts uWSGI process. This can be used either manually or from
# systemd service script.
#

. $(dirname $0)/common.sh
. ${VIRTUALENV_DIR}/bin/activate

echo "Starting daphne:"
echo " * user ${APP_USER}"
echo " * group ${APP_USER}"
echo " * working dir ${APP_DIR}"
echo ""

cd ${APP_DIR}
exec daphne --port 8000 \
            --bind 127.0.0.1 \
            --access-log ${LOGS_DIR}/daphne.log \
            openvpnathome.asgi:application

