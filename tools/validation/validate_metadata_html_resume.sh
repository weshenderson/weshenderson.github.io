#!/usr/bin/env bash

source "$(dirname $0)/artifact_list.sh"

if ! grep 'Alea Build Information' ${HTML_RESUME}; then
    exit 6
fi

if grep 'ALEA_BUILD' ${HTML_RESUME}; then
    exit 7
fi

if grep 'ALEA_RUN_ID' ${HTML_RESUME}; then
    exit 8
fi

if grep 'ALEA_ATTEMPT' ${HTML_RESUME}; then
    exit 9
fi

if grep 'ALEA_COMMIT' ${HTML_RESUME}; then
    exit 10
fi

if grep 'ALEA_DATE' ${HTML_RESUME}; then
    exit 11
fi

#if ! grep "${BUILD_SHA}" ${HTML_RESUME}; then
#    echo "RESUME: ${HTML_RESUME}"
#    echo "SHA: ${BUILD_SHA}"
#    echo "MATCH: $(grep 'Commit' ${HTML_RESUME})"
#    exit 12
#fi