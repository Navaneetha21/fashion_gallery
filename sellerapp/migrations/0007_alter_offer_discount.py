# Generated by Django 4.2.9 on 2024-02-09 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0006_product_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='discount',
            field=models.IntegerField(),
        ),
    ]
