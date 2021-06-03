#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

BASE_DIR=$(cd $(dirname $(dirname "$0")); pwd)

echo "Set environment variables"
export $(xargs <"${BASE_DIR}/.env.local")

# if docker containers are not running, then start them
if [[ (! "$(docker ps -q -f name=localstack)") || (! "$(docker ps -q -f name=rds-local)") || (! "$(docker ps -q -f name=dynamodb-local)") ]]; then
    bash "${BASE_DIR}/localstack/setup.sh"
fi

echo "Start serverless local"
npx sls offline start -c serverless.yml --stage local
