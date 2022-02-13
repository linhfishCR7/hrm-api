from django.urls import path
from .views import (
    ListCreateCertificateTypesAPIView,
    RetrieveUpdateDestroyCertificateTypesAPIView
)


urlpatterns = [
    path('', ListCreateCertificateTypesAPIView.as_view(), name='list-create-certificate-types'),
    path('<uuid:id>/', RetrieveUpdateDestroyCertificateTypesAPIView.as_view(), name='retrieve-update-destroy-certificate-types'),
]
