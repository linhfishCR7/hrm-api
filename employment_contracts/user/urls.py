from django.urls import path
from .views import (
    ListEmploymentContractAPIView
)


urlpatterns = [
    path('list-employment-contract/', ListEmploymentContractAPIView.as_view(), name='list-employment-contract'),
]
