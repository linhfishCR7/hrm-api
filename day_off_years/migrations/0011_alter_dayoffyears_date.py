# Generated by Django 3.2.6 on 2022-03-27 01:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('day_off_years', '0010_alter_dayoffyears_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayoffyears',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 3, 27, 1, 49, 39, 108556, tzinfo=utc)),
        ),
    ]
