from itertools import islice
from pprint import pprint
from typing import Dict, Iterable, Iterator, List

import boto3

boto3.setup_default_session(profile_name="session")
client = boto3.client("ssm", region_name="ap-northeast-1")


def chunks(objs: Iterable, limit: int) -> Iterator[List]:
    objs = iter(objs)
    while True:
        batch = list(islice(objs, limit))
        if not batch:
            break
        yield batch


def get_parameters(prefixes: List[str]):
    for prefix in prefixes:
        response = client.describe_parameters(
            ParameterFilters=[
                {"Key": "Name", "Option": "Contains", "Values": [prefix]},
            ],
            MaxResults=50,
        )
        for item in response["Parameters"]:
            response = client.get_parameter(Name=item["Name"])
            yield response["Parameter"]["Name"], f'{response["Parameter"]["Value"]}:{response["Parameter"]["Version"]}'
            # yield response


def update_parameters(data: Dict[str, str], overwrite=False):
    for key, value in data.items():
        try:
            client.put_parameter(
                Name=key,
                Description=key,
                Value=value,
                Type="String",
                Tier="Standard",
                DataType="text",
                Tags=[{"Key": "Owner", "Value": "materially"}],
            )
            print("created new", key)
        except Exception as e:
            if overwrite:
                client.put_parameter(
                    Name=key,
                    Description=key,
                    Value=value,
                    Type="String",
                    Overwrite=True,
                    Tier="Standard",
                    DataType="text",
                )
                print("overwrited", key)
            else:
                print(f"Parameter {key} is existing")


def delete_parameters(names: List[str]):
    for chunk in chunks(names, 10):
        try:
            response = client.delete_parameters(Names=chunk)
            print("deleted", response["DeletedParameters"])
        except Exception as e:
            print(e)
    # for name in names:
    #     try:
    #         response = client.delete_parameter(Name=name)
    #         print("deleted", response["DeletedParameter"])
    #     except Exception as e:
    #         print(e)


def main():
    dev_data = {
        "/di2/dynamodb/DELETE_ARTICLE_TABLE_NAME": "di2DeletedArticles",
        "/di2/dynamodb/ARTICLE_TABLE_NAME": "di2OriginArticles",
        "/di2/dynamodb/ARCHIVE_TABLE_NAME": "di2ArchiveLogs",
        "/di2/dynamodb/MONITORING_ARTICLE_TABLE_NAME": "di2OriginMonitors",
        "/di2/dynamodb/REGION_NAME": "ap-northeast-1",
        "/di2/sqs/MONITOR_LOGS_URL": "https://sqs.ap-northeast-1.amazonaws.com/251123607109/di2_monitor_logs_queue",
        "/di2/sqs/MONITOR_ERROR_LOGS_URL": "https://sqs.ap-northeast-1.amazonaws.com/251123607109/di2_monitor_error_logs_queue",
        "/di2/sqs/HTTP_NEXT_PROVIDER_URL": "https://sqs.ap-northeast-1.amazonaws.com/251123607109/di2_http_next_provider_queue",
        "/di2/sqs/FTP_NEXT_PROVIDER_URL": "https://sqs.ap-northeast-1.amazonaws.com/251123607109/di2_ftp_next_provider_queue",
        "/di2/sqs/FTP_PARSER_URL": "https://sqs.ap-northeast-1.amazonaws.com/251123607109/di2_ftp_parser_queue.fifo",
        "/di2/sqs/RDS_PARSER_URL": "https://sqs.ap-northeast-1.amazonaws.com/251123607109/di2_rds_data_queue",
        "/di2/sns/NIKKEI_PUBLISH_TOPIC_ARN": "arn:aws:sns:ap-northeast-1:251123607109:di2-Nikkei-Publish-Topic",
        "/di2/s3/S3_BUCKET": "di2-dev",
    }
    update_parameters(dev_data)


if __name__ == "__main__":
    main()
