from employment_contract_types.models import EmploymentContractTypes
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class EmploymentContractTypesSerializer(serializers.ModelSerializer):
    employment_contract_types = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(
            queryset=EmploymentContractTypes.objects.filter(
                is_deleted=False,
                deleted_at=None
            )
        )]
    )
    class Meta:
        model = EmploymentContractTypes
        fields = [
            'id',
            'employment_contract_types',
            'name'
        ]