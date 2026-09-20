#!/usr/bin/env bash

source "$(dirname $0)/artifact_list.sh"

if ! grep 'Alea Build Information' ${MD_RESUME}; then
    exit 6
fi

if grep 'ALEA_BUILD' ${MD_RESUME}; then
    exit 7
fi

if grep 'ALEA_RUN_ID' ${MD_RESUME}; then
    exit 8
fi

if grep 'ALEA_ATTEMPT' ${MD_RESUME}; then
    exit 9
fi

if grep 'ALEA_COMMIT' ${MD_RESUME}; then
    exit 10
fi

if grep 'ALEA_DATE' ${MD_RESUME}; then
    exit 11
fi

if ! grep "${GITHUB_SHA}" ${MD_RESUME}; then
    echo "RESUME: ${MD_RESUME}"
    echo "SHA: ${GITHUB_SHA}"
    echo "MATCH: $(grep 'Commit' ${MD_RESUME})"
    exit 12
fi