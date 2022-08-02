#!/bin/bash

set -o errexit
set -o pipefail

cat << EOF
Select a stage:
1 - dev
2 - prod
EOF

read -p "Choose from 1, 2 [1]: " input
input=${input:-1}

if [ "$input" == 1 ]; then
  ARN=arn:aws:iam::322940739131:mfa/neos-vietha
  PROFILE=di2dev
elif [ "$input" == 2 ]; then
  ARN=arn:aws:iam::556975058824:mfa/neos-vietha
  PROFILE=di2prod
else
  echo "Invalid input: $input"
  exit 1
fi

read -p "Enter the MFA code: " MFA

response=$(aws sts get-session-token --serial-number "$ARN" --token-code "$MFA" --profile $PROFILE)
AccessKeyId=$(jq -r ".Credentials .AccessKeyId" <<< "$response")
SecretAccessKey=$(jq -r ".Credentials .SecretAccessKey" <<< "$response")
SessionToken=$(jq -r ".Credentials .SessionToken" <<< "$response")

printf "Request success!!\n\n"
printf "AccessKeyId: $AccessKeyId \nSecretAccessKey: $SecretAccessKey \nSessionToken: $SessionToken\n"

aws configure set aws_access_key_id "$AccessKeyId" --profile di2mfa
aws configure set aws_secret_access_key "$SecretAccessKey" --profile di2mfa
aws configure set aws_session_token  "$SessionToken" --profile di2mfa
aws configure set region us-east-1 --profile di2mfa
aws configure set output json --profile di2mfa

echo DONE
