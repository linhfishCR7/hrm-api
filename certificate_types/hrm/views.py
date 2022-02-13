from django.utils import timezone
from base.permissions import IsHrm
from base.paginations import ItemIndexPagination
from certificate_types.models import CertificateTypes
from .serializers import (
    CertificateTypesSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter

class ListCreateCertificateTypesAPIView(generics.ListCreateAPIView):
    
    model = CertificateTypes
    serializer_class = CertificateTypesSerializer
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['name', 'certificate_types']
    filter_fields = {
        'certificate_types': ['exact', 'in'],
    }
    
    def get_queryset(self):
        return CertificateTypes.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).order_by("-created_at")
    
    @property
    def paginator(self):
        if self.request.query_params.get("no_pagination", "") == "true":
            return None
        return super().paginator

class RetrieveUpdateDestroyCertificateTypesAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    model = CertificateTypes
    serializer_class = CertificateTypesSerializer
    permission_classes = [IsHrm]
    lookup_url_kwarg = "id"
    
    def get_queryset(self):
        return CertificateTypes.objects.filter(
            is_deleted=False,
            deleted_at=None,
        )
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.deleted_by = self.request.user.id
        instance.save()