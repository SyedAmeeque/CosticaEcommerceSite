from django.db import models
from django.contrib.auth.models import AbstractUser, User
# Create your models here.

class customer_details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)

    