import json

from graphene_django.utils.testing import GraphQLTestCase

from . import schema
from .models import Product


class ProductTestCase(GraphQLTestCase):
    GRAPHENE_SCHEMA = schema.schema

    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="Test description",
            price=10.99,
            stock_quantity=100,
        )

    def test_query_all_mymodels(self):
        response = self.query(
            """
            query {
                products {
                    id
                    name
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        data = json.loads(response.content.decode("utf-8"))["data"]
        self.assertEqual(len(data["products"]), Product.objects.count())

    def test_query_single_product(self):
        response = self.query(
            """
            query {
                product(id: %s) {
                    id
                    name
                    description
                    price
                    stockQuantity
                }
            }
            """
            % self.product.id
        )

        self.assertResponseNoErrors(response)
        data = json.loads(response.content.decode("utf-8"))["data"]
        self.assertEqual(data["product"]["name"], self.product.name)
        self.assertEqual(data["product"]["description"], self.product.description)
        self.assertEqual(float(data["product"]["price"]), float(self.product.price))
        self.assertEqual(data["product"]["stockQuantity"], self.product.stock_quantity)
