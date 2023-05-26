import concurrent.futures

import boto3

boto3.setup_default_session(profile_name="neos")
client = boto3.client("s3")

executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)


def list_buckets():
    response = client.list_buckets()
    for item in response["Buckets"]:
        yield item["Name"]


def put_bucket_lifecycle(bucket_name):
    response = client.put_bucket_lifecycle_configuration(
        Bucket=bucket_name,
        LifecycleConfiguration={
            "Rules": [
                {
                    "Expiration": {"Days": 30},
                    "NoncurrentVersionExpiration": {
                        "NoncurrentDays": 30,
                    },
                    "ID": "ExpireRule",
                    "Filter": {"Prefix": ""},
                    "Status": "Enabled",
                }
            ]
        },
    )
    print(response)


def delete_bucket_lifecycle(bucket_name):
    response = client.delete_bucket_lifecycle(Bucket=bucket_name)
    print(response)


def main():
    buckets = list_buckets()
    for bucket_name in buckets:
        try:
            delete_bucket_lifecycle(bucket_name)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
