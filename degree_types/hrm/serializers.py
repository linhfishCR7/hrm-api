from degree_types.models import DegreeTypes
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class DegreeTypesSerializer(serializers.ModelSerializer):
    degree_types = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(
            queryset=DegreeTypes.objects.filter(
                is_deleted=False,
                deleted_at=None
            )
        )]
    )
    class Meta:
        model = DegreeTypes
        fields = [
            'id',
            'degree_types',
            'name'
        ]