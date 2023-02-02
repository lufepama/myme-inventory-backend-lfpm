from django.db import models
from apps.product.models import Product
from apps.warehouse.models import Warehouse


class WareProducts(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)

    @property
    def decrease_product_amount(self):
        pass

    @property
    def get_product_data(self):
        return {
            'id': self.product.pk,
            'name': self.product.name,
            'description': self.product.description,
            'price': self.product.price,
            'amount': self.amount
        }
