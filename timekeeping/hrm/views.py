from django.utils import timezone
from base.permissions import IsHrm
from base.paginations import ItemIndexPagination
from base.utils import print_value
from timekeeping.models import Timekeeping
from .serializers import (
    TimekeepingSerializer,
    RetrieveAndListTimekeepingSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class ListCreateTimekeepingAPIView(generics.ListCreateAPIView):
    
    model = Timekeeping
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = [
        'staff_project__staff__user__first_name', 
        'staff_project__staff__user__last_name', 
        'staff_project__staff__staff',
        'staff_project__project__name'
        ]
    filter_fields = {
        'date': ['exact', 'in'],
        'staff_project__staff__user__first_name': ['exact', 'in'],
        'staff_project__staff__user__last_name': ['exact', 'in'],
        'staff_project__staff__id': ['exact', 'in'],
    }
    
    def get_queryset(self):
        return Timekeeping.objects.filter(
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
            return RetrieveAndListTimekeepingSerializer
        if self.request.method == 'POST':
            return TimekeepingSerializer

class RetrieveUpdateDestroyTimekeepingAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    model = Timekeeping
    permission_classes = [IsHrm]
    lookup_url_kwarg = "id"
    
    def get_queryset(self):
        return Timekeeping.objects.filter(
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
            return TimekeepingSerializer
        else: 
            return RetrieveAndListTimekeepingSerializer