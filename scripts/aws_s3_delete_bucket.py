#!/usr/bin/python3
import concurrent.futures

import boto3

resource = boto3.resource("s3")
executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
buckets = (
    "s3-logs",
    "api-gateway-logs",
)


def delete_bucket(bucket_name):
    bucket = resource.Bucket(bucket_name)
    bucket.objects.all().delete()
    bucket.object_versions.delete()
    bucket.delete()
    print(f"delete {bucket_name} success")


if __name__ == "__main__":
    for name in buckets:
        print(f"start delete {name}")
        executor.submit(delete_bucket, name)
