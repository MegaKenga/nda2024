# Generated by Django 4.2.7 on 2023-12-07 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_product_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='ref',
        ),
    ]
