#!/usr/bin/env bash

source "$(dirname $0)/artifact_list.sh"

if ! jq -e .meta.buildData.Commit ${JSON_RESUME}; then
    exit 6
fi
