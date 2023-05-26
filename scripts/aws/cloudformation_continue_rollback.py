#!/usr/bin/python3
# Auto rollback cloudformation stack in failed state (UPDATE_ROLLBACK_FAILED, UPDATE_FAILED, CREATE_FAILED)
# by skip fail resource and continue rollback
# note: standard stack, not nested stack or stack set
import argparse
import logging
import time

import boto3

_session = boto3.session.Session()
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stack", help="cloudformation stack name", required=True)
parser.add_argument("-r", "--region", help="region name", default=_session.region_name)
parser.add_argument("-p", "--profile", help="aws cli profile id", default=_session.profile_name)
args = parser.parse_args()

boto3.setup_default_session(profile_name=args.profile)
logger = logging.getLogger()
client = boto3.client("cloudformation", region_name=args.region)


def get_stack_status(stack_name):
    """
    Get stack status
    :param stack_name: (str) stack name
    :return: (str) stack status
    """
    response = client.describe_stacks(StackName=stack_name)
    stacks = response["Stacks"]
    return stacks[0]["StackStatus"]


def get_failed_resources(stack_name):
    """
    Get events at previous deployment
    :param stack_name: (str)
    :return: (List) events
    """
    response = client.describe_stack_events(StackName=stack_name)
    events = response["StackEvents"]
    # drop stack fail event
    if events[0]["LogicalResourceId"] == "stack_name":
        events.pop(0)
    # get failed resources
    for event in events:
        if event["ResourceStatus"] in ("UPDATE_FAILED", "CREATE_FAILED", "DELETE_FAILED"):
            yield event["LogicalResourceId"]
        if event["LogicalResourceId"] == "stack_name":
            break


def rollback(stack_name: str, retries: int = 30):
    """
    Rollback cloudformation stack
    :param stack_name: (str) stack name
    :param retries: (int) max retries time
    :return:
    """
    stack_status = get_stack_status(stack_name)
    logger.debug(f"{stack_name} status {stack_status}")

    if stack_status == "UPDATE_ROLLBACK_FAILED":
        # get failed resources
        resource_ids = get_failed_resources(stack_name)
        # rollback stack
        client.continue_update_rollback(StackName=stack_name, ResourcesToSkip=resource_ids)
        logger.debug(f"{stack_name} rollback in progess, skip resources {' '.join(resource_ids)}")

        if retries:
            logger.debug("sleep 30s")
            time.sleep(30)
            return rollback(stack_name, retries - 1)
        else:
            logger.warning("Exceed max retries time")

    elif stack_status in ("UPDATE_ROLLBACK_COMPLETE", "UPDATE_COMPLETE", "CREATE_COMPLETE"):
        logger.debug(f"{stack_name} rollback complete")


if __name__ == "__main__":
    rollback(args.stack)
