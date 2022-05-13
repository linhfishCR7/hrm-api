from base.serializers import ApplicationMethodFieldSerializer
from base.utils import generate_number_contract
from rest_framework import serializers
from employment_contracts.models import EmploymentContract
from employment_contract_types.models import EmploymentContractTypes
from staffs.models import Staffs
from users.models import User
from departments.models import Departments
from branchs.models import Branchs
from companies.models import Companies
from addresses.models import Address
from literacy.models import Literacy
from positions.models import Positions


from pathlib import Path
from django.template.loader import get_template
from base.services.s3_services import MediaUpLoad
import os
from django.conf import settings
from weasyprint import HTML, default_url_fetcher
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'image',
            'date_of_birth'
        ]
        read_only_fields = ['id']

    def to_representation(self, instance):
        """
        To show the data response to users
        """
        response = super().to_representation(instance)
        if instance.image:
            response['image'] = ApplicationMethodFieldSerializer.get_list_image(instance.image)
        
        return response


class AddressesSerializer(serializers.ModelSerializer):
    address = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    city = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    province = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    district = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    commune = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    country = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    postcode = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    lat = serializers.FloatField(required=False)
    lng = serializers.FloatField(required=False)
    class Meta:
        model = Address
        fields = [
            'id',
            'address',
            'city',
            'province',
            'district',
            'commune',
            'country',
            'postcode',
            'lat',
            'lng',
            'type'
        ]
        
        read_only_fields = ['id']
    

class CompaniesSerializer(serializers.ModelSerializer):
    addresses = AddressesSerializer(many=True, allow_null=True, required=False)
    class Meta:
        model = Companies
        fields = [
            'id',
            'company',
            'name',
            'email',
            'phone',
            'fax',
            'addresses'
        ]


class BranchSerializer(serializers.ModelSerializer):
    company = CompaniesSerializer(read_only=True)
    class Meta:
        model = Branchs
        fields = [
            'id',
            'branch',
            'name',
            'company',
        ]
        read_only_fields = ['id']


class DepartmentSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    class Meta:
        model = Departments
        fields = [
            'id',
            'department',
            'name',
            'branch'
        ]
        read_only_fields = ['id']


class LiteracySerializer(serializers.ModelSerializer):

    class Meta:
        model = Literacy
        fields = [
            'id',
            'literacy',
            'name'
        ]


class PositionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Positions
        fields = [
            'id',
            'position',
            'name',
        ]


class StaffsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    addresses = AddressesSerializer(many=True, allow_null=True, required=False)
    # literacy = LiteracySerializer(read_only=True)
    # position = PositionsSerializer(read_only=True)
    class Meta:
        model = Staffs
        fields = [
            'id',
            'staff',
            'gender',
            'marital_status',
            'number_of_children',
            'identity_card',
            'issuance_date',
            'place_of_issuance',
            'start_work_date',
            'probationary_end_date',
            'labor_contract_signing_date',
            'personal_email',
            'social_insurance_number',
            'tax_code',
            'department',
            'literacy',
            'position',
            'addresses',
            'user'
        ]
        read_only_fields = ['id']


class EmploymentContractTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentContractTypes
        fields = [
            'id',
            'employment_contract_types',
            'name'
        ]
        read_only_fields = ['id']


class EmploymentContractSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EmploymentContract
        fields = [
            "id",
            "number_contract",
            "name",
            "from_date",
            "to_date",
            "place_working",
            "number_employee",
            "content",
            "time_working",
            "uniform",
            "vehicles",
            "basic_salary",
            "extra",
            "other_support",
            "transfer",
            "up_salary",
            "bonus",
            "training",
            "resort_mode",
            "insurance",
            "sign_day",
            "status",
            "employer",
            "position",
            "type",
            "staff",
        ]

    def create(self, validated_data):
        type_data = EmploymentContractTypes.objects.filter(
            id=validated_data['type'].id
        ).first()
        staff_data = Staffs.objects.filter(
            id=validated_data['staff'].id
        ).first()
        department_data = Departments.objects.filter(id=staff_data.department_id).first()

        number_contract = generate_number_contract(
            department=department_data.department,
            type=type_data.employment_contract_types,
            staff=staff_data.staff,
        )
        validated_data['number_contract'] = number_contract
        return super().create(validated_data)

class RetrieveAndListEmploymentContractSerializer(serializers.ModelSerializer):
    type = EmploymentContractTypeSerializer(read_only=True)
    staff = StaffsSerializer(read_only=True)

    class Meta:
        model = EmploymentContract
        fields = [
            "id",
            "number_contract",
            "name",
            "from_date",
            "to_date",
            "place_working",
            "number_employee",
            "content",
            "time_working",
            "uniform",
            "vehicles",
            "basic_salary",
            "extra",
            "other_support",
            "transfer",
            "up_salary",
            "bonus",
            "training",
            "resort_mode",
            "insurance",
            "sign_day",
            "status",
            "employer",
            "position",
            "type",
            "staff",
        ]

    def to_representation(self, instance):
        """
        To show the data response to users
        """
        response = super().to_representation(instance)
        response['type_name'] = instance.type.name
        response['type_data'] = instance.type.id
        response['total_salary'] = f"{instance.basic_salary+instance.extra+instance.other_support:,}"
        response['basic_salary_data'] = f"{instance.basic_salary:,}"
        response['extra_data'] = f"{instance.extra:,}"
        response['other_support_data'] = f"{instance.other_support:,}"

        if instance.status==False:
            response['status_data'] = "Hết Hiệu Lực"
        else:
            response['status_data'] = "Còn Hiệu Lực"
        
        return response
    

class RetrieveAndListEmploymentContractReportSerializer(serializers.ModelSerializer):
    type = EmploymentContractTypeSerializer(read_only=True)
    staff = StaffsSerializer(read_only=True)

    class Meta:
        model = EmploymentContract
        fields = [
            "id",
            "number_contract",
            "name",
            "from_date",
            "to_date",
            "place_working",
            "number_employee",
            "content",
            "time_working",
            "uniform",
            "vehicles",
            "basic_salary",
            "extra",
            "other_support",
            "transfer",
            "up_salary",
            "bonus",
            "training",
            "resort_mode",
            "insurance",
            "sign_day",
            "status",
            "employer",
            "position",
            "type",
            "staff",
        ]

    def to_representation(self, instance):
        """
        To show the data response to users
        """
        response = super().to_representation(instance)
        response['type_name'] = instance.type.name
        response['type_data'] = instance.type.id
        response['total_salary'] = f"{instance.basic_salary+instance.extra+instance.other_support:,}"
        response['basic_salary_data'] = f"{instance.basic_salary:,}"
        response['extra_data'] = f"{instance.extra:,}"
        response['other_support_data'] = f"{instance.other_support:,}"

        if instance.status==False:
            response['status_data'] = "Hết Hiệu Lực"
        else:
            response['status_data'] = "Còn Hiệu Lực"
        
        company_data = Companies.objects.filter(id=instance.staff.department.branch.company.id).prefetch_related('addresses').values('addresses__type', 'addresses__address')
        for item in company_data:
            if item['addresses__type']=='head_office_address':
                response['head_office_address'] = item['addresses__address']
            if item['addresses__type']=='working_office_address':
                response['working_office_address'] = item['addresses__address']
                
        staff_data = Staffs.objects.filter(id=instance.staff.id).prefetch_related('addresses').values('addresses__type', 'addresses__address')
        for item in staff_data:
            if item['addresses__type']=='permanent_address':
                response['permanent_address'] = item['addresses__address']
            
        if instance.is_print==True:
            data = {
                "company": instance.staff.department.branch.company.name,
                "full_name": f"{instance.staff.user.last_name} {instance.staff.user.first_name}",
                "department": instance.staff.department.name,
                "birthday": instance.staff.user.date_of_birth,
                "position": instance.staff.position.name if instance.staff.position else '',
                "leracy": instance.staff.literacy.name if instance.staff.literacy else '',
                "card": instance.staff.identity_card,
                "date_card": instance.staff.issuance_date,
                "place_card": instance.staff.place_of_issuance,
                "mobile_phone": instance.staff.mobile_phone,
                "address_company": response['head_office_address'],
                "address_staff": response['permanent_address'],
                "phone": instance.staff.department.branch.company.phone,
                "fax": instance.staff.department.branch.company.fax,
                "number_contract": instance.number_contract,
                "name": instance.name,
                "from_date": instance.from_date,
                "to_date": instance.to_date,
                "place_working": instance.place_working,
                "number_employee": instance.number_employee,
                "content": instance.content,
                "time_working": instance.time_working,
                "uniform": instance.uniform,
                "vehicles": instance.vehicles,
                "basic_salary": instance.basic_salary,
                "extra": instance.extra,
                "other_support": instance.other_support,
                "transfer": instance.transfer,
                "up_salary": instance.up_salary,
                "bonus": instance.bonus,
                "training": instance.training,
                "resort_mode": instance.resort_mode,
                "insurance": instance.insurance,
                "sign_day": instance.sign_day,
                "employer": instance.employer,
                "position_employer": instance.position,
                "total_salary": f"{instance.basic_salary+instance.extra+instance.other_support:,}",
                "basic_salary_data": f"{instance.basic_salary:,}",
                "extra_data": f"{instance.extra:,}",
                "other_support_data": f"{instance.other_support:,}"
            }
            template = get_template('contract_report_template.html')
            context = template.render(data).encode("UTF-8")
            filename = '{}_{}_contract_report.pdf'.format(f"{instance.staff.staff}", instance.staff.department.department)
            f = open(filename, "w+b")
            HTML(string=context).write_pdf(f)
            f.close()
            key = MediaUpLoad().upload_pdf_to_s3(os.path.join(settings.BASE_DIR, filename), filename)
            if os.path.exists(filename):
                os.remove(filename)
            response['key'] = MediaUpLoad().get_file_url(key)
            EmploymentContract.objects.filter(id=instance.id).update(
                link_contract=response['key'],
                is_print=True
            )
        else:
            response['key'] = instance.link_contract
        
        return response