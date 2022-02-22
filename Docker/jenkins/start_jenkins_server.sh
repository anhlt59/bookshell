#!/bin/bash

JENKINS_DIR=/mnt/d/tmp/jenkins
mkdir -p ${JENKINS_DIR}/data

cd $JENKINS_DIR || exit
docker run -d \
  -v ${JENKINS_DIR}/data:/var/jenkins_home \
  -p 8080:8080 -p 50000:50000 \
  --user 1000:999 \
  --name jenkins-server \
  jenkins/jenkins:lts

#  -v /var/run/docker.sock:/var/run/docker.sock -v $(which docker):$(which docker) \

# v /var/run/docker.sock:/var/run/docker.sock -v $(which docker):$(which docker) >> mount docker on host to container
#docker run -d \
#  -v /d/tmp/jenkins/data:/var/jenkins_home \
#  -p 8080:8080 -p 50000:50000 \
#  --name jenkins-server \
#  jenkins/jenkins:lts
