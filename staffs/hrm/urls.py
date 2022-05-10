from django.urls import path
from .views import (
    ListCreateStaffsAPIView,
    RetrieveUpdateDestroyStaffsAPIView,
    ListStaffsReportAPIView
)


urlpatterns = [
    path('', ListCreateStaffsAPIView.as_view(), name='list-create-staff'),
    path('list-all-staff-report/', ListStaffsReportAPIView.as_view(), name='list-staff-report'),
    path('<uuid:id>/', RetrieveUpdateDestroyStaffsAPIView.as_view(), name='retrieve-update-destroy-staff'),
]
