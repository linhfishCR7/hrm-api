from django.utils import timezone
from base.permissions import IsHrm
from base.paginations import ItemIndexPagination
from base.utils import print_value
from salaries.models import Salary
from .serializers import (
    SalarySerializer,
    RetrieveAndListSalarySerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.views import APIView
from base.tasks import push_all_user_notification_hrm_approved_send_salary, salary_email_to_all_user
from rest_framework.response import Response


class ListCreateSalaryAPIView(generics.ListCreateAPIView):
    
    model = Salary
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['staff__user__first_name', 'staff__user__last_name', 'date__month']
    filter_fields = {
        'staff__user__first_name': ['exact', 'in'],
        'staff__user__last_name': ['exact', 'in']
    }
    
    def perform_create(self, serializer):
        serializer.save(
            created_at=timezone.now(),
            created_by=self.request.user.id,
        )
    
    def get_queryset(self):
        return Salary.objects.filter(
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
            return RetrieveAndListSalarySerializer
        if self.request.method == 'POST':
            return SalarySerializer

class RetrieveUpdateDestroySalaryAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    model = Salary
    permission_classes = [IsHrm]
    lookup_url_kwarg = "id"
    
    def get_queryset(self):
        return Salary.objects.filter(
            is_deleted=False,
            deleted_at=None,
        )
    
    def perform_update(self, serializer):
        serializer.save(
            modified_at=timezone.now(),
            modified_by=self.request.user.id,
        )
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.deleted_by = self.request.user.id
        instance.save()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return SalarySerializer
        else: 
            return RetrieveAndListSalarySerializer


class ActiveSalaryAPIView(APIView):
    
    model = Salary
    permission_classes = [IsHrm]

    def get(self, request, *args, **kwargs):

        Salary.objects.filter(
            is_deleted=False,
            date__month=timezone.now().month-1,
            date__year=timezone.now().year
        ).update(is_active=True)

        salary_email_to_all_user.delay()
        push_all_user_notification_hrm_approved_send_salary.delay()
        return Response(dict(message='OK'))

        


