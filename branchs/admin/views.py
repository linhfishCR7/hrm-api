from django.utils import timezone
from base.permissions import IsAdmin
from base.paginations import ItemIndexPagination
from base.utils import print_value
from branchs.models import Branchs
from .serializers import (
    BranchsSerializer,
    RetrieveAndListBranchsSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class ListCreateBranchsAPIView(generics.ListCreateAPIView):
    
    model = Branchs
    permission_classes = [IsAdmin]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['name', 'branch']
    filter_fields = {
        'name': ['exact', 'in'],
        'company__id': ['exact', 'in'],
    }
    
    def get_queryset(self):
        return Branchs.objects.filter(
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
            return RetrieveAndListBranchsSerializer
        if self.request.method == 'POST':
            return BranchsSerializer

class RetrieveUpdateDestroyBranchsAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    model = Branchs
    permission_classes = [IsAdmin]
    lookup_url_kwarg = "id"
    
    def get_queryset(self):
        return Branchs.objects.filter(
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
            return BranchsSerializer
        else: 
            return RetrieveAndListBranchsSerializer


class ListBranchsAPIView(generics.ListAPIView):
    
    model = Branchs
    permission_classes = []
    serializer_class = BranchsSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['name', 'branch']
    filter_fields = {
        'name': ['exact', 'in'],
        'company__id': ['exact', 'in'],
    }
    def get_queryset(self):
        return Branchs.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).order_by("-created_at")