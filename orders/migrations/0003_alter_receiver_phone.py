# Generated by Django 3.2.10 on 2021-12-14 14:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20211204_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receiver',
            name='phone',
            field=models.CharField(max_length=20, unique=True, validators=[django.core.validators.RegexValidator(regex='^((\\+7|7|8)+([0-9]){10})$')]),
        ),
    ]
