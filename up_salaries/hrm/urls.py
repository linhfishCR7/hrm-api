from django.urls import path
from .views import (
    ListCreateUpSalaryAPIView,
    RetrieveUpdateDestroyUpSalaryAPIView,
    ListUpSalaryAPIView
)


urlpatterns = [
    path('', ListCreateUpSalaryAPIView.as_view(), name='list-create-up-salary'),
    path('before/', ListUpSalaryAPIView.as_view(), name='list-create-before'),
    path('<uuid:id>/', RetrieveUpdateDestroyUpSalaryAPIView.as_view(), name='retrieve-update-destroy-up-salary'),
]
