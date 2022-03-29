from base.serializers import ApplicationMethodFieldSerializer
from base.utils import generate_number_contract
from rest_framework import serializers
from employment_contracts.models import EmploymentContract
from employment_contract_types.models import EmploymentContractTypes
from staffs.models import Staffs
from users.models import User

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
        number_contract = generate_number_contract()
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