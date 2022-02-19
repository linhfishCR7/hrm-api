from nationalities.models import Nationalities
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class NationalitiesSerializer(serializers.ModelSerializer):
    nationality = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(
            queryset=Nationalities.objects.filter(
                is_deleted=False,
                deleted_at=None
            )
        )]
    )
    class Meta:
        model = Nationalities
        fields = [
            'id',
            'nationality',
            'name'
        ]