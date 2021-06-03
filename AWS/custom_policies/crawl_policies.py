import os
from pathlib import Path

import boto3
import yaml

DIR = os.path.dirname(os.path.realpath(__file__))
boto3.setup_default_session(profile_name='anhlt')
iam_client = boto3.client('iam')


def list_groups():
    response = iam_client.list_groups(MaxItems=200)
    for group in response.get('Groups', []):
        yield group


def list_group_policies(name):
    response = iam_client.list_attached_group_policies(GroupName=name, MaxItems=200)
    for policy in response.get('AttachedPolicies', []):
        yield policy


def get_policy(arn):
    policy_response = iam_client.get_policy(PolicyArn=arn)
    version_id = policy_response['Policy']['DefaultVersionId']
    return iam_client.get_policy_version(PolicyArn=arn, VersionId=version_id)


def save_yaml(data, path):
    Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
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
