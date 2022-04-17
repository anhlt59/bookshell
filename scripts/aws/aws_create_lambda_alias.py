import argparse

import boto3
from botocore.exceptions import ClientError

parser = argparse.ArgumentParser()
parser.add_argument("stage", default="tr0")
args = parser.parse_args()

ALIAS = "latest"
FUNCTION_NAMES = [
    f"paw-{args.stage}-AddSecuredHeaders",
    f"paw-{args.stage}-CloudfrontSignedCookies",
    f"paw-{args.stage}-CloudfrontClearSignedCookies",
    f"paw-{args.stage}-CloudfrontRedirectToRegion",
]

client = boto3.client("lambda", region_name="us-east-1")

for function_name in FUNCTION_NAMES:
    try:
        response = client.list_versions_by_function(FunctionName=function_name)
        # get latest version
        function_versions = response.get("Versions")
        lastest_version = function_versions[-1]["Version"]

        # map alias with latest version
        client.create_alias(FunctionName=function_name, Name=ALIAS, FunctionVersion=lastest_version)
        print(f"function {function_name} map alias `latest` with version {lastest_version}")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceConflictException":
            print(function_name, " alias `latest` already map with latest version")
        else:
            print(function_name, e)
            exit(1)
