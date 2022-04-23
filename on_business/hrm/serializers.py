from base.serializers import ApplicationMethodFieldSerializer
from on_business.models import OnBusiness
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


class OnBusinessSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OnBusiness
        fields = [
            'id',
            'date',
            'company',
            'position',
            'content',
            'start_date',
            'staff',
        ]
        
    
class RetrieveAndListOnBusinessSerializer(serializers.ModelSerializer):
    staff = StaffsSerializer()

    class Meta:
        model = OnBusiness
        fields = [
            'id',
            'date',
            'company',
            'position',
            'content',
            'start_date',
            'staff',
        ]
    
    def to_representation(self, instance):
        """
        To show the data response to users
        """
        response = super().to_representation(instance)
        response['date_data'] = f"{instance.start_date} - {instance.date}"
        
        return response