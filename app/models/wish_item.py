from django.db import models
from django.contrib.auth.models import User
from .wishlist import Wishlist
from .product import Product
# Create your models here.

class Wish_item(models.Model):
    wish =  models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
 