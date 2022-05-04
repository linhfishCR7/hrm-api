from django.utils import timezone
from base.permissions import IsUser
from base.paginations import ItemIndexPagination
from base.utils import print_value
from day_off_years.models import DayOffYears
from day_off_year_details.models import DayOffYearDetails
from .serializers import (
    DayOffYearsSerializer,
    RetrieveAndListDayOffYearsSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class ListCreateDayOffYearsAPIView(generics.ListCreateAPIView):
    
    model = DayOffYears
    permission_classes = [IsUser]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['date']
    filter_fields = {
        'date': ['exact', 'in'],
        'staff__id': ['exact', 'in'],
    }
    
    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user.id,
            created_at=timezone.now(),
            created_by=self.request.user.id,
        )
    
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
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RetrieveAndListDayOffYearsSerializer
        if self.request.method == 'POST':
            return DayOffYearsSerializer

class RetrieveUpdateDestroyDayOffYearsAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    model = DayOffYears
    permission_classes = [IsUser]
    lookup_url_kwarg = "id"
    
    def get_queryset(self):
        return DayOffYears.objects.filter(
            is_deleted=False,
            deleted_at=None,
        )
    
    def perform_update(self, serializer):
        serializer.save(
            modified_at=timezone.now(),
            modified_by=self.request.user.id,
        )
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.deleted_by = self.request.user.id
        
        DayOffYearDetails.objects.filter(day_off_years=instance.id).update(
            is_deleted=True,
            deleted_at = timezone.now()
        )
        instance.save()
        

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return DayOffYearsSerializer
        else: 
            return RetrieveAndListDayOffYearsSerializer