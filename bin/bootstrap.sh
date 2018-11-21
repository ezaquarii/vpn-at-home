#!/usr/bin/env bash

#
# This script performs application setup: db and user creation, etc.
# You should call it after installation to finalize the app deployment.
#

ADMIN=""
PASSWORD=""
SMTP_SERVER=""
SMTP_PORT="25"
SMTP_LOGIN=""
SMTP_PASSWORD=""
ASK_FOR_SMTP="yes"
FORCE=""

# Silence IDE warnings - those vars are set by common.sh
MANAGE=""
PYTHON=""
DATABASE_DIR=""

. $(dirname $0)/common.sh

ARGS=$(getopt -n "$0" -o fhs --longoptions force,no-smtp,smtp-server:,smtp-port:,smtp-login:,smtp-password: -- "$@")
eval set -- "${ARGS}"

print_usage() {
    echo "OpenVPN@Home bootstrapping utility."
    echo
    echo "Usage:"
    echo "  $0 [options] [admin@email [admin_password]]"
    echo
    echo "Options:"
    echo
    echo "  --help                    - displays this help message"
    echo "  --force, -f               - force settings.json rewrite"
    echo "  --no-smtp                 - DO NOT interactively ask for SMTP config using GNU Dialog"
    echo
    echo "Set SMTP options in settings.json. SMTP will be configured during DB migrations."
    echo "If all SMTP settings are provided via command line interactive form will be disabled"
    echo
    echo "  --smtp-server   HOST      - set SMTP server"
    echo "  --smtp-port     PORT      - set SMTP server port (TLS)"
    echo "  --smtp-login    LOGIN     - set SMTP server login"
    echo "  --smtp-password PASSWORD  - set SMTP server password (beware of shell history!)"
    echo
    return 0
}

bootstrap_default_config() {
    if [ -z "$ADMIN" ] || [ -z "$PASSWORD" ]; then
        echo "Runtime error: ADMIN and PASSWORD must be set"
        exit 255
    fi

    CONFIG_ARGS="--accept --admin-email \"${ADMIN}\""

    [[ ! -z "${SMTP_SERVER}"   ]] && CONFIG_ARGS="${CONFIG_ARGS} --smtp-server \"${SMTP_SERVER}\""
    [[ ! -z "${SMTP_PORT}"     ]] && CONFIG_ARGS="${CONFIG_ARGS} --smtp-port \"${SMTP_PORT}\""
    [[ ! -z "${SMTP_LOGIN}"    ]] && CONFIG_ARGS="${CONFIG_ARGS} --smtp-login \"${SMTP_LOGIN}\""
    [[ ! -z "${SMTP_PASSWORD}" ]] && CONFIG_ARGS="${CONFIG_ARGS} --smtp-password \"${SMTP_PASSWORD}\""
    [[ ! -z "${FORCE}"         ]] && CONFIG_ARGS="${CONFIG_ARGS} --force"

    echo "Creating settings.json file."
    eval ${PYTHON} ${MANAGE} configure ${CONFIG_ARGS}

    echo "Database init can take a bit of time... Please be patient."
    mkdir -p "${DATABASE_DIR}"
    ${PYTHON} ${MANAGE} migrate

    echo "Creating admin account ${ADMIN} \"${PASSWORD}\""
    eval ${PYTHON} ${MANAGE} set_admin "${ADMIN}" \"${PASSWORD}\"
}

# Interactively ask for SMTP server configuration using GNU Dialog.
# It terminates the script if SMTP configuration is not fully
# provided.
ask_for_smtp_config() {
    exec 3>&1
    local VALUES=$(dialog --title "SMTP account configuration" \
                    --form "SMTP account is needed to send diagnostic e-mails and configuration files to users." \
                    12 50 0 \
                    "SMTP server" 1 1 "${SMTP_SERVER}"   1 15 30 0\
                    "Port (TLS)"  2 1 "${SMTP_PORT}"     2 15 30 0\
                    "Login:"      3 1 "${SMTP_LOGIN}"    3 15 30 0\
                    "Password"    4 1 "${SMTP_PASSWORD}" 4 15 30 0\
                    2>&1 1>&3)
    exec 3>&-

    # Values returned in lines - use sed to break it into individual variables
    SMTP_SERVER=$(sed -n 1p <<< ${VALUES})
    SMTP_PORT=$(sed -n 2p <<< ${VALUES})
    SMTP_LOGIN=$(sed -n 3p <<< ${VALUES})
    SMTP_PASSWORD=$(sed -n 4p <<< ${VALUES})

    if ! is_smtp_configured; then
        echo "SMTP server is not configured. If you do not wish to have SMTP enabled, use --no-smtp option."
        exit 1
    fi
}

# Check if SMTP configuration is sane.
is_smtp_configured() {
    # All SMTP options must be set
    if [[ ! "${SMTP_SERVER}" ]] || [[ ! "${SMTP_PORT}" ]] || [[ ! "${SMTP_LOGIN}" ]] || [[ ! "${SMTP_PASSWORD}" ]]; then
        return 1
    else
        return 0
    fi
}

# Interactively ask for admin e-mail. It terminates the script
# if input is empty, but does not validate input otherwise.
ask_for_admin_email() {
    exec 3>&1
    ADMIN=$(dialog --title "Admin e-mail" \
                   --inputbox "" 7 50 "" \
                   2>&1 1>&3)
    exec 3>&-

    if [[ -z "${ADMIN}" ]]; then
        echo "Admin e-mail is required"
        exit 1
    fi
}

# Interactively ask for admin password twice.
# Passwords must match. If they don't match then
# terminate the script with error message.
ask_for_admin_password() {
    exec 3>&1
    PASSWORD=$(dialog --title "Admin account password" \
                      --insecure \
                      --passwordbox "" 7 50 \
                      2>&1 1>&3)

    PASSWORD_CHECK=$(dialog --title "Admin account password (repeat)" \
                            --insecure \
                            --passwordbox "" 7 50 \
                            2>&1 1>&3)
    exec 3>&-

    if [[ "${PASSWORD}" != "${PASSWORD_CHECK}" ]]; then
        echo "Passwords do not match. Plesae try again."
        exit 1
    fi

    if [[ ${#PASSWORD} -lt 8 ]]; then
        echo "Password must be at least 8 characters long. Please try again."
        exit 1
    fi
}

while true; do

    case "$1" in
        --help|-h)
            print_usage;
            exit 0
        ;;

        --force|-f)
            FORCE="1"
            shift
        ;;

        --no-smtp|-s)
            ASK_FOR_SMTP=""
            shift
        ;;

        --smtp-login)
            SMTP_LOGIN="$2"
            shift 2
        ;;

        --smtp-password)
            SMTP_PASSWORD="$2"
            shift 2
        ;;

        --smtp-server)
            SMTP_SERVER="$2"
            shift 2
        ;;

        --smtp-port)
            SMTP_PORT="$2"
            shift 2
        ;;

        --) shift; break ;;
    esac

done

if [[ -z "$1" ]]; then
    ask_for_admin_email
else
    ADMIN="$1"
fi

if [[ -z "$2" ]]; then
    ask_for_admin_password
else
    echo "Password supplied from commandline. Make sure it is not stored in shell history."
    PASSWORD="$2"
fi

if is_smtp_configured; then
    echo "Using supplied SMTP configuration"
else
    if [[ "${ASK_FOR_SMTP}" ]]; then
        ask_for_smtp_config
    else
        echo "SMTP configuration skipped"
    fi
fi

create_database_dir
create_logs_dir
bootstrap_default_config
create_ssh_key

if [[ "${USER}" == "root" ]]; then
    set_database_permissions
    set_config_permissions
    set_ssh_permissions
fi

if [[ "${USER}" != "root" ]]; then
    echo "Restarting service skipped."
else
    echo "Restarting server..."
    systemctl restart openvpnathome.service
fi

echo
echo "OpenVPN@Home is ready. Enjoy!"
echo
