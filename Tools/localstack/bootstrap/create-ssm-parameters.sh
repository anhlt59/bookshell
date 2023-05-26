#!/usr/bin/env bash

set -euo pipefail

echo "configuring ssm parameter store"
echo "==================="

LOCALSTACK_ENDPOINT=http://localhost:4566
AWS_REGION=us-east-1

# https://docs.aws.amazon.com/cli/latest/reference/ssm/put-parameter.html
create_parameter() {
	local NAME=$1
	local TYPE=$2
	local VALUE=$3
	awslocal ssm put-parameter \
	    --name "$NAME" \
	    --type "$TYPE" \
	    --value "$VALUE" \
	    --region "$AWS_REGION" \
	    --endpoint-url "$LOCALSTACK_ENDPOINT"
}

create_parameter /local/foo String bar
