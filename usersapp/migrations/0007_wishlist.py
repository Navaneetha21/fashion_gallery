# Generated by Django 4.2.9 on 2024-02-02 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0003_remove_boysdrs_description_remove_jeans_description_and_more'),
        ('usersapp', '0006_alter_review_product_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('wishlist_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to='sellerapp.product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usersapp.user')),
            ],
            options={
                'db_table': 'wishlist_table',
            },
        ),
    ]