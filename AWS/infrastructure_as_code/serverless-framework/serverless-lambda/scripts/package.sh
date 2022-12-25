#!/bin/bash

source "$(cd "$(dirname "$0")" || exit 1; pwd)"/base.sh

echo Packaging for stage "$STAGE" ...
npx serverless package -s "$STAGE"

echo Validating AWS CloudFormation template ...
cfn-lint

echo Done
