#!/usr/bin/env bash

ENV_FILE='.build.parameters'
BASE_PATH="$(git rev-parse --show-toplevel)"

if [ -f /wsl ]; then
    COMPOSE_BIN='/mnt/c/Program Files/Docker/Docker/resources/bin/docker-compose'
else
    COMPOSE_BIN='docker-compose'
fi

function create-pdf-resume {
    pushd "${BASE_PATH}" &>/dev/null
        source ${ENV_FILE}
        cp ${RESUME} ${TMP}
        sed -i 's@<!-- H-ONLY -->.*<!-- /H-ONLY -->@@g' ${TMP}
    "${COMPOSE_BIN}" up
        rm -f ${TMP}
    popd &>/dev/null
}

create-pdf-resume
