from users.models import User
from rest_framework import serializers

class ListUsersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
        ]
        

class DetailsUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'image',
            'phone',
            'date_of_birth'
        ]