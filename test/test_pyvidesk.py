import unittest

from pyvidesk.pyvidesk import Pyvidesk
from pyvidesk.apis.services import Services

class TestApi(unittest.TestCase):

    def test_has_services(self):
        pyvidesk = Pyvidesk('sampleToken')
        self.assertIsInstance(pyvidesk.services, Services)

