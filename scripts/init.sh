#!/usr/bin/env bash

export BIN_DIR=$(readlink -f $(dirname "$0"))
export PATH=${BIN_DIR}:${PATH}

echo "Initializing VPN@Home in ${PWD}"
echo "Running init.sh from ${BIN_DIR}"

export APP_WORKING_DIR="${PWD}"
export DATA_DIR="${APP_WORKING_DIR}/data"
export DATABASE_DIR="${DATA_DIR}/db"
export LOGS_DIR="${DATA_DIR}/logs"
export SSH_KEY_DIR="${DATA_DIR}/ssh"
export SSH_DEPLOYMENT_KEY="${SSH_KEY_DIR}/vpnathome_server_deployment_key"

ARGS=$(getopt -n "$0" -o fhsd --longoptions help,force,no-smtp,development,smtp-server:,smtp-port:,smtp-login:,smtp-password: -- "$@")
eval set -- "${ARGS}"

print_usage() {
    echo "VPN@Home init utility."
    echo
    echo "Usage:"
    echo "  $0 [options] [admin@email [admin_password]]"
    echo
    echo "Database and settings will be initialized in current directory:"
    echo "${PWD}"
    echo
    echo "Options:"
    echo
    echo "  --help                    - displays this help message"
    echo "  --force, -f               - force settings.json rewrite"
    echo "  --no-smtp                 - DO NOT interactively ask for SMTP config using GNU Dialog"
    echo "  --development, -d         - initialized app for development"
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

    [[ ! -z "${NO_SMTP}"       ]] && CONFIG_ARGS="${CONFIG_ARGS} --no-smtp"
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

# Creates SMTP options for configure script
function create_smtp_config_opts() {
	if [[ "${SMTP_LOGIN}" ]]; then
		SMTP_LOGIN_OPT="--smtp-login ${SMTP_LOGIN}"
	fi

	if [[ "${SMTP_PASSWORD}" ]]; then
		SMTP_PASSWORD_OPT="--smtp-password ${SMTP_PASSWORD}"
	fi

	if [[ "${SMTP_PORT}" ]]; then
		SMTP_PORT_OPT="--smtp-port ${SMTP_PORT}"
	fi

	if [[ "${SMTP_SERVER}" ]]; then
		SMTP_SERVER_OPT="--smtp-server ${SMTP_SERVER}"
	fi

	if [[ "${ADMIN}" ]]; then
		ADMIN_EMAIL_OPT="--admin-email ${ADMIN}"
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

#
# Creates application data directories.
#
create_data_dirs() {
    mkdir -p "${DATA_DIR}"
    mkdir -p "${DATABASE_DIR}"
    mkdir -p "${LOGS_DIR}"
    mkdir -p "${SSH_KEY_DIR}"
}

#
# Create application deployment SSH key if not exists.
#
create_ssh_key() {
    mkdir -p "${SSH_KEY_DIR}"
    if [[ ! -f "${SSH_DEPLOYMENT_KEY}" ]]; then
        echo "Creating ssh key in ${SSH_KEY_DIR}"
        ssh-keygen -N '' -C VPN@Home -f "${SSH_DEPLOYMENT_KEY}"
    else
        echo "SSH deployment key already created. Skipping."
    fi
}


ASK_FOR_SMTP="yes"
SMTP_OPTS=""

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
            NO_SMTP_OPT="--no-smtp"
            shift
        ;;

        --development|-d)
            DEVELOPMENT_OPT="--development"
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

create_data_dirs
create_ssh_key
create_smtp_config_opts
manage.py configure --output data/settings.json \
					--accept \
					${DEVELOPMENT_OPT} \
					${NO_SMTP_OPT} \
					${ADMIN_EMAIL_OPT} \
					${SMTP_LOGIN_OPT} \
					${SMTP_PASSWORD_OPT} \
					${SMTP_SERVER_OPT} \
					${SMTP_PORT_OPT}
manage.py migrate
manage.py set_admin "${ADMIN}" "${PASSWORD}"
