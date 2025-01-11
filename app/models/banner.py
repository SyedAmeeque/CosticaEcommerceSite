from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Banner(models.Model):
    image =  models.ImageField(upload_to='media', blank=True, null=True)
    title=models.CharField(max_length=200)
    subtitle=models.CharField(max_length=300)
    deccription = models.CharField(max_length=500)
    video_link = models.CharField(max_length=1000, blank=True, null=True)