from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    user_image = models.ImageField(upload_to='users/photos/', blank=True, null=True)
    bio = models.CharField(max_length=355, blank=True, null=True)