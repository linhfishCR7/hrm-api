from day_off_types.models import DayOffTypes
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class DayOffTypesSerializer(serializers.ModelSerializer):
    day_off_types = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(
            queryset=DayOffTypes.objects.filter(
                is_deleted=False,
                deleted_at=None
            )
        )]
    )
    class Meta:
        model = DayOffTypes
        fields = [
            'id',
            'day_off_types',
            'name'
        ]