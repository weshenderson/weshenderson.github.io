#!/usr/bin/env bash
set -e

source "$(dirname $0)/artifact_list.sh"

if ! python ./tools/metadata_viewer_docx.py | grep -q "${GITHUB_SHA}"; then
    exit 43
fi