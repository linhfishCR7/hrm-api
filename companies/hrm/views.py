from django.utils import timezone
from base.permissions import IsHrm
from base.paginations import ItemIndexPagination
from companies.models import Companies
from .serializers import (
    CompaniesSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class ListCreateCompaniesAPIView(generics.ListCreateAPIView):
    
    model = Companies
    serializer_class = CompaniesSerializer
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['name', 'company']
    filter_fields = {
        'company': ['exact', 'in'],
    }
    
    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            created_at=timezone.now(),
            created_by=self.request.user.id,
        )
    
    def get_queryset(self):
        return Companies.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).order_by("-created_at")
    
    @property
    def paginator(self):
        if self.request.query_params.get("no_pagination", "") == "true":
            return None
        return super().paginator

class RetrieveUpdateDestroyCompaniesAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    model = Companies
    serializer_class = CompaniesSerializer
    permission_classes = [IsHrm]
    lookup_url_kwarg = "id"
    
    def get_queryset(self):
        return Companies.objects.filter(
            is_deleted=False,
            deleted_at=None,
        )
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.deleted_by = self.request.user.id
        instance.save()