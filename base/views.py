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
from rest_framework.filters import OrderingFilter, SearchFilter

# Application imports
# Base imports
from base.services.s3_services import MediaUpLoad
from base.templates.error_templates import ErrorTemplate
from base.constants.common import AppConstants
from base.decorators import (
    uuid_error_handler,
)
from base.constants.common import AppConstants
from base.constants.common import AppConstants, ViewConstants

from base.serializers import (
    BaseUploadFileSerializer,
    UploadResourceSerializer
)
from base.utils import print_value
from base.paginations import ItemIndexPagination


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


class BaseHealthCheckAPIView(APIView):
    permission_classes = ()

    @staticmethod
    def get(request):
        return Response(dict(message="Ok"))


class BaseListCreateAPIView(generics.ListCreateAPIView):
    model = None
    action = None
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    pagination_class = ItemIndexPagination
    
    @property
    def paginator(self):
        if self.request.query_params.get('no_pagination', '') == 'true':
            return None
        return super().paginator

    # Set action
    def get(self, request, *args, **kwargs):
        self.action = ViewConstants.Action.LIST
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.action = ViewConstants.Action.CREATE
        return self.create(request, *args, **kwargs)

    # Set default query, create
    @uuid_error_handler
    def get_queryset(self):
        return self.model.objects.filter(deleted_at=None, is_deleted=False)

    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user.id)
        return instance


class BaseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    model = None
    action = None

    # Set action
    @uuid_error_handler
    def get(self, request, *args, **kwargs):
        self.action = ViewConstants.Action.RETRIEVE
        return self.retrieve(request, *args, **kwargs)

    @uuid_error_handler
    def put(self, request, *args, **kwargs):
        self.action = ViewConstants.Action.UPDATE
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.action = ViewConstants.Action.UPDATE
        return self.partial_update(request, *args, **kwargs)

    @uuid_error_handler
    def delete(self, request, *args, **kwargs):
        self.action = ViewConstants.Action.DELETE
        return self.destroy(request, *args, **kwargs)

    # Set default query, update, destroy
    @uuid_error_handler
    def get_queryset(self):
        return self.model.objects.filter(deleted_at=None, is_deleted=False)

    def perform_update(self, serializer):
        instance = serializer.save(
            modified_by=self.request.user.id,
            modified_at=timezone.now(),
        )
        return instance

    @uuid_error_handler
    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @uuid_error_handler
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.deleted_by = self.request.user.id
        instance.save()


class BaseListAPIView(generics.ListAPIView):
    model = None
    action = None
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    pagination_class = ItemIndexPagination
    
    @property
    def paginator(self):
        if self.request.query_params.get("no_pagination", "") == "true":
            return None
        return super().paginator

    # Set action
    def get(self, request, *args, **kwargs):
        self.action = ViewConstants.Action.LIST
        return self.list(request, *args, **kwargs)

    # Set default query, create
    def get_queryset(self):
        return self.model.objects.filter(deleted_at=None, is_deleted=False)


class BaseCreateAPIView(generics.CreateAPIView):
    model = None
    action = None

    # Set action
    def post(self, request, *args, **kwargs):
        self.action = ViewConstants.Action.CREATE
        return self.create(request, *args, **kwargs)

    # Set default query, create
    def get_queryset(self):
        return self.model.objects.filter(deleted_at=None, is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id)


class BaseRetrieveAPIView(generics.RetrieveAPIView):
    model = None
    action = None

    # Set action
    @uuid_error_handler
    def get(self, request, *args, **kwargs):
        self.action = ViewConstants.Action.RETRIEVE
        return self.retrieve(request, *args, **kwargs)

    # Set default query, update, destroy
    def get_queryset(self):
        return self.model.objects.filter(deleted_at=None, is_deleted=False)


class BaseUpdateAPIView(generics.UpdateAPIView):
    model = None
    action = None

    @uuid_error_handler
    def put(self, request, *args, **kwargs):
        self.action = ViewConstants.Action.UPDATE
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.action = ViewConstants.Action.UPDATE
        return self.partial_update(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(deleted_at=None, is_deleted=False)

    def perform_update(self, serializer):
        serializer.save(
            modified_by=self.request.user.id, 
            modified_at=timezone.now(),
        )


class BaseDestroyAPIView(generics.DestroyAPIView):
    model = None
    action = None

    def delete(self, request, *args, **kwargs):
        self.action = ViewConstants.Action.DELETE
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.deleted_by = self.request.user.id
        instance.save()


class BaseActivateAPIView(APIView):
    model = None
    action = None

    def put(self, request, pk):
        self.action = ViewConstants.Action.UPDATE
        entity = self.model.objects.filter(id=pk, deleted_at=None, is_active=False).first()
        if entity:
            entity.is_active = True
            entity.save()
            return Response(dict(message='ACTIVATED'))
        raise Http404


class BaseDeactivateAPIView(APIView):
    model = None
    action = None

    def put(self, request, pk):
        self.action = ViewConstants.Action.UPDATE
        entity = self.model.objects.filter(id=pk, deleted_at=None, is_active=True).first()
        if entity:
            entity.is_active = False
            entity.save()
            return Response(dict(message='DEACTIVATED'))
        raise Http404