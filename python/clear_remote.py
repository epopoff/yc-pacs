import json
import boto3
import requests
from requests.auth import HTTPBasicAuth
import os
import uuid
from boto3.dynamodb.conditions import Key, Attr

# Credentials for API PACS
cloud_rw_pacs_auth = HTTPBasicAuth(os.environ['CLOUD_RW_PACS_USER'], os.environ['CLOUD_RW_PACS_PASSWORD'])
remote_pacs_auth = HTTPBasicAuth(os.environ['REMOTE_PACS_USER'], os.environ['REMOTE_PACS_PASSWORD'])

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

i = get_index('last_change_cloud_pacs')

def handler(event, context):
    # Get index of last changes from DB
    i = get_index('last_change_cloud_pacs')

    res = requests.get(
        f"{os.environ['CLOUD_RW_PACS_ENDPOINT']}/changes",
        params={
            'since': i,
            'limit': 100000
        },
        auth=cloud_rw_pacs_auth)

    for change in res.json()['Changes']:
        if change['ChangeType']=='StableStudy':
            studyID = change['ID']
            # Get study information from cloud-pacs
            study = requests.get(
                f"{os.environ['CLOUD_RW_PACS_ENDPOINT']}/studies/{studyID}",
                auth=cloud_rw_pacs_auth
            )

            # Get study statistics from cloud-pacs
            statistics = requests.get(
                f"{os.environ['CLOUD_RW_PACS_ENDPOINT']}/studies/{studyID}/statistics",
                auth=cloud_rw_pacs_auth
            )
            countInstancesCloud = int(statistics.json()['CountInstances'])
            DiskSizeCloud = int(statistics.json()['DiskSize'])

            # Get study information and statistics from DB
            q = get_docapi_table('studies').query(
                KeyConditionExpression = Key('StudyInstanceUID').eq(study.json()['MainDicomTags']['StudyInstanceUID'])
            )
            countInstancesRemote = int(q['Items'][0]['RemoteInfo']['CountInstances'])
            DiskSizeRemote = int(q['Items'][0]['RemoteInfo']['DiskSize'])

            # Delete study from remote-pacs
            if countInstancesCloud == countInstancesRemote and DiskSizeCloud == DiskSizeRemote:
                remoteStudyID = q['Items'][0]['RemoteInfo']['StudyID']
                delete = requests.delete(
                    f"{os.environ['REMOTE_PACS_ENDPOINT']}/studies/{remoteStudyID}",
                    auth=remote_pacs_auth
                )
                # Change status in DB
                get_docapi_table('studies').update_item(
                    Key = {'StudyInstanceUID': study.json()['MainDicomTags']['StudyInstanceUID']},
                    AttributeUpdates = {
                        'Status': {'Value': 'Deleted frome remote-pacs', 'Action': 'PUT'}
                    }
                )
                print('Исследование успешно удалено из remote-pacs')
            else:
                print(f"Исследование {study.json()['MainDicomTags']['StudyInstanceUID']} скопировано не верно! Нужно написать код, который сам будет обрабатывать этот косяк))")

    # Update index of last changes in DB
    i = res.json()['Last']
    changeIndex = get_docapi_table('index').put_item(
        Item={
            'index': 'last_change_cloud_pacs',
            'value': i
        }
    )

    return "OK"