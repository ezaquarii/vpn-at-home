#!/bin/sh

export ROOT_DIR=$(readlink -f $(dirname "$0")/../)
export APP_DIR="${ROOT_DIR}/backend/"
export VIRTUALENV_DIR="${ROOT_DIR}/env/"
export STATIC_DIR="${ROOT_DIR}/static/"
export DATABASE_DIR="${ROOT_DIR}/db/"
export SETTINGS_FILE="${ROOT_DIR}/settings.json"
export MANAGE=${APP_DIR}/manage.py

if [ ${USER} = "root" ]; then
    APP_USER=openvpnathome
else
    APP_USER=${USER}
fi
