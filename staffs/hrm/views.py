from django.utils import timezone
from base.permissions import IsHrm
from base.paginations import ItemIndexPagination
from staffs.models import Staffs
from .serializers import (
    StaffsSerializer,
    RetrieveAndListStaffsSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class ListCreateStaffsAPIView(generics.ListCreateAPIView):
    
    model = Staffs
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = [
        'user__first_name', 
        'user__last_name', 
        'staff', 
        'gender',
        'marital_status',
    ]
    filter_fields = {
        'staff': ['exact', 'in'],
        'nationality__name': ['exact', 'in'],
        'ethnicity__name': ['exact', 'in'],
        'religion__name': ['exact', 'in'],
        'literacy__name': ['exact', 'in'],        
    }
    
    def perform_create(self, serializer):
        serializer.save(
            # user=self.request.user,
            created_at=timezone.now(),
            created_by=self.request.user.id,
        )
    
    def get_queryset(self):
        return Staffs.objects.filter(
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
            return RetrieveAndListStaffsSerializer
        if self.request.method == 'POST':
            return StaffsSerializer

class RetrieveUpdateDestroyStaffsAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    model = Staffs
    permission_classes = [IsHrm]
    lookup_url_kwarg = "id"
    
    def get_queryset(self):
        return Staffs.objects.filter(
            is_deleted=False,
            deleted_at=None,
        )
    
    def perform_update(self, serializer):
        serializer.save(
            user=self.request.user,
            modified_at=timezone.now(),
            modified_by=self.request.user.id,
        )
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.deleted_by = self.request.user.id
        instance.save()
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return StaffsSerializer
        else: 
            return RetrieveAndListStaffsSerializer