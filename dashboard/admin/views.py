from rest_framework.response import Response
from django.utils import timezone
from base.permissions import IsHrm
from users.models import User
from companies.models import Companies
from branchs.models import Branchs
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
        """Count Users"""
        total_user = User.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).count()
        
        """Count Company"""
        total_company = Companies.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).count()

        """Count Branch"""
        total_branch = Branchs.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).count() 

        """Count department"""
        total_department = Departments.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).count() 
        
        return Response({
            "total_user" : total_user,
            "total_company" : total_company,
            "total_branch" : total_branch,
            "total_department" : total_department,
        })
