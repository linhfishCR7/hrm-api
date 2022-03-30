from base.serializers import ApplicationMethodFieldSerializer
from base.tasks import day_off_year_email_to_user, push_user_notification_hrm_approved_day_off_year
from base.utils import print_value
from day_off_years.models import DayOffYears
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


class DayOffYearsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DayOffYears
        fields = [
            'id',
            'date',
            'reason',
            'contact',
            'status',
            'hand_over',
            'approved_by',
        ]
        
    def update(self, instance, validated_data):
        
        day_off_year = DayOffYears.objects.filter(id=instance.id).first()        
        day_off_year.status=validated_data['status']
        day_off_year.save()
        updated_instance = super().update(instance, validated_data)
        
        staff = Staffs.objects.filter(id=instance.staff.id).first()
        
        user = User.objects.filter(
            id=staff.user_id,
            is_deleted=False,
            deleted_at=None
        ).first()
        
        if validated_data['status']==True:
            day_off_year_email_to_user.delay(dict(name=f'{user.first_name} {user.last_name}', link=instance.id, user_id=user.id))
            push_user_notification_hrm_approved_day_off_year.delay(metadata=user.id, user_id=user.id)
        
        return updated_instance
    
    
class RetrieveAndListDayOffYearsSerializer(serializers.ModelSerializer):
    staff = StaffsSerializer()
    class Meta:
        model = DayOffYears
        fields = [
            'id',
            'date',
            'reason',
            'contact',
            'status',
            'hand_over',
            'approved_by',
            'staff'
        ]
        read_only_fields = [
            'id',
            'status',
            'approved_by'
        ]