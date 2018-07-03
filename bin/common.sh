#!/bin/sh
#
# This script is sourced from all utility scripts
# and provides common environment variables and functions.
#

export ROOT_DIR=$(readlink -f $(dirname "$0")/../)
export APP_DIR="${ROOT_DIR}/backend/"
export VIRTUALENV_DIR="${ROOT_DIR}/env/"
export STATIC_DIR="${ROOT_DIR}/static/"
export DATABASE_DIR="${ROOT_DIR}/db/"
export DATABASE_FILE="${DATABASE_DIR}/db.sqlite3"
export SETTINGS_FILE="${ROOT_DIR}/settings.json"
export LOGS_DIR="${ROOT_DIR}/logs"
export BIN_DIR="${ROOT_DIR}/bin"
export ANSIBLE_DIR="${ROOT_DIR}/ansible"

export PYTHON="${VIRTUALENV_DIR}/bin/python3"
export MANAGE=${APP_DIR}/manage.py

if [ ${USER} = "root" ]; then
    APP_USER=openvpnathome
else
    APP_USER=${USER}
fi

export OWNERSHIP=${APP_USER}:${APP_USER}

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
    echo "Creating database dir ${DATABASE_DIR} owned by ${OWNERSHIP}"
    mkdir -p --mode 0770 "${DATABASE_DIR}"
    chown ${OWNERSHIP} "${DATABASE_DIR}"
}

remove_database_dir() {
    rm -rf "${ROOT_DIR}"
}

set_database_permissions() {
    echo "Setting database permissions"
    chown -R ${OWNERSHIP} "${DATABASE_DIR}"
    chmod 0750 "${DATABASE_DIR}"
    chmod 0640 "${DATABASE_FILE}"
}

set_config_permissions() {
    echo "Setting settings.json permissions"
    chown ${OWNERSHIP} "${SETTINGS_FILE}"
    chmod 0440 "${SETTINGS_FILE}"
}


create_logs_dir() {
    echo "Creating logs dir owned by ${OWNERSHIP}"
    mkdir -p --mode 0770 "${LOGS_DIR}"
    chown ${OWNERSHIP} "${LOGS_DIR}"
}

remove_user() {
    if [ $(getent passwd ${APP_USER}) ]; then
        echo "Removing user ${APP_USER}"
        userdel ${APP_USER}
    fi
}

set_manage_py_interpreter() {
    echo "Setting virtual environment interpreter in ${ROOT_DIR}/backend"
    sed -i 's/\/usr\/bin\/env.*/\/srv\/openvpnathome\/env\/bin\/python3/' "${ROOT_DIR}/backend/manage.py"
}
