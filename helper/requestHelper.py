import requests

class RequestUtility():
    def __init__(self):
        self.headers = {"content-type": "application/json"}

    def send_request(self, method, url, message=None):
        try:
            response = requests.request(method, url=url, headers=self.headers, data=message)
        except Exception as e:
            print(e)
        finally:
            return response