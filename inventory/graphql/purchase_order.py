import graphene
from graphene_django.types import DjangoObjectType

from inventory.models import Customer, Product, PurchaseOrder, PurchaseOrderProduct


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer


class PurchaseOrderProductType(DjangoObjectType):
    class Meta:
        model = PurchaseOrderProduct


class PurchaseOrderType(DjangoObjectType):
    customer = graphene.Field(CustomerType)
    products = graphene.List(PurchaseOrderProductType)

    class Meta:
        model = PurchaseOrder

    def resolve_customer(self, info):
        return self.customer

    def resolve_products(self, info):
        return self.purchaseorderproduct_set.all()


class PurchaseOrderProductInputType(graphene.InputObjectType):
    product_id = graphene.Int(required=True)
    quantity = graphene.Int(required=True)
    price = graphene.Int()


class PurchaseOrderInputType(graphene.InputObjectType):
    products = graphene.List(PurchaseOrderProductInputType)
    customer_id = graphene.Int()


class CreatePurchaseOrder(graphene.Mutation):
    class Arguments:
        order_data = PurchaseOrderInputType(required=True)

    purchase_order = graphene.Field(PurchaseOrderType)

    def mutate(self, info, order_data):
        # Create PurchaseOrder
        purchase_order = PurchaseOrder.objects.create(customer_id=order_data.customer_id)

        for product_data in order_data.products:
            product = Product.objects.get(id=product_data.product_id)
            PurchaseOrderProduct.objects.create(
                purchase_order=purchase_order,
                product=product,
                quantity=product_data.quantity,
                price=product_data.price or product.price,
            )

        return CreatePurchaseOrder(purchase_order=purchase_order)
