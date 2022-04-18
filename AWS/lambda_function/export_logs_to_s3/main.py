import logging
import os
import time

import boto3

logger = logging.getLogger()
logs = boto3.client('logs')
ssm = boto3.client('ssm')


class CheckPoint:
    def __init__(self, _id):
        self.id = _id
        self.value = None

    def get_value(self):
        if not self.value:
            try:
                ssm_response = ssm.get_parameter(Name=self.id)
                self.value = ssm_response['Parameter']['Value']
            except ssm.exceptions.ParameterNotFound:
                self.value = "0"
        return self.value

    def set_value(self, value):
        self.value = value
        ssm.put_parameter(Name=self.id, Type="String", Value=str(value), Overwrite=True)


class Logs:
    @staticmethod
    def list_log_groups(**kwargs):
        response = logs.describe_log_groups(**kwargs)
        log_groups = response['logGroups']

        if next_token := response.get("nextToken"):
            return log_groups + Logs.list_log_groups(nextToken=next_token)
        return log_groups

    @staticmethod
    def export(log_group_name, destination, from_time, to_time):
        try:
            response = logs.create_export_task(
                logGroupName=log_group_name,
                fromTime=int(from_time),
                to=to_time,
                destination=destination,
                destinationPrefix=log_group_name.strip("/")
            )
            logger.debug("    Task created: %s" % response['taskId'])
        except logs.exceptions.LimitExceededException:
            logger.error("    Need to wait until all tasks are finished (LimitExceededException). Continuing later...")
        except Exception as e:
            logger.error("    Error exporting %s: %s" % (log_group_name, getattr(e, 'message', repr(e))))


def lambda_handler(event, context):
    extra_args = {}
    log_groups = []
    log_groups_to_export = []

    if 'S3_BUCKET' not in os.environ:
        print("Error: S3_BUCKET not defined")
        return

    print("--> S3_BUCKET=%s" % os.environ["S3_BUCKET"])

    while True:
        response = logs.describe_log_groups(**extra_args)
        log_groups = log_groups + response['logGroups']

        if not 'nextToken' in response:
            break
        extra_args['nextToken'] = response['nextToken']

    for log_group in log_groups:
        response = logs.list_tags_log_group(logGroupName=log_group['logGroupName'])
        log_group_tags = response['tags']
        if 'ExportToS3' in log_group_tags and log_group_tags['ExportToS3'] == 'true':
            log_groups_to_export.append(log_group['logGroupName'])

    for log_group_name in log_groups_to_export:
        ssm_parameter_name = ("/log-exporter-last-export/%s" % log_group_name).replace("//", "/")
        try:
            ssm_response = ssm.get_parameter(Name=ssm_parameter_name)
            ssm_value = ssm_response['Parameter']['Value']
        except ssm.exceptions.ParameterNotFound:
            ssm_value = "0"

        export_to_time = int(round(time.time() * 1000))

        print("--> Exporting %s to %s" % (log_group_name, os.environ['S3_BUCKET']))

        if export_to_time - int(ssm_value) < (24 * 60 * 60 * 1000):
            # Haven't been 24hrs from the last export of this log group
            print("    Skipped until 24hrs from last export is completed")
            continue

        try:
            response = logs.create_export_task(
                logGroupName=log_group_name,
                fromTime=int(ssm_value),
                to=export_to_time,
                destination=os.environ['S3_BUCKET'],
                destinationPrefix=log_group_name.strip("/")
            )
            print("    Task created: %s" % response['taskId'])
            time.sleep(5)

        except logs.exceptions.LimitExceededException:
            print("    Need to wait until all tasks are finished (LimitExceededException). Continuing later...")
            return

        except Exception as e:
            print("    Error exporting %s: %s" % (log_group_name, getattr(e, 'message', repr(e))))
            continue

        ssm_response = ssm.put_parameter(
            Name=ssm_parameter_name,
            Type="String",
            Value=str(export_to_time),
            Overwrite=True)
