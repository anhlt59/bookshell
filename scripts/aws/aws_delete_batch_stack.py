import boto3

boto3.setup_default_session(profile_name="jenkins")

STAGE = "pnt"
REGION = "eu-central-1"

REPO = f"paw-{STAGE}-batch-job"
STACKS = [
    f"paw-{STAGE}-batch",
    # f"paw-{STAGE}-edge",
    # f"paw-{STAGE}-backend",
]

# # delete repo
# try:
# 	client = boto3.client("ecr", region_name=REGION)
# 	image_ids = client.list_images(repositoryName=REPO).get("imageIds")
# 	response = client.batch_delete_image(repositoryName=REPO, imageIds=image_ids)
# 	print("DELETE IMAGES", image_ids)
# except Exception as e:
# 	print(e)


# # delete batch
# client = boto3.client("cloudformation", region_name=REGION)
# for stack in STACKS:
# 	response = client.delete_stack(StackName=stack)
# 	print("DELETE STACK", stack)
