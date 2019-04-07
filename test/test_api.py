import unittest

from pyvidesk.api import Api

class TestApi(unittest.TestCase):

    def test_token(self):
        api = Api('sampleToken')
        self.assertEqual(api.token, 'sampleToken')

