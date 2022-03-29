from base.serializers import ApplicationMethodFieldSerializer
from up_salaries.models import UpSalary

from staffs.models import Staffs
from users.models import User
from rest_framework import serializers


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


class UpSalarySerializer(serializers.ModelSerializer):
    old_coefficient = serializers.FloatField(required=False)
    class Meta:
        model = UpSalary
        fields = [
            'id',
            'date',
            'old_coefficient',
            'coefficient',
            'staff',
        ]
        
    
class RetrieveAndListUpSalarySerializer(serializers.ModelSerializer):
    staff = StaffsSerializer()
    old_coefficient = serializers.FloatField(required=False)

    class Meta:
        model = UpSalary
        fields = [
            'id',
            'date',
            'old_coefficient',
            'coefficient',
            'staff'
        ]