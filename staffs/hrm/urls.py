from django.urls import path
from .views import (
    ListCreateStaffsAPIView,
    RetrieveUpdateDestroyStaffsAPIView,
    ListStaffsReportAPIView,
    ListAllStaffsReportAPIView,
    RetrieveStaffsReportAPIView
)


urlpatterns = [
    path('', ListCreateStaffsAPIView.as_view(), name='list-create-staff'),
    path('list-staff-report/', ListStaffsReportAPIView.as_view(), name='list-staff-report'),
    path('staff-report/<uuid:id>/', RetrieveStaffsReportAPIView.as_view(), name='staff-report'),
    path('list-all-staff-report/', ListAllStaffsReportAPIView.as_view(), name='list-all-staff-report'),
    path('<uuid:id>/', RetrieveUpdateDestroyStaffsAPIView.as_view(), name='retrieve-update-destroy-staff'),
]
