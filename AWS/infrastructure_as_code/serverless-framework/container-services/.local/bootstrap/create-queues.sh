#!/bin/bash

set -euo pipefail
# enable debug
# set -x


echo "configuring sqs"
echo "==================="

LOCALSTACK_ENDPOINT=http://localhost:4566
AWS_REGION=us-east-1


# https://docs.aws.amazon.com/cli/latest/reference/sqs/create-queue.html
create_queue() {
	local QUEUE_NAME=$1
	awslocal sqs create-queue --queue-name "$QUEUE_NAME" --attributes VisibilityTimeout=30 --region "$AWS_REGION" --endpoint-url="$LOCALSTACK_ENDPOINT"
}

create_queue local-Queue
