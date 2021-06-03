#!/bin/bash

set -o errexit

IMAGE_NAME=test
CONTAINER_NAME=test

docker build . -t $IMAGE_NAME
docker run --name $CONTAINER_NAME $IMAGE_NAME ls
docker cp $CONTAINER_NAME:/opt ./opt
#docker cp $CONTAINER_NAME:/tmp ./tmp
docker rm -f $CONTAINER_NAME && docker image prune -f && docker container prune -f

#export PATH=${PATH}:/opt/bin
#export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/lib
