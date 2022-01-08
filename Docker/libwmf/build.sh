#!/bin/bash

set -o errexit

IMAGE_NAME=libwmf
CONTAINER_NAME=layer

docker build . -t $IMAGE_NAME
docker run --name $CONTAINER_NAME $IMAGE_NAME
docker cp $CONTAINER_NAME:/opt ./opt
docker rm -f $CONTAINER_NAME && docker image prune -f