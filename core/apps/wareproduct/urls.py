from django.urls import path, include
from . import views

urlpatterns = [
    path('get-products', views.get_warehouse_products,
         name='get-warehouse-products'),
    path('create-product', views.create_warehouse_product,
         name='create-warehouse-product'),
    path('create-multiple-product', views.create_multiple_warehouse_product,
         name='create-warehouse-product'),
    path('delete-product', views.delete_warehouse_product,
         name='get-warehouse-products'),
    path('delete-multiple-product', views.delete_multiple_warehouse_product,
         name='get-warehouse-products'),
    path('update-product-amount', views.update_amount_warehouse_product,
         name='update-warehouse-products'),
]
