#!/usr/bin/python3
import argparse
import datetime
import time
from itertools import islice
from pprint import pprint

import boto3

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stage", help="stage name", default="testing")
parser.add_argument("-r", "--region", help="region name", default="us-east-1")
# parser.add_argument("-p", "--profile", help="aws cli profile", default='materially')
args = parser.parse_args()

# boto3.setup_default_session(profile_name=args.profile)
TABLE_NAME = f"materially-{args.stage}-table"

dynamo_client = boto3.resource("dynamodb")
table = dynamo_client.Table(TABLE_NAME)


def chunks(objs, limit=100):
    objs = iter(objs)
    while True:
        batch = list(islice(objs, limit))
        if not batch:
            break
        yield batch


def dynamo_get_all_items(**query_params):
    """get_all_dynamo_items(TableName=TABLE_NAME)"""
    # dummy start_key
    start_key = True
    while start_key:
        try:
            response = table.scan(**query_params)
        except Exception as e:
            print(f"Couldn't get dynamo items - {e}, Retry get dynamo item")
            time.sleep(1)
        else:
            for item in response.get("Items", []):
                yield item
            if start_key := response.get("LastEvaluatedKey"):
                query_params.update(ExclusiveStartKey=start_key)


def update_loadout_plant(item):
    """
    a. ticketingSystem field should be added and have a default value. (LoadoutPlant migration)
    - for all records, add a new field, `ticketingSystem` with the value of `BMG`
    """
    return {
        "Update": {
            "TableName": TABLE_NAME,
            "Key": {"PK": {"S": item["PK"]}, "SK": {"S": item["SK"]}},
            "UpdateExpression": "SET ticketingSystem = :v",
            "ExpressionAttributeValues": {":v": "BMG"},
        }
    }


def update_order(item):
    """
    a. deliveryStartDate should be updated.
      - timezone offset should be added (+5 OR 0 hours).
    b. deliveryEndDate should be updated.
      - timezone offset should be added (+5 hours +23 hours +59 mins +59 secs OR 0).
      - for SINGLE_DAY order, deliveryEndDate should be deliveryStartDate + 23:59:59.
    c. GSI3PK/externalOrderId should be updated.
      - for MULTI_DAY order, it should be empty/NULL.
      - for SINGLE_DAY order, don't update it at this stage, as it should be used for associating scheduled shipments.
    """
    return {
        "Update": {
            "TableName": TABLE_NAME,
            "Key": {"PK": {"S": item["PK"]}, "SK": {"S": item["SK"]}},
            "UpdateExpression": "SET deliveryStartDate = :deliveryStartDate AND deliveryEndDate = :deliveryEndDate AND GSI3PK = :GSI3PK",
            "ExpressionAttributeValues": {
                ":deliveryStartDate": "deliveryStartDate",
                ":deliveryEndDate": "deliveryEndDate",
                ":GSI3PK": "GSI3PK",
            },
        }
    }


def update_order_log(item):
    """
    a. triggeredBy should be updated.
    - BMG Data Bridge should be SUPPLIER.
    b. userName should be updated.
    - BMG should be empty/NULL.
    """
    return {
        "Update": {
            "TableName": TABLE_NAME,
            "Key": {"PK": {"S": item["PK"]}, "SK": {"S": item["SK"]}},
            "UpdateExpression": "SET deliveryStartDate = :deliveryStartDate AND deliveryEndDate = :deliveryEndDate AND GSI3PK = :GSI3PK",
            "ExpressionAttributeValues": {
                ":deliveryStartDate": "deliveryStartDate",
                ":deliveryEndDate": "deliveryEndDate",
                ":GSI3PK": "GSI3PK",
            },
        }
    }


def update_shipment(item):
    """a. All the scheduled shipments on Prod should be deleted."""
    return item


def update_ticket(item):
    """
    a. departureDate should be updated.
    - timezone offset should be added (+5 hours OR +4 hours OR 0).
    b. departureDateTime should be updated.
    - timezone offset should be added (+5 hours OR +4 hours).
    c. scheduleDate should be updated.
    - timezone offset should be added (+5 hours OR +4 hours OR 0)
    """
    return item


def main():
    print(f"Total items: {table.item_count}")
    all_items = dynamo_get_all_items(TableName=TABLE_NAME, Limit=10)

    for items in chunks(all_items, 25):
        transact_items = []
        for item in items:
            if item.get("GSI0PK") == "LOADOUTPLANT":
                transact_items.append(update_loadout_plant(item))
            elif item.get("GSI0PK") == "ORDER":
                transact_items.append(update_order(item))
            elif item.get("GSI0PK") == "EXTERNALORDER":
                transact_items.append(update_shipment(item))
            elif item.get("GSI0PK") == "TICKET":
                transact_items.append(update_ticket(item))
            elif item.get("GSI0PK") == "ORDERLOG":
                transact_items.append(update_order_log(item))
            dynamo_client.transact_write_items(TransactItems=transact_items)


if __name__ == "__main__":
    main()
