from django.urls import path
from .views import (
    ListCreateCompaniesAPIView,
    RetrieveUpdateDestroyCompaniesAPIView,
    ListCompaniesAPIView
)


urlpatterns = [
    path('', ListCreateCompaniesAPIView.as_view(), name='list-create-companies'),
    path('list/', ListCompaniesAPIView.as_view(), name='list-companies'),
    path('<uuid:id>/', RetrieveUpdateDestroyCompaniesAPIView.as_view(), name='retrieve-update-destroy-companies'),
]
