import uuid
from random import random, randint

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
    statistics = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.statistics = [randint(200, 700) for _ in range(7)]
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

class Order(models.Model):
    class OrderTypes(models.TextChoices):
        TODO = 'to do', 'To Do'
        DOING = 'doing', 'Doing'
        DONE = 'done', 'Done'

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    status = models.CharField(max_length=10, choices=OrderTypes.choices, default=OrderTypes.TODO)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(blank=True)
    customer_id = models.CharField(unique=True, blank=True, max_length=15)

    def save(self, *args, **kwargs):
        price = self.product.price
        self.price = price * self.amount
        if not self.customer_id:
            self.customer_id = str(uuid.uuid4())[:15]
        # super().save(*args, **kwargs)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name}: {self.user}'