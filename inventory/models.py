from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    ordered_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Customer(BaseModel):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.TextField()

    def __str__(self):
        return self.name


class PurchaseOrder(BaseModel):
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField(Product, through="PurchaseOrderProduct")

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Save to get the primary key
            super().save(*args, **kwargs)
            self.order_number = f"O{str(self.pk).zfill(5)}"
            self.__class__.objects.filter(pk=self.pk).update(order_number=self.order_number)
        else:
            super().save(*args, **kwargs)


class PurchaseOrderProduct(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    class Meta:
        unique_together = ("purchase_order", "product")

    def __str__(self):
        return f"{self.purchase_order.order_number} - {self.product.name} - {self.quantity}"
