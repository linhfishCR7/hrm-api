# Generated by Django 3.2.6 on 2022-03-13 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffs', '0002_staffs_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffs',
            name='elect_decision',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
