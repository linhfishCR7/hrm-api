# Generated by Django 3.2.6 on 2022-03-13 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffs', '0003_staffs_elect_decision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffs',
            name='staff',
            field=models.SlugField(default=None, max_length=255, unique=True),
        ),
    ]
