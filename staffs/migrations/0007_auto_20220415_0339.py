# Generated by Django 3.2.6 on 2022-04-15 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ethnicities', '0001_initial'),
        ('religions', '0001_initial'),
        ('nationalities', '0001_initial'),
        ('addresses', '0006_auto_20220312_2319'),
        ('staffs', '0006_rename_address_staffs_addresses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffs',
            name='addresses',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='staff_addresses', to='addresses.Address'),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='ethnicity',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff_ethnicities', to='ethnicities.ethnicities'),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='nationality',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff_nationalities', to='nationalities.nationalities'),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='religion',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff_religions', to='religions.religions'),
        ),
    ]
