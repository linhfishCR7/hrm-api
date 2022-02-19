from django.utils import timezone
from base.permissions import IsHrm
from base.paginations import ItemIndexPagination
from ethnicities.models import Ethnicities
from .serializers import (
    EthnicitiesSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class ListCreateEthnicitiesAPIView(generics.ListCreateAPIView):
    
    model = Ethnicities
    serializer_class = EthnicitiesSerializer
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['name', 'ethnicity']
    filter_fields = {
        'ethnicity': ['exact', 'in'],
    }
    
    def get_queryset(self):
        return Ethnicities.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).order_by("-created_at")
    
    @property
    def paginator(self):
        if self.request.query_params.get("no_pagination", "") == "true":
            return None
        return super().paginator

class RetrieveUpdateDestroyEthnicitiesAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    model = Ethnicities
    serializer_class = EthnicitiesSerializer
    permission_classes = [IsHrm]
    lookup_url_kwarg = "id"
    
    def get_queryset(self):
        return Ethnicities.objects.filter(
            is_deleted=False,
            deleted_at=None,
        )
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.deleted_by = self.request.user.id
        instance.save()