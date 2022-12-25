#!/bin/bash

source "$(cd "$(dirname "$0")" || exit 1; pwd)"/package.sh

echo Deploying for stage "$STAGE" ...
npx serverless deploy -s "$STAGE" --package "$BASE_DIR"/.serverless

echo Done
