from religions.models import Religions
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class ReligionsSerializer(serializers.ModelSerializer):
    religion = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(
            queryset=Religions.objects.filter(
                is_deleted=False,
                deleted_at=None
            ),
        )]
    )
    class Meta:
        model = Religions
        fields = [
            'id',
            'religion',
            'name'
        ]