# Generated by Django 5.1.3 on 2024-12-02 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_product_brand_alter_product_product_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wish_item',
            name='total_price',
        ),
        migrations.AlterField(
            model_name='product_image',
            name='alternate_text',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
