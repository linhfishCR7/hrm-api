from django.utils import timezone
from django.utils.timezone import now    

from base.permissions import IsHrm
from base.paginations import ItemIndexPagination
from base.utils import print_value
from salaries.hrm.filter import SalaryFilter
from salaries.models import Salary
from staffs.models import Staffs
from departments.models import Departments
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

from django.template.loader import get_template
from base.services.s3_services import MediaUpLoad
import os
from django.conf import settings
from weasyprint import HTML


class ListCreateSalaryAPIView(generics.ListCreateAPIView):
    
    model = Salary
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['staff__user__first_name', 'staff__user__last_name', 'date__month']
    filter_fields = {
        'staff__id': ['exact', 'in'],
        'staff__department__id': ['exact', 'in'],
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


class ListAllSalaryReportAPIView(generics.ListCreateAPIView):
    
    model = Salary
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['staff__user__first_name', 'staff__user__last_name', 'date__month']
    filter_fields = {
        'staff__id': ['exact', 'in'],
        'staff__department__id': ['exact', 'in'],
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
            date__month=self.request.GET.get('month', None),
            date__year=self.request.GET.get('year', None)
        ).order_by("staff__department__id")
        
    def list(self, request, *args, **kwargs):
        """Over write list to show total unread """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            key_salary = ''
            salary_check = Salary.objects.filter(
                Q(deleted_at=None) &
                Q(is_deleted=False) &
                Q(date__month=self.request.GET.get('month', None))&
                Q(date__year=self.request.GET.get('year', None))
                ).first()
            if salary_check.is_print==False:
                salary = Salary.objects.filter(
                    Q(deleted_at=None) &
                    Q(is_deleted=False) &
                    Q(date__month=self.request.GET.get('month', None))&
                    Q(date__year=self.request.GET.get('year', None))
                    ).values()
                total_salary = 0
                total_salary_month = 0
                list_id = []
                for item in salary:
                    total_salary += item['basic_salary']+item['extra']+item['other_support']
                    total_salary_month += item['basic_salary']*item['coefficient']+item['extra']+item['other_support']+item['other']
                    list_id.append(item['id'])
                data = {
                    "data": serializer.data,
                    "total_salary_month": f"{total_salary_month:,}",
                    "month": self.request.GET.get('month', None),            
                    "year": self.request.GET.get('year', None),

                }    
                template = get_template('list_salary_report_template.html')
                context = template.render(data).encode("UTF-8")
                filename = '{}_{}_list_salary_report.pdf'.format(self.request.GET.get('month', None),self.request.GET.get('year', None))
                f = open(filename, "w+b")
                HTML(string=context).write_pdf(f)
                f.close()
                key = MediaUpLoad().upload_pdf_to_s3(os.path.join(settings.BASE_DIR, filename), filename)
                
                key_salary_data = MediaUpLoad().get_file_url(key)
                Salary.objects.filter(id__in=list_id).update(
                    link_list_salary=key_salary_data,
                    is_print=True
                )

                
                return Response(dict(
                    self.get_paginated_response(serializer.data).data,
                    key_salary=key_salary_data,
                ))
            else:
                return Response(dict(
                    self.get_paginated_response(serializer.data).data,
                key_salary=salary_check.link_list_salary,
                ))
            
        serializer = self.get_serializer(queryset, many=True)

        key_salary = ''
        salary_check = Salary.objects.filter(
            Q(deleted_at=None) &
            Q(is_deleted=False) &
            Q(date__month=self.request.GET.get('month', None))&
            Q(date__year=self.request.GET.get('year', None))
            ).first()
        if salary_check.is_print==False:
            salary = Salary.objects.filter(
                Q(deleted_at=None) &
                Q(is_deleted=False) &
                Q(date__month=self.request.GET.get('month', None))&
                Q(date__year=self.request.GET.get('year', None))
                ).values()
            total_salary = 0
            total_salary_month = 0
            list_id = []
            for item in salary:
                total_salary += item['basic_salary']+item['extra']+item['other_support']
                total_salary_month += item['basic_salary']*item['coefficient']+item['extra']+item['other_support']+item['other']
                list_id.append(item['id'])
            data = {
                "data": serializer.data,
                "total_salary_month": f"{total_salary_month:,}",
                "month": self.request.GET.get('month', None),            
                "year": self.request.GET.get('year', None),

            }    
            template = get_template('list_salary_report_template.html')
            context = template.render(data).encode("UTF-8")
            filename = '{}_{}_list_salary_report.pdf'.format(self.request.GET.get('month', None),self.request.GET.get('year', None))
            f = open(filename, "w+b")
            HTML(string=context).write_pdf(f)
            f.close()
            key = MediaUpLoad().upload_pdf_to_s3(os.path.join(settings.BASE_DIR, filename), filename)
            
            key_salary_data = MediaUpLoad().get_file_url(key)
            Salary.objects.filter(id__in=list_id).update(
                link_list_salary=key_salary_data,
                is_print=True
            )
            return Response(dict(
                results=serializer.data,
                key_salary=key_salary_data,
            ))   
        else:
            return Response(dict(
                results=serializer.data,
                key_salary=salary_check.link_list_salary,
            ))   
        
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


class ListDepartmentSalaryReportAPIView(generics.ListAPIView):
    
    model = Salary
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['staff__user__first_name', 'staff__user__last_name', 'date__month']
    filter_fields = {
        'staff__id': ['exact', 'in'],
        'staff__department__id': ['exact', 'in'],
    }    
 
    def get_queryset(self):
        return Salary.objects.filter(
            is_deleted=False,
            deleted_at=None,
            date__month=self.request.GET.get('month', None),
            date__year=self.request.GET.get('year', None),
            staff__department__id=self.request.GET.get('department', None),
        ).order_by("-created_at")
        
    def list(self, request, *args, **kwargs):
        """Over write list to show total unread """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            key_salary = ''
            salary_check = Salary.objects.filter(
                Q(deleted_at=None) &
                Q(is_deleted=False) &
                Q(staff__department__id=self.request.GET.get('department', None))&
                Q(date__month=self.request.GET.get('month', None))&
                Q(date__year=self.request.GET.get('year', None))
                ).first()
            if salary_check.is_print==False:
                salary = Salary.objects.filter(
                    Q(deleted_at=None) &
                    Q(is_deleted=False) &
                    Q(staff__department__id=self.request.GET.get('department', None))&
                    Q(date__month=self.request.GET.get('month', None))&
                    Q(date__year=self.request.GET.get('year', None))
                    ).values()
                total_salary = 0
                total_salary_month = 0
                list_id = []
                for item in salary:
                    total_salary += item['basic_salary']+item['extra']+item['other_support']
                    total_salary_month += item['basic_salary']*item['coefficient']+item['extra']+item['other_support']+item['other']
                    list_id.append(item['id'])
                
                department = Departments.objects.filter(id=self.request.GET.get('department', None)).first()
                data = {
                    "data": serializer.data,
                    "total_salary_month": f"{total_salary_month:,}",
                    "month": self.request.GET.get('month', None),            
                    "year": self.request.GET.get('year', None),
                    "department": department.name,

                }    
                template = get_template('list_salary_department_report_template.html')
                context = template.render(data).encode("UTF-8")
                filename = '{}_{}_{}_list_salary_report.pdf'.format(department.department, self.request.GET.get('month', None),self.request.GET.get('year', None))
                f = open(filename, "w+b")
                HTML(string=context).write_pdf(f)
                f.close()
                key = MediaUpLoad().upload_pdf_to_s3(os.path.join(settings.BASE_DIR, filename), filename)
                
                key_salary_data = MediaUpLoad().get_file_url(key)
                Salary.objects.filter(id__in=list_id).update(
                    link_list_department_salary=key_salary_data,
                    is_print=True
                )

                return Response(dict(
                    self.get_paginated_response(serializer.data).data,
                    key_salary=key_salary_data,
                ))
            else:
                return Response(dict(
                    self.get_paginated_response(serializer.data).data,
                    key_salary=salary_check.link_list_salary,
                ))
            
        serializer = self.get_serializer(queryset, many=True)

        key_salary = ''
        salary_check = Salary.objects.filter(
            Q(deleted_at=None) &
            Q(is_deleted=False) &
            Q(staff__department__id=self.request.GET.get('department', None))&
            Q(date__month=self.request.GET.get('month', None))&
            Q(date__year=self.request.GET.get('year', None))
            ).first()
        if salary_check.is_print==False:
            salary = Salary.objects.filter(
                Q(deleted_at=None) &
                Q(is_deleted=False) &
                Q(staff__department__id=self.request.GET.get('department', None))&
                Q(date__month=self.request.GET.get('month', None))&
                Q(date__year=self.request.GET.get('year', None))
                ).values()
            total_salary = 0
            total_salary_month = 0
            list_id = []
            for item in salary:
                total_salary += item['basic_salary']+item['extra']+item['other_support']
                total_salary_month += item['basic_salary']*item['coefficient']+item['extra']+item['other_support']+item['other']
                list_id.append(item['id'])
            
            department = Departments.objects.filter(id=self.request.GET.get('department', None)).first()
            data = {
                "data": serializer.data,
                "total_salary_month": f"{total_salary_month:,}",
                "month": self.request.GET.get('month', None),            
                "year": self.request.GET.get('year', None),
                "department": department.name,

            }    
            template = get_template('list_salary_department_report_template.html')
            context = template.render(data).encode("UTF-8")
            filename = '{}_{}_{}_list_salary_report.pdf'.format(department.department, self.request.GET.get('month', None),self.request.GET.get('year', None))
            f = open(filename, "w+b")
            HTML(string=context).write_pdf(f)
            f.close()
            key = MediaUpLoad().upload_pdf_to_s3(os.path.join(settings.BASE_DIR, filename), filename)
            
            key_salary_data = MediaUpLoad().get_file_url(key)
            Salary.objects.filter(id__in=list_id).update(
                link_list_department_salary=key_salary_data,
                is_print=True
            )
            return Response(dict(
                results=serializer.data,
                key_salary=key_salary_data,
            ))   
        else:
            return Response(dict(
                results=serializer.data,
                key_salary=salary_check.link_list_department_salary,
            ))   
        
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
            # is_active=False,
            date__month=timezone.now().month,
            date__year=timezone.now().year
        ).count()
        if salary > 0:
            salary_email_to_all_user.delay()
            push_all_user_notification_hrm_approved_send_salary.delay()
            Salary.objects.filter(
                is_deleted=False,
                date__month=timezone.now().month,
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



