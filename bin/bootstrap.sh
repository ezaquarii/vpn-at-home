#!/usr/bin/env bash
#
# This script performs application setup: db and user creation, etc.
# You should call it after installation to finalize the app deployment.
#

. $(dirname $0)/common.sh

print_usage() {
    echo "OpenVPN@Home bootstrapping utility."
    echo ""
    echo "Usage:"
    echo "  $0 admin@email [admin_password]"
    echo ""
    echo "If no admin password is provided, you will be asked for it."
    echo "This is useful if you are concerned about shell history."
    return 0
}

ask_for_password() {
    read -s -p "Provide admin password: (no echo) " PASSWORD
    echo
    read -s -p "Repeat the password:    (no echo) " PASSWORD_CHECK
    echo
    if [ "${PASSWORD}" != "${PASSWORD_CHECK}" ]; then
        echo "Passwords do not match. Plesae try again."
        exit 1
    fi

    if [ ${#PASSWORD} -lt 8 ]; then
        echo "Password must be at least 8 characters long. Please try again."
        exit 1
    fi
}


bootstrap_default_config() {
    ${PYTHON} ${MANAGE} configure --accept
    echo "Database init can take a bit of time... Please be patient."
    mkdir -p "${DATABASE_DIR}"
    ${PYTHON} ${MANAGE} migrate

    echo "Creating admin account $1 $2"
    ${PYTHON} ${MANAGE} set_admin "${1}" "${2}"
}

if [ -z "$1" ]; then
    print_usage
    exit 0
else
    ADMIN="$1"
fi

if [ -z "$2" ]; then
    ask_for_password
else
    echo "Password supplied from commandline. Make sure it is not stored in shell history."
    PASSWORD="$2"
fi

create_database_dir
create_logs_dir
bootstrap_default_config "${ADMIN}" "${PASSWORD}"

if [ "${USER}" == "root" ]; then
    set_database_permissions
    set_config_permissions
fi

if [ "${USER}" != "root" ]; then
    echo "Restarting service skipped."
else
    echo "Restarting server..."
    systemctl restart openvpnathome.service
fi

echo ""
echo "OpenVPN@Home is ready. Enjoy!"
echo ""
