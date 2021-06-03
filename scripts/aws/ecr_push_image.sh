#!/bin/bash

# push image to specific region (default ap-northeast-1)
# Params:
#   0: region name
#   1: repo

set -o errexit
set -o pipefail
set -o nounset

BASE_DIR=$(cd $(dirname $(dirname "$0")); pwd)

REGION=${1:-ap-northeast-1}
ECR_REPO=${2:-dev}

ECR_REGISTRY_ID=$(aws ecr describe-registry --profile mfa | jq -r '.registryId')
ECR_REGISTRY="${ECR_REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com"
echo "ECR registry: ${ECR_REGISTRY}"

GITHUB_SHA=$(git rev-parse HEAD)
echo "Build a image with tags: ${GITHUB_SHA} & latest"

# build image
docker build "${BASE_DIR}" -t "${ECR_REGISTRY}/${ECR_REPO}:${GITHUB_SHA}" -t "${ECR_REGISTRY}/${ECR_REPO}:latest" --target run-stage

# login ecr
aws ecr get-login-password --region "$REGION" | docker login --username AWS --password-stdin "$ECR_REGISTRY"

# push docker image to ecr
docker push "${ECR_REGISTRY}/${ECR_REPO}" --all-tags
