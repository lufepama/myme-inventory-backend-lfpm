from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    # quantity = models.IntegerField(default=1, null=True, blank=True)
    # is_available = models.BooleanField(default=True)
