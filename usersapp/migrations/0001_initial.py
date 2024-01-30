# Generated by Django 4.2.9 on 2024-01-21 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sellerapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=100)),
                ('create_date', models.DateField(auto_now=True)),
                ('status', models.CharField(default='Active', max_length=100)),
            ],
            options={
                'db_table': 'user_table',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='sellerapp.product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usersapp.user')),
            ],
            options={
                'db_table': 'cart_table',
            },
        ),
    ]
