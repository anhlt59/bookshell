import json

import boto3

PROFILE = "jenkins"
BUCKET_NAMES = (
    # "paw-tr0-1-web",
    # "paw-tr1-web",
    # "paw-tr2-web",
    # "paw-tr2-t-web",
    # "paw-tr2-v-web",
    # "paw-ts1-web",
    # "paw-ts2-web",
    "paw-ts1-t-web",
    "paw-ts1-v-web",
    # "paw-pnt-web",
    # "paw-prv-web",
    # "paw-prd-web",
    # "paw-prd-v-web",
    # "paw-prd-t-web",
)
KEY = "resources/printerlist/help_printerlist.txt"

boto3.setup_default_session(profile_name=PROFILE)
s3 = boto3.client("s3")

# for bucket_name in BUCKET_NAMES:
# 	try:
# 		s3.copy_object(
# 			Key=KEY, Bucket=bucket_name,
#             CopySource={"Bucket": "paw-tr0-1-web", "Key": KEY},
#             ContentType='binary/octet-stream',
#         )
# 	except Exception as e:
# 		print(bucket_name, e)

bucket_name = "paw-tr0-web"
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity EH7M2RVNEJ4YM"},
            "Action": ["s3:GetObject", "s3:ListBucket"],
            "Resource": ["arn:aws:s3:::paw-tr0-web/*", "arn:aws:s3:::paw-tr0-web"],
            "Condition": {"Bool": {"aws:SecureTransport": "true"}},
        },
        {
            "Sid": "ForceSSLOnlyAccess",
            "Effect": "Deny",
            "Principal": {"AWS": "*"},
            "Action": "s3:*",
            "Resource": ["arn:aws:s3:::paw-tr0-web/*", "arn:aws:s3:::paw-tr0-web"],
            "Condition": {"Bool": {"aws:SecureTransport": "false"}},
        },
    ],
}
bucket_policy = json.dumps(bucket_policy)
s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
