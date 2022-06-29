from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.utils import CustomUserManager

class User(AbstractUser):
    
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)

    username = None

    REQUIRED_FIELDS = ["first_name", "last_name"]
    USERNAME_FIELD = "email"
    objects = CustomUserManager()