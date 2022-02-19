from django.urls import path
from .views import (
    ListCreateEmploymentContractTypesAPIView,
    RetrieveUpdateDestroyEmploymentContractTypesAPIView
)


urlpatterns = [
    path('', ListCreateEmploymentContractTypesAPIView.as_view(), name='list-create-employment-contract-types'),
    path('<uuid:id>/', RetrieveUpdateDestroyEmploymentContractTypesAPIView.as_view(), name='retrieve-update-destroy-employment-contract-types'),
]
