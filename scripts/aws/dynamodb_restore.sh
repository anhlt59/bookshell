#!/bin/bash

# Restoring a DynamoDB table from a backup of another DynamoDB table
#
# optional arguments:
#   -r, --region: AWS region (default: us-east-1)
#   -s, --source: the source stage(default: production)
#   -t, --target: the target stage (default: testing)
#
# example: restore production > testing
# $ ./scripts/dynamodb_restore.sh -t testing -s production
# or
# $ ./scripts/dynamodb_restore.sh # default arguments

set -o errexit
set -o pipefail
set -o nounset

# default value
REGION=us-east-1
TARGET_STAGE=testing
SOURCE_STAGE=production

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

# get the latest backup arn of SOURCE_TABLE
BACKUP_ARN=$(aws ssm get-parameter --name "/Lambdas/${SOURCE_STAGE}/LatestDynamoBackupArn" --region "$REGION" |
  jq -r ".Parameter.Value")
if [ "$BACKUP_ARN" == null ]; then
  echo "No backup found"
  exit 1
fi
echo "Backup Arn: $BACKUP_ARN"

# Delete old table
set +e
TARGET_TABLE=materially-${TARGET_STAGE}-table
echo "Deleting $TARGET_TABLE"
aws dynamodb delete-table \
  --table-name "$TARGET_TABLE" \
  --region "$REGION"
sleep 60
set +e

# Restore a new table from a backup
echo "Restoring $TARGET_TABLE"
aws dynamodb restore-table-from-backup \
  --target-table-name "$TARGET_TABLE" \
  --backup-arn "$BACKUP_ARN" \
  --region "$REGION"
echo Done
