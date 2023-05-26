#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

BASE_DIR=$(cd $(dirname $(dirname "$0")); pwd)

echo "Set environment variables"
export $(xargs <"${BASE_DIR}/.env.local")

echo "Start docker-compose"
docker-compose -f "${BASE_DIR}/docker-compose.yml" up -d

echo "Setup dynamodb local"
python "${BASE_DIR}/localstack/dynamodb/create_table.py"

echo "Setup rds local"
python "${BASE_DIR}/localstack/rds/create_table.py"
