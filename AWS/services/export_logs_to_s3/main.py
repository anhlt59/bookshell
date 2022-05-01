import logging
import time

from . import ssm, logs

logger = logging.getLogger(__name__)

EXPORT_STATUS_TAG = {"Key": "ExportToS3", "Value": "true"}
EXPORT_BUCKET_TAG_KEY = "ExportBucket"


def lambda_handler(event, context):
    log_groups = logs.list_log_groups()

    for log_group in log_groups:
        log_group_name = log_group['logGroupName']
        tags = logs.list_tags(log_group_name)

        # export log to s3 when tag ExportToS3=true
        if tags.get(EXPORT_STATUS_TAG["Key"]) == EXPORT_STATUS_TAG["Value"]:
            export_bucket = tags.get(EXPORT_BUCKET_TAG_KEY)
            from_time = ssm.get_value(log_group_name)
            to_time = round(time.time() * 1000)
            # export logs to s3
            logs.export_to_s3(log_group_name, export_bucket, from_time, to_time)
            # save timestamp as checkpoint
            ssm.set_value(log_group_name, to_time)
