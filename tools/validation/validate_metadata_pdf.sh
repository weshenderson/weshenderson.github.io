#!/usr/bin/env bash

source "$(dirname $0)/artifact_list.sh"

if ! python ./tools/metadata_viewer_pdf.py | grep -q "${GITHUB_SHA}"; then
    exit 42
fi