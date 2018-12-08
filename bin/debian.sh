#!/bin/bash
#
# Debian script implementing postinst and prerm functionality.
# Package scripts should call this script.
#

. $(dirname $0)/common.sh

set -e

check_is_root

case "$1" in
    postinst)
        create_user
        create_data_dirs
        set_data_permissions
        set_manage_py_interpreter
        if [[ -x "$(command -v systemctl)" ]]; then
            systemctl enable openvpnathome
            systemctl start openvpnathome.service
        fi
    ;;

    prerm)
        if [[ -x "$(command -v systemctl)" ]]; then
            systemctl stop openvpnathome.service
            systemctl disable openvpnathome
        fi
        remove_user
    ;;

    *)
        echo "Script called with unknown argument \`$1'" >&2
        exit 1
    ;;
esac
