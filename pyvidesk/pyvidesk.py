from .apis.api import Api
from .apis.services import Services

class Pyvidesk:

    def __init__(self, token):
        api = Api(token)
        self.services = Services(api)
