from base.serializers import ApplicationMethodFieldSerializer
from base.tasks import (day_off_year_email, day_off_year_email_to_user,
    day_off_year_refuse_email_to_user, push_user_notification_hrm_approved_day_off_year,
    push_user_notification_hrm_refused_day_off_year)
from base.utils import print_value
from day_off_years.models import DayOffYears
from staffs.models import Staffs
from users.models import User
from rest_framework import serializers
from departments.models import Departments
from branchs.models import Branchs
from day_off_year_details.models import DayOffYearDetails

from pathlib import Path
from django.template.loader import get_template
from base.services.s3_services import MediaUpLoad
import os
from django.conf import settings
from weasyprint import HTML, default_url_fetcher

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


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branchs
        fields = [
            'id',
            'branch',
            'name',
        ]
        read_only_fields = ['id']


class DepartmentSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    class Meta:
        model = Departments
        fields = [
            'id',
            'department',
            'name',
            'branch'
        ]
        read_only_fields = ['id']


class StaffsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    class Meta:
        model = Staffs
        fields = [
            'id',
            'staff',
            'user',
            'department'
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
            'modified_by',
        ]

        read_only_fields = [
            'id',
            'date',
            'reason',
            'contact',
            'hand_over',
        ]
        
    def update(self, instance, validated_data):
        status = validated_data['status']
        day_off_year = DayOffYears.objects.filter(id=instance.id).first()    
        if status==True:
            day_off_year.status=status
            day_off_year.save()
            updated_instance = super().update(instance, validated_data)
            staff = Staffs.objects.filter(id=instance.staff.id).first()
            user = User.objects.filter(
                id=staff.user_id,
                is_deleted=False,
                deleted_at=None
            ).first()
            
            day_off_year_email_to_user.delay(dict(name=f'{user.first_name} {user.last_name}', link=instance.id, user_id=user.id))
            push_user_notification_hrm_approved_day_off_year.delay(metadata=instance.modified_by, user_id=user.id)
        else:
            day_off_year.status=status
            day_off_year.approved_by=None
            day_off_year.save()
            updated_instance = super().update(instance, validated_data)
            staff = Staffs.objects.filter(id=instance.staff.id).first()
            user = User.objects.filter(
                id=staff.user_id,
                is_deleted=False,
                deleted_at=None
            ).first()
            
            day_off_year_refuse_email_to_user.delay(dict(name=f'{user.first_name} {user.last_name}', link=instance.id, user_id=user.id))
            push_user_notification_hrm_refused_day_off_year.delay(metadata=instance.modified_by, user_id=user.id)

        return updated_instance
    
    
class RetrieveAndListDayOffYearsSerializer(serializers.ModelSerializer):
    staff = StaffsSerializer()
    approved_by=StaffsSerializer()
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

    def to_representation(self, instance):
        """
        To show the data response to users
        """
        response = super().to_representation(instance)
        if instance.approved_by:
            response['approved_by_name'] = instance.approved_by.user.first_name + ' ' + instance.approved_by.user.last_name
        else:
            response['approved_by_name'] = 'Chưa Phê Duyệt'
        
        if instance.status == False:
            response['status_text'] = 'Chờ Phê Duyệt'
        else:
            response['status_text'] = 'Đã Phê Duyệt'
        return response
    

class RetrieveAndListDayOffYearsReportSerializer(serializers.ModelSerializer):
    staff = StaffsSerializer()
    approved_by=StaffsSerializer()
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

    def to_representation(self, instance):
        """
        To show the data response to users
        """
        response = super().to_representation(instance)
        if instance.approved_by:
            response['approved_by_name'] = instance.approved_by.user.first_name + ' ' + instance.approved_by.user.last_name
        else:
            response['approved_by_name'] = 'Chưa Phê Duyệt'
        
        if instance.status == False:
            response['status_text'] = 'Chờ Phê Duyệt'
        else:
            response['status_text'] = 'Đã Phê Duyệt'
            
        response['month'] = f"{instance.date:%m}"
        response['year'] = f"{instance.date:%Y}"
        response['day_off_year_detail'] = DayOffYearDetails.objects.filter(day_off_years=instance).select_related('day_off_types').values('from_date', 'to_date', 'amount', 'note' ,'day_off_types__name')
            
        if instance.is_print==True:
            data = {
                "staff": instance.staff,
                "full_name": f"{instance.staff.user.last_name} {instance.staff.user.first_name}",
                "month": response['month'],
                "year": response['year'],
                "department": instance.staff.department.name,
                "branch": instance.staff.department.branch.name,
                "reason": instance.reason,
                "contact": instance.contact,
                "hand_over": instance.hand_over,
                "date": f"{instance.date:%d-%m-%Y}",
                "approved_by": f"{instance.approved_by.user.last_name} {instance.approved_by.user.first_name}",
                "day_off_year_detail": response['day_off_year_detail']
            }
            template = get_template('day_off_year_report_template.html')
            context = template.render(data).encode("UTF-8")
            filename = '{}_{}_{}_day_off_year_report.pdf'.format(f"{instance.staff.staff}", response['month'], response['year'])
            f = open(filename, "w+b")
            HTML(string=context).write_pdf(f)
            f.close()
            key = MediaUpLoad().upload_pdf_to_s3(os.path.join(settings.BASE_DIR, filename), filename)
            if os.path.exists(filename):
                os.remove(filename)
            response['key'] = MediaUpLoad().get_file_url(key)
            DayOffYears.objects.filter(id=instance.id).update(
                link_day_off_year=response['key'],
                is_print=True
            )
        else:
            response['key'] = instance.link_day_off_year
        return response