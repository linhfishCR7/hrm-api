# Generated by Django 3.2.6 on 2022-04-15 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffs', '0007_auto_20220415_0339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffs',
            name='identity_card',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
