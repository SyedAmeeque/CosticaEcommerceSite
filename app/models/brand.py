from django.db import models

# Create your models here.

class Brand(models.Model):
    brand = models.CharField(max_length=50) 

    def __str__(self):
        return self.brand
    