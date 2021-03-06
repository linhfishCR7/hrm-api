# Generated by Django 3.2.6 on 2022-04-25 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='attach',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='expire',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='level',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='name',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='note',
            field=models.TextField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='number',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='place',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
