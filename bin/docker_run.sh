#!/bin/bash

DATA_VOLUME=data

function docker_run() {
    docker run \
        -p 127.0.0.1:8000:8000 \
        --volume ${DATA_VOLUME}:/srv/openvpnathome/data \
        -i \
        -t openvpnathome \
        $*
}

if [[ $1 = "run" ]]; then
    docker_run 	/srv/openvpnathome/bin/daphne.sh --bind 0.0.0.0
elif [[ "$1" = "bootstrap" ]]; then
    docker_run /srv/openvpnathome/bin/bootstrap.sh
else
    echo "$0 [bootstrap|run]"
fi
