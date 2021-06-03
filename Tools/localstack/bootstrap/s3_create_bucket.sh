#!/usr/bin/env bash

set -euo pipefail

# enable debug
# set -x


echo "configuring s3"
LOCALSTACK_ENDPOINT=http://localhost:4566
AWS_REGION=us-east-1
S3_BUCKET_NAME=dev
LOCAL_DIR=/home/data/s3

# https://docs.aws.amazon.com/cli/latest/reference/s3/mb.html
create_bucket() {
	local NAME=$1
	awslocal s3 mb "s3://${NAME}" \
	    --region "$AWS_REGION" \
	    --endpoint-url "$LOCALSTACK_ENDPOINT"
}

# https://docs.aws.amazon.com/cli/latest/reference/s3/cp.html
put_object() {
	local BUCKET_NAME=$1
	local FILE_PATH=$2
	local S3_OBJECT_KEY=$3

	awslocal s3 cp \
	    "$FILE_PATH" \
	    "s3://${BUCKET_NAME}/${S3_OBJECT_KEY}" \
	    --region "$AWS_REGION" \
	    --endpoint-url "$LOCALSTACK_ENDPOINT"
}

create_bucket "$S3_BUCKET_NAME"
