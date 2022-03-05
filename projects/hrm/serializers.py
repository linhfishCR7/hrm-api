from base.serializers import ApplicationMethodFieldSerializer
from projects.models import Projects
from customers.models import Customers
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from base.constants.common import ProjectStatus

class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customers
        fields = [
            'id',
            'name'
        ]
        read_only_fields = ['id']
    


class ProjectsSerializer(serializers.ModelSerializer):
    project = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(
            queryset=Projects.objects.filter(
                is_deleted=False,
                deleted_at=None
            )
        )]
    )
    project = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    status = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    size = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    note = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    file = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = Projects
        fields = [
            'id',
            'project',
            'name',
            'location',
            'service',
            'contract_number',
            'signing_date',
            'start_date',
            'finish_date',
            'status',
            'size',
            'image',
            'note',
            'file',
            'customer',
            
        ]
        
    def create(self, validated_data):
        
        project = Projects.objects.create(
            **validated_data,
            project=f"{validated_data['name']}-{validated_data['signing_date']}",
            status=ProjectStatus.PENDING_PROJECT
        )
        
        return project
        

class RetrieveAndListProjectsSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = Projects
        fields = [
            'id',
            'project',
            'name',
            'location',
            'service',
            'contract_number',
            'signing_date',
            'start_date',
            'finish_date',
            'status',
            'size',
            'image',
            'note',
            'file',
            'customer',
            
        ]

    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        if instance.image:
            response['image'] = ApplicationMethodFieldSerializer.get_list_image(instance.image)
        
        return response