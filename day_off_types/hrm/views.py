from django.utils import timezone
from base.permissions import IsHrm, IsUser
from base.paginations import ItemIndexPagination
from day_off_types.models import DayOffTypes
from .serializers import (
    DayOffTypesSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter

class ListCreateDayOffTypesAPIView(generics.ListCreateAPIView):
    
    model = DayOffTypes
    serializer_class = DayOffTypesSerializer
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['name', 'day_off_types']
    filter_fields = {
        'day_off_types': ['exact', 'in'],
    }
    
    def get_queryset(self):
        return DayOffTypes.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).order_by("-created_at")
    
    @property
    def paginator(self):
        if self.request.query_params.get("no_pagination", "") == "true":
            return None
        return super().paginator

class RetrieveUpdateDestroyDayOffTypesAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    model = DayOffTypes
    serializer_class = DayOffTypesSerializer
    permission_classes = [IsHrm]
    lookup_url_kwarg = "id"
    
    def get_queryset(self):
        return DayOffTypes.objects.filter(
            is_deleted=False,
            deleted_at=None,
        )
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.deleted_by = self.request.user.id
        instance.save()