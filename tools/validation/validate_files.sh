#!/usr/bin/env bash

source "$(dirname $0)/artifact_list.sh"

for file in ${FILES[@]}; do
    if [ ! -f ${file} ]; then
        echo "File not found: ${file}"
        exit 1
    fi
done