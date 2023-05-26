import boto3

boto3.setup_default_session(profile_name="jenkins")
client = boto3.client("iam")

# response = client.list_roles(MaxItems=100)
role_names = ("appsync-ds-ddb-eyzs3u-paw-local-relation",)
