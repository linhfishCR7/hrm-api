from certificate_types.models import CertificateTypes
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class CertificateTypesSerializer(serializers.ModelSerializer):
    certificate_types = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(
            queryset=CertificateTypes.objects.filter(
                is_deleted=False,
                deleted_at=None
            )
        )]
    )
    class Meta:
        model = CertificateTypes
        fields = [
            'id',
            'certificate_types',
            'name'
        ]