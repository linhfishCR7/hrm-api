from base.serializers import ApplicationMethodFieldSerializer
from base.tasks import day_off_year_email, push_hrn_notification_user_created_day_off_year
from base.utils import print_value
from day_off_year_details.models import DayOffYearDetails
from day_off_years.models import DayOffYears
from day_off_types.models import DayOffTypes
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
            'staff',
            'status'

        ]
        

class DayOffTypesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DayOffTypes
        fields = [
            'id',
            'day_off_types',
            'name'
        ]

        
class DayOffYearDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayOffYearDetails
        fields = [
            'id',
            'from_date',
            'to_date',
            'amount',
            'note',
            'day_off_types',
            'day_off_years'
        ]
        
    def create(self, validated_data):
        
        day_off_year_detail = DayOffYearDetails.objects.create(
            from_date=validated_data['from_date'],
            to_date=validated_data['to_date'],
            amount=validated_data['amount'],
            note=validated_data['note'],
            day_off_years=validated_data['day_off_years'],
            day_off_types=validated_data['day_off_types']
        )
        
        user = User.objects.filter(
            id=validated_data['user'],
            is_deleted=False,
            deleted_at=None
        ).first()
        
        day_off_year_email.delay(dict(name=f'{user.first_name} {user.last_name}', link=day_off_year_detail.id))
        push_hrn_notification_user_created_day_off_year.delay(metadata=user.id, name=f'{user.first_name} {user.last_name}')
        
        return day_off_year_detail
        
    
class RetrieveAndListDayOffYearDetailsSerializer(serializers.ModelSerializer):
    day_off_years = DayOffYearsSerializer()
    day_off_types = DayOffTypesSerializer()
    class Meta:
        model = DayOffYearDetails
        fields = [
            'id',
            'from_date',
            'to_date',
            'amount',
            'note',
            'day_off_types',
            'day_off_years',
        ]

    def to_representation(self, instance):
        """
        To show the data response to users
        """
        response = super().to_representation(instance)
        response['day_off_type_name'] = instance.day_off_types.name
        response['day_off_years_id'] = instance.day_off_years.id
        response['day_off_years_status'] = instance.day_off_years.status
        response['full_name'] = f"{instance.day_off_years.staff.user.first_name} {instance.day_off_years.staff.user.last_name}"
        return response