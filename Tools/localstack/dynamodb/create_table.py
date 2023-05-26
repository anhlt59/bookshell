#!/usr/bin/python3
import json
import os
import sys
import time

import boto3
from botocore.exceptions import EndpointConnectionError

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ENDPOINT = os.getenv("DYNAMO_ENDPOINT", "http://localhost:8000")
ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID", "")
SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY", "")
REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

resource = boto3.resource(
    "dynamodb",
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    endpoint_url=ENDPOINT,
    region_name=REGION,
)


def create_table(schema, retries=3):
    try:
        table = resource.create_table(**schema)
        print(f"Creating {schema['TableName']}...")
        table.wait_until_exists()
    except EndpointConnectionError as e:
        print(e)
        if retries:
            print("Retry connect to Dynamo ...")
            time.sleep(1)
            return create_table(schema, retries - 1)
        else:
            print("Exceeded maximum retry time")
            sys.exit(1)
    except Exception as e:
        print(e)


def main():
    schemas = [
        json.load(open(os.path.join(CURRENT_DIR, "di2ArchiveLogsSchema.json"))),
        json.load(open(os.path.join(CURRENT_DIR, "di2DeletedArticlesSchema.json"))),
        json.load(open(os.path.join(CURRENT_DIR, "di2OriginArticles.json"))),
        json.load(open(os.path.join(CURRENT_DIR, "di2OriginMonitors.json"))),
    ]
    for schema in schemas:
        create_table(schema)


if __name__ == "__main__":
    main()
