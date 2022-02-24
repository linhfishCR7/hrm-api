# Python imports
import random
import string
import uuid
import os

# Django imports
from django.http import Http404
from django.utils import timezone
from django_filters.rest_framework import (
    DjangoFilterBackend,
)

# Rest framework imports
from rest_framework import generics, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Application imports
# Base imports
from base.services.s3_services import MediaUpLoad
from base.templates.error_templates import ErrorTemplate
from base.constants.common import AppConstants
from base.decorators import (
    uuid_error_handler,
)
from base.constants.common import AppConstants

from base.serializers import (
    BaseUploadFileSerializer,
    UploadResourceSerializer
)
from base.utils import print_value


# Upload Media - Large and Multiple File - Presigned
class BaseFilePresignedUploadAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BaseUploadFileSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        file_name, file_extension = os.path.splitext(data['file_name'])
        file_extension = file_extension.lower()
            
        key = str(uuid.uuid4())
        upload_path = AppConstants.Upload.FILE_OPTIONS[str(data['file_type'])]
        file_name = upload_path + "/" + str(key[:12]) + str(data['file_name'])

        data = MediaUpLoad().presign_url(key=file_name, file_extension=file_extension, file_type=data['file_type'])

        return Response(data)
    
    
class BaseUploadImageAPIView(APIView):
    permission_classes = ()
    
    def post(self, request):
        # Validate file exist
        file = request.data.get('UploadFiles')
        if not file:
            raise ValidationError(dict(UploadFiles=["This field is required."]))

        # Validate file type
        media_s3_service = MediaUpLoad()
        key = media_s3_service.upload_media_to_s3(file)

        # Response
        return Response(dict(url=media_s3_service.get_image_url(key), key=key))


class FilePolicyAPI(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = UploadResourceSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        key = str(uuid.uuid4())
        file_name = str(key[:12]) + str(data['file_name'])
        """ Validate file extension """
        file_extension = "." +file_name.split(".")[len(file_name.split(".")) - 1]
        if file_extension.lower() not in AppConstants.VALID_FILE_EXTENSION:
            raise ValidationError(ErrorTemplate.Upload.INVALID_FILE_EXTENSION(AppConstants.VALID_FILE_EXTENSION))
        
        data = MediaUpLoad().presign_image_url(
            key=file_name
        )

        return Response(data)
