from base.serializers import ApplicationMethodFieldSerializer
from branchs.models import Branchs
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from certificate.models import Certificate
from certificate_types.models import CertificateTypes
from staffs.models import Staffs
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'image',
        ]
        read_only_fields = ['id']

    def to_representation(self, instance):
        """
        To show the data response to users
        """
        response = super().to_representation(instance)
        if instance.image:
            response['image'] = ApplicationMethodFieldSerializer.get_list_image(instance.image)
        
        return response


class StaffsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Staffs
        fields = [
            'id',
            'staff',
            'user'
        ]
        read_only_fields = ['id']


class CertificateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateTypes
        fields = [
            'id',
            'certificate_types',
            'name'
        ]
        read_only_fields = ['id']


class CertificateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Certificate
        fields = [
            "id",
            "number",
            "name",
            "level",
            "date",
            "expire",
            "place",
            "note",
            "attach",
            "type",
            "staff",
        ]
        

class RetrieveAndListCertificateSerializer(serializers.ModelSerializer):
    type = CertificateTypeSerializer(read_only=True)
    staff = StaffsSerializer(read_only=True)

    class Meta:
        model = Certificate
        fields = [
            "id",
            "number",
            "name",
            "level",
            "date",
            "expire",
            "place",
            "note",
            "attach",
            "type",
            "staff",
        ]