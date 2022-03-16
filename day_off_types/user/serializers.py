from day_off_types.models import DayOffTypes
from rest_framework import serializers

class DayOffTypesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DayOffTypes
        fields = [
            'id',
            'day_off_types',
            'name'
        ]