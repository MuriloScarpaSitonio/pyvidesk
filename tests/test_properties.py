import unittest

from pyvidesk.tickets import Tickets
from tests.config import TOKEN

# TODO: expand this module


class TestQuery(unittest.TestCase):
    """Classe que testa a classe Query utilizando a entity Tickets"""

    properties = Tickets(token=TOKEN).get_properties()

    def test_contains_string_property(self):
        prop = self.properties["subject"]
        expected = "contains(subject, 'name')"
        result = prop.contains("name")
        self.assertEqual(result, expected)

    def test_contains_string_complex_property(self):
        prop = self.properties["clients"].businessName
        expected = "contains(clients/businessName, 'name')"
        result = prop.contains("name")
        self.assertEqual(result, expected)