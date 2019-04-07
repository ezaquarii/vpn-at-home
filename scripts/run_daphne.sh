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

echo "Activating Python virtualenv"
export VPNATHOME_BIN_DIR=$(dirname $0)
. ${VPNATHOME_BIN_DIR}/activate

mkdir -p data/logs/

echo "Starting daphne:"
echo " * user:              ${USER}"
echo " * group:             ${USER}"
echo " * working dir:       ${PWD}"
echo " * listening on:      ${BIND_ADDRESS}:${PORT}"
echo " * vpnathome bin dir: ${VPNATHOME_BIN_DIR}"
echo ""

exec daphne --port ${PORT} \
            --bind ${BIND_ADDRESS} \
            --access-log "data/logs/daphne.log" \
            vpnathome.asgi:application
