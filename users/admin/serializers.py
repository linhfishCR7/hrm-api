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
            'image',
            'phone',
            'date_of_birth',
            'is_active',
            'is_staff',
            'created_at',
            'is_verified_email',
            'is_superuser'
        ]

        read_only_field = ['id', 'username', 'created_at']

    def to_representation(self, instance):
        """
        To show the data response to users
        """
        response = super().to_representation(instance)
        response['created_at_data'] = f"{instance.created_at:%H:%M, %d-%m-%Y}"
        if instance.is_active == True:
            response['is_active_data'] = 'Hoạt Động'
        else:
            response['is_active_data'] = 'Bị Khoá'

        if instance.is_staff == True and instance.is_superuser == False:
            response['role_data'] = 'QLNS'
        else:
            response['role_data'] = 'NHÂN VIÊN'
            
        if (instance.is_superuser == True and instance.is_staff == True) or (instance.is_superuser == True and instance.is_staff == False):
            response['role_data'] = 'ADMIN'
        

        return response
