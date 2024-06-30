import json

from inventory.models import Product
from inventory.tests.base import BaseTest


class ProductTestCase(BaseTest):
    def setUp(self):
        super().setUp()

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
            % self.product_jacket.id
        )

        self.assertResponseNoErrors(response)
        data = json.loads(response.content.decode("utf-8"))["data"]
        self.assertEqual(data["product"]["name"], self.product_jacket.name)
        self.assertEqual(data["product"]["description"], self.product_jacket.description)
        self.assertEqual(float(data["product"]["price"]), float(self.product_jacket.price))
        self.assertEqual(data["product"]["stockQuantity"], self.product_jacket.stock_quantity)
