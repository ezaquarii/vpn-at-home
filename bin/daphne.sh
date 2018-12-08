#!/usr/bin/env bash
#
# Starts ASGI server process. This can be used either manually or from
# systemd service script.
#

set -e
ARGS=$(getopt -n "$0" -o b: --longoptions help,bind:,local -- "$@")
eval set -- "${ARGS}"

BIND_ADDRESS=127.0.0.1
PORT=8000

while true; do
    case "$1" in
        --help|-h)
            echo "$0 [--bind ADDRESS] [--port PORT]"
            echo
            echo "Run Daphne server on http://ADDRESS:PORT"
            echo "By default Daphne will listen on 127.0.0.1:8000"
            exit 0
        ;;

        --bind|-b)
            BIND_ADDRESS="$2"
            shift 2
        ;;

        --port|-p)
            PORT="$2"
            shift 2
        ;;

        --) shift; break ;;
    esac

done

. $(dirname $0)/common.sh
. ${VIRTUALENV_DIR}/bin/activate

echo "Starting daphne:"
echo " * user:         ${APP_USER}"
echo " * group:        ${APP_USER}"
echo " * working dir:  ${APP_DIR}"
echo " * listening on: ${BIND_ADDRESS}:${PORT}"
echo ""

create_data_dirs
cd "${APP_DIR}"
exec daphne --port ${PORT} \
            --bind ${BIND_ADDRESS} \
            --access-log "${LOGS_DIR}/daphne.log" \
            openvpnathome.asgi:application
