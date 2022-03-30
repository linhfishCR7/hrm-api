# Generated by Django 3.2.6 on 2022-03-25 01:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('certificate_types', '0002_certificatetypes_name'),
        ('staffs', '0006_rename_address_staffs_addresses'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.UUIDField(null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('modified_by', models.UUIDField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('deleted_by', models.UUIDField(null=True)),
                ('number', models.CharField(default=None, max_length=255)),
                ('name', models.CharField(default=None, max_length=255)),
                ('level', models.CharField(default=None, max_length=255)),
                ('date', models.DateField()),
                ('expire', models.DateField()),
                ('place', models.CharField(default=None, max_length=255)),
                ('note', models.TextField(default=None, max_length=255)),
                ('attach', models.CharField(default=None, max_length=255)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificate_staff', to='staffs.staffs')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificate_certificate_type', to='certificate_types.certificatetypes')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]