from django.db import models
from django.contrib.auth.models import User
from .cart import Cart
from .product import Product

# Create your models here.

class Cart_item(models.Model):
    cart =  models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(decimal_places=2,max_digits=5)