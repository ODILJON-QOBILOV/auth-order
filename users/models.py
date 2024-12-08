from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    class UserTypes(models.TextChoices):
        User = 'user', 'User'
        Manager = 'manager', 'Manager'
    user_image = models.ImageField(upload_to='users/photos/', blank=True, null=True)
    bio = models.CharField(max_length=355, blank=True, null=True)
    role = models.CharField(max_length=25, choices=UserTypes.choices, default=UserTypes.User)

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

