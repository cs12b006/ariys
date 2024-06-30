from graphene_django.utils import GraphQLTestCase

from inventory import schema
from inventory.models import Customer, Product, PurchaseOrder, PurchaseOrderProduct


class BaseTest(GraphQLTestCase):
    GRAPHQL_URL = "/graphql/"
    GRAPHENE_SCHEMA = schema.schema

    def setUp(self):
        self.product_saree = Product.objects.create(
            name="Test Saree Product",
            description="Test description",
            price=100,
            stock_quantity=100,
        )
        self.product_jacket = Product.objects.create(
            name="Test Jacket Product",
            description="Test description",
            price=10,
            stock_quantity=100,
        )
        self.customer = Customer.objects.create(name="botcha", address="MVV city")
        self.purchase_order = PurchaseOrder.objects.create(customer=self.customer)
        PurchaseOrderProduct.objects.create(
            purchase_order=self.purchase_order,
            product=self.product_saree,
            quantity=1,
            price=self.product_saree.price,
        )
        PurchaseOrderProduct.objects.create(
            purchase_order=self.purchase_order,
            product=self.product_jacket,
            quantity=2,
            price=self.product_jacket.price,
        )
