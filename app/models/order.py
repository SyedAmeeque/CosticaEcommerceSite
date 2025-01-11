from django.db import models
from django.contrib.auth.models import User
from .order_info import Order_info
from .product import Product
# Create your models here.

class Order(models.Model):
    order_details = models.ForeignKey(Order_info, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(decimal_places=2,max_digits=5)

    
