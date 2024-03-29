# Generated by Django 4.2.9 on 2024-01-21 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainCategory',
            fields=[
                ('maincategory_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('maincategory_name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'maincategory_table',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('subcategory_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('subcategory_name', models.CharField(max_length=100)),
                ('maincategory_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminsapp.maincategory')),
            ],
            options={
                'db_table': 'subcategory_table',
            },
        ),
    ]
