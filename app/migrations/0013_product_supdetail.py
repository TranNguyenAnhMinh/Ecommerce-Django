# Generated by Django 4.2.4 on 2023-08-27 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_remove_product_supdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='supdetail',
            field=models.TextField(blank=True, null=True),
        ),
    ]
