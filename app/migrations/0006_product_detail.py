# Generated by Django 4.2.4 on 2023-08-16 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='detail',
            field=models.TextField(max_length=200, null=True),
        ),
    ]
