#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

INVALID_STAGES=("local" "development" "production")

STAGE=${1:-local}
BASE_DIR=$(dirname "$(cd "$(dirname "$0")"; pwd)")


if [[ "${INVALID_STAGES[*]}" =~ ${STAGE} ]]; then
    echo Stage:  "$STAGE"
else
    echo Error: Invalid stage "$STAGE"
    echo - Valid stage are "${INVALID_STAGES[*]}"
    exit 1;
fi

cd "$BASE_DIR"
