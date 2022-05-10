from base.serializers import ApplicationMethodFieldSerializer
from branchs.models import Branchs
from companies.models import Companies
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = [
            'id',
            'company',
            'name',
        ]


class BranchsSerializer(serializers.ModelSerializer):
    branch = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(
            queryset=Branchs.objects.filter(
                is_deleted=False,
                deleted_at=None
            )
        )]
    )

    class Meta:
        model = Branchs
        fields = [
            'id',
            'branch',
            'name',
            'company'
        ]
        

class RetrieveAndListBranchsSerializer(serializers.ModelSerializer):
    company = CompaniesSerializer(read_only=True)

    class Meta:
        model = Branchs
        fields = [
            'id',
            'branch',
            'name',
            'company'
        ]
    
    def to_representation(self, instance):
        """
        To show the data response to users
        """
        response = super().to_representation(instance)
        response['company_data'] = instance.company.name

        return response