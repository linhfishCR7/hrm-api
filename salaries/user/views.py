from django.http import HttpResponse
from django.views.generic import View
from rest_framework.response import Response
from rest_framework import filters, generics, status
from salaries.models import Salary
from staffs.models import Staffs
from .serializers import (
    RetrieveAndListSalarySerializer
)
from base.permissions import IsUser
from base.paginations import ItemIndexPagination
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter

class GeneratePdf(generics.RetrieveAPIView):
    model = Salary
    permission_classes = [IsUser]
    lookup_url_kwarg = "id"
    serializer_class = RetrieveAndListSalarySerializer

    def get_queryset(self):
        staff = Staffs.objects.filter(user_id=self.request.user.id).first()
        return Salary.objects.filter(
            is_deleted=False,
            deleted_at=None,
            is_active=True,
            staff=staff
        )


class ListSalaryAPIView(generics.ListAPIView):
    
    model = Salary
    serializer_class = RetrieveAndListSalarySerializer
    permission_classes = [IsUser]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['staff__user__first_name', 'staff__user__last_name', 'date__month']
    filter_fields = {
        'staff__id': ['exact', 'in'],
    }    

    def get_queryset(self):

        return Salary.objects.filter(
            is_deleted=False,
            deleted_at=None,
            is_active=True,
        ).order_by("-created_at")
    
    @property
    def paginator(self):
        if self.request.query_params.get("no_pagination", "") == "true":
            return None
        return super().paginator
