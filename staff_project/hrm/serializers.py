from base.serializers import ApplicationMethodFieldSerializer
from projects.models import Projects
from rest_framework import serializers
from staff_project.models import StaffProject
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


class StaffProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProject
        fields = [
            'id',
            'StaffProject_types',
            'name'
        ]
        read_only_fields = ['id']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = [
            'id',
            'project',
            'name'
        ]
        read_only_fields = ['id']


class StaffProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StaffProject
        fields = [
            "id",
            "project",
            "staff",
        ]
        

class RetrieveAndListStaffProjectSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    staff = StaffsSerializer(read_only=True)

    class Meta:
        model = StaffProject
        fields = [
            "id",
            "project",
            "staff",
        ]