#!/bin/bash

TAG=${1}
COMMIT=${2}

if [ $TAG ]; then

  if [ -z $COMMIT ]; then
    COMMIT=$(git rev-parse HEAD)
  fi
  echo tag $TAG commit $COMMIT

  git tag -f $TAG $COMMIT
  git push -f origin $TAG

fi
