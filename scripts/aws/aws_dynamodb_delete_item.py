from pprint import pprint

import boto3
from boto3.dynamodb.conditions import Key

dynamo_client = boto3.resource("dynamodb", verify=False)
table = dynamo_client.Table("paw-pnt-users")


def get_dynamo_items(items=None, **query_params):
    if not items:
        items = []

    try:
        response = table.query(**query_params)
    except Exception as e:
        print(f"Couldn't get dynamo items: {e}")
    else:
        items.extend(response.get("Items", []))

        if start_key := response.get("LastEvaluatedKey"):
            query_params.update(ExclusiveStartKey=start_key)
            return get_dynamo_items(items, **query_params)

    return items


def get_deprecated_users():
    items = get_dynamo_items(
        ProjectionExpression="hashKey, rangeKey",
        KeyConditionExpression=Key("hashKey").eq("user;"),
    )
    return list(filter(lambda x: not x["rangeKey"].endswith(";"), items))


def get_user_items(hash_key):
    return get_dynamo_items(
        ProjectionExpression="hashKey, rangeKey", KeyConditionExpression=Key("hashKey").eq(hash_key)
    )


def dynamodb_delete_items(items):
    if items:
        with table.batch_writer() as batch:
            for item in items:
                batch.delete_item(Key={"hashKey": item["hashKey"], "rangeKey": item["rangeKey"]})


def main():
    deprecated_users = get_deprecated_users()
    dynamodb_delete_items(deprecated_users)
    pprint(deprecated_users)
    print(f"Delete {len(deprecated_users)} items")


if __name__ == "__main__":
    main()
