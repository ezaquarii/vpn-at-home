#!/bin/bash
#
# Debian script implementing postinst and prerm functionality.
# Package scripts should call this script.
#

. $(dirname $0)/common.sh

check_is_root() {
    if [ ! "${USER}" = "root" ]; then
        echo "This script requires root permissions"
        exit 1
    fi
}

create_user() {
    if [ -z $(getent passwd ${APP_USER}) ]; then
        echo "Creating user ${APP_USER}"
        useradd --system ${APP_USER}
    fi
}

create_database_dir() {
    mkdir -p "${ROOT_DIR}"
    chown ${APP_USER}:${APP_USER} "${ROOT_DIR}"
    chmod 0775 "${ROOT_DIR}"
}

remove_database_dir() {
    rm -rf "${ROOT_DIR}"
}

remove_user() {
    if [ $(getent passwd ${APP_USER}) ]; then
        echo "Removing user ${APP_USER}"
        userdel ${APP_USER}
    fi
}

set_manage_py_interpreter() {
    sed -i 's/\/usr\/bin\/env.*/\/srv\/openvpnathome\/env\/bin\/python3/' "${ROOT_DIR}/backend/manage.py"
}

bootstrap_app() {
    # Run bootstrap with default login/password for admin.
    # Generate settings; settings should be writable by root,
    # so it can't be overwritten by malfunctioning app.
    # It is safe to re-run them - bootstrap and configure are idempotent.
    ${MANAGE} bootstrap
    ${MANAGE} configure
    chown -R ${APP_USER}:${APP_USER} "${DATABASE_DIR}"
    chown root:${APP_USER} "${SETTINGS_FILE}"
    chmod 0640 "${SETTINGS_FILE}"
}

set -e

check_is_root

case "$1" in
    postinst)
        create_user
        create_database_dir
        set_manage_py_interpreter
        bootstrap_app
        systemctl enable openvpnathome
        systemctl start openvpnathome.service
    ;;

    prerm)
        systemctl stop openvpnathome.service
        systemctl disable openvpnathome
        remove_user
    ;;

    *)
        echo "Script called with unknown argument \`$1'" >&2
        exit 1
    ;;
esac
