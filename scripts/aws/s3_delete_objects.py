import concurrent.futures

import boto3

# PROFILE = "jenkins"
BUCKET = "materially-production-apex"
PREFIXES = (
    "apex-Plants",
    "apex-Products",
)

# boto3.setup_default_session(profile_name=PROFILE)
resource = boto3.resource("s3")
bucket = resource.Bucket(BUCKET)


def delete_objects(prefix):
    try:
        bucket.objects.filter(Prefix=prefix).delete()
        print(f"delete {BUCKET}/{prefix} success")
    except Exception as e:
        print(e)


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    for prefix in PREFIXES:
        print(f"start delete {BUCKET}/{prefix}")
        executor.submit(delete_objects, prefix)
