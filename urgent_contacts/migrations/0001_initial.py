# Generated by Django 3.2.6 on 2022-03-16 07:42

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staffs', '0006_rename_address_staffs_addresses'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrgentContacts',
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
                ('full_name', models.CharField(default=None, max_length=255)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('mobile_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('address', models.CharField(default=None, max_length=255)),
                ('type', models.CharField(default='Vợ', max_length=255)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urgent_contact_staff', to='staffs.staffs')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]