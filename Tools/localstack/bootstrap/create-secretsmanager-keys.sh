#!/usr/bin/env bash

set -euo pipefail

echo "configuring secretsmanager"
echo "==================="

LOCALSTACK_ENDPOINT=http://localhost:4566
AWS_REGION=us-east-1

# https://docs.aws.amazon.com/cli/latest/reference/secretsmanager/create-secret.html
create_secret() {
    local NAME=$1
    local VALUE=$2
    awslocal secretsmanager create-secret \
        --name "$NAME" \
        --secret-string "$VALUE" \
        --region "$AWS_REGION" \
        --endpoint-url "$LOCALSTACK_ENDPOINT"
}

create_secret di2/AFR '{"x-api-key":"01234567-8910-1234-adb8-eefbbc900c32"}'
