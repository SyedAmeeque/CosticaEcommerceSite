from django.db import models
from .category import Category
from .brand import Brand
from .tags import Tag
from .type import Type
from .sale import Sale
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=100) 
    excerpt = models.CharField(max_length=500)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    compared_price = models.DecimalField(decimal_places=2,max_digits=5)
    sale_price = models.DecimalField(decimal_places=2,max_digits=5)
    category = models.ManyToManyField('Category')
    tag = models.ManyToManyField('Tag', null=True, blank=True)
    brand = models.ForeignKey('brand',null=True, blank=True, on_delete=models.CASCADE)
    sku = models.CharField(max_length=20, null=True, blank=True)
    product_type = models.ForeignKey('Type', null=True, blank=True, on_delete=models.CASCADE)
    product_reviews = models.FloatField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    sold = models.PositiveIntegerField()
    slug= models.SlugField(unique=True, blank=True, max_length=300)
    date = models.DateField(auto_now_add=True)
    link = models.CharField(max_length=255, blank=True)
    sale = models.ForeignKey(Sale, null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it doesn't exist
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while Product.objects.filter(slug=unique_slug).exists():  # Ensure uniqueness
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        self.link = f'http://127.0.0.1:8000/product/{self.slug}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product_Image(models.Model):
    image = models.ImageField(upload_to='media', null=True, blank=True)
    alternate_text = models.CharField(max_length=500, blank=True)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)