from django.urls import path, include

urlpatterns = [
    path('user/', include('apps.user.urls')),
    path('product/', include('apps.product.urls')),
    path('warehouse/', include('apps.warehouse.urls')),
    path('wareproduct/', include('apps.wareproduct.urls')),
]
