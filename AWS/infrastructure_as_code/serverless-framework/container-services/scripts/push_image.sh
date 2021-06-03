#!/usr/bin/bash

# push image to specific region (default us-east-1)
# Params:
#   0: region name
#   1: stage

set -o errexit
set -o pipefail
set -o nounset

BASE_DIR=$(dirname $(cd "$(dirname "$0")"; pwd))

REGION=${1:-us-east-1}
STAGE=${2:-development}
ACCOUNT_ID=${3:-251623506909}

ECR_REGISTRY="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"
ECR_REPO=materially-app-${STAGE}
GITHUB_SHA=$(git rev-parse HEAD)
SHORT_SHA=${GITHUB_SHA::7}

# login ecr
aws ecr get-login-password --region "$REGION" | docker login --username AWS --password-stdin "$ECR_REGISTRY"

# build image
docker build "${BASE_DIR}/app" -t "${ECR_REGISTRY}/${ECR_REPO}:${SHORT_SHA}" --target production
#
# push docker image to ecr
docker push "${ECR_REGISTRY}/${ECR_REPO}:${SHORT_SHA}"
