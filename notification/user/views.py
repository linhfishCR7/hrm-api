# Django imports
from django.utils import timezone
from django.db.models import Q
from base.constants.common import NotificationType
from base.permissions import IsUser

# Base View Imports
from rest_framework import filters, generics, status
from rest_framework.views import APIView
from .serializers import (
    ListNotificationSerializer
)

# Base Permission Imports
# Model Imports
from notification.models import Notification

# Serializer Imports
from rest_framework.response import Response



class ListNotificationAPIView(generics.ListAPIView):
    """
    List create Notification view 
    """
    model = Notification
    permission_classes = [IsUser]
    serializer_class = ListNotificationSerializer
    filterset_fields = [
        'is_seen',
        'notification_type'
    ]
    def get_queryset(self):
        return Notification.objects.filter(
            is_deleted=False,
            deleted_at=None,
            user=self.request.user,
            is_seen=False,
        ).order_by("-created_at")
    
    @property
    def paginator(self):
        if self.request.query_params.get("no_pagination", "") == "true":
            return None
        return super().paginator
    
    def list(self, request, *args, **kwargs):
        """Over write list to show total unread """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            total_unread = Notification.objects.filter(
                Q(deleted_at=None) &
                Q(is_deleted=False) &
                Q(is_seen=False) &
                Q(user=self.request.user)
            ).count()
            return Response(dict(
                self.get_paginated_response(serializer.data).data,
                total_unread=total_unread,
            ))
            
        serializer = self.get_serializer(queryset, many=True)
        total_unread = Notification.objects.filter(
                Q(deleted_at=None) &
                Q(is_deleted=False) &
                Q(is_seen=False) &
                Q(user=self.request.user)
            ).count()
        return Response(dict(
            results=serializer.data,
            total_unread=total_unread
        ))
         

class ReadOneNotificationAPIView(APIView):
    permission_classes = [IsUser]

    def put(self, request, *args, **kwargs):

        Notification.objects.filter(
            Q(id=self.kwargs['id'])&            
            Q(user=self.request.user)
        ).update(
            is_seen=True,
            modified_by=self.kwargs['user_id'],
            modified_at=timezone.now(),
        )

        return Response(dict(message="OK"))
    

class ReadAllNotificationAPIView(APIView):
    permission_classes = [IsUser]

    def put(self, request, *args, **kwargs):    
        Notification.objects.filter(
            Q(user=self.request.user)
        ).update(
            is_seen=True,
            modified_by=self.kwargs['user_id'],
            modified_at=timezone.now(),
        )
        return Response(dict(message="OK"))
    
        
        
        