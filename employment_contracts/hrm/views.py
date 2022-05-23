from django.utils import timezone
from base.permissions import IsHrm
from base.paginations import ItemIndexPagination
from base.utils import print_value
from employment_contracts.models import EmploymentContract
from .serializers import (
    EmploymentContractSerializer,
    RetrieveAndListEmploymentContractSerializer,
    RetrieveAndListEmploymentContractReportSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class ListCreateEmploymentContractAPIView(generics.ListCreateAPIView):
    
    model = EmploymentContract
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = [
        'name', 
        'staff__user__last_name', 
        'staff__user__first_name',
        'type__name'
    ]
    filter_fields = {
        'name': ['exact', 'in'],
        'staff__user__last_name': ['exact', 'in'],
        'staff__user__first_name': ['exact', 'in'],
        'staff__id': ['exact', 'in'],
    }
    
    def get_queryset(self):
        return EmploymentContract.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).order_by("-created_at")
    
    def perform_create(self, serializer):
        serializer.save(
            created_at=timezone.now(),
            created_by=self.request.user.id,
        )
    
    @property
    def paginator(self):
        if self.request.query_params.get("no_pagination", "") == "true":
            return None
        return super().paginator

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RetrieveAndListEmploymentContractSerializer
        if self.request.method == 'POST':
            return EmploymentContractSerializer

class RetrieveUpdateDestroyEmploymentContractAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    model = EmploymentContract
    permission_classes = [IsHrm]
    lookup_url_kwarg = "id"
    
    def get_queryset(self):
        return EmploymentContract.objects.filter(
            is_deleted=False,
            deleted_at=None,
        )
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.deleted_by = self.request.user.id
        instance.save()

    def perform_update(self, serializer):
        serializer.save(
            is_print=False
        )
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return EmploymentContractSerializer
        else: 
            return RetrieveAndListEmploymentContractSerializer


class ListEmploymentContractAPIView(generics.ListAPIView):
    
    model = EmploymentContract
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    serializer_class = RetrieveAndListEmploymentContractReportSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = [
        'name', 
        'staff__user__last_name', 
        'staff__user__first_name',
        'type__name'
    ]
    filter_fields = {
        'name': ['exact', 'in'],
        'staff__user__last_name': ['exact', 'in'],
        'staff__user__first_name': ['exact', 'in'],
        'staff__id': ['exact', 'in'],
        'id': ['exact', 'in'],
    }
    
    def get_queryset(self):
        return EmploymentContract.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).order_by("-created_at")
    
    @property
    def paginator(self):
        if self.request.query_params.get("no_pagination", "") == "true":
            return None
        return super().paginator