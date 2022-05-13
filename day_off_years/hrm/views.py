from django.utils import timezone
from base.permissions import IsHrm
from base.paginations import ItemIndexPagination
from base.utils import print_value
from day_off_years.models import DayOffYears
from staffs.models import Staffs
from .serializers import (
    DayOffYearsSerializer,
    RetrieveAndListDayOffYearsSerializer,
    RetrieveAndListDayOffYearsReportSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class ListDayOffYearsAPIView(generics.ListAPIView):
    
    model = DayOffYears
    permission_classes = [IsHrm]
    serializer_class = RetrieveAndListDayOffYearsSerializer
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['date']
    filter_fields = {
        'date': ['exact', 'in'],
        'staff__id': ['exact', 'in'],
    }
    
    def get_queryset(self):
        return DayOffYears.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).order_by("-created_at")
    
    @property
    def paginator(self):
        if self.request.query_params.get("no_pagination", "") == "true":
            return None
        return super().paginator


class RetrieveUpdateDestroyDayOffYearsAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    model = DayOffYears
    permission_classes = [IsHrm]
    lookup_url_kwarg = "id"
    
    def get_queryset(self):
        return DayOffYears.objects.filter(
            is_deleted=False,
            deleted_at=None,
        )
        
    def perform_update(self, serializer):
        staff = Staffs.objects.filter(user_id=self.request.user.id).first()
        serializer.save(
        # user=self.request.user.id,
        modified_at=timezone.now(),
        modified_by=self.request.user.id,
        approved_by=staff
    )
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.deleted_by = self.request.user.id
        instance.save()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return DayOffYearsSerializer
        else: 
            return RetrieveAndListDayOffYearsSerializer
        

class ListDayOffYearsReportAPIView(generics.ListAPIView):
    
    model = DayOffYears
    permission_classes = [IsHrm]
    serializer_class = RetrieveAndListDayOffYearsReportSerializer
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['date']
    filter_fields = {
        'date': ['exact', 'in'],
        'staff__id': ['exact', 'in'],
        'id': ['exact', 'in'],
    }
    
    def get_queryset(self):
        return DayOffYears.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).order_by("-created_at")
    
    @property
    def paginator(self):
        if self.request.query_params.get("no_pagination", "") == "true":
            return None
        return super().paginator