#!/bin/bash

set -euo pipefail
# enable debug
# set -x

echo "configuring sqs"
echo "==================="

LOCALSTACK_ENDPOINT=http://localhost:4566
AWS_REGION=us-east-1

# https://docs.aws.amazon.com/cli/latest/reference/sqs/create-queue.html
create_topic() {
	local TOPIC_NAME=$1
	awslocal sns create-topic --name="$TOPIC_NAME" --region "$AWS_REGION" --endpoint-url="$LOCALSTACK_ENDPOINT"
}

create_topic local-Topic
