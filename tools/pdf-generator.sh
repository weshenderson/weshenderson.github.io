#!/usr/bin/env bash

ENV_FILE='.env'
BASE_PATH="$(git rev-parse --show-toplevel)"

if [ -f /wsl ]; then
    COMPOSE_BIN='/mnt/c/Program Files/Docker/Docker/resources/bin/docker-compose'
else
    COMPOSE_BIN='docker-compose'
fi

function create-pdf-resume {
    pushd "${BASE_PATH}" &>/dev/null
        "${COMPOSE_BIN}" \
            --project-directory . \
            --env-file docker/pdf_resume/.env \
            --file docker/pdf_resume/docker-compose.yml \
            up --build
    popd &>/dev/null
}

create-pdf-resume
