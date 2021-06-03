import os
import logging

import boto3

__all__ = ["get_value", "set_value"]

ssm = boto3.client('ssm', region_name=os.getenv("REGION"))
logger = logging.getLogger(__name__)


def get_value(name, default=0):
    try:
        response = ssm.get_parameter(Name=name)
        return response['Parameter']['Value']
    except ssm.exceptions.ParameterNotFound:
        logger.info(f"SSM name {name} not found")
        return default


def set_value(name, value):
    logger.debug(f"set SSM name {name} to {value}")
    ssm.put_parameter(Name=name, Type="String", Value=value, Overwrite=True)
