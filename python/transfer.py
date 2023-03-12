import json
import boto3
import requests
from requests.auth import HTTPBasicAuth
import os
import sys

boto_session = None
docapi_table = None

cloud_rw_pacs_auth = HTTPBasicAuth(os.environ['CLOUD_RW_PACS_USER'], os.environ['CLOUD_RW_PACS_PASSWORD'])

# Create session
def get_boto_session():
    global boto_session
    if boto_session is not None:
        return boto_session

    # extract values from env
    access_key = os.environ['ACCESS_KEY_ID']
    secret_key = os.environ['SECRET_ACCESS_KEY']

    # initialize boto session
    boto_session = boto3.session.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    return boto_session

def get_docapi_table(table_name):
    # global docapi_table
    # if docapi_table is not None:
    #     return docapi_table

    docapi_table = get_boto_session().resource(
        'dynamodb',
        endpoint_url=os.environ['DOCAPI_ENDPOINT'],
        region_name='ru-central1'
    ).Table(table_name)
    return docapi_table


def handler(event, context):
    # Credentials for API PACS
    cloud_rw_pacs_auth = HTTPBasicAuth(os.environ['CLOUD_RW_PACS_USER'], os.environ['CLOUD_RW_PACS_PASSWORD'])

    for message in event['messages']:
        body_json = json.loads(message['details']['message']['body'])
        studyID = body_json['id']
        res = requests.post(
            f"{os.environ['CLOUD_RW_PACS_ENDPOINT']}/transfers/pull",
            data=json.dumps({
                    "Resources": [{"Level": "Study", "ID": studyID}],
                    "Compression" : "gzip",
                    "Peer" : "remote-pacs"
                }),
        auth=cloud_rw_pacs_auth)

    return 'OK'