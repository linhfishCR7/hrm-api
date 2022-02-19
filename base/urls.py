# Django imports
from django.urls import path

# Rest framework imports

# Application imports
from .views import (
    BaseFilePresignedUploadAPIView,
    BaseUploadImageAPIView,
    FilePolicyAPI
)


urlpatterns = [
    path('upload/policy/', FilePolicyAPI.as_view(), name='image-presigned'),
    path('upload/', BaseFilePresignedUploadAPIView.as_view(), name='file-presigned'),
    path('upload/image/', BaseUploadImageAPIView.as_view(), name='upload-image'),
]
