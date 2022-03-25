from django.urls import path
from .views import (
    ListCreateCertificateAPIView,
    RetrieveUpdateDestroyCertificateAPIView
)


urlpatterns = [
    path('', ListCreateCertificateAPIView.as_view(), name='list-create-certificate'),
    path('<uuid:id>/', RetrieveUpdateDestroyCertificateAPIView.as_view(), name='retrieve-update-destroy-certificate'),
]
