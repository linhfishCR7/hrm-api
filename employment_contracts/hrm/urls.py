from django.urls import path
from .views import (
    ListCreateEmploymentContractAPIView,
    RetrieveUpdateDestroyEmploymentContractAPIView,
    ListEmploymentContractAPIView
)


urlpatterns = [
    path('', ListCreateEmploymentContractAPIView.as_view(), name='list-create-employment-contract'),
    path('list-employment-contract/', ListEmploymentContractAPIView.as_view(), name='list-employment-contract'),

    path('<uuid:id>/', RetrieveUpdateDestroyEmploymentContractAPIView.as_view(), name='retrieve-update-destroy-employment-contract'),
]
