# Generated by Django 3.2.6 on 2022-03-16 14:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('day_off_years', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayoffyears',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 3, 16, 14, 31, 0, 785112, tzinfo=utc)),
        ),
    ]
