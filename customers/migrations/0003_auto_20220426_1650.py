# Generated by Django 3.2.6 on 2022-04-26 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_alter_customers_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='company',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customers',
            name='file',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customers',
            name='website',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
