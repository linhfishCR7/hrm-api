# Generated by Django 3.2.6 on 2022-02-12 17:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmploymentContractTypes',
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
                ('employment_contract_types', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
