from django.urls import path
from .views import (
    ListCreateUpSalaryAPIView,
    RetrieveUpdateDestroyUpSalaryAPIView,
)


urlpatterns = [
    path('', ListCreateUpSalaryAPIView.as_view(), name='list-create-up-salary'),
    path('<uuid:id>/', RetrieveUpdateDestroyUpSalaryAPIView.as_view(), name='retrieve-update-destroy-up-salary'),
]
