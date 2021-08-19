import boto3
import sys
import time

DYNAMO_URL = "http://dynamodb:8000"
S3_URL = "http://s3:9000"
S3_AWS_ACCESS_KEY_ID = "root"
S3_AWS_SECRET_ACCESS_KEY = "abc@123456"
TABLE_NAMES = ("users", "master")
BUCKET_NAMES = ("users", "master")

# connect to local resources
dynamo_client = boto3.resource('dynamodb', endpoint_url=DYNAMO_URL)
s3_client = boto3.client('s3', endpoint_url=S3_URL,
                         aws_access_key_id=S3_AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=S3_AWS_SECRET_ACCESS_KEY)


def create_table(client, table_name):
    client.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'hashKey',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'rangeKey',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'hashKey',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'rangeKey',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )


def create_bucket(client, bucket_name):
    client.create_bucket(Bucket=bucket_name)


def get_tables(client, retries=30):
    if retries:
        try:
            result = [i.name for i in client.tables.all()]
        except:
            time.sleep(1)
            print(f"Retries connect dynamodb")
            result = get_tables(client, retries - 1)
    else:
        print("Retry limit exceeded")
        sys.exit(1)
    return result


def get_buckets(client, retries=30):
    if retries:
        try:
            result = [i.get("Name") for i in client.list_buckets().get("Buckets", [])]
        except:
            time.sleep(1)
            print(f"Retries connect s3")
            result = get_buckets(client, retries - 1)
    else:
        print("Retry limit exceeded")
        sys.exit(1)
    return result


# create dynamodb tables
existed_tables = get_tables(dynamo_client)
print("Existed Tables:", existed_tables)
for name in set(TABLE_NAMES) - set(existed_tables):
    create_table(dynamo_client, name)
    print(f"create {name} bucket success")

# create s3 buckets
existed_buckets = get_buckets(s3_client)
print("Existed Buckets:", existed_buckets)
for name in set(BUCKET_NAMES) - set(existed_buckets):
    create_bucket(s3_client, name)
    print(f"create {name} bucket success")
