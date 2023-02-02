from django.db import models
from django.contrib.auth.models import AbstractUser

"""
    The user auth is carried out using username/password
"""

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
