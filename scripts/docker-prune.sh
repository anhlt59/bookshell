#!/bin/bash

# remove exited container
docker rm -f $(docker ps -a | grep Exited | awk '{print $1}')

# docker prune
docker image prune -f & docker container prune -f & docker volume prune -f
