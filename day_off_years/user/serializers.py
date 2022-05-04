from base.serializers import ApplicationMethodFieldSerializer
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
            'staff',
        ]
        
    def create(self, validated_data):

        day_off_year = DayOffYears.objects.create(
            date=validated_data['date'],
            reason=validated_data['reason'],
            contact=validated_data['contact'],
            hand_over=validated_data['hand_over'],
            status=False,
            approved_by=None,
            staff=validated_data['staff'],
        )
        
        return day_off_year
    
    def update(self, instance, validated_data):
        
        day_off_year = DayOffYears.objects.filter(id=instance.id).first()
        day_off_year.status=False
        day_off_year.approved_by=instance.approved_by
        day_off_year.save()
        updated_instance = super().update(instance, validated_data)
        
        return updated_instance
    
    
class RetrieveAndListDayOffYearsSerializer(serializers.ModelSerializer):
    staff = StaffsSerializer()
    approved_by = StaffsSerializer()
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