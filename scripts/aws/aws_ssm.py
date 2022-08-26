from pprint import pprint

import boto3

client = boto3.client("ssm")

# response = client.describe_parameters(
#     ParameterFilters=[
#         {
#             'Key': 'Name',
#             'Option': 'BeginsWith',
#             'Values': [
#                 '/Dev/materially',
#             ]
#         },
#     ],
# )
# pprint(response)

response = client.get_parameter(Name="/Dev/materially/firebase_client_email")
pprint(response)
