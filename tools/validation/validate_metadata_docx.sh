#!/usr/bin/env bash
# Currently unused (WIP)

source "$(dirname $0)/artifact_list.sh"

if ! python ./tools/metadata_viewer_docx.py | grep -q "${BUILD_SHA}"; then
    echo "RESUME: ${DOCX_RESUME}"
    echo "SHA: ${BUILD_SHA}"
    echo "MATCH: $(grep 'Commit' ${DOCX_RESUME})"
    exit 43
fi