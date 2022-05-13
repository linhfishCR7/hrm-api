from django.utils import timezone
from base.permissions import IsHrm
from base.paginations import ItemIndexPagination
from base.tasks import push_admin_notification_staff_deleted
from base.utils import print_value
from staffs.models import Staffs
from users.models import User
from .serializers import (
    StaffsSerializer,
    RetrieveAndListStaffsSerializer,
    ListStaffsReportSerializer,
    ListAllStaffsReportSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import Subquery, OuterRef, Q
from rest_framework.response import Response

from django.template.loader import get_template
from base.services.s3_services import MediaUpLoad
import os
from django.conf import settings
from weasyprint import HTML, default_url_fetcher


class ListCreateStaffsAPIView(generics.ListCreateAPIView):

    model = Staffs
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__email',
        'user__phone',
        'staff',
        'gender',
        'marital_status',
        'personal_email'
    ]
    filter_fields = {
        'id': ['exact', 'in'],
        'nationality__name': ['exact', 'in'],
        'ethnicity__name': ['exact', 'in'],
        'religion__name': ['exact', 'in'],
        'literacy__name': ['exact', 'in'],
        'department__name': ['exact', 'in'],
        'department__id': ['exact', 'in'],
        'is_active': ['exact', 'in'],
    }

    def perform_create(self, serializer):
        serializer.save(
            # user=self.request.user,
            created_at=timezone.now(),
            created_by=self.request.user.id,
        )

    def get_queryset(self):
        return Staffs.objects.filter(
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
            return RetrieveAndListStaffsSerializer
        if self.request.method == 'POST':
            return StaffsSerializer


class RetrieveUpdateDestroyStaffsAPIView(generics.RetrieveUpdateDestroyAPIView):

    model = Staffs
    permission_classes = [IsHrm]
    lookup_url_kwarg = "id"

    def get_queryset(self):
        return Staffs.objects.filter(
            is_deleted=False,
            deleted_at=None,
        )

    def perform_update(self, serializer):
        serializer.save(
            # user=self.request.user,
            modified_at=timezone.now(),
            modified_by=self.request.user.id,
        )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.deleted_by = self.request.user.id
        instance.save()
        user = User.objects.filter(id=instance.user.id).first()
        push_admin_notification_staff_deleted.delay(metadata=user.id, name=f"{user.first_name} {user.last_name}", email=user.email)

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return StaffsSerializer
        else:
            return RetrieveAndListStaffsSerializer


class ListAllStaffsReportAPIView(generics.ListAPIView):

    model = Staffs
    permission_classes = [IsHrm]
    serializer_class = ListAllStaffsReportSerializer
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__email',
        'user__phone',
        'staff',
        'gender',
        'marital_status',
        'personal_email'
    ]
    filter_fields = {
        'id': ['exact', 'in'],
        'department__branch__id': ['exact', 'in'],
        'department__branch__name': ['exact', 'in'],
    }

    def get_queryset(self):
        return Staffs.objects.filter(
            is_deleted=False,
            deleted_at=None,
            is_active=True
        ).order_by("department__name")
    
    def list(self, request, *args, **kwargs):
        """Over write list to show total unread """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            key_list_staff = ''
            staff_check = Staffs.objects.filter(
                Q(deleted_at=None) &
                Q(is_deleted=False) &
                Q(is_active=True) &
                Q(department__branch__id=self.request.GET.get('branch', None))
            ).first()
            if staff_check.is_print==False:
                data = {
                    "data": serializer.data,
                    "branch": staff_check.department.branch.branch,
                }    
                template = get_template('list_staff_report_template.html')
                context = template.render(data).encode("UTF-8")
                filename = '{}_list_staff_report.pdf'.format(staff_check.department.branch.branch)
                f = open(filename, "w+b")
                HTML(string=context).write_pdf(f)
                f.close()
                key = MediaUpLoad().upload_pdf_to_s3(os.path.join(settings.BASE_DIR, filename), filename)
                key_list_staff_data = MediaUpLoad().get_file_url(key)
                staff = Staffs.objects.filter(
                    Q(deleted_at=None) &
                    Q(is_deleted=False) &
                    Q(is_active=True) &
                    Q(department__branch__id=self.request.GET.get('branch', None))
                ).values()
                
                list_id = []
                
                for item in staff: 
                    list_id.append(item['id'])
                
                Staffs.objects.filter(id__in=list_id).update(
                    link_all_staff=key_list_staff_data,
                    is_print=True
                )

                return Response(dict(
                    self.get_paginated_response(serializer.data).data,
                    key_list_staff=key_list_staff_data,
                ))
            else:
                return Response(dict(
                    self.get_paginated_response(serializer.data).data,
                    key_list_staff=staff_check.link_all_staff,
                ))
            
        serializer = self.get_serializer(queryset, many=True)

        key_list_staff = ''
        staff_check = Staffs.objects.filter(
            Q(deleted_at=None) &
            Q(is_deleted=False) &
            Q(is_active=True) &
            Q(department__branch__id=self.request.GET.get('branch', None))
            ).first()
        if staff_check.is_print==False:
            
            data = {
                "data": serializer.data,
                "branch": staff_check.department.branch.branch,
            }    
            template = get_template('list_staff_report_template.html')
            context = template.render(data).encode("UTF-8")
            filename = '{}_list_staff_report.pdf'.format(staff_check.department.branch.branch)
            f = open(filename, "w+b")
            HTML(string=context).write_pdf(f)
            f.close()
            key = MediaUpLoad().upload_pdf_to_s3(os.path.join(settings.BASE_DIR, filename), filename)
            key_list_staff_data = MediaUpLoad().get_file_url(key)
            
            staff = Staffs.objects.filter(
                Q(deleted_at=None) &
                Q(is_deleted=False) &
                Q(is_active=True) &
                Q(department__branch__id=self.request.GET.get('branch', None))
            ).values()
            
            list_id = []
            
            for item in staff: 
                list_id.append(item['id'])
            
            Staffs.objects.filter(id__in=list_id).update(
                link_all_staff=key_list_staff_data,
                is_print=True
            )
            return Response(dict(
                results=serializer.data,
                key_list_staff=key_list_staff_data,
            ))   
        else:
            return Response(dict(
                results=serializer.data,
                key_list_staff=staff_check.link_all_staff,
            ))   
    
    @property
    def paginator(self):
        if self.request.query_params.get("no_pagination", "") == "true":
            return None
        return super().paginator


class ListStaffsReportAPIView(generics.ListCreateAPIView):

    model = Staffs
    permission_classes = [IsHrm]
    serializer_class = ListStaffsReportSerializer
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__email',
        'user__phone',
        'staff',
        'gender',
        'marital_status',
        'personal_email'
    ]
    filter_fields = {
        'id': ['exact', 'in'],
        'nationality__name': ['exact', 'in'],
        'ethnicity__name': ['exact', 'in'],
        'religion__name': ['exact', 'in'],
        'literacy__name': ['exact', 'in'],
        'department__name': ['exact', 'in'],
        'department__id': ['exact', 'in'],
        'is_active': ['exact', 'in'],
    }

    def get_queryset(self):
        return Staffs.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).order_by("-created_at")
        
    @property
    def paginator(self):
        if self.request.query_params.get("no_pagination", "") == "true":
            return None
        return super().paginator


class RetrieveStaffsReportAPIView(generics.RetrieveAPIView):

    model = Staffs
    permission_classes = [IsHrm]
    lookup_url_kwarg = "id"
    serializer_class = ListStaffsReportSerializer
    def get_queryset(self):
        return Staffs.objects.filter(
            is_deleted=False,
            deleted_at=None,
        )