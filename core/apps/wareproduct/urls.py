from django.urls import path, include
from .views import get_warehouse_products, delete_warehouse_product, create_warehouse_product

urlpatterns = [
    path('get-products', get_warehouse_products, name='get-warehouse-products'),
    path('create-product', create_warehouse_product,
         name='create-warehouse-product'),
    path('delete-product', delete_warehouse_product,
         name='get-warehouse-products'),
]
