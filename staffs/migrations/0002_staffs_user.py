# Generated by Django 3.2.6 on 2022-03-13 04:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('staffs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffs',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='staff_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
