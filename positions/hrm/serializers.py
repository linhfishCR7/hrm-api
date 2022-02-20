from positions.models import Positions
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class PositionsSerializer(serializers.ModelSerializer):
    position = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(
            queryset=Positions.objects.filter(
                is_deleted=False,
                deleted_at=None
            )
        )]
    )
    class Meta:
        model = Positions
        fields = [
            'id',
            'position',
            'name'
        ]