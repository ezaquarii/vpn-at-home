#!/bin/sh
#
# This script is sourced from all utility scripts
# and provides common environment variables and functions.
#

export ROOT_DIR=$(readlink -f $(dirname "$0")/../)
export APP_DIR="${ROOT_DIR}/backend"
export DATA_DIR="${ROOT_DIR}/data"
export VIRTUALENV_DIR="${ROOT_DIR}/env"
export STATIC_DIR="${ROOT_DIR}/static"
export DATABASE_DIR="${DATA_DIR}/db/"
export DATABASE_FILE="${DATABASE_DIR}/db.sqlite3"
export SETTINGS_FILE="${DATA_DIR}/settings.json"
export LOGS_DIR="${DATA_DIR}/logs"
export BIN_DIR="${ROOT_DIR}/bin"
export ANSIBLE_DIR="${ROOT_DIR}/ansible"
export SSH_KEY_DIR="${DATA_DIR}/ssh"
export SSH_DEPLOYMENT_KEY="${SSH_KEY_DIR}/vpnathome_server_deployment_key"
export APP_HOME="${DATA_DIR}/home/"

export PYTHON="${VIRTUALENV_DIR}/bin/python3"
export MANAGE=${APP_DIR}/manage.py
export USER=$(whoami)

if [[ "${USER}" = "root" ]]; then
    APP_USER=vpnathome
else
    APP_USER=${USER}
fi

export OWNERSHIP=${APP_USER}:${APP_USER}

run_systemctl() {
    if [[ -x "$(command -v systemctl)" ]]; then
        systemctl $*
    else
        echo "Command systemctl is not available - skipping. Args: " $*
    fi
}

check_is_root() {
    if [[ ! "${USER}" = "root" ]]; then
        echo "This script requires root permissions"
        exit 1
    fi
}

create_user() {
    if [[ -z $(getent passwd ${APP_USER}) ]]; then
        echo "Creating user ${APP_USER}"
        useradd --system --home-dir "${APP_HOME}" "${APP_USER}"
        mkdir -p "${APP_HOME}"
        chmod 0700 "${APP_HOME}"
        chown ${OWNERSHIP} "${APP_HOME}"
    fi
}

create_data_dirs() {
    mkdir -p "${DATA_DIR}"
    mkdir -p "${DATABASE_DIR}"
    mkdir -p "${LOGS_DIR}"
}

set_data_permissions() {
    echo "Setting application data files permissions"
    chown -R ${OWNERSHIP} "${DATA_DIR}"
    chmod 0750 "${DATABASE_DIR}"  2> /dev/null || true
    chmod 0640 "${DATABASE_FILE}" 2> /dev/null || true
    chmod 0440 "${SETTINGS_FILE}" 2> /dev/null || true
    chmod 0700 "${SSH_KEY_DIR}"   2> /dev/null || true
    chmod 0600 "${SSH_KEY_DIR}"/* 2> /dev/null || true
}

remove_user() {
    if [[ $(getent passwd ${APP_USER}) ]]; then
        echo "Removing user ${APP_USER}"
        userdel ${APP_USER}
    fi
}

set_manage_py_interpreter() {
    echo "Setting virtual environment interpreter in ${ROOT_DIR}/backend"
    sed -i 's/\/usr\/bin\/env.*/\/srv\/vpnathome\/env\/bin\/python3/' "${ROOT_DIR}/backend/manage.py"
}

create_ssh_key() {
    mkdir -p "${SSH_KEY_DIR}"
    if [[ ! -f "${SSH_DEPLOYMENT_KEY}" ]]; then
        echo "Creating ssh key in ${SSH_KEY_DIR}"
        ssh-keygen -N '' -C VPN@Home -f "${SSH_DEPLOYMENT_KEY}"
    else
        echo "SSH deployment key already created. Skipping."
    fi
}

update_bad_domains() {
    $(MANAGE) update_bad_domains
}
