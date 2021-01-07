import unittest

from pyvidesk.lambdas import All, AllAll, AllAny, Any, AnyAll, AnyAny
from pyvidesk.tickets import Tickets


class TestLambdas(unittest.TestCase):
    """Classe que testa as funções do arquivo lambdas.py"""

    properties = Tickets(token="").get_properties()

    def test_lambda_any(self):
        result = Any(self.properties["clients"].id == "2")
        expected = "clients/any(x: x/id eq '2')"
        self.assertEqual(result, expected)

    def test_lambda_any_and_multi_splitabble_value(self):
        """Teste da funcao Any quando o valor tem espacos"""
        expected = "clients/any(x: x/businessName eq 'Nome grande para teste')"
        result = Any(
            self.properties["clients"].businessName == "Nome grande para teste"
        )
        self.assertEqual(result, expected)

    def test_subproperty_lambda_any(self):
        expected = "clients/any(x: x/organization/id eq '2')"
        result = Any(self.properties["clients"].organization.id == "2")
        self.assertEqual(result, expected)

    def test_lambda_all(self):
        expected = "clients/all(x: x/id eq '2')"
        result = All(self.properties["clients"].id == "2")
        self.assertEqual(result, expected)

    def test_subproperty_and_lambda_all(self):
        expected = "clients/all(x: x/organization/id eq '2')"
        result = All(self.properties["clients"].organization.id == "2")
        self.assertEqual(result, expected)

    def test_anyany(self):
        """Teste usando dois operadores lambda: any e any"""
        expected = (
            "customFieldValues/any(x: x/items/any"
            "(y: y/customFieldItem eq 'MGSSUSTR6-06R'))"
        )
        result = AnyAny(
            self.properties["customFieldValues"].items.customFieldItem
            == "MGSSUSTR6-06R"
        )
        self.assertEqual(result, expected)

    def test_lambda_anyany_and_splitabble_value(self):
        """Teste da funcao any e any quando o valor tem espacos"""
        expected = (
            "customFieldValues/any(x: x/items/any"
            "(y: y/customFieldItem eq 'MGSSUSTR6-06R e MGSSUSTR6-06P'))"
        )
        result = AnyAny(
            self.properties["customFieldValues"].items.customFieldItem
            == "MGSSUSTR6-06R e MGSSUSTR6-06P"
        )
        self.assertEqual(result, expected)

    def test_lambda_anyall(self):
        """Teste usando dois operadores lambda: any e all"""
        expected = "customFieldValues/any(x: x/items/all(y: y/customFieldItem eq 'MGSSUSTR6-06R'))"
        result = AnyAll(
            self.properties["customFieldValues"].items.customFieldItem
            == "MGSSUSTR6-06R"
        )
        self.assertEqual(result, expected)

    def test_lambda_allany(self):
        """Teste usando dois operadores lambda: all e any"""
        expected = "customFieldValues/all(x: x/items/any(y: y/customFieldItem eq 'MGSSUSTR6-06R'))"
        result = AllAny(
            self.properties["customFieldValues"].items.customFieldItem
            == "MGSSUSTR6-06R"
        )
        self.assertEqual(result, expected)

    def test_lambda_allall(self):
        """Teste usando dois operadores lambda: all e all"""
        expected = "customFieldValues/all(x: x/items/all(y: y/customFieldItem eq 'MGSSUSTR6-06R'))"
        result = AllAll(
            self.properties["customFieldValues"].items.customFieldItem
            == "MGSSUSTR6-06R"
        )
        self.assertEqual(result, expected)

    def test_lambda_anyany_and_more_than_three_properties(self):
        expected = (
            "actions/any(x: x/timeAppointments/any"
            "(y: y/createdBy/businessName eq 'Gustavo Adriano'))"
        )
        result = AnyAny(
            self.properties["actions"].timeAppointments.createdBy.businessName
            == "Gustavo Adriano"
        )
        self.assertEqual(result, expected)
