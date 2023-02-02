from django.urls import path
from .views import create_product, delete_product, get_products

urlpatterns = [
    path('create', create_product, name='create-product'),
    path('get-products', get_products, name='get-product'),
    path('delete/<int:productId>', delete_product, name='delete-product'),
]
