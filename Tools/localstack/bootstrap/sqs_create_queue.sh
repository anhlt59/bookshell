#!/usr/bin/env bash

set -euo pipefail

# enable debug
# set -x

echo "configuring sqs"
LOCALSTACK_ENDPOINT=http://localhost:4566
AWS_REGION=us-east-1
VISIBILITY_TIMEOUT=30

# https://docs.aws.amazon.com/cli/latest/reference/sqs/create-queue.html
create_queue() {
    local QUEUE_NAME=$1
    local ENABLE_FIFO=${2:-false}

    if [ "$ENABLE_FIFO" == false ]; then
        local ATTRIBUTES="VisibilityTimeout=${VISIBILITY_TIMEOUT}"
    else
        local ATTRIBUTES="VisibilityTimeout=${VISIBILITY_TIMEOUT},FifoQueue=true"
    fi

    awslocal sqs create-queue \
        --queue-name "$QUEUE_NAME" \
        --attributes "$ATTRIBUTES" \
        --region "$AWS_REGION" \
        --endpoint-url "$LOCALSTACK_ENDPOINT"
}

create_queue "di2_rds_data_queue" true
