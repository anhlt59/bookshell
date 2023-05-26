#!/bin/bash

# Restore OpenSearch data from a snapshot
#
# optional arguments:
#   -r, --region: AWS region (default: us-east-1)
#   -s, --source: source stage (default: production)
#   -t, --target: target stage (default: testing)
#
# example: restore testing from a production snapshot
# $ ./scripts/opensearch_restore.sh -t testing -s production

set -o errexit
set -o pipefail
set -o nounset

# default value
REGION=us-east-1
TARGET_STAGE=testing
SOURCE_STAGE=production
SNAPSHOT_ROLE_ARN=arn:aws:iam::251623506909:role/TheSnapshotRole

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
  -r | --region)
    REGION="$2"
    shift # past argument
    shift # past value
    ;;
  -s | --source)
    SOURCE_STAGE="$2"
    shift
    shift
    ;;
  -t | --target)
    TARGET_STAGE="$2"
    shift
    shift
    ;;
  *) # unknown option
    shift
    ;;
  esac
done

echo "Target stage: $TARGET_STAGE"
echo "Source stage: $SOURCE_STAGE"

# Assume LambdaFunction role
ROLE_ARN="arn:aws:iam::251623506909:role/materially-lambda-${TARGET_STAGE}-LambdaFunctionRole"
source "$(dirname "$0")/assume_role.sh" "$ROLE_ARN"

# get OpenSearch endpoint
DOMAIN_NAME="materially-app-${TARGET_STAGE}"
OPENSEARCH_ENDPOINT=$(aws opensearch describe-domain --domain-name "$DOMAIN_NAME" --region "$REGION" |
  jq -r ".DomainStatus.Endpoint")
if [ "$OPENSEARCH_ENDPOINT" == null ]; then
  echo "OpenSearch domain ${DOMAIN_NAME} does not exists"
  exit 1
fi
echo "OpenSearch endpoint: $OPENSEARCH_ENDPOINT"

# get OpenSearch authentication
OPENSEARCH_AUTH_PARAMETER=/materially-app/${TARGET_STAGE}/OPENSEARCH_AUTH
OPENSEARCH_AUTH=$(aws ssm get-parameter --name "$OPENSEARCH_AUTH_PARAMETER" --region "$REGION" |
  jq -r ".Parameter.Value")
if [ "$OPENSEARCH_AUTH" == null ]; then
  echo "SSM parameter ${OPENSEARCH_AUTH_PARAMETER} does not exists"
  exit 1
fi

# get OpenSearch snapshot id
SNAPSHOT_ID=$(aws ssm get-parameter --name "/Lambdas/${SOURCE_STAGE}/LatestOpenSearchSnapshot" --region "$REGION" |
  jq -r ".Parameter.Value")
if [ "$SNAPSHOT_ID" == null ]; then
  echo "No snapshot found"
  exit 1
fi
echo "Snapshot Id: $SNAPSHOT_ID"

# https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-snapshots.html#managedomains-snapshot-restore
# delete materially index
echo "Deleting materially index"
set -e
curl -XDELETE "https://${OPENSEARCH_AUTH}@${OPENSEARCH_ENDPOINT}/materially" \
  --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
  --header "x-amz-security-token: $AWS_SESSION_TOKEN" \
  --aws-sigv4 "aws:amz:${REGION}:es"
sleep 30
set +e

# if the snapshot repository is not registered, then register the snapshot repository
OPENSEARCH_REPO="materially-${SOURCE_STAGE}-snapshots"
error=$(curl -XGET "https://${OPENSEARCH_AUTH}@${OPENSEARCH_ENDPOINT}/_snapshot/${OPENSEARCH_REPO}" \
  --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
  --header "x-amz-security-token: $AWS_SESSION_TOKEN" \
  --aws-sigv4 "aws:amz:${REGION}:es" | jq -r ".error")
if [ "$error" != null ]; then
  echo "Create a new repo"
  curl -XPUT "https://${OPENSEARCH_AUTH}@${OPENSEARCH_ENDPOINT}/_snapshot/${OPENSEARCH_REPO}" \
    --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
    --header "x-amz-security-token: $AWS_SESSION_TOKEN" \
    --aws-sigv4 "aws:amz:${REGION}:es" \
    -d "{\"type\" :\"s3\",\"settings\":{\"bucket\":\"materially-app-${TARGET_STAGE}-snapshots\",\"region\":\"${REGION}\",\"role_arn\":\"${SNAPSHOT_ROLE_ARN}\"}}" \
    -H 'Content-Type: application/json'
fi

# restore from a snapshot
echo "Restoring snapshot: $SNAPSHOT_ID"
curl -XPOST "https://${OPENSEARCH_AUTH}@${OPENSEARCH_ENDPOINT}/_snapshot/${OPENSEARCH_REPO}/${SNAPSHOT_ID}/_restore" \
  --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
  --header "x-amz-security-token: $AWS_SESSION_TOKEN" \
  --aws-sigv4 "aws:amz:${REGION}:es" \
  -d '{"indices": "materially"}' \
  -H 'Content-Type: application/json'
echo Done
