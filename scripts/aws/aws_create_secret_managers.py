import json
from pprint import pprint

import boto3

boto3.setup_default_session(profile_name="mfa")

# client = boto3.client('secretsmanager', region_name='us-east-1', endpoint_url='http://localhost:4566')
client = boto3.client("secretsmanager", region_name="ap-northeast-1")


def read_setting_file(path):
    with open(path) as file:
        data = json.load(file)
        for item in data:
            yield item


def delete_secret(key):
    response = client.delete_secret(SecretId=key, ForceDeleteWithoutRecovery=True)
    pprint(response)


def list_secrets():
    response = client.list_secrets(Filters=[{"Key": "name", "Values": ["di2/"]}], SortOrder="asc")
    for item in response.get("SecretList", []):
        yield item


def get_secret_value(key):
    response = client.get_secret_value(SecretId=key)
    return response


def main():
    path = "/Users/anhlt/Projects/neos/di2-curation/config/staging/Settings.json"
    pprint(get_secret_value("di2/AFR"))
    # for item in read_setting_file(path):
    #
    #     try:
    #         key = item.get("Code", "").replace(":", "/").replace('di2_', '')
    #         print(f'di2/{key}')
    #         # response = client.create_secret(
    #         #     Name=f'di2/{key}',
    #         #     Description=f'Di2 {item["Code"]}',
    #         #     SecretString=json.dumps(item),
    #         #     Tags=[{'Key': 'billing', 'Value': 'di2'}],
    #         # )
    #         # if response.get('HTTPStatusCode') == 200:
    #         #     print('Create', key, 'successfully')
    #         # else:
    #         #     print('Fail to create', key)
    #     except Exception as e:
    #         print(e)
    # # pprint(list(list_secrets()))


if __name__ == "__main__":
    main()
