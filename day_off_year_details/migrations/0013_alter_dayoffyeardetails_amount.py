# Generated by Django 3.2.6 on 2022-03-27 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('day_off_year_details', '0012_auto_20220327_0248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayoffyeardetails',
            name='amount',
            field=models.IntegerField(default=1),
        ),
    ]
