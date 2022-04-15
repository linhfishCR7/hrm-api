from rest_framework.response import Response
from django.utils import timezone
from base.permissions import IsHrm
from customers.models import Customers
from staffs.models import Staffs
from projects.models import Projects
from departments.models import Departments
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Sum, Count, Value
from django.db.models.functions import TruncMonth
from django.db.models.expressions import F
from django.db.models import Q
from django.db.models.functions import Extract

class Dashboard(APIView):
    
    permission_classes = (IsHrm,)
    def get(self, request, *args, **kwargs):
        """Count Staffs"""
        total_staff = Staffs.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).count()
        
        """Count Customer"""
        total_customer = Customers.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).count()

        """Count project"""
        total_project = Projects.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).count() 

        """Count department"""
        total_department = Departments.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).count() 
        
        return Response({
            "total_staff" : total_staff,
            "total_customer" : total_customer,
            "total_project" : total_project,
            "total_department" : total_department,
        })


class ProjectsByTime(APIView):
    
    permission_classes = (IsHrm,)
    
    def get(self, request, *args, **kwargs):
        current_year = kwargs.get('current_year', timezone.now().year)
        pros = Projects.objects.filter(
            Q(
                created_at__year=current_year,
                is_deleted=False,
                deleted_at=None
            )
        ).annotate( 
            month=Extract(F('created_at'), 'month'),
        ).values('month').annotate(sum_amount=Count('id'), year=Value(current_year)).values('month','year', 'sum_amount')

        pro_response = []
        for month in range(12):
            if month+1 not in [pro_temp['month'] for pro_temp in pros]:
                pro_response.append(
                    dict(
                        month=month+1,
                        sum_amount=0,
                        year=current_year
                    )
                )
            else:
                index_pro = -1
                for index, pro in enumerate(pros):
                    if pro['month'] == month+1:
                        index_pro = index
                        break
                if index >= 0:
                    pro_response.append(
                        pros[index_pro]
                    )
    
        return Response(pro_response)


class StaffByTime(APIView):
    
    permission_classes = (IsHrm,)
    
    def get(self, request, *args, **kwargs):
        current_year = kwargs.get('current_year', timezone.now().year)
        stafs = Staffs.objects.filter(
            Q(
                created_at__year=current_year,
                is_deleted=False,
                deleted_at=None
            )
        ).annotate( 
            month=Extract(F('created_at'), 'month'),
        ).values('month').annotate(sum_amount=Count('id'), year=Value(current_year)).values('month','year', 'sum_amount')

        staf_response = []
        for month in range(12):
            if month+1 not in [staf_temp['month'] for staf_temp in stafs]:
                staf_response.append(
                    dict(
                        month=month+1,
                        sum_amount=0,
                        year=current_year
                    )
                )
            else:
                index_staf = -1
                for index, staf in enumerate(stafs):
                    if staf['month'] == month+1:
                        index_staf = index
                        break
                if index >= 0:
                    staf_response.append(
                        stafs[index_staf]
                    )
    
        return Response(staf_response)


class CustomerByTime(APIView):
    
    permission_classes = (IsHrm,)
    
    def get(self, request, *args, **kwargs):
        current_year = kwargs.get('current_year', timezone.now().year)
        customers = Customers.objects.filter(
            Q(
                created_at__year=current_year,
                is_deleted=False,
                deleted_at=None
            )
        ).annotate( 
            month=Extract(F('created_at'), 'month'),
        ).values('month').annotate(sum_amount=Count('id'), year=Value(current_year)).values('month','year', 'sum_amount')

        customer_response = []
        for month in range(12):
            if month+1 not in [customer_temp['month'] for customer_temp in customers]:
                customer_response.append(
                    dict(
                        month=month+1,
                        sum_amount=0,
                        year=current_year
                    )
                )
            else:
                index_customer = -1
                for index, customer in enumerate(customers):
                    if customer['month'] == month+1:
                        index_customer = index
                        break
                if index >= 0:
                    customer_response.append(
                        customers[index_customer]
                    )
    
        return Response(customer_response)