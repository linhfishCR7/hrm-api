from django.urls import path
from .views import (
    ListCreateCompaniesAPIView,
    RetrieveUpdateDestroyCompaniesAPIView
)


urlpatterns = [
    path('', ListCreateCompaniesAPIView.as_view(), name='list-create-companies'),
    path('<uuid:id>/', RetrieveUpdateDestroyCompaniesAPIView.as_view(), name='retrieve-update-destroy-companies'),
]
