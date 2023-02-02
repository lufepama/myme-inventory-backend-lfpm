from django.db import models


class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
