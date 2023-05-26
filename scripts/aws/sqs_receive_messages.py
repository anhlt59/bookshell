import json
from pprint import pprint

import boto3

# Create SQS client
sqs = boto3.client("sqs")


def get_sqs_messages(queue_url):
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=["SentTimestamp"],
        MaxNumberOfMessages=10,
        MessageAttributeNames=["All"],
        VisibilityTimeout=10,
    )
    if items := response.get("Messages", []):
        for item in items:
            yield json.loads(item["Body"])

        next_items = get_sqs_messages(queue_url)
        for item in next_items:
            yield item


def main():
    queue_url = "https://sqs.us-east-1.amazonaws.com/251623506909/materially-v105-LoadQueue"
    messages = list(get_sqs_messages(queue_url))

    # uniq = set()
    # for message in messages:
    #     uniq.add(message['item']['PK'] + message['item']['SK'])

    # pprint(messages)
    # print(f'got {len(messages)} messages')
    # print(f'got {len(uniq)} unique messages')

    with open("/Users/anhlt/Projects/freelance/materially-bridge-app-lambdas/tests/messages.json", "w") as f:
        json.dump(messages, f)


if __name__ == "__main__":
    main()
