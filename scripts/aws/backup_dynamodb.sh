#!/bin/bash

# Backup a DynamoDB table
#
# optional arguments:
#   -r, --region: AWS region (default: us-east-1)
#   -t, --target: the target stage (default: production)
#
# example: backup production
# $ ./scripts/backup_dynamodb.sh -s production

set -o errexit
set -o pipefail
set -o nounset

# default value
REGION=us-east-1
TARGET_STAGE=production

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

TARGET_TABLE="materially-${TARGET_STAGE}-table"
BACKUP_NAME="${TARGET_STAGE}_$(date +%s)"
echo "Target table: ${TARGET_TABLE}"

# Assume LambdaFunction role
ROLE_ARN="arn:aws:iam::251623506909:role/materially-lambda-${TARGET_STAGE}-LambdaFunctionRole"
source "$(dirname "$0")/assume_role.sh" "$ROLE_ARN"

echo "Creating a backup: $BACKUP_NAME"
BACKUP_ARN=$(aws dynamodb create-backup \
  --table-name "$TARGET_TABLE" \
  --backup-name "$BACKUP_NAME" \
  --region "$REGION" |
  jq -r ".BackupDetails.BackupArn")
echo "Backup Arn: $BACKUP_ARN"

# update LatestDynamoSnapshot ssm parameter
aws ssm put-parameter --name "/Lambdas/${TARGET_STAGE}/LatestDynamoBackupArn" \
  --value "$BACKUP_ARN" \
  --type String \
  --overwrite
echo "Updated SSM parameter /Lambdas/${TARGET_STAGE}/LatestDynamoBackupArn: $BACKUP_ARN"
echo Done
