#!/bin/bash

set -o errexit
set -o pipefail

cat <<EOF
Select a stage:
1 - nikkei dev
2 - nikkei prod
3 - neos
4 - denaribots
EOF
read -rp "Choose from 1, 2, 3, 4 [1]: " input
input=${input:-1}

MFA=false
if [ "$input" == 1 ]; then
  ARN=arn:aws:iam::***:mfa/neos-vietha
  PROFILE=dev
  MFA=true
elif [ "$input" == 2 ]; then
  ARN=arn:aws:iam::556975058824:mfa/neos-vietha
  PROFILE=prod
  MFA=true
elif [ "$input" == 3 ]; then
  ARN=arn:aws:iam::251123607109:role/least-privileged-ci-github-actions-dev
  # ARN=arn:aws:iam::251123607109:mfa/anhlt
  PROFILE=neos
  MFA=false
elif [ "$input" == 4 ]; then
  ARN=arn:aws:iam::691802122630:role/denaribot-deployment
  PROFILE=nbdb
else
  echo "Invalid input: $input"
  exit 1
fi

if [ "$MFA" == true ]; then
  read -rp "Enter the MFA code: " MFA
  response=$(aws sts get-session-token --serial-number "$ARN" --token-code "$MFA" --profile "$PROFILE")
else
  response=$(aws sts assume-role --role-arn "$ARN" --role-session-name dev --profile "$PROFILE")
fi
AccessKeyId=$(jq -r ".Credentials .AccessKeyId" <<<"$response")
SecretAccessKey=$(jq -r ".Credentials .SecretAccessKey" <<<"$response")
SessionToken=$(jq -r ".Credentials .SessionToken" <<<"$response")
printf "\nAccessKeyId: %s \nSecretAccessKey: %s \nSessionToken: %s\n\n" "$AccessKeyId" "$SecretAccessKey" "$SessionToken"

# set credential to  profile
aws configure set aws_access_key_id "$AccessKeyId" --profile session
aws configure set aws_secret_access_key "$SecretAccessKey" --profile session
aws configure set aws_session_token "$SessionToken" --profile session
aws configure set region ap-northeast-1 --profile session
aws configure set output json --profile session
echo "Done!!! You can use aws cli with 'session' profile now."
