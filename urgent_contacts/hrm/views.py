from django.utils import timezone
from base.permissions import IsHrm
from base.paginations import ItemIndexPagination
from base.utils import print_value
from urgent_contacts.models import UrgentContacts
from .serializers import (
    UrgentContactsSerializer,
    RetrieveAndListUrgentContactsSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class ListCreateUrgentContactsAPIView(generics.ListCreateAPIView):
    
    model = UrgentContacts
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['full_name']
    filter_fields = {
        'type': ['exact', 'in'],
        'staff__id': ['exact', 'in'],
    }
    
    def perform_create(self, serializer):
        serializer.save(
            created_at=timezone.now(),
            created_by=self.request.user.id,
        )
    
    def get_queryset(self):
        return UrgentContacts.objects.filter(
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
            return RetrieveAndListUrgentContactsSerializer
        if self.request.method == 'POST':
            return UrgentContactsSerializer

class RetrieveUpdateDestroyUrgentContactsAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    model = UrgentContacts
    permission_classes = [IsHrm]
    lookup_url_kwarg = "id"
    
    def get_queryset(self):
        return UrgentContacts.objects.filter(
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
            return UrgentContactsSerializer
        else: 
            return RetrieveAndListUrgentContactsSerializer