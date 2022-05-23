from base.serializers import ApplicationMethodFieldSerializer
from branchs.models import Branchs
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from departments.models import Departments

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branchs
        fields = [
            'id',
            'company',
            'name',
        ]


class DepartmentsSerializer(serializers.ModelSerializer):
    department = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(
            queryset=Departments.objects.filter(
                is_deleted=False,
                deleted_at=None
            )
        )]
    )

    class Meta:
        model = Departments
        fields = [
            'id',
            'department',
            'name',
            'branch'
        ]
             

class RetrieveAndListDepartmentsSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)

    class Meta:
        model = Departments
        fields = [
            'id',
            'department',
            'name',
            'branch'
        ]
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['data'] = f"{instance.branch.company.name} - {instance.branch.name} - {instance.name}"
        
        return response