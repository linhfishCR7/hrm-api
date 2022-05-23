from base.serializers import ApplicationMethodFieldSerializer
from branchs.models import Branchs
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from staff_project.models import StaffProject
from timekeeping.models import Timekeeping
from base.constants.common import TypeTimeKeeping
from staffs.models import Staffs
from users.models import User
from kinds_of_work.models import KindsOfWork
from projects.models import Projects
from datetime import datetime
from base.templates.error_templates import ErrorTemplate
from rest_framework.exceptions import ValidationError

from base.utils import print_value

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


class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Projects
        fields = [
            "id",
            "project",
            "name",
            "status"
        ]


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
    staff = StaffsSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    class Meta:
        model = StaffProject
        fields = [
            'id',
            'staff',
            'project'
        ]
        read_only_fields = ['id']


class KindsOfWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = KindsOfWork
        fields = [
            'id',
            'work',
            'name'
        ]
        read_only_fields = ['id']


class TimekeepingSerializer(serializers.ModelSerializer):
    amount_in_project = serializers.FloatField(required=False)
    amount_time = serializers.FloatField(required=False)
    class Meta:
        model = Timekeeping
        fields = [
            "id",
            "date",
            "amount_in_project",
            "amount_time",
            "note",
            "type",
            "type_work",
            "staff_project",
        ]
        
    # def create(self, validated_data):
    #     staff_project = StaffProject.objects.filter(
    #         project__status=2,
    #         is_deleted=False
    #     ).values_list('id', flat=True)
    #     print_value(staff_project)
        
    #     for item in staff_project:
    #         data = Timekeeping.objects.filter(
    #             date=datetime.today().strftime('%Y-%m-%d'),
    #             staff_project__in=staff_project
    #         )

    #         if data:
    #             raise ValidationError(ErrorTemplate.TimeKeepingError.TIME_KEEPING_ALREADY_CREATED)
        
    #     return super().create(validated_data)

            
class RetrieveAndListTimekeepingSerializer(serializers.ModelSerializer):
    type_work = KindsOfWorkSerializer(read_only=True)
    staff_project = StaffProjectSerializer(read_only=True)
    class Meta:
        model = Timekeeping
        fields = [
            "id",
            "date",
            "amount_in_project",
            "amount_time",
            "note",
            "type",
            "type_work",
            "staff_project",
        ]
    
    def to_representation(self, instance):
        """
        To show the data response to users
        """
        response = super().to_representation(instance)
        if instance.type_work:
            response['type_work_name'] = instance.type_work.name
            response['type_work_id'] = instance.type_work.id
            
        if instance.staff_project.project.name:
            response['project_name'] = instance.staff_project.project.name
        if instance.staff_project:
            response['project_id'] = instance.staff_project.id
        
        if instance.staff_project.staff.user:
            response['staff_name'] = instance.staff_project.staff.user.last_name + ' ' + instance.staff_project.staff.user.first_name
            response['staff_staff'] = instance.staff_project.staff.staff
            
        if instance.type == 1:
            response['type_time'] = "Giờ Hành Chính"
        elif instance.type == 1.5:
            response['type_time'] = "Làm Thêm Ngày Thường"
        elif instance.type == 2.0:
            response['type_time'] = "Làm Thêm Ngày Cuối Tuần"
        else:
            response['type_time'] = "Làm Thêm Ngày Lễ Tết"
        response['month'] = f"{instance.date:%m}"
        response['year'] = f"{instance.date:%Y}"
        return response