#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

PYTHON_VERSION=python3.8
IMAGE_NAME=lambda-layer

docker build . -t $IMAGE_NAME --build-arg PYTHON_VERSION=$PYTHON_VERSION
docker run --rm ${IMAGE_NAME}:/opt $IMAGE_NAME ./output
