from django.urls import path
from .views import (
    ListCreateSalaryAPIView,
    RetrieveUpdateDestroySalaryAPIView,
    ActiveSalaryAPIView
)


urlpatterns = [
    path('', ListCreateSalaryAPIView.as_view(), name='list-create-salary'),
    path('<uuid:id>/', RetrieveUpdateDestroySalaryAPIView.as_view(), name='retrieve-update-destroy-salary'),
    path('active-salary/', ActiveSalaryAPIView.as_view(), name='active-salary'),
]
