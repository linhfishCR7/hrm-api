# Generated by Django 3.2.6 on 2022-03-25 04:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('day_off_years', '0008_alter_dayoffyears_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayoffyears',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 3, 25, 4, 19, 29, 163859, tzinfo=utc)),
        ),
    ]
