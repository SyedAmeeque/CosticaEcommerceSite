from django.db import models
from django.contrib.auth.models import User
from .product import Product
from django.core.validators import MaxValueValidator, MinValueValidator


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.FloatField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    date = models.DateField(auto_now=True)
