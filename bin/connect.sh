#!/bin/bash
#
# This script is used by OpenVPN server to obtain extra config options
# on client's connection.
#
# This script should be executable by nobody (OpenVPNs runtime user).
#
# See --client-connect in OpenVPN manual.
#

. $(dirname $0)/common.sh

echo "Dupa!"

if [ -z "${common_name}" ]; then
    echo "No common_name environment variable set."
    return 1
fi

"${PYTHON}" "${MANAGE}" generate_client_config --common-name "${common_name}" -o "${1}"

exit $?
