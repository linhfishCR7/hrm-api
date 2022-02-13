from certificate_types.models import CertificateTypes
from rest_framework import serializers


class CertificateTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateTypes
        fields = [
            'id',
            'certificate_types',
            'name'
        ]