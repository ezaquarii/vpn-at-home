#!/usr/bin/env bash
#
# Ansible VPN deployment script. You can use it to deploy OpenVPN
# either on your localhost machine or remote machine (address taken
# from server config)
#

. $(dirname $0)/common.sh

if [ -z "$1" ]; then
    echo "Usage:"
    echo "$0 [local | remote]"
    echo ""
    echo "local  - deploy OpenVPN server on the current machine (localhost)"
    echo "remote - deploy OpenVPN server on remote machine (hostname from server configuration)"
    exit 0
fi


if [ "${1}" = "local" ]; then
    echo "Deploying on localhost"
    ansible-playbook -i "${BIN_DIR}/local_inventory.sh" -K "${ANSIBLE_DIR}/local.yml"
    exit $?
fi

if [ "${1}" = "remote" ]; then
    ansible-playbook --inventory "${BIN_DIR}/inventory.sh" \
                     --private-key "${SSH_KEY_DIR}/openvpnathome_server_deployment_key" \
                     --ssh-common-args "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" \
                     "${ANSIBLE_DIR}/remote.yml"
    exit $?
fi
