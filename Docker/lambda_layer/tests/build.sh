#!/bin/bash

set -ex
set -o errexit
set -o pipefail
set -o nounset

PYTHON_VERSION=python3.8
IMAGE_NAME=lambda-layer-pdftocairo

docker build . -t $IMAGE_NAME --build-arg PYTHON_VERSION=${PYTHON_VERSION}
docker run $IMAGE_NAME python test.py
#docker run -it $IMAGE_NAME bash
#docker run --rm ${IMAGE_NAME}:/opt $IMAGE_NAME ./output
#docker cp ${IMAGE_NAME}:/opt  ./data
