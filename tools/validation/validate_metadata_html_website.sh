#!/usr/bin/env bash

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

if ! grep "${BUILD_SHA}" ${WEBSITE}; then
    echo "WEBSITE: ${WEBSITE}"
    echo "SHA: ${BUILD_SHA}"
    echo "MATCH: $(grep 'Commit' ${WEBSITE})"
    exit 12
fi