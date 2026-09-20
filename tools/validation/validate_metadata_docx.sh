#!/usr/bin/env bash

source "$(dirname $0)/artifact_list.sh"

if ! python ./tools/metadata_viewer_docx.py | grep -q "${GITHUB_SHA}"; then
    echo "RESUME: ${DOCX_RESUME}"
    echo "SHA: ${GITHUB_SHA}"
    echo "MATCH: $(grep 'Commit' ${DOCX_RESUME})"
    exit 43
fi