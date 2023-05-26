#!/bin/bash

# Backup a OpenSearch domain
#
# Optional arguments:
#   -r, --region: AWS region (default: us-east-1)
#   -t, --target: target stage (default: production)
#
# example: backup production
# $ ./scripts/opensearch_backup.sh -s production

set -o errexit
set -o pipefail
set -o nounset

# default value
REGION=us-east-1
TARGET_STAGE=production
SNAPSHOT_ROLE_ARN=arn:aws:iam::251623506909:role/TheSnapshotRole

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
  -r | --region)
    REGION="$2"
    shift # past argument
    shift # past value
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

if [ "$TARGET_STAGE" == "production" ]; then
  OPENSEARCH_ENDPOINT=search.materially.com
elif [ "$TARGET_STAGE" == "staging" ]; then
  OPENSEARCH_ENDPOINT=search-staging.materially.com
elif [ "$TARGET_STAGE" == "development" ]; then
  OPENSEARCH_ENDPOINT=search-dev.materially.com
elif [ "$TARGET_STAGE" == "testing" ]; then
  OPENSEARCH_ENDPOINT=search-testing.materially.com
else
  echo "Unknown stage ${TARGET_STAGE}"
  exit 1
fi

echo "Target stage: $TARGET_STAGE"

# Assume LambdaFunction role
ROLE_ARN="arn:aws:iam::251623506909:role/materially-lambda-${TARGET_STAGE}-LambdaFunctionRole"
source "$(dirname "$0")/assume_role.sh" "$ROLE_ARN"

# get OpenSearchAuth from ssm parameter
OPENSEARCH_AUTH=$(aws ssm get-parameter --name "/materially-app/${TARGET_STAGE}/OPENSEARCH_AUTH" |
  jq -r ".Parameter.Value")
OPENSEARCH_REPO="materially-${TARGET_STAGE}-snapshots"

# if the snapshot repository is not registered, then register the snapshot repository
error=$(curl -XGET "https://${OPENSEARCH_AUTH}@${OPENSEARCH_ENDPOINT}/_snapshot/${OPENSEARCH_REPO}" \
  --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
  --header "x-amz-security-token: $AWS_SESSION_TOKEN" \
  --aws-sigv4 "aws:amz:${REGION}:es" | jq -r ".error")
if [ "$error" != null ]; then
  echo "Register a snapshot repository"
  curl -XPUT "https://${OPENSEARCH_AUTH}@${OPENSEARCH_ENDPOINT}/_snapshot/${OPENSEARCH_REPO}" \
    --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
    --header "x-amz-security-token: $AWS_SESSION_TOKEN" \
    --aws-sigv4 "aws:amz:${REGION}:es" \
    -d "{\"type\" :\"s3\",\"settings\":{\"bucket\":\"materially-app-${TARGET_STAGE}-snapshots\",\"region\":\"${REGION}\",\"role_arn\":\"${SNAPSHOT_ROLE_ARN}\"}}" \
    -H 'Content-Type: application/json'
fi
echo "Snapshot repository: $OPENSEARCH_REPO"

# take a snapshot
SNAPSHOT_ID=${TARGET_STAGE}-$(date +%s)
curl -XPUT "https://${OPENSEARCH_AUTH}@${OPENSEARCH_ENDPOINT}/_snapshot/${OPENSEARCH_REPO}/${SNAPSHOT_ID}" \
  --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
  --header "x-amz-security-token: $AWS_SESSION_TOKEN" \
  --aws-sigv4 "aws:amz:${REGION}:es" \
  -d '{"indices": "materially"}' \
  -H 'Content-Type: application/json'
echo "Snapshot Id: $SNAPSHOT_ID"

# update LatestOpenSearchSnapshot ssm parameter
aws ssm put-parameter --name "/Lambdas/${TARGET_STAGE}/LatestOpenSearchSnapshot" \
  --value "$SNAPSHOT_ID" \
  --type String \
  --overwrite
echo "Updated SSM parameter /Lambdas/${TARGET_STAGE}/LatestOpenSearchSnapshot: $SNAPSHOT_ID"
echo Done
