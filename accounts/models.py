from django.db import models
from django.contrib.auth.models import AbstractUser


# Custom User Model
class CustomUser(AbstractUser):
    bio = models.TextField()
    location = models.CharField(max_length=200)
