from ethnicities.models import Ethnicities
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class EthnicitiesSerializer(serializers.ModelSerializer):
    ethnicity = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(
            queryset=Ethnicities.objects.filter(
                is_deleted=False,
                deleted_at=None
            )
        )]
    )
    class Meta:
        model = Ethnicities
        fields = [
            'id',
            'ethnicity',
            'name'
        ]