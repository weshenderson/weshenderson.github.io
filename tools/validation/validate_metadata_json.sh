#!/usr/bin/env bash
set -e

source "$(dirname $0)/artifact_list.sh"

if ! grep 'buildData' ${JSON_RESUME}; then
    exit 6
fi

if ! grep "${GITHUB_SHA}" ${JSON_RESUME}; then
    exit 7
fi
