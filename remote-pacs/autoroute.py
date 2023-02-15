import orthanc
import json
import requests

TOKEN = orthanc.GenerateRestApiAuthorizationToken()
BASE_URL = 'http://127.0.0.1:8042'

def OnChange(changeType, level, resourceId):
    if changeType == orthanc.ChangeType.STABLE_STUDY:    
        res = json.loads(orthanc.RestApiGet(f"/studies/{resourceId}"))
        
        # отправляем исследование с помощью transfer acceleration plugin в другой инстанс
        res = requests.post(
            f"{BASE_URL}/transfers/send",
            headers={"Authorization": TOKEN},
            data=json.dumps({
                "Resources": [{"Level": "Study", "ID": resourceId}],
                "Compression" : "gzip",
                "Peer" : "cloud-rw-pacs"
            })
        )        
orthanc.RegisterOnChangeCallback(OnChange)
