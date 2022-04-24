# Django imports
from django.db.models import Count, Sum
from base.serializers import ApplicationMethodFieldSerializer

# Rest Framework Imports
from rest_framework import serializers

# Model Imports
from notification.models import Notification
from users.models import User

# Serializer Imports


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


class ListNotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Notification
        fields = [
            "id",
            "title",
            "body",
            "is_seen",
            "created_at",
            "notification_type",
            "user",
            "metadata"
            
        ]
    
    def to_representation(self, instance):
        """
        To show the data response to users
        """
        response = super().to_representation(instance)

        if instance.metadata:
            user = User.objects.filter(
                id=instance.metadata['user_id'], 
                is_deleted=False
            ).first()
            if user:
                if user.image:
                    image = ApplicationMethodFieldSerializer.get_list_image(user.image)
                    response['user_image'] = image['image_s3_url']
                else:
                    response['user_image'] = None
                if user.first_name:
                    response['first_name_data'] = user.first_name
                else:
                    response['first_name_data'] = 'NameLess'
            else:
                response['user_image'] = None
                response['first_name_data'] = 'NameLess'
        else:
            response['user_image'] = None
            response['first_name_data'] = 'NameLess'
        return response
        
        
