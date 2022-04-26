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
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'image',
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


class StaffsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Staffs
        fields = [
            'id',
            'staff',
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