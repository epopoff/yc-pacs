import json
import boto3
import requests
from requests.auth import HTTPBasicAuth
import os

import boto3
import requests

boto_session = None
storage_client = None
docapi_table = None
ymq_queue = None

def get_boto_session():
    global boto_session
    if boto_session is not None:
        return boto_session

    access_key = os.environ['ACCESS_KEY_ID']
    secret_key = os.environ['SECRET_ACCESS_KEY']

    # initialize boto session
    boto_session = boto3.session.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    return boto_session

def get_ymq_queue():
    # global ymq_queue
    # if ymq_queue is not None:
    #     return ymq_queue

    ymq_queue = get_boto_session().resource(
        service_name='sqs',
        endpoint_url='https://message-queue.api.cloud.yandex.net',
        region_name='ru-central1'
    ).Queue(os.environ['YMQ_ENDPOINT'])
    return ymq_queue

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

def get_index(index_name):
    i = get_docapi_table('index').get_item(
        Key={
            'index': index_name
        }
    )['Item']['value']
    return i

def handler(event, context):
    # Credentials for API PACS
    remote_pacs_auth = HTTPBasicAuth(os.environ['REMOTE_PACS_USER'], os.environ['REMOTE_PACS_PASSWORD'])
    # Get index of last changes from DB
    i = get_index('last_change_remote_pacs')

    # Request changes on remote PACS
    res = requests.get(
        f"{os.environ['REMOTE_PACS_ENDPOINT']}/changes",
        params={
            'since': i,
            'limit': 100000
        },
        auth=remote_pacs_auth)
    
    # Choosing stable studies
    for change in res.json()['Changes']:
        if change['ChangeType']=='StableStudy':
            studyID = change['ID']
            # Get study information
            study = requests.get(
                f"{os.environ['REMOTE_PACS_ENDPOINT']}/studies/{studyID}",
                params = {
                    'requestedTags': 'ModalitiesInStudy;BodyPartExamined'
                },
                auth=remote_pacs_auth
            )

            # Get study statistics
            statistics = requests.get(
                f"{os.environ['REMOTE_PACS_ENDPOINT']}/studies/{studyID}/statistics",
                auth=remote_pacs_auth
            )

            # Record of study information to DB
            get_docapi_table('studies').put_item(Item={
                    'StudyInstanceUID': study.json()['MainDicomTags']['StudyInstanceUID'],
                    'PatientID': study.json()['PatientMainDicomTags']['PatientID'],
                    'Status': 'new',
                    'ModalitiesInStudy': study.json()['RequestedTags']['ModalitiesInStudy'],
                    # 'BodyPartExamined': study.json()['RequestedTags']['BodyPartExamined'],
                    'RemoteInfo': {
                        'StudyID': study.json()['ID'],
                        'CountInstances': statistics.json()['CountInstances'],
                        'CountSeries': statistics.json()['CountSeries'],
                        'DiskSizeMB': statistics.json()['DiskSizeMB']
                        },
                    })
            
            print(f'Successfully added to YDB: {studyID}')

            get_ymq_queue().send_message(
                MessageBody=json.dumps({
                    'id': studyID
                })
            )
    
    # Update index of last changes in DB      
    i = res.json()['Last']
    res = get_docapi_table('index').put_item(
        Item={
            'index': 'last_change_remote_pacs',
            'value': i
        }
    )

    return "OK"