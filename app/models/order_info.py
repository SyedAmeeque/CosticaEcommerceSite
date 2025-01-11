from django.db import models
from django.contrib.auth.models import User
from .product import Product

# Create your models here.

class Order_info(models.Model):
    order_id = models.CharField(max_length=200, unique=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    shipping_address = models.CharField(max_length=500)
    delivery_charges = models.DecimalField(null=True, blank=True, decimal_places=2,max_digits=5)
    shipping_charges = models.DecimalField(null=True, blank=True,decimal_places=2,max_digits=5)
    total_order_amount = models.DecimalField(null=True, blank=True,decimal_places=2,max_digits=5)
    date = models.DateField(auto_now_add=True)
    order_status = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if not self.pk:  # This means the object is being created, not updated
            if not self.order_id:  # Generate order_id only if it doesn't exist
                base_id = 3000
                unique_id = f'ord-{base_id}'
                while Order_info.objects.filter(order_id=unique_id).exists():
                    base_id += 1
                    unique_id = f'ord-{base_id}'
                self.order_id = unique_id
        super().save(*args, **kwargs)