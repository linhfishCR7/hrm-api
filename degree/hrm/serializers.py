from base.serializers import ApplicationMethodFieldSerializer
from rest_framework import serializers
from degree.models import Degree
from degree_types.models import DegreeTypes
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


class DegreeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DegreeTypes
        fields = [
            'id',
            'degree_types',
            'name'
        ]
        read_only_fields = ['id']


class DegreeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Degree
        fields = [
            "id",
            "number",
            "name",
            "date",
            "place",
            "attach",
            "type",
            "staff",
        ]
        

class RetrieveAndListDegreeSerializer(serializers.ModelSerializer):
    type = DegreeTypeSerializer(read_only=True)
    staff = StaffsSerializer(read_only=True)

    class Meta:
        model = Degree
        fields = [
            "id",
            "number",
            "name",
            "date",
            "place",
            "attach",
            "type",
            "staff",
        ]