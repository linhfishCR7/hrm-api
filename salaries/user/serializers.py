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

from django.template.loader import get_template
from base.services.s3_services import MediaUpLoad
import os
from django.conf import settings
from weasyprint import HTML
from positions.models import Positions
from departments.models import Departments

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
    department = DepartmentSerializer(read_only=True)
    position = PositionsSerializer(read_only=True)
    class Meta:
        model = Staffs
        fields = [
            'id',
            'staff',
            'user',
            'department',
            'position'
        ]
        read_only_fields = ['id']


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


        response['actual_salary'] = f"{total_salary * (instance.actual_time/(SalaryContant.STANDARD_TIME))-salary_allowance+(total_salary*instance.overtime/SalaryContant.STANDARD_TIME-instance.tax):,}"
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
            
            response['key'] = MediaUpLoad().get_file_url(key)
            Salary.objects.filter(id=instance.id).update(
                link_salary=response['key'],
                is_print=True
            )
        else:
            response['key'] = instance.link_salary

        return response