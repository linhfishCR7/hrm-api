import decimal
from base.constants.common import ProjectStatus, SalaryContant
from base.serializers import ApplicationMethodFieldSerializer
from base.utils import print_value
from day_off_year_details.models import DayOffYearDetails
from day_off_years.models import DayOffYears
from employment_contracts.models import EmploymentContract
from projects.models import Projects
from salaries.models import Salary
from staff_project.models import StaffProject
from staffs.models import Staffs
from timekeeping.models import Timekeeping
from up_salaries.models import UpSalary
from users.models import User
from rest_framework import serializers
from django.utils import timezone
from django.db.models import Q, Count, Exists, OuterRef, Sum
from positions.models import Positions
from departments.models import Departments

from django.template.loader import get_template
from base.services.s3_services import MediaUpLoad
import os
from django.conf import settings
from weasyprint import HTML

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = [
            'id',
            'name',
        ]
        read_only_fields = ['id']


class PositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Positions
        fields = [
            'id',
            'name',
        ]
        read_only_fields = ['id']
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


class SalarySerializer(serializers.ModelSerializer):
    allowance = serializers.DecimalField(required=False, max_digits=20, decimal_places=2)
    tax = serializers.DecimalField(required=False, max_digits=20, decimal_places=2)
    extra = serializers.IntegerField(required=False)
    basic_salary = serializers.IntegerField(required=False)
    coefficient = serializers.FloatField(required=False)
    other_support = serializers.FloatField(required=False)
    other = serializers.FloatField(required=False)
    class Meta:
        model = Salary
        fields = [
            "id",
            "date",
            "standard_time",
            "actual_time",
            "basic_salary",
            "extra",
            "coefficient",
            "allowance",
            "other_support",
            "tax",
            "overtime",
            "other",
            "note",
            "staff",
        ]

    def create(self, validated_data):
        
        """
        Get day off of staffs
        """

        day_off_year = DayOffYears.objects.filter(
            is_deleted=False,
            staff=validated_data['staff'],
            status=True
        ).first()
        day_off_year_detail = []
        if day_off_year: 
            day_off_year_detail = DayOffYearDetails.objects.filter(
                day_off_years=day_off_year.id,
                from_date__month=timezone.now().month,
                to_date__month=timezone.now().month,
                # day_off_types=
            ).first()
            
        # get coefficient
        up_salary = UpSalary.objects.filter(
            is_deleted=False,
            deleted_at=None,
            staff=validated_data['staff']
        ).order_by("-created_at").first()

        # work project by overtime
        staff_project = StaffProject.objects.filter(
            staff=validated_data['staff'],
            project__status=2
        )

        if staff_project:
            for item in staff_project:
                overtime = Timekeeping.objects.filter(
                    staff_project=item.id,
                    date__month=timezone.now().month
                ).values()
                total = 0
                for overtime_data in overtime:
                    total += overtime_data['amount_time']*overtime_data['type']
        else:
            total = 0
            
        employment_contract = EmploymentContract.objects.filter(
            is_active=True,
            is_deleted=False,
            staff=validated_data['staff']
        ).order_by('-created_at').first()
        
        basic_salary=employment_contract.basic_salary,
        coefficient=up_salary.coefficient if up_salary.coefficient else SalaryContant.BASIC_COEFFICIENT

        if not 'extra' in validated_data:
            extra=employment_contract.extra
        else:
            extra=validated_data['extra']

        other_support=validated_data['other_support'] if validated_data['other_support']!=0.0 else employment_contract.other_support
        
        other=validated_data['other'] if validated_data['other'] else 0.0

        basic_salary=int(basic_salary[0])
        coefficient=coefficient
        extra=int(extra) 
        other_support=int(other_support)
        other=int(other)
        # overtime=int(overtime[0])
        actual_time = total+SalaryContant.STANDARD_TIME-(day_off_year_detail.amount*8) if day_off_year_detail else total+SalaryContant.STANDARD_TIME

        # caculate tax
        total_salary = basic_salary*coefficient+extra+other_support+other
        salary_allowance = (basic_salary*coefficient+extra)*(SalaryContant.ALLOWANCE)
        month_salary = total_salary*(actual_time/(SalaryContant.STANDARD_TIME))-salary_allowance
        
        if month_salary <= SalaryContant.M5:
            tax = 0.0
        elif month_salary > SalaryContant.M5 and month_salary <= SalaryContant.M10:
            tax = 0.0
        elif month_salary > SalaryContant.M10 and month_salary <= SalaryContant.M18:
            tax = (month_salary - SalaryContant.M10) * (SalaryContant.UP_M10_M18)
        elif month_salary > SalaryContant.M18 and month_salary <= SalaryContant.M32:
            tax = (month_salary - SalaryContant.M18) * (SalaryContant.UP_M18_M32)
        elif month_salary > SalaryContant.M32 and month_salary <= SalaryContant.M52:
            tax = (month_salary-SalaryContant.M32) * (SalaryContant.UP_M32_M52)
        elif month_salary > SalaryContant.M52 and month_salary <= SalaryContant.M80:
            tax = (month_salary-SalaryContant.M52) * (SalaryContant.UP_M52_M80)
        else:
            tax = (month_salary-SalaryContant.UP_M52_M80) * (SalaryContant.UP_M80)

        # create basic salary from input data
        salary = Salary.objects.create(
            date=validated_data['date'],
            standard_time=SalaryContant.STANDARD_TIME,
            actual_time=actual_time,
            basic_salary=basic_salary,
            extra=extra,
            coefficient=coefficient,
            allowance=SalaryContant.ALLOWANCE,
            tax=tax,
            other_support=other_support,
            overtime=total,
            other=other,
            note=validated_data['note'],
            staff=validated_data['staff'],
            is_active=False,
            is_print=False
        )
        
        return salary
        
    
class RetrieveAndListSalarySerializer(serializers.ModelSerializer):
    staff = StaffsSerializer()

    class Meta:
        model = Salary
        fields = [
            "id",
            "date",
            "standard_time",
            "actual_time",
            "basic_salary",
            "extra",
            "coefficient",
            "allowance",
            "other_support",
            "tax",
            "overtime",
            "other",
            "note",
            "staff",
            "link_list_salary"
        ]

    
    def update(self, instance, validated_data):
        
        """
        Get day off of staffs
        """

        day_off_year = DayOffYears.objects.filter(
            is_deleted=False,
            staff=validated_data['staff'],
            status=True
        ).first()

        day_off_year_detail = DayOffYearDetails.objects.filter(
            day_off_years=day_off_year.id,
            from_date__month=timezone.now().month,
            to_date__month=timezone.now().month,
            # day_off_types=
        ).first()


        # get coefficient
        up_salary = UpSalary.objects.filter(
            is_deleted=False,
            deleted_at=None,
            staff=validated_data['staff']
        ).order_by("-created_at").first()


        # work project by overtime
        staff_project = StaffProject.objects.filter(
            staff=validated_data['staff'],
            project__status=2
        )
        if staff_project:
            for item in staff_project.data:
                overtime = Timekeeping.objects.filter(
                    staff_project=item['id'],
                    date__month=timezone.now().month
                ).values()
                total = 0
                for overtime_data in overtime:
                    total += overtime_data['amount_time']*overtime_data['type']
        else:
            total = 0
            

        
        basic_salary=validated_data['basic_salary'] if validated_data['basic_salary'] else instance.basic_salary,
        # coefficient=validated_data['coefficient'] if validated_data['coefficient'] else instance.coefficient
        coefficient=up_salary.coefficient if up_salary.coefficient else SalaryContant.BASIC_COEFFICIENT
        extra=validated_data['extra'] if validated_data['extra'] else instance.extra
        other_support=validated_data['other_support'] if validated_data['other_support'] else instance.other_support
        
        other=validated_data['other'] if validated_data['other'] else instance.other
        date=validated_data['date'] if validated_data['date'] else instance.date
        note=validated_data['note'] if validated_data['note'] else instance.note

        basic_salary=int(basic_salary[0])
        coefficient=coefficient
        extra=int(extra) 
        other_support=int(other_support)
        other=int(other[0])
        # overtime=int(overtime[0])
        if day_off_year_detail: 
            actual_time = total+SalaryContant.STANDARD_TIME-day_off_year_detail.amount*8
        else:
            actual_time =  total+SalaryContant.STANDARD_TIME

        # caculate tax
        total_salary = basic_salary*coefficient+extra+other_support+other
        salary_allowance = (basic_salary*coefficient+extra)*(SalaryContant.ALLOWANCE)
        month_salary = total_salary*(actual_time/(SalaryContant.STANDARD_TIME))-salary_allowance
        
        if month_salary <= SalaryContant.M5:
            tax = 0.0
        elif month_salary > SalaryContant.M5 and month_salary <= SalaryContant.M10:
            tax = 0.0
        elif month_salary > SalaryContant.M10 and month_salary <= SalaryContant.M18:
            tax = (month_salary - SalaryContant.M10) * (SalaryContant.UP_M10_M18)
        elif month_salary > SalaryContant.M18 and month_salary <= SalaryContant.M32:
            tax = (month_salary - SalaryContant.M18) * (SalaryContant.UP_M18_M32)
        elif month_salary > SalaryContant.M32 and month_salary <= SalaryContant.M52:
            tax = (month_salary-SalaryContant.M32) * (SalaryContant.UP_M32_M52)
        elif month_salary > SalaryContant.M52 and month_salary <= SalaryContant.M80:
            tax = (month_salary-SalaryContant.M52) * (SalaryContant.UP_M52_M80)
        else:
            tax = (month_salary-SalaryContant.UP_M52_M80) * (SalaryContant.UP_M80)


        salary = Salary.objects.filter(id=instance.id).first()

        salary.date=date
        salary.actual_time=actual_time
        salary.basic_salary=basic_salary
        salary.extra=extra
        salary.coefficient=coefficient
        salary.tax=tax
        salary.other_support=other_support
        salary.overtime=total
        salary.other=other
        salary.note=note
        salary.is_print=False
        salary.save()

        return salary

    def to_representation(self, instance):
        """
        To show the data response to users
        """
        response = super().to_representation(instance)
        total_salary_pre = instance.basic_salary+instance.extra+instance.other_support
        response['total_salary_pre'] = f"{total_salary_pre:,}"
        total_salary = instance.basic_salary*instance.coefficient+instance.extra+instance.other_support+instance.other
        salary_allowance = (instance.basic_salary*instance.coefficient+instance.extra)*(SalaryContant.ALLOWANCE)
        response['extra_data'] = f"{instance.extra:,}"
        response['basic_salary_data'] = f"{instance.basic_salary:,}"
        response['tax_data'] = f"{instance.tax:,}"
        response['other_support_data'] = f"{instance.other_support:,}"
        response['other_data'] = f"{instance.other:,}"
        response['extra_data'] = f"{instance.extra:,}"
        response['coefficient_data'] = f"{instance.coefficient:,}"
        response['allowance_data'] = f"{instance.allowance:,}"
        response['tax_data'] = f"{instance.tax:,}"
        response['overtime_data'] = f"{instance.overtime:,}"
        response['standard_time_data'] = f"{instance.standard_time:,}"
        response['actual_time_data'] = f"{instance.actual_time:,}"

        actual_salary_number = total_salary * (instance.actual_time/(SalaryContant.STANDARD_TIME))-salary_allowance+(total_salary*instance.overtime/SalaryContant.STANDARD_TIME-instance.tax)
        response['actual_salary_number'] = actual_salary_number
        
        response['actual_salary'] = f"{actual_salary_number:,}"
        response['total_salary'] = f"{total_salary:,}"

        response['month'] = f"{instance.date:%m}"
        response['year'] = f"{instance.date:%Y}"
        response['staff_id'] = instance.staff.id
        response['staff_data'] = instance.staff.staff
        response['department_name_data'] = instance.staff.department.name
        response['position_name_data'] = instance.staff.position.name
        response['user_fullname'] = f"{instance.staff.user.first_name} {instance.staff.user.last_name}"
        
        # if instance.is_print==False:
        #     data = {
        #         "standard_time_data": response['standard_time_data'],
        #         "actual_time_data": response['actual_time_data'],
        #         "total_salary_pre": response['total_salary_pre'],
        #         "extra_data": response['extra_data'],
        #         "basic_salary_data": response['basic_salary_data'],
        #         "tax_data": response['tax_data'],
        #         "other_support_data": response['other_support_data'],
        #         "other_data": response['other_data'],
        #         "extra_data": response['extra_data'],
        #         "coefficient_data": response['coefficient_data'],
        #         "allowance_data": response['allowance_data'],
        #         "tax_data": response['tax_data'],
        #         "overtime_data": response['overtime_data'],
        #         "actual_salary": response['actual_salary'],
        #         "total_salary": response['total_salary'],
        #         "month": response['month'],
        #         "year": response['year'],
        #         "staff_id": response['staff_id'],
        #         "staff_data": response['staff_data'],
        #         "department_name_data": response['department_name_data'],
        #         "position_name_data": response['position_name_data'],
        #         "user_fullname": response['user_fullname'],
        #     }
        #     template = get_template('salary_report_template.html')
        #     context = template.render(data).encode("UTF-8")
        #     filename = '{}_{}_{}_salary_report.pdf'.format(response['user_fullname'],response['month'],response['year'])
        #     f = open(filename, "w+b")
        #     HTML(string=context).write_pdf(f)
        #     f.close()
        #     key = MediaUpLoad().upload_pdf_to_s3(os.path.join(settings.BASE_DIR, filename), filename)
            
        #     response['key'] = MediaUpLoad().get_file_url(key)
        #     Salary.objects.filter(id=instance.id).update(
        #         link_salary=response['key'],
        #         is_print=True
        #     )
        # else:
        #     response['key'] = instance.link_salary

        return response
    

class RetrieveAndListReportSalarySerializer(serializers.ModelSerializer):
    staff = StaffsSerializer()

    class Meta:
        model = Salary
        fields = [
            "id",
            "date",
            "standard_time",
            "actual_time",
            "basic_salary",
            "extra",
            "coefficient",
            "allowance",
            "other_support",
            "tax",
            "overtime",
            "other",
            "note",
            "staff",
            "link_list_salary"
        ]

    def to_representation(self, instance):
        """
        To show the data response to users
        """
        response = super().to_representation(instance)
        total_salary_pre = instance.basic_salary+instance.extra+instance.other_support
        response['total_salary_pre'] = f"{total_salary_pre:,}"
        total_salary = instance.basic_salary*instance.coefficient+instance.extra+instance.other_support+instance.other
        salary_allowance = (instance.basic_salary*instance.coefficient+instance.extra)*(SalaryContant.ALLOWANCE)
        response['extra_data'] = f"{instance.extra:,}"
        response['basic_salary_data'] = f"{instance.basic_salary:,}"
        response['tax_data'] = f"{instance.tax:,}"
        response['other_support_data'] = f"{instance.other_support:,}"
        response['other_data'] = f"{instance.other:,}"
        response['extra_data'] = f"{instance.extra:,}"
        response['coefficient_data'] = f"{instance.coefficient:,}"
        response['allowance_data'] = f"{instance.allowance:,}"
        response['tax_data'] = f"{instance.tax:,}"
        response['overtime_data'] = f"{instance.overtime:,}"
        response['standard_time_data'] = f"{instance.standard_time:,}"
        response['actual_time_data'] = f"{instance.actual_time:,}"

        actual_salary_number = total_salary * (instance.actual_time/(SalaryContant.STANDARD_TIME))-salary_allowance+(total_salary*instance.overtime/SalaryContant.STANDARD_TIME-instance.tax)
        response['actual_salary_number'] = actual_salary_number
        
        response['actual_salary'] = f"{actual_salary_number:,}"
        response['total_salary'] = f"{total_salary:,}"

        response['month'] = f"{instance.date:%m}"
        response['year'] = f"{instance.date:%Y}"
        response['staff_id'] = instance.staff.id
        response['staff_data'] = instance.staff.staff
        response['department_name_data'] = instance.staff.department.name
        response['position_name_data'] = instance.staff.position.name
        response['user_fullname'] = f"{instance.staff.user.first_name} {instance.staff.user.last_name}"
        
        if instance.is_print==False:
            data = {
                "standard_time_data": response['standard_time_data'],
                "actual_time_data": response['actual_time_data'],
                "total_salary_pre": response['total_salary_pre'],
                "extra_data": response['extra_data'],
                "basic_salary_data": response['basic_salary_data'],
                "tax_data": response['tax_data'],
                "other_support_data": response['other_support_data'],
                "other_data": response['other_data'],
                "extra_data": response['extra_data'],
                "coefficient_data": response['coefficient_data'],
                "allowance_data": response['allowance_data'],
                "tax_data": response['tax_data'],
                "overtime_data": response['overtime_data'],
                "actual_salary": response['actual_salary'],
                "total_salary": response['total_salary'],
                "month": response['month'],
                "year": response['year'],
                "staff_id": response['staff_id'],
                "staff_data": response['staff_data'],
                "department_name_data": response['department_name_data'],
                "position_name_data": response['position_name_data'],
                "user_fullname": response['user_fullname'],
            }
            template = get_template('salary_report_template.html')
            context = template.render(data).encode("UTF-8")
            filename = '{}_{}_{}_salary_report.pdf'.format(response['user_fullname'],response['month'],response['year'])
            f = open(filename, "w+b")
            HTML(string=context).write_pdf(f)
            f.close()
            key = MediaUpLoad().upload_pdf_to_s3(os.path.join(settings.BASE_DIR, filename), filename)
            if os.path.exists(filename):
                os.remove(filename)
            response['key'] = MediaUpLoad().get_file_url(key)
            Salary.objects.filter(id=instance.id).update(
                link_salary=response['key'],
                is_print=True
            )
        else:
            response['key'] = instance.link_salary

        return response