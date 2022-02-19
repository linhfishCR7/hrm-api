from django.utils import timezone
from base.permissions import IsHrm
from base.paginations import ItemIndexPagination
from degree_types.models import DegreeTypes
from .serializers import (
    DegreeTypesSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class ListCreateDegreeTypesAPIView(generics.ListCreateAPIView):
    
    model = DegreeTypes
    serializer_class = DegreeTypesSerializer
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['name', 'degree_types']
    filter_fields = {
        'degree_types': ['exact', 'in'],
    }
    
    def get_queryset(self):
        return DegreeTypes.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).order_by("-created_at")
    
    @property
    def paginator(self):
        if self.request.query_params.get("no_pagination", "") == "true":
            return None
        return super().paginator

class RetrieveUpdateDestroyDegreeTypesAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    model = DegreeTypes
    serializer_class = DegreeTypesSerializer
    permission_classes = [IsHrm]
    lookup_url_kwarg = "id"
    
    def get_queryset(self):
        return DegreeTypes.objects.filter(
            is_deleted=False,
            deleted_at=None,
        )
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.deleted_by = self.request.user.id
        instance.save()