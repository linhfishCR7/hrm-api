from django.utils import timezone
from base.permissions import IsHrm
from base.paginations import ItemIndexPagination
from base.utils import print_value
from certificate.models import Certificate
from .serializers import (
    CertificateSerializer,
    RetrieveAndListCertificateSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class ListCreateCertificateAPIView(generics.ListCreateAPIView):
    
    model = Certificate
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['name', 'staff__user__last_name', 'staff__user__first_name']
    filter_fields = {
        'name': ['exact', 'in'],
        'staff__id': ['exact', 'in'],
        'staff__user__last_name': ['exact', 'in'],
        'staff__user__first_name': ['exact', 'in'],
    }
    
    def get_queryset(self):
        return Certificate.objects.filter(
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
            return RetrieveAndListCertificateSerializer
        if self.request.method == 'POST':
            return CertificateSerializer

class RetrieveUpdateDestroyCertificateAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    model = Certificate
    permission_classes = [IsHrm]
    lookup_url_kwarg = "id"
    
    def get_queryset(self):
        return Certificate.objects.filter(
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
            return CertificateSerializer
        else: 
            return RetrieveAndListCertificateSerializer