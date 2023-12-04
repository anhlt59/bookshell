#!/usr/local/bin/python3
import time
from datetime import datetime, timedelta
from pprint import pprint
from typing import List

import boto3

boto3.setup_default_session(profile_name="mfa")

# STAGE = "development"
# DELTA_TIME = 0.5  # hours
# LAMBDA_PREFIX = f"/aws/lambda/materially-{STAGE}"
QUERY = """
fields @timestamp, @message, @logStream, @log\n| filter @message like /(?i)(insert)/\n| sort @timestamp desc\n| limit 500\n
"""
LOG_GROUPS = ["/aws/lambda/di2_govhk_xml_file_parser"]

client = boto3.client("logs", region_name="ap-northeast-1")


def query_logs(query: str, log_groups: List[str], start_time: int, end_time: int, timeout: int = 15, delay: int = 1):
    def _get_query_results():
        nonlocal query_id, timeout, delay

        response = client.get_query_results(queryId=query_id)
        if response["status"] == "Running":
            if timeout <= 0:
                raise Exception("Query timed out")
            print("Waiting for query to complete ...")
            time.sleep(delay)
            return _get_query_results()
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
    result = query_logs(
        QUERY,
        LOG_GROUPS,
        start_time=1687305600,
        end_time=1687333199,
    )
    pprint(result)
    import json

    with open("./logs.json", "w") as f:
        json.dump(result, f, indent=4)


if __name__ == "__main__":
    main()
