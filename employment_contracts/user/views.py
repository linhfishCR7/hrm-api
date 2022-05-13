from django.utils import timezone
from base.permissions import IsUser
from base.paginations import ItemIndexPagination
from base.utils import print_value
from employment_contracts.models import EmploymentContract
from .serializers import (
    RetrieveAndListEmploymentContractReportSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class ListEmploymentContractAPIView(generics.ListAPIView):
    
    model = EmploymentContract
    permission_classes = [IsUser]
    pagination_class = ItemIndexPagination
    serializer_class = RetrieveAndListEmploymentContractReportSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = [
        'name', 
        'staff__user__last_name', 
        'staff__user__first_name',
        'type__name'
    ]
    filter_fields = {
        'name': ['exact', 'in'],
        'staff__user__last_name': ['exact', 'in'],
        'staff__user__first_name': ['exact', 'in'],
        'staff__id': ['exact', 'in'],
        'id': ['exact', 'in'],
    }
    
    def get_queryset(self):
        return EmploymentContract.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).order_by("-created_at")
    
    @property
    def paginator(self):
        if self.request.query_params.get("no_pagination", "") == "true":
            return None
        return super().paginator