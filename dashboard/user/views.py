import django.db
from rest_framework.response import Response
from django.utils import timezone
from base.permissions import IsUser
from day_off_years.models import DayOffYears
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Sum, Count, Value
from django.db.models.functions import TruncMonth
from django.db.models.expressions import F
from django.db.models import Q
from django.db.models.functions import Extract
from salaries.models import Salary
from staff_project.models import StaffProject
from timekeeping.models import Timekeeping
from employment_contracts.models import EmploymentContract
import datetime
from base.utils import print_value


class Dashboard(APIView):
    
    permission_classes = (IsUser,)
    def get(self, request, *args, **kwargs):
        """Count Day Off Year"""
        total_day_off_year = DayOffYears.objects.filter(
            is_deleted=False,
            deleted_at=None,
            staff=self.request.GET.get('staff', None)
        ).count()
        
        """Count Project"""
        total_project = StaffProject.objects.filter(
            is_deleted=False,
            deleted_at=None,
            staff_id=self.request.GET.get('staff', None)
        ).count()
        
        """Count Salary"""
        total_salary = Salary.objects.filter(
            is_deleted=False,
            deleted_at=None,
            staff_id=self.request.GET.get('staff', None)
        ).count()
        
        """Count time """
        data = StaffProject.objects.filter(
            is_deleted=False,
            deleted_at=None,
            staff_id=self.request.GET.get('staff', None)
        ).values_list('id', flat=True)

        data_time = Timekeeping.objects.filter(
            is_deleted=False,
            deleted_at=None,
            staff_project__in=data
        ).annotate(total_time_keeping=Sum('amount_in_project')*8+Sum('amount_time')).values('total_time_keeping')
        total_time_keeping = 0
        for item in data_time:
            total_time_keeping+=item['total_time_keeping']
            
        
        return Response({
            "total_day_off_year" : total_day_off_year,
            "total_project" : total_project,
            "total_time_keeping" : total_time_keeping,
            "total_salary": total_salary
        })
