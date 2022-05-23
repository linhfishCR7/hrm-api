# Django imports
from django.urls import path

# Rest framework imports

# Application imports
from .views import (
    BaseFilePresignedUploadAPIView,
    BaseUploadImageAPIView,
    FilePolicyAPI,
    BaseHealthCheckAPIView
)


urlpatterns = [
    path('health-check/', BaseHealthCheckAPIView.as_view(), name="health-check"),
    path('upload/policy/', FilePolicyAPI.as_view(), name='image-presigned'),
    path('upload/', BaseFilePresignedUploadAPIView.as_view(), name='file-presigned'),
    path('upload/image/', BaseUploadImageAPIView.as_view(), name='upload-image'),
]
