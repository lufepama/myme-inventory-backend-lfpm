from django.urls import path
from .views import create_user, Login, logout

urlpatterns = [
    path('signup', create_user, name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
]
