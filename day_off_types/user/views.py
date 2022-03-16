from django.utils import timezone
from base.permissions import IsUser
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

class ListDayOffTypesAPIView(generics.ListAPIView):
    
    model = DayOffTypes
    serializer_class = DayOffTypesSerializer
    permission_classes = [IsUser]
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