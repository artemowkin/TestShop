# Generated by Django 3.2.10 on 2021-12-14 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20211024_1409'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('price', '-pub_datetime', 'title'), 'verbose_name': 'product', 'verbose_name_plural': 'products'},
        ),
    ]
