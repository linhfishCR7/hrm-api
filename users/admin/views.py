
from cgitb import lookup
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    ListUsersSerializer,
    DetailsUsersSerializer
)
from rest_framework import filters, generics, serializers, status, viewsets
from base.permissions import IsAdmin
from users.models import User
from base.paginations import ItemIndexPagination

class GetListUsers(generics.ListAPIView):
    serializer_class = ListUsersSerializer
    permission_classes = [IsAdmin, ]
    pagination_class = ItemIndexPagination
    
    def get_queryset(self):
        return User.objects.filter(
            is_deleted=False,
            deleted_at=None
        )
        
    @property
    def paginator(self):
        if self.request.query_params.get("no_pagination", "") == "true":
            return None
        return super().paginator
    

class GetDetailsUser(generics.RetrieveAPIView):
    serializer_class = DetailsUsersSerializer
    permission_classes = [IsAdmin, ]
    lookup_url_kwarg = "id"
    def get_queryset(self):
        return User.objects.filter(
            is_deleted=False,
            deleted_at=None
        )


class BlockUnBlockUserAPIView(generics.UpdateAPIView):
    model = User
    permission_classes = [IsAdmin]
    lookup_url_kwarg = "id"
    
    def put(self, request, *args, **kwargs):
        user = self.model.objects.filter(
            id=self.kwargs.get('id'), 
            deleted_at=None,
            is_deleted=False
        ).first()
        if user:
            if user.is_active == True:
                user.is_active = False
                user.save()
                """Send mail"""
                """ Notification """
                return Response(dict(message='BLOCKED'))
            if user.is_active == False:
                user.is_active = True
                user.save()
                """Send mail"""
                """ Notification """
                return Response(dict(message='ACTIVE'))
        raise Http404
