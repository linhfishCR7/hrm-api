from django.utils import timezone
from base.permissions import IsHrm
from base.paginations import ItemIndexPagination
from base.utils import print_value
from departments.models import Departments
from .serializers import (
    DepartmentsSerializer,
    RetrieveAndListDepartmentsSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class ListCreateDepartmentsAPIView(generics.ListCreateAPIView):
    
    model = Departments
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['name', 'department']
    filter_fields = {
        'name': ['exact', 'in'],
    }
    
    def get_queryset(self):
        return Departments.objects.filter(
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
            return RetrieveAndListDepartmentsSerializer
        if self.request.method == 'POST':
            return DepartmentsSerializer

class RetrieveUpdateDestroyDepartmentsAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    model = Departments
    permission_classes = [IsHrm]
    lookup_url_kwarg = "id"
    
    def get_queryset(self):
        return Departments.objects.filter(
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
            return DepartmentsSerializer
        else: 
            return RetrieveAndListDepartmentsSerializer


class ListDepartmentsAPIView(generics.ListAPIView):
    
    model = Departments
    permission_classes = []
    serializer_class = DepartmentsSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['name', 'branch']
    filter_fields = {
        'name': ['exact', 'in'],
        'branch__id': ['exact', 'in'],
    }
    def get_queryset(self):
        return Departments.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).order_by("-created_at")