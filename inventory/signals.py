from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PurchaseOrderProduct

@receiver(post_save, sender=PurchaseOrderProduct)
def update_product_ordered_quantity_on_save(sender, instance, created, **kwargs):
    product = instance.product
    if created:
        product.ordered_quantity += instance.quantity
    else:
        # Get the previous instance to update the ordered quantity correctly
        previous_instance = sender.objects.get(pk=instance.pk)
        product.ordered_quantity -= previous_instance.quantity
        product.ordered_quantity += instance.quantity
    product.save()

@receiver(post_delete, sender=PurchaseOrderProduct)
def update_product_ordered_quantity_on_delete(sender, instance, **kwargs):
    product = instance.product
    product.ordered_quantity -= instance.quantity
    product.save()
