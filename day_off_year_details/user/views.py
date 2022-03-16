from django.utils import timezone
from base.permissions import IsUser
from base.paginations import ItemIndexPagination
from base.utils import print_value
from day_off_year_details.models import DayOffYearDetails
from .serializers import (
    DayOffYearDetailsSerializer,
    RetrieveAndListDayOffYearDetailsSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class ListCreateDayOffYearDetailsAPIView(generics.ListCreateAPIView):
    
    model = DayOffYearDetails
    permission_classes = [IsUser]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['date']
    filter_fields = {
        'from_date': ['exact', 'in']
    }
    
    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user.id,
            created_at=timezone.now(),
            created_by=self.request.user.id,
        )
    
    def get_queryset(self):
        return DayOffYearDetails.objects.filter(
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
            return RetrieveAndListDayOffYearDetailsSerializer
        if self.request.method == 'POST':
            return DayOffYearDetailsSerializer

class RetrieveUpdateDestroyDayOffYearDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    model = DayOffYearDetails
    permission_classes = [IsUser]
    lookup_url_kwarg = "id"
    
    def get_queryset(self):
        return DayOffYearDetails.objects.filter(
            is_deleted=False,
            deleted_at=None,
        )
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.deleted_by = self.request.user.id
        instance.save()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return DayOffYearDetailsSerializer
        else: 
            return RetrieveAndListDayOffYearDetailsSerializer