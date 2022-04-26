from django.urls import path
from .views import (
    ListCreateSalaryAPIView,
    RetrieveUpdateDestroySalaryAPIView,
    ActiveSalaryAPIView,
    ListPastalaryAPIView,
    ListCurrentalaryAPIView,
    CheckSalaryAPIView
)


urlpatterns = [
    path('', ListCreateSalaryAPIView.as_view(), name='list-create-salary'),
    path('current/', ListCurrentalaryAPIView.as_view(), name='list-current-salary'),
    path('past/', ListPastalaryAPIView.as_view(), name='list-past-salary'),
    path('<uuid:id>/', RetrieveUpdateDestroySalaryAPIView.as_view(), name='retrieve-update-destroy-salary'),
    path('active-salary/', ActiveSalaryAPIView.as_view(), name='active-salary'),
    path('check-salary/', CheckSalaryAPIView.as_view(), name='check-salary'),
]
