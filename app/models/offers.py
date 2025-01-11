from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Offers(models.Model):
  offer_text = models.CharField(max_length=200)
  offer_discount = models.PositiveIntegerField(blank=True, null=True)
   