from django.db import models
from django.utils.text import slugify


# Create your models here.

class Category(models.Model):
    cat_image = models.ImageField(upload_to='media',null=True,blank=True)
    name = models.CharField(max_length=50) 
  
    def __str__(self):
        return self.name
    

