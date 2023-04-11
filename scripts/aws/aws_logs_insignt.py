#!/usr/local/bin/python3
import time
from datetime import datetime, timedelta
from pprint import pprint
from typing import List

import boto3

STAGE = "development"
DELTA_TIME = 0.5  # hours
LAMBDA_PREFIX = f"/aws/lambda/materially-{STAGE}"
QUERY = """
fields @timestamp, @message
| filter @message like /(?i)(exception|error|fail)/
| sort @timestamp desc
| limit 100
"""

client = boto3.client("logs")


def query_logs(query: str, log_groups: List[str], start_time: int, end_time: int, timeout: int = 15, delay: int = 1):
    def _get_query_results():
        nonlocal query_id, timeout, delay

        response = client.get_query_results(queryId=query_id)
        if response["status"] == "Running":
            if timeout <= 0:
                raise Exception("Query timed out")
            print("Waiting for query to complete ...")
            time.sleep(delay)
            return _get_query_results(query_id, timeout - delay)
        return response.get("results")

    start_query_response = client.start_query(
        logGroupNames=log_groups,
        startTime=start_time,
        endTime=end_time,
        queryString=query,
    )
    if query_id := start_query_response.get("queryId"):
        return _get_query_results()


def list_log_groups(prefix: str):
    response = client.describe_log_groups(
        logGroupNamePrefix=prefix,
    )
    for item in response.get("logGroups", []):
        yield item["logGroupName"]


def main():
    log_groups = list(list_log_groups(LAMBDA_PREFIX))
    pprint(log_groups)
    result = query_logs(
        QUERY,
        log_groups,
        start_time=int((datetime.today() - timedelta(hours=DELTA_TIME)).timestamp()),
        end_time=int(datetime.now().timestamp()),
    )
    pprint(result)


if __name__ == "__main__":
    main()
