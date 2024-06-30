import json

from inventory.models import PurchaseOrder
from inventory.tests.base import BaseTest


class PurchaseOrderTestCase(BaseTest):
    def test_query_all_purchase_orders(self):
        response = self.query(
            """
            query {
                purchaseOrders {
                    id
                    orderNumber
                    customer {
                        name
                    }
                    products {
                        product {
                            name
                        }
                        quantity
                    }
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        data = json.loads(response.content.decode("utf-8"))["data"]
        self.assertEqual(len(data["purchaseOrders"]), PurchaseOrder.objects.count())
        purchase_order = data["purchaseOrders"][0]
        self.assertEqual(purchase_order["customer"]["name"], self.customer.name)
        self.assertEqual(len(purchase_order["products"]), 2)
        self.assertEqual(purchase_order["products"][0]["product"]["name"], self.product_saree.name)
        self.assertEqual(purchase_order["products"][0]["quantity"], 1)
        self.assertEqual(purchase_order["products"][1]["product"]["name"], self.product_jacket.name)
        self.assertEqual(purchase_order["products"][1]["quantity"], 2)

    def test_create_purchase_order(self):
        # before saree ordered
        saree_global_orders = self.product_saree.ordered_quantity
        response = self.query(
            """
            mutation {
                createPurchaseOrder(orderData: {
                    customerId: %d,
                    products: [
                        { productId: %d, quantity: 3 },
                        { productId: %d, quantity: 4 }
                    ]
                }) {
                    purchaseOrder {
                        orderNumber
                        id
                    }
                }
            }
            """
            % (self.customer.id, self.product_saree.id, self.product_jacket.id)
        )
        self.assertResponseNoErrors(response)
        data = json.loads(response.content.decode("utf-8"))["data"]
        purchase_order_id = data["createPurchaseOrder"]["purchaseOrder"]["id"]
        purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
        self.assertIsNotNone(purchase_order.order_number)
        self.assertEqual(purchase_order.customer.name, self.customer.name)
        self.assertEqual(purchase_order.products.count(), 2)

        product_saree_order = purchase_order.purchaseorderproduct_set.get(product=self.product_saree)
        self.assertEqual(product_saree_order.quantity, 3)
        self.assertEqual(self.product_saree.ordered_quantity, saree_global_orders+3)

        product_jacket_order = purchase_order.purchaseorderproduct_set.get(product=self.product_jacket)
        self.assertEqual(product_jacket_order.quantity, 4)
