from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Wishlist(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)