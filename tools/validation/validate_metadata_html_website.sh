#!/usr/bin/env bash
set -e

source "$(dirname $0)/artifact_list.sh"

if ! grep 'Alea Build Information' ${WEBSITE}; then
    exit 6
fi

if grep 'ALEA_BUILD' ${WEBSITE}; then
    exit 7
fi

if grep 'ALEA_RUN_ID' ${WEBSITE}; then
    exit 8
fi

if grep 'ALEA_ATTEMPT' ${WEBSITE}; then
    exit 9
fi

if grep 'ALEA_COMMIT' ${WEBSITE}; then
    exit 10
fi

if grep 'ALEA_DATE' ${WEBSITE}; then
    exit 11
fi

if ! grep "${GITHUB_SHA}" ${WEBSITE}; then
    exit 12
fi