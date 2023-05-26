from itertools import islice
from pprint import pprint
from typing import Dict, Iterable, Iterator, List

import boto3

boto3.setup_default_session(profile_name="mfa")
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
            yield response["Parameter"]["Name"], response["Parameter"]["Value"]


def update_parameters(data: Dict[str, str]):
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
            client.put_parameter(
                Name=key, Description=key, Value=value, Type="String", Overwrite=True, Tier="Standard", DataType="text"
            )
            print("overwrited", key)


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
    keys = ["/Lambdas/production/"]
    # {
    #  '/Lambdas/production/ApexGetPlants/lastDate': '2022-11-18T11:47:00.000',
    #  '/Lambdas/production/ApexInitPlants/lastId': "'71'",
    #  '/Lambdas/production/ApexInitProducts/lastDate': '2023-05-15T00:00:00.000',
    #  '/Lambdas/production/BMGExtractorCustomers/lastDate': '1900-01-01',
    #  '/Lambdas/production/BMGExtractorFleets/lastDate': '1900-01-01',
    #  '/Lambdas/production/BMGExtractorJobs/lastDate': '1900-01-01',
    #  '/Lambdas/production/BMGExtractorLoads/lastDate': '1900-01-01',
    #  '/Lambdas/production/BMGExtractorPlants/lastDate': '1900-01-01',
    #  '/Lambdas/production/BMGExtractorShipments/lastDate': '1900-01-01',
    #  '/Lambdas/production/BMGExtractorTickets/lastDate': '1900-01-01',
    #  '/Lambdas/production/BMGExtractorTrucks/lastDate': '1900-01-01',
    #  '/Lambdas/production/BMGExtractors/companyId': 'COMPANY#01GMN-MNM89-AK35E-ZWDR1-D968PZ',
    #  '/Lambdas/production/LatestDynamoBackupArn': 'arn:aws:dynamodb:us-east-1:251623506909:table/materially-production-table/backup/01684130401874-64b25dc4',
    #  '/Lambdas/production/LatestOpenSearchSnapshot': 'production-1684130402151',
    #  '/Lambdas/production/LatestSnapshot': 'production-1675058420697',
    #  '/Lambdas/production/SilviExtractors/companyId': 'COMPANY#01GMN-MNM89-AK35E-ZWDR1-D968PZ',
    #  '/Lambdas/production/SilviGetDailyOrderTruckGroups/lastDate': '2023-01-23T17:02:00.000',
    #  '/Lambdas/production/SilviGetDailyOrders/lastDate': '2023-05-15T14:55:34.000',
    #  '/Lambdas/production/SilviGetPlants/lastDate': '2023-01-18T11:08:19.637',
    #  '/Lambdas/production/SilviGetRTTickets/lastDate': '2023-01-23T17:53:27.633',
    #  '/Lambdas/production/SilviGetSalesOrders/lastDate': '2023-05-15T08:57:15.397',
    #  '/Lambdas/production/SilviGetTickets/lastDate': '2023-05-15 14:54',
    #  '/Lambdas/production/SilviGetTruckGroupTrucks/lastDate': '2023-01-23T16:59:01.503',
    #  '/Lambdas/production/SilviGetTrucks/lastDate': '2023-01-23T17:43:00.000',
    #  '/Lambdas/production/SilviInitDailyOrderTruckGroups/lastId': '8392708',
    #  '/Lambdas/production/SilviInitDailyOrders/lastId': '159430',
    #  '/Lambdas/production/SilviInitPlants/lastId': '15',
    #  '/Lambdas/production/SilviInitRTTickets/lastId': '2145304',
    #  '/Lambdas/production/SilviInitSalesOrders/lastId': '22283',
    #  '/Lambdas/production/SilviInitTickets/lastId': '2173791',
    #  '/Lambdas/production/SilviInitTruckGroupTrucks/lastId': '72411',
    #  '/Lambdas/production/SilviInitTrucks/lastId': '6054463'
    # #  }
    # data =  {
    #   '/Lambdas/production/BMG/ExtractorCustomers/lastDate': '2023-04-13',
    #   '/Lambdas/production/BMG/ExtractorDrivers/lastDate': '2023-04-13',
    #   '/Lambdas/production/BMG/ExtractorFleets/lastDate': '2023-04-13',
    #   '/Lambdas/production/BMG/ExtractorJobs/lastDate': '1970-01-01',
    #   '/Lambdas/production/BMG/ExtractorLoads/lastDate': '2023-04-13',
    #   '/Lambdas/production/BMG/ExtractorPlants/lastDate': '1970-01-01',
    #   '/Lambdas/production/BMG/ExtractorShipments/lastDate': '2023-04-13',
    #   '/Lambdas/production/BMG/ExtractorTickets/lastDate': '2023-04-13',
    #   '/Lambdas/production/BMG/ExtractorTrucks/lastDate': '2023-04-13',
    #   '/Lambdas/production/BMG/companyId': 'COMPANY#01GMN-MNM89-AK35E-ZWDR1-D968PZ',
    # }
    dev_data = {
        # "/di2/dynamodb/DELETE_ARTICLE_TABLE_NAME": "di2DeletedArticles",
        # "/di2/dynamodb/ARTICLE_TABLE_NAME": "di2OriginArticles",
        # "/di2/dynamodb/ARCHIVE_TABLE_NAME": "di2ArchiveLogs",
        # "/di2/dynamodb/MONITORING_ARTICLE_TABLE_NAME": "di2OriginMonitors",
        # "/di2/dynamodb/REGION_NAME": "ap-northeast-1",
        # "/di2/sqs/MONITOR_LOGS_URL": "https://sqs.ap-northeast-1.amazonaws.com/322940739131/di2_monitor_logs_queue",
        # "/di2/sqs/MONITOR_ERROR_LOGS_URL": "https://sqs.ap-northeast-1.amazonaws.com/322940739131/di2_monitor_error_logs_queue",
        # "/di2/sqs/HTTP_NEXT_PROVIDER_URL": "https://sqs.ap-northeast-1.amazonaws.com/322940739131/di2_http_next_provider_queue",
        # "/di2/sqs/FTP_NEXT_PROVIDER_URL": "https://sqs.ap-northeast-1.amazonaws.com/322940739131/di2_ftp_next_provider_queue",
        # "/di2/sqs/FTP_PARSER_URL": "https://sqs.ap-northeast-1.amazonaws.com/322940739131/di2_ftp_parser_queue.fifo",
        # "/di2/sqs/RDS_PARSER_URL": "https://sqs.ap-northeast-1.amazonaws.com/322940739131/di2_rds_data_queue",
        # "/di2/sns/NIKKEI_PUBLISH_TOPIC_ARN": "arn:aws:sns:ap-northeast-1:322940739131:di2-Nikkei-Publish-Topic",
        "/di2/s3/S3_BUCKET": "di2.dev",
    }
    # prod_data = {
    #     '/di2/dynamodb/DELETE_ARTICLE_TABLE_NAME': 'di2DeletedArticles',
    #     '/di2/dynamodb/ARTICLE_TABLE_NAME': 'di2OriginArticles',
    #     '/di2/dynamodb/ARCHIVE_TABLE_NAME': 'di2ArchiveLogs',
    #     '/di2/dynamodb/MONITORING_ARTICLE_TABLE_NAME': 'di2OriginMonitors',
    #     '/di2/dynamodb/REGION_NAME': 'ap-northeast-1',
    #     '/di2/sqs/MONITOR_LOGS_URL': 'https://sqs.ap-northeast-1.amazonaws.com/556975058824/di2_monitor_logs_queue',
    #     '/di2/sqs/MONITOR_ERROR_LOGS_URL': 'https://sqs.ap-northeast-1.amazonaws.com/556975058824/di2_monitor_error_logs_queue',
    #     '/di2/sqs/HTTP_NEXT_PROVIDER_URL': 'https://sqs.ap-northeast-1.amazonaws.com/556975058824/di2_http_next_provider_queue',
    #     '/di2/sqs/FTP_NEXT_PROVIDER_URL': 'https://sqs.ap-northeast-1.amazonaws.com/556975058824/di2_ftp_next_provider_queue',
    #     '/di2/sqs/RDS_PARSER_URL': 'https://sqs.ap-northeast-1.amazonaws.com/556975058824/di2_rds_data_queue',
    #     '/di2/sqs/FTP_PARSER_URL': 'https://sqs.ap-northeast-1.amazonaws.com/556975058824/di2_ftp_parser_queue.fifo',
    #     '/di2/sns/NIKKEI_PUBLISH_TOPIC_ARN': 'arn:aws:sns:ap-northeast-1:556975058824:di2-Nikkei-Publish-Topic',
    #     "/di2/s3/S3_BUCKET": "di2.nikkei.data",
    # }

    # pprint(dict(get_parameters(['/avex'])))
    # data = {'/avex/ACCESS_TOKEN': '3284710273-dZySN1ZzB08qPINy6AQdt9U8zdXgvtzTALfxNbj',
    #  '/avex/ACCESS_TOKEN_SECRET': 'vhfhdU4UJCl3opgrXWOSweLdMYgjF4hKFcqH4Awac35eW',
    #  '/avex/AWS_SNS_TOPIC_ARN': 'arn:aws:sns:us-east-2:435947900805:crawl-twitter-accounts-topic',
    #  '/avex/AWS_SQS_QUEUE_NAME': 'TwitterAccountsQueue',
    #  '/avex/CONSUMER_KEY': 'cK9YmKOjfHVTdFox11ymuUvzT',
    #  '/avex/CONSUMER_SECRET': '3qfYCcJu2DXdNzcSttQp7P9o1vJUtxZczaWMeVPkEOykKxe7uj',
    #  '/avex/S3_BUCKET': 'avex-staging-bucket',
    #  '/avex/SLACK_WEBHOOK_URL': 'https://hooks.slack.com/services/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',
    #  '/avex/SPREADSHEET_ID': '180wofDEAdbnbO30WpGDMmrbFQowMTaMTn7Z1TXwf65o',
    #  '/avex/SPREADSHEET_RANGE_NAME': 'C2:C',
    #  '/avex/SPREADSHEET_SCOPES': 'https://www.googleapis.com/auth/spreadsheets.readonly'}
    update_parameters(dev_data)


if __name__ == "__main__":
    main()
