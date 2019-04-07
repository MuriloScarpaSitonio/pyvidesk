import requests

class Api:

    BASE_URL = "https://api.movidesk.com/public/v1"

    def __init__(self, token):
        self.token = token

    def get(self, url, params):
        params['token'] = self.token
        return requests.get(url, params=params)
