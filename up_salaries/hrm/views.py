from django.utils import timezone
from base.permissions import IsHrm
from base.paginations import ItemIndexPagination
from base.utils import print_value
from up_salaries.models import UpSalary
from .serializers import (
    UpSalarySerializer,
    RetrieveAndListUpSalarySerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class ListCreateUpSalaryAPIView(generics.ListCreateAPIView):
    
    model = UpSalary
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['coefficient', 'staff__user__last_name', 'staff__user__first_name']
    filter_fields = {
        'coefficient': ['exact', 'in'],
        'staff__id': ['exact', 'in'],
    }
    
    
    def get_queryset(self):
        return UpSalary.objects.filter(
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
            return RetrieveAndListUpSalarySerializer
        if self.request.method == 'POST':
            return UpSalarySerializer

class RetrieveUpdateDestroyUpSalaryAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    model = UpSalary
    permission_classes = [IsHrm]
    lookup_url_kwarg = "id"
    
    def get_queryset(self):
        return UpSalary.objects.filter(
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
            return UpSalarySerializer
        else: 
            return RetrieveAndListUpSalarySerializer
