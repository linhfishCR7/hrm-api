import django.db
from rest_framework.response import Response
from django.utils import timezone
from base.permissions import IsHrm
from day_off_years.models import DayOffYears
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
        """Count Day Off Year"""
        total_day_off_year = DayOffYears.objects.filter(
            is_deleted=False,
            deleted_at=None,
            staff=self.request.GET.get('staff', None)
        ).count()
        
        return Response({
            "total_day_off_year" : total_day_off_year,
        })
