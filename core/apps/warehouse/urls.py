from django.urls import path
from .views import create_warehouse, delete_warehouse, get_warehouses

urlpatterns = [
    path('create', create_warehouse, name='create-warehouse'),
    path('get-warehouses', get_warehouses, name='get-warehouse'),
    path('delete/<int:warehouseId>', delete_warehouse, name='delete-warehouse'),
]
