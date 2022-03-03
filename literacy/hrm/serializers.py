from literacy.models import Literacy
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class LiteracySerializer(serializers.ModelSerializer):
    literacy = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(
            queryset=Literacy.objects.filter(
                is_deleted=False,
                deleted_at=None
            )
        )]
    )
    class Meta:
        model = Literacy
        fields = [
            'id',
            'literacy',
            'name'
        ]