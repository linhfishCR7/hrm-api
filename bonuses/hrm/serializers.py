from base.serializers import ApplicationMethodFieldSerializer
from bonuses.models import Bonuses
from staffs.models import Staffs
from users.models import User
from rest_framework import serializers


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


class BonusesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bonuses
        fields = [
            'id',
            'date',
            'amount',
            'reason',
            'note',
            'staff',
        ]
        
    
class RetrieveAndListBonusesSerializer(serializers.ModelSerializer):
    staff = StaffsSerializer()

    class Meta:
        model = Bonuses
        fields = [
            'id',
            'date',
            'amount',
            'reason',
            'note',
            'staff',
        ]