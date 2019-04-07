#!/usr/bin/env bash
#
# Ansible VPN deployment script. You can use it to deploy OpenVPN
# either on your localhost machine or remote machine (address taken
# from server config)
#

function print_usage() {
    echo "Usage:"
    echo "$0 [--help|--local|--host HOST]"
    echo ""
    echo "--help  - usage"
    echo "--local - deploy OpenVPN server on the current machine (localhost)"
    echo "--host  - deploy selected OpenVPN server only"
    echo
}

ARGS=$(getopt -n "$0" -o fhs --longoptions help,host:,local -- "$@")
eval set -- "${ARGS}"

LOCALHOST="no"
LIMIT_OPT=""

while true; do

    case "$1" in
        --help|-h)
            print_usage;
            exit 0
        ;;

        --host)
            LIMIT_OPT="--limit=$2"
            shift 2
        ;;

        --local)
            LOCALHOST="yes"
            shift
        ;;

        --)
            shift
            break
        ;;
    esac

done

export BIN_DIR=$(dirname $0)
export ANSIBLE_DIR="${BIN_DIR}/../../ansible"
export SSH_KEY_DIR="${PWD}/data/ssh"

if [ "${LOCALHOST}" = "yes" ]; then
    echo "Deploying on localhost"
    ansible-playbook -i "${BIN_DIR}/local_inventory.sh" -K "${ANSIBLE_DIR}/local.yml"
    exit $?
else
    ansible-playbook --inventory "${BIN_DIR}/inventory.sh" \
                     --private-key "${SSH_KEY_DIR}/vpnathome_server_deployment_key" \
                     --ssh-common-args "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" \
                     ${LIMIT_OPT} \
                     "${ANSIBLE_DIR}/remote.yml"
    exit $?
fi
