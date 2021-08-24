from django.db import models
from django.contrib.auth.models import AbstractUser


# Custom User Model
class CustomUser(AbstractUser):
   # user = models.ForeignKey(AbstractUser, on_delete=models.CASCADE, null=True, blank=True)
    bio = models.TextField()
    location = models.CharField(max_length=200)