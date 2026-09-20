#!/usr/bin/env bash
# Currently unused (WIP)

source "$(dirname $0)/artifact_list.sh"

if ! python ./tools/metadata_viewer_pdf.py | grep -q "${BUILD_SHA}"; then
    echo "RESUME: ${PDF_RESUME}"
    echo "SHA: ${BUILD_SHA}"
    echo "MATCH: $(grep 'Commit' ${PDF_RESUME})"
    exit 42
fi