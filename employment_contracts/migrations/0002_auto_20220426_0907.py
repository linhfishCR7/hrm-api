# Generated by Django 3.2.6 on 2022-04-26 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employment_contracts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employmentcontract',
            name='bonus',
            field=models.CharField(blank=True, default='Theo qui định của công ty', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='employmentcontract',
            name='insurance',
            field=models.CharField(blank=True, default='Theo qui định của công ty', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='employmentcontract',
            name='number_employee',
            field=models.CharField(blank=True, default='N/A', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='employmentcontract',
            name='place_working',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='employmentcontract',
            name='resort_mode',
            field=models.CharField(blank=True, default='Theo qui định của công ty', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='employmentcontract',
            name='time_working',
            field=models.CharField(blank=True, default='Theo nội qui của công ty', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='employmentcontract',
            name='training',
            field=models.CharField(blank=True, default='Theo qui định của công ty', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='employmentcontract',
            name='transfer',
            field=models.CharField(blank=True, default='Chuyển khoản ngân hàng', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='employmentcontract',
            name='uniform',
            field=models.CharField(blank=True, default='Theo nội qui của công ty', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='employmentcontract',
            name='up_salary',
            field=models.CharField(blank=True, default='Theo qui định của công ty', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='employmentcontract',
            name='vehicles',
            field=models.CharField(blank=True, default='Tự túc', max_length=255, null=True),
        ),
    ]
