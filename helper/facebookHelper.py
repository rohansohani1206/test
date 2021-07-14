import sys
sys.path.append(".")
from config.config import FB_TOKEN
from helper.requestHelper import RequestUtility
import json

class FacebookUtility():

    def __init__(self, senderId):
        self.sender_id = senderId
        self.fb_token = FB_TOKEN

    def get_Name(self):
        request_utility = RequestUtility()
        url = 'https://graph.facebook.com/{}?fields=name&access_token={}'.format(self.sender_id, self.fb_token)
        response = request_utility.send_request("GET", url)
        data = json.loads(response.text)
        fullname = data.get("name")
        return fullname