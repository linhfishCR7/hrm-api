from django.utils import timezone
from base.permissions import IsHrm
from base.paginations import ItemIndexPagination
from on_business.models import OnBusiness
from .serializers import (
    OnBusinessSerializer,
    RetrieveAndListOnBusinessSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class ListCreateOnBusinessAPIView(generics.ListCreateAPIView):
    
    model = OnBusiness
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['company']
    filter_fields = {
        'staff__id': ['exact', 'in'],
    }
    
    def perform_create(self, serializer):
        serializer.save(
            created_at=timezone.now(),
            created_by=self.request.user.id,
        )
    
    def get_queryset(self):
        return OnBusiness.objects.filter(
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
            return RetrieveAndListOnBusinessSerializer
        if self.request.method == 'POST':
            return OnBusinessSerializer

class RetrieveUpdateDestroyOnBusinessAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    model = OnBusiness
    permission_classes = [IsHrm]
    lookup_url_kwarg = "id"
    
    def get_queryset(self):
        return OnBusiness.objects.filter(
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
            return OnBusinessSerializer
        else: 
            return RetrieveAndListOnBusinessSerializer