from itertools import islice
from pprint import pprint
from typing import Dict, Iterable, Iterator, List

import boto3

client = boto3.client("ssm", region_name="us-east-1", endpoint_url=None)


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


def main():
    keys = ["/Lambdas/development/"]
    pprint(dict(get_parameters(keys)))


if __name__ == "__main__":
    main()
