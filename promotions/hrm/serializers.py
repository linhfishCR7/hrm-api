from base.serializers import ApplicationMethodFieldSerializer
from promotions.models import Promotions
from staffs.models import Staffs
from positions.models import Positions
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


class PositionsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Positions
        fields = [
            'id',
            'name',
            'position'
        ]
        read_only_fields = ['id']    


class PromotionsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Promotions
        fields = [
            'id',
            'date',
            'content',
            'file',
            'note',
            'staff',
            'position',
        ]
        
    
class RetrieveAndListPromotionsSerializer(serializers.ModelSerializer):
    staff = StaffsSerializer()
    position = PositionsSerializer()

    class Meta:
        model = Promotions
        fields = [
            'id',
            'date',
            'content',
            'file',
            'note',
            'staff',
            'position',
            
        ]
    
    def to_representation(self, instance):
        """
        To show the data response to users
        """
        response = super().to_representation(instance)
        response['position_data'] = instance.position.id
        response['position_name'] = instance.position.name
            
        return response