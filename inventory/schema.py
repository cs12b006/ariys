import graphene
from graphene_django import DjangoObjectType

from .models import Product


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class Query(graphene.ObjectType):
    products = graphene.List(ProductType)
    product = graphene.Field(ProductType, id=graphene.Int())

    def resolve_products(self, info, **kwargs):
        return Product.objects.all().order_by('-ordered_quantity')

    def resolve_product(self, info, id):
        return Product.objects.get(pk=id)


schema = graphene.Schema(query=Query)
