import graphene
from graphene_django import DjangoObjectType

from .graphql.purchase_order import CreatePurchaseOrder, PurchaseOrderType
from .models import Product, PurchaseOrder


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class Mutation(graphene.ObjectType):
    create_purchase_order = CreatePurchaseOrder.Field()


class Query(graphene.ObjectType):
    products = graphene.List(ProductType)
    product = graphene.Field(ProductType, id=graphene.Int())
    purchase_orders = graphene.List(PurchaseOrderType)

    def resolve_products(self, info, **kwargs):
        return Product.objects.all().order_by("-ordered_quantity")

    def resolve_purchase_orders(self, info, **kwargs):
        return PurchaseOrder.objects.all().order_by("-updated_at")

    def resolve_product(self, info, id):
        return Product.objects.get(pk=id)


schema = graphene.Schema(query=Query, mutation=Mutation)
