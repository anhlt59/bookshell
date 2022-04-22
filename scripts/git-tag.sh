#!/bin/bash

TAG=${1}
COMMIT=${2}

if [ -z $TAG ]; then
  echo TAG is required
  exit 1
fi
if [ -z $COMMIT ]; then
  COMMIT=$(git rev-parse HEAD)
fi
echo tag $TAG
echo commit $COMMIT

git tag -f $TAG $COMMIT
git push -f origin $TAG
