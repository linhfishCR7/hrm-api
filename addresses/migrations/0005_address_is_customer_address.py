# Generated by Django 3.2.6 on 2022-03-03 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0004_address_province'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='is_customer_address',
            field=models.BooleanField(default=False),
        ),
    ]
