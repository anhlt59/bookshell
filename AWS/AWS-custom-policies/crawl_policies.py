import os
from pathlib import Path

import boto3
import yaml

DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AWS', 'AWS-custom-policies')
boto3.setup_default_session(profile_name='anhlt')
iam_client = boto3.client('iam')


def list_groups():
    response = iam_client.list_groups(MaxItems=200)
    groups = response.get("Groups", [])
    for group in groups:
        yield group


def list_group_policies(name):
    response = iam_client.list_attached_group_policies(GroupName=name, MaxItems=200)
    policies = response.get("AttachedPolicies", [])
    for policy in policies:
        yield policy


def get_policy(arn):
    policy_response = iam_client.get_policy(PolicyArn=arn)
    version_id = policy_response['Policy']['DefaultVersionId']
    return iam_client.get_policy_version(PolicyArn=arn, VersionId=version_id)


def save_yaml(data, path):
    base_dir = os.path.dirname(path)
    Path(base_dir).mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as file:
        yaml.dump(data, file)


def main():
    for group_item in list_groups():
        group_name = group_item['GroupName']
        for policy_item in list_group_policies(group_name):
            policy_info = get_policy(policy_item['PolicyArn'])

            file_path = os.path.join(DIR, group_name, f"{policy_item['PolicyName']}.yaml")
            save_yaml(policy_info['PolicyVersion']['Document'], file_path)


if __name__ == '__main__':
    main()
