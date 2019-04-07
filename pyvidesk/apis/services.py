from pyvidesk.apis.api import Api

class Services:

    def __init__(self, api):
        self.api = api
        assert isinstance(api, Api), "Pyvidesk.Services didn't receive a valid Api object"

    def get_by_id(self, serviceId):
        params = { 'id': serviceId }
        r = self.api.get('/services', params)
        return r.json()
