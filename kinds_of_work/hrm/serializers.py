from kinds_of_work.models import KindsOfWork
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class KindsOfWorkSerializer(serializers.ModelSerializer):
    work = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(
            queryset=KindsOfWork.objects.filter(
                is_deleted=False,
                deleted_at=None
            )
        )]
    )
    class Meta:
        model = KindsOfWork
        fields = [
            'id',
            'work',
            'name'
        ]