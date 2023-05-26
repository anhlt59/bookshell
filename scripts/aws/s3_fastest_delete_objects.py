import boto3

bucket = "bridge-app-production"
s3_client = boto3.client("s3")
object_response_paginator = s3_client.get_paginator("list_object_versions")

delete_marker_list = []
version_list = []

for object_response_itr in object_response_paginator.paginate(Bucket=bucket):
    if "DeleteMarkers" in object_response_itr:
        for delete_marker in object_response_itr["DeleteMarkers"]:
            delete_marker_list.append({"Key": delete_marker["Key"], "VersionId": delete_marker["VersionId"]})

    if "Versions" in object_response_itr:
        for version in object_response_itr["Versions"]:
            version_list.append({"Key": version["Key"], "VersionId": version["VersionId"]})

for i in range(0, len(delete_marker_list), 1000):
    response = s3_client.delete_objects(
        Bucket=bucket, Delete={"Objects": delete_marker_list[i : i + 1000], "Quiet": True}
    )
    print(response)

for i in range(0, len(version_list), 1000):
    response = s3_client.delete_objects(Bucket=bucket, Delete={"Objects": version_list[i : i + 1000], "Quiet": True})
    print(response)
