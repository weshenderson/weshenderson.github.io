#!/usr/bin/env bash

source "$(dirname $0)/artifact_list.sh"

USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'
INTERNAL_LINKS=()
SECURITY_OVERRIDES=('linkedin.com'
                    'bsky.app'
                    'makerworld.com')

for site in ${HTML_FILES[@]}; do
    LINK=$(grep -Po 'href="\K[^"]+' ${site} | grep "^http")
    INTERNAL_LINKS+=${LINK}
done

for url in ${INTERNAL_LINKS[@]}; do
    SKIP='false'
    for override in ${SECURITY_OVERRIDES[@]}; do
        if echo "${url}" | grep -q "${override}"; then
            SKIP='true'
        fi
    done

    if [ "${SKIP}" == "false" ]; then
        if ! curl -skIL -A "${USER_AGENT}" ${url} | awk '/HTTP/ {print $2}' | grep -q '^20'; then
            exit 67
        fi
    fi
done
