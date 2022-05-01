import logging
import os
import time

import boto3

__all__ = ["list_log_groups", "list_tags", "export_to_s3"]

logs = boto3.client('logs', region_name=os.getenv("REGION"))
logger = logging.getLogger(__name__)

EXPORT_INTERVAL = 24 * 60 * 60 * 1000
SLEEP_INTERVAL = 3


def list_log_groups(**kwargs):
    response = logs.describe_log_groups(**kwargs)
    log_groups = response['logGroups']

    if next_token := response.get("nextToken"):
        return log_groups.extend(list_log_groups(nextToken=next_token))

    return log_groups


def list_tags(log_group_name):
    response = logs.list_tags_log_group(logGroupName=log_group_name)
    return response['tags']


def wait_export_task_done(task_id, retries=30):
    time.sleep(SLEEP_INTERVAL)
    response = logs.describe_export_tasks(taskId=task_id)

    for task in response['exportTasks']:
        if task.get("status", {}).get("code") == "PENDING":
            return wait_export_task_done(task_id, retries - 1)


def export_to_s3(log_group_name, destination, from_time, to_time, retries=3):
    if from_time - to_time < EXPORT_INTERVAL:
        logger.debug("Skipped until 24hrs from last export is completed")
    else:
        try:
            response = logs.create_export_task(
                logGroupName=log_group_name,
                fromTime=from_time,
                to=to_time,
                destination=destination,
                destinationPrefix=log_group_name.strip("/")
            )
            logger.debug(f"Task created: {response['taskId']}")
            wait_export_task_done(response['taskId'])
        except logs.exceptions.LimitExceededException:
            logger.error("Need to wait until all tasks are finished (LimitExceededException)")
            time.sleep(SLEEP_INTERVAL)
            return export_to_s3(log_group_name, destination, from_time, to_time, retries - 1)
        except Exception as e:
            logger.error(f"Error exporting {log_group_name}: {e}")
