from datetime import date
import unittest

from pyvidesk.tickets import Tickets
from pyvidesk.query import Q
from tests.config import TOKEN


class TestQuery(unittest.TestCase):
    """Classe que testa a classe Query utilizando a entity Tickets"""

    tickets = Tickets(token=TOKEN)
    properties = tickets.get_properties()

    def test_query(self):
        expected = self.tickets.api.base_url
        result = self.tickets.query.as_url()
        self.assertEqual(result, expected)

    def test_order_by(self):
        expected = self.tickets.api.base_url + "&$select=id&$orderby=id"
        result = self.tickets.query.select("id").order_by("id").as_url()
        self.assertEqual(result, expected)

    def test_order_by_property(self):
        expected = self.tickets.api.base_url + "&$select=id&$orderby=id"
        result = (
            self.tickets.query.select("id").order_by(self.properties["id"]).as_url()
        )
        self.assertEqual(result, expected)

    def test_order_by_property_asc(self):
        expected = self.tickets.api.base_url + "&$select=id&$orderby=id asc"
        result = (
            self.tickets.query.select("id")
            .order_by(self.properties["id"].asc())
            .as_url()
        )
        self.assertEqual(result, expected)

    def test_order_by_property_desc(self):
        expected = self.tickets.api.base_url + "&$select=id&$orderby=id desc"
        result = (
            self.tickets.query.select("id")
            .order_by(self.properties["id"].desc())
            .as_url()
        )
        self.assertEqual(result, expected)

    def test_order_by_property_and_string(self):
        expected = self.tickets.api.base_url + "&$select=id&$orderby=createdDate,id"
        result = (
            self.tickets.query.select("id")
            .order_by(self.properties["createdDate"], "id")
            .as_url()
        )
        self.assertEqual(result, expected)

    def test_order_by_property_desc_and_string(self):
        expected = (
            self.tickets.api.base_url + "&$select=id&$orderby=createdDate desc,id"
        )
        result = (
            self.tickets.query.select("id")
            .order_by(self.properties["createdDate"].desc(), "id")
            .as_url()
        )
        self.assertEqual(result, expected)

    def test_order_by_property_desc_and_property(self):
        expected = (
            self.tickets.api.base_url + "&$select=id&$orderby=createdDate desc,id"
        )
        result = (
            self.tickets.query.select("id")
            .order_by(self.properties["createdDate"].desc(), self.properties["id"])
            .as_url()
        )
        self.assertEqual(result, expected)

    def test_order_by_property_desc_and_property_asc(self):
        expected = (
            self.tickets.api.base_url + "&$select=id&$orderby=createdDate desc,id asc"
        )
        result = (
            self.tickets.query.select("id")
            .order_by(
                self.properties["createdDate"].desc(), self.properties["id"].asc()
            )
            .as_url()
        )
        self.assertEqual(result, expected)

    def test_query_with_filter_eq_operator(self):
        my_filter = self.properties["id"] == "2"
        expected = self.tickets.api.base_url + "&id=2"
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_with_filter_gt_operator(self):
        today = date.today()
        my_filter = self.properties["createdDate"] > today
        expected = (
            self.tickets.api.base_url
            + f"&$filter=createdDate gt {today.strftime('%Y-%m-%d')}Z"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_with_filter_ge_operator(self):
        today = date.today()
        my_filter = self.properties["createdDate"] >= today
        expected = (
            self.tickets.api.base_url
            + f"&$filter=createdDate ge {today.strftime('%Y-%m-%d')}Z"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_with_filter_lt_operator(self):
        today = date.today()
        my_filter = self.properties["createdDate"] < today
        expected = (
            self.tickets.api.base_url
            + f"&$filter=createdDate lt {today.strftime('%Y-%m-%d')}Z"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_with_filter_le_operator(self):
        today = date.today()
        my_filter = self.properties["createdDate"] <= today
        expected = (
            self.tickets.api.base_url
            + f"&$filter=createdDate le {today.strftime('%Y-%m-%d')}Z"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_filter_with_or_operator(self):
        my_filter = Q(self.properties["clients"].id == 55) | Q(
            self.properties["clients"].organization.id == 55
        )
        expected = (
            self.tickets.api.base_url
            + "&$filter=(clients/id eq '55' or clients/organization/id eq '55')"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_array_property_contains(self):
        my_filter = self.properties["tags"].has("My tag")
        expected = self.tickets.api.base_url + "&$filter=tags/any(x: x eq 'My tag')"
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_array_property_contains_negation_operator(self):
        my_filter = self.properties["tags"].has("My tag")
        expected = self.tickets.api.base_url + "&$filter=not tags/any(x: x eq 'My tag')"
        result = self.tickets.query.filter(~Q(my_filter)).as_url()
        self.assertEqual(result, expected)

    def test_query_subproperty_with_filter(self):
        my_filter = self.properties["owner"].id == "2"
        expected = self.tickets.api.base_url + "&$filter=owner/id eq '2'"
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_subproperty_that_is_array(self):
        my_filter = self.properties["actions"].tags.has("My tag")
        expected = self.tickets.api.base_url + (
            "&$filter=actions/any(x: x/tags/any(y: y eq 'My tag'))"
        )
        result = self.tickets.query.filter(my_filter).as_url()
        self.assertEqual(result, expected)

    def test_query_expand_complex_type(self):
        """Teste de expansão com expansão interna, select interno e select externo"""
        expected = self.tickets.api.base_url + "&$expand=customFieldValues"
        result = self.tickets.query.expand(
            self.properties["customFieldValues"],
        ).as_url()
        self.assertEqual(result, expected)

    def test_query_expand_complex_type_with_select(self):
        """Teste de expansão com expansão interna, select interno e select externo"""
        expected = (
            self.tickets.api.base_url + "&$expand=customFieldValues($select=value)"
        )
        result = self.tickets.query.expand(
            self.properties["customFieldValues"],
            select=self.properties["customFieldValues"].value,
        ).as_url()
        self.assertEqual(result, expected)

    def test_query_expand_complex_type_inner_expand(self):
        """Teste de expansão com expansão interna, select interno e select externo"""
        expected = self.tickets.api.base_url + (
            "&$expand=customFieldValues($expand=items)"
        )
        result = self.tickets.query.expand(
            self.properties["customFieldValues"],
            inner={
                "expand": self.properties["customFieldValues"].items,
            },
        ).as_url()
        self.assertEqual(result, expected)

    def test_query_expand_complex_type_inner_expand_and_select(self):
        """Teste de expansão com expansão interna, select interno e select externo"""
        expected = self.tickets.api.base_url + (
            "&$expand=customFieldValues($expand=items($select=customFieldItem))"
        )
        result = self.tickets.query.expand(
            self.properties["customFieldValues"],
            inner={
                "expand": self.properties["customFieldValues"].items,
                "select": self.properties["customFieldValues"].items.customFieldItem,
            },
        ).as_url()
        self.assertEqual(result, expected)

    def test_query_expand_complex_type_with_select_inner_expand_and_select(self):
        """Teste de expansão com expansão interna, select interno e select externo"""
        expected = self.tickets.api.base_url + (
            "&$expand=customFieldValues($expand=items($select=customFieldItem);$select=items)"
        )
        result = self.tickets.query.expand(
            self.properties["customFieldValues"],
            inner={
                "expand": self.properties["customFieldValues"].items,
                "select": self.properties["customFieldValues"].items.customFieldItem,
            },
            select=self.properties["customFieldValues"].items,
        ).as_url()
        self.assertEqual(result, expected)

    def test_query_expand_complex_type_with_multiple_inner_both_expand(self):
        """Teste de expansão com expansão interna, select interno e select externo"""
        expected = self.tickets.api.base_url + (
            "&$expand=actions($expand=timeAppointments($expand=createdBy))"
        )
        result = self.tickets.query.expand(
            self.properties["actions"],
            inner={
                "expand": self.properties["actions"].timeAppointments,
                "inner": {
                    "expand": self.properties["actions"].timeAppointments.createdBy,
                },
            },
        ).as_url()
        self.assertEqual(result, expected)

    def test_query_expand_complex_type_with_multiple_inner_both_expand_inner_select(
        self,
    ):
        """Teste de expansão com expansão interna, select interno e select externo"""
        expected = self.tickets.api.base_url + (
            "&$expand=actions($expand=timeAppointments($expand=createdBy($select=id)))"
        )
        result = self.tickets.query.expand(
            self.properties["actions"],
            inner={
                "expand": self.properties["actions"].timeAppointments,
                "inner": {
                    "expand": self.properties["actions"].timeAppointments.createdBy,
                    "select": self.properties["actions"].timeAppointments.createdBy.id,
                },
            },
        ).as_url()
        self.assertEqual(result, expected)

    def test_query_expand_complex_type_with_multiple_inner_both_expand_both_select(
        self,
    ):
        """Teste de expansão com expansão interna, select interno e select externo"""
        expected = self.tickets.api.base_url + (
            "&$expand=actions($expand=timeAppointments($expand=createdBy($select=id);$select=activity))"
        )
        result = self.tickets.query.expand(
            self.properties["actions"],
            inner={
                "expand": self.properties["actions"].timeAppointments,
                "inner": {
                    "expand": self.properties["actions"].timeAppointments.createdBy,
                    "select": self.properties["actions"].timeAppointments.createdBy.id,
                },
                "select": self.properties["actions"].timeAppointments.activity,
            },
        ).as_url()
        self.assertEqual(result, expected)

    def test_query_expand_complex_type_with_multiple_inner_both_expand_all_selects(
        self,
    ):
        """Teste de expansão com expansão interna, select interno e select externo"""
        expected = self.tickets.api.base_url + (
            "&$expand=actions($expand=timeAppointments($expand=createdBy($select=id);$select=activity);$select=id)"
        )
        result = self.tickets.query.expand(
            self.properties["actions"],
            inner={
                "expand": self.properties["actions"].timeAppointments,
                "inner": {
                    "expand": self.properties["actions"].timeAppointments.createdBy,
                    "select": self.properties["actions"].timeAppointments.createdBy.id,
                },
                "select": self.properties["actions"].timeAppointments.activity,
            },
            select=self.properties["actions"].id,
        ).as_url()
        self.assertEqual(result, expected)
