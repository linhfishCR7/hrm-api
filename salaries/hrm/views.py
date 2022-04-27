from django.utils import timezone
from django.utils.timezone import now    

from base.permissions import IsHrm
from base.paginations import ItemIndexPagination
from base.utils import print_value
from salaries.hrm.filter import SalaryFilter
from salaries.models import Salary
from staffs.models import Staffs
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
from django.db.models import Subquery, OuterRef, Q


class ListCreateSalaryAPIView(generics.ListCreateAPIView):
    
    model = Salary
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['staff__user__first_name', 'staff__user__last_name', 'date__month']
    filter_fields = {
        'staff__id': ['exact', 'in'],
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


class ListPastalaryAPIView(generics.ListAPIView):
    
    model = Salary
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    serializer_class = RetrieveAndListSalarySerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['staff__user__first_name', 'staff__user__last_name', 'date__month']
    filter_fields = {
        'staff__id': ['exact', 'in'],
    }
    

    def get_queryset(self):
        return Salary.objects.filter(
             Q(is_deleted=False)&
             Q(deleted_at=None)&
            ~Q(date__month=now().month,date__year=now().year)
        ).order_by("-created_at")

    @property
    def paginator(self):
        if self.request.query_params.get("no_pagination", "") == "true":
            return None
        return super().paginator


class ListCurrentalaryAPIView(generics.ListAPIView):
    
    model = Salary
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    serializer_class = RetrieveAndListSalarySerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['staff__user__first_name', 'staff__user__last_name', 'date__month']
    filter_fields = {
        'staff__id': ['exact', 'in'],
    }
    

    def get_queryset(self):
        return Salary.objects.filter(
            Q(is_deleted=False)&
            Q(deleted_at=None)&
            Q(date__month=now().month,date__year=now().year)
        ).order_by("-created_at")

    @property
    def paginator(self):
        if self.request.query_params.get("no_pagination", "") == "true":
            return None
        return super().paginator


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
        salary = Salary.objects.filter(
            is_deleted=False,
            is_active=False,
            date__month=timezone.now().month-1,
            date__year=timezone.now().year
        ).count()
        if salary > 0:
            salary_email_to_all_user.delay()
            push_all_user_notification_hrm_approved_send_salary.delay()
            Salary.objects.filter(
                is_deleted=False,
                date__month=timezone.now().month-1,
                date__year=timezone.now().year
            ).update(is_active=True)

        
            return Response(dict(message='Active Phiếu Lương Thành Công'))
        else:
            return Response(dict(message='Đã Active Phiếu Lương Tháng Này'))
        
class CheckSalaryAPIView(APIView):
    
    permission_classes = (IsHrm,)
    
    def get(self, request, *args, **kwargs):

        staff_all = Staffs.objects.filter(
            is_deleted=False,
            is_active=True
        ).values_list('id', flat=True)

        staff_salary = Salary.objects.filter(
            is_deleted=False,
            date__month=now().month,date__year=now().year
        ).values_list('staff_id', flat=True)

        staff_list = []
        for item in staff_all:
            if not item in staff_salary:
                staff_list.append(item)
        if staff_list:
            return Response(staff_list)
        else:
            return Response(dict(message=f"Tháng {now().month} Năm {now().year} Đã Tạo Phiếu Lương Xong"))



