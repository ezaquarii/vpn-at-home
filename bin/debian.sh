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
        create_database_dir
        create_logs_dir
        set_manage_py_interpreter
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
