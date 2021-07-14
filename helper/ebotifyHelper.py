import json
import requests
import os
from datetime import datetime, timedelta

class EbotifyUtility():

    def get_token(self):

        f = open('ebotify_auth.json', 'rt')
        auth = json.load(f)
        f.close()

        curdate = datetime.now()
        
        if len(auth) == 0 or datetime.strptime(auth['expiry_date'], '%Y-%m-%dT%H:%M:%S.%f') < curdate:
            return None
        else:
            return auth['token']

    def generate_token(self):
        
        url = "https://dev2-api.ebotify.chat/api/v2/user/login"

        headers = {
            'accept': "application/json",
            'Content-Type': "application/json",
            'urlDomain': "dev2.ebotify.chat"
            }

        payload = {"email": "epurohit@ebotify.com",  "password": "epurohit@123"}

        data = json.dumps(payload)
        response = requests.request("POST", url, data=data, headers=headers)
        generated_token = json.loads(response.text)['body']['token']

        curdate = datetime.now()
        curdate += timedelta(days=2)
        new_exp_date = datetime(curdate.year, curdate.month, curdate.day, curdate.hour, curdate.minute, curdate.second, curdate.microsecond)
        auth = {}
        auth['token'] = 'Bearer ' + str(generated_token)
        auth['expiry_date'] = new_exp_date.strftime('%Y-%m-%dT%H:%M:%S.%f')

        f = open('ebotify_auth.json', 'wt')
        f.write(json.dumps(auth))
        f.close()
        return auth['token']