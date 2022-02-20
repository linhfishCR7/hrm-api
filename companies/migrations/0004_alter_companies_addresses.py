# Generated by Django 3.2.6 on 2022-02-19 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0004_address_province'),
        ('companies', '0003_auto_20220219_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companies',
            name='addresses',
            field=models.ManyToManyField(default=None, null=True, related_name='company_addresses', to='addresses.Address'),
        ),
    ]
