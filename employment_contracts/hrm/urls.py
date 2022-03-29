from django.urls import path
from .views import (
    ListCreateEmploymentContractAPIView,
    RetrieveUpdateDestroyEmploymentContractAPIView
)


urlpatterns = [
    path('', ListCreateEmploymentContractAPIView.as_view(), name='list-create-employment-contract'),
    path('<uuid:id>/', RetrieveUpdateDestroyEmploymentContractAPIView.as_view(), name='retrieve-update-destroy-employment-contract'),
]
