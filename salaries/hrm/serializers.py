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
                from_date__month=timezone.now().month-1,
                to_date__month=timezone.now().month-1,
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
                    date__month=timezone.now().month-1
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
            tax = month_salary * (SalaryContant.M0_M5)
        elif month_salary > SalaryContant.M5 and month_salary <= SalaryContant.M10:
            tax = month_salary * (SalaryContant.UP_M5_M10)
        elif month_salary > SalaryContant.M10 and month_salary <= SalaryContant.M18:
            tax = month_salary * (SalaryContant.UP_M10_M18)
        elif month_salary > SalaryContant.M18 and month_salary <= SalaryContant.M32:
            tax = month_salary * (SalaryContant.UP_M18_M32)
        elif month_salary > SalaryContant.M32 and month_salary <= SalaryContant.M52:
            tax = month_salary * (SalaryContant.UP_M32_M52)
        elif month_salary > SalaryContant.M52 and month_salary <= SalaryContant.M80:
            tax = month_salary * (SalaryContant.UP_M52_M80)
        else:
            tax = month_salary * (SalaryContant.UP_M80)

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
            is_active=False
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
            from_date__month=timezone.now().month-1,
            to_date__month=timezone.now().month-1,
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
                    date__month=timezone.now().month-1
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
            tax = month_salary * (SalaryContant.M0_M5)
        elif month_salary > SalaryContant.M5 and month_salary <= SalaryContant.M10:
            tax = month_salary * (SalaryContant.UP_M5_M10)
        elif month_salary > SalaryContant.M10 and month_salary <= SalaryContant.M18:
            tax = month_salary * (SalaryContant.UP_M10_M18)
        elif month_salary > SalaryContant.M18 and month_salary <= SalaryContant.M32:
            tax = month_salary * (SalaryContant.UP_M18_M32)
        elif month_salary > SalaryContant.M32 and month_salary <= SalaryContant.M52:
            tax = month_salary * (SalaryContant.UP_M32_M52)
        elif month_salary > SalaryContant.M52 and month_salary <= SalaryContant.M80:
            tax = month_salary * (SalaryContant.UP_M52_M80)
        else:
            tax = month_salary * (SalaryContant.UP_M80)


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
        salary.save()

        return salary

    def to_representation(self, instance):
        """
        To show the data response to users
        """
        response = super().to_representation(instance)
        total_salary = instance.basic_salary*instance.coefficient+instance.extra+instance.other_support+instance.other
        salary_allowance = (instance.basic_salary*instance.coefficient+instance.extra)*(SalaryContant.ALLOWANCE)
        response['extra_data'] = f"{instance.extra:,}"
        response['basic_salary_data'] = f"{instance.basic_salary:,}"
        response['tax_data'] = f"{instance.tax:,}"
        response['other_support_data'] = f"{instance.other_support:,}"
        response['other_data'] = f"{instance.other:,}"


        response['actual_salary'] = f"{total_salary * (instance.actual_time/(SalaryContant.STANDARD_TIME))-salary_allowance+(total_salary*instance.overtime/SalaryContant.STANDARD_TIME-instance.tax):,}"
        response['total_salary'] = f"{total_salary:,}"

        response['month'] = f"{instance.date:%m}"
        response['year'] = f"{instance.date:%Y}"
        response['staff_id'] = instance.staff.id
        response['staff_data'] = instance.staff.staff
        response['user_fullname'] = f"{instance.staff.user.first_name} {instance.staff.user.last_name}"


        return response