# Generated by Django 4.2.9 on 2024-02-10 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersapp', '0011_alter_order_offer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ordered_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
