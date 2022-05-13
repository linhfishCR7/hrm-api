from django.urls import path
from .views import (
    ListCreateSalaryAPIView,
    RetrieveUpdateDestroySalaryAPIView,
    ActiveSalaryAPIView,
    ListPastalaryAPIView,
    ListCurrentalaryAPIView,
    CheckSalaryAPIView,
    ListAllSalaryReportAPIView,
    ListDepartmentSalaryReportAPIView,
    ListSalaryReportAPIView,
    RetrieveSalaryReportAPIView
)


urlpatterns = [
    path('', ListCreateSalaryAPIView.as_view(), name='list-create-salary'),
    path('list-salary-report/', ListSalaryReportAPIView.as_view(), name='list-salary-report'),
    path('salary-report/<uuid:id>/', RetrieveSalaryReportAPIView.as_view(), name='retrieve-salary-report'),
    path('list-all-salary-report/', ListAllSalaryReportAPIView.as_view(), name='list-all-salary-report'),
    path('list-department-salary-report/', ListDepartmentSalaryReportAPIView.as_view(), name='list-department-salary-report'),
    path('current/', ListCurrentalaryAPIView.as_view(), name='list-current-salary'),
    path('past/', ListPastalaryAPIView.as_view(), name='list-past-salary'),
    path('<uuid:id>/', RetrieveUpdateDestroySalaryAPIView.as_view(), name='retrieve-update-destroy-salary'),
    path('active-salary/', ActiveSalaryAPIView.as_view(), name='active-salary'),
    path('check-salary/', CheckSalaryAPIView.as_view(), name='check-salary'),
]
