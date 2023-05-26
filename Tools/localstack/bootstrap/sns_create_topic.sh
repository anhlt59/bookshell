#!/usr/bin/env bash

set -euo pipefail

# enable debug
# set -x


echo "configuring sqs"
LOCALSTACK_ENDPOINT=http://localhost:4566
AWS_REGION=us-east-1

# https://docs.aws.amazon.com/cli/latest/reference/sns/create-topic.html
create_topic() {
	local NAME=$1
	awslocal sns create-topic \
	    --name "$NAME" \
	    --region "$AWS_REGION" \
	    --endpoint-url "$LOCALSTACK_ENDPOINT"
}

create_topic "Publib-Topic"
