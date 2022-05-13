# Generated by Django 3.2.6 on 2022-05-12 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employment_contracts', '0002_auto_20220426_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='employmentcontract',
            name='is_print',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='employmentcontract',
            name='link_contract',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]