#!/usr/bin/env bash
set -e

source "$(dirname $0)/artifact_list.sh"

for url in ${ENDPOINTS[@]}; do
    if ! curl -skIL ${url} | awk '/HTTP/ {print $2}' | grep '^20'; then
        exit 67
    fi
done