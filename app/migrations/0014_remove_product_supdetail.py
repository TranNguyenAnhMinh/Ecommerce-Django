# Generated by Django 4.2.4 on 2023-08-27 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_product_supdetail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='supdetail',
        ),
    ]
