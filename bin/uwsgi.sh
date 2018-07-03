#!/bin/sh
#
# Starts uWSGI process. This can be used either manually or from
# systemd service script.
#

. $(dirname $0)/common.sh
. ${VIRTUALENV_DIR}/bin/activate

echo "Starting uwsgi:"
echo " * user ${APP_USER}"
echo " * group ${APP_USER}"
echo " * working dir ${APP_DIR}"
echo ""

exec uwsgi --ini ${APP_DIR}/uwsgi.ini \
           --chdir ${APP_DIR} \
           --static-map "/static=${STATIC_DIR}" \
           --uid ${APP_USER} \
           --gid ${APP_USER} \
           --logger file:logfile=${LOGS_DIR}/uwsgi.log,maxsize=10485760
