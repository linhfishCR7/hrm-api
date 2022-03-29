# Generated by Django 3.2.6 on 2022-03-29 13:20

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employment_contract_types', '0002_employmentcontracttypes_name'),
        ('staffs', '0006_rename_address_staffs_addresses'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmploymentContract',
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
                ('number_contract', models.CharField(default='MTC-HDLD-0000', max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('place_working', models.CharField(default=None, max_length=255)),
                ('number_employee', models.CharField(default='N/A', max_length=255)),
                ('content', models.TextField(blank=True, default='Theo sự phân công của giám đốc', null=True)),
                ('time_working', models.CharField(default='Theo nội qui của công ty', max_length=255)),
                ('uniform', models.CharField(default='Theo nội qui của công ty', max_length=255)),
                ('vehicles', models.CharField(default='Tự túc', max_length=255)),
                ('basic_salary', models.IntegerField(blank=True, null=True)),
                ('extra', models.IntegerField(blank=True, null=True)),
                ('other_support', models.IntegerField(blank=True, null=True)),
                ('transfer', models.CharField(default='Chuyển khoản ngân hàng', max_length=255)),
                ('up_salary', models.CharField(default='Theo qui định của công ty', max_length=255)),
                ('bonus', models.CharField(default='Theo qui định của công ty', max_length=255)),
                ('training', models.CharField(default='Theo qui định của công ty', max_length=255)),
                ('resort_mode', models.CharField(default='Theo qui định của công ty', max_length=255)),
                ('insurance', models.CharField(default='Theo qui định của công ty', max_length=255)),
                ('sign_day', models.DateField()),
                ('status', models.BooleanField(default=False)),
                ('employer', models.CharField(default='Huỳnh Tuấn Hoàng', max_length=255)),
                ('position', models.CharField(default='Giám đốc', max_length=255)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employment_contract_staff', to='staffs.staffs')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employment_contract_employment_contract_types', to='employment_contract_types.employmentcontracttypes')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
