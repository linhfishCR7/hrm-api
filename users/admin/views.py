
from cgitb import lookup
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    ListUsersSerializer
)
from rest_framework import filters, generics, serializers, status, viewsets
from base.permissions import IsAdmin
from users.models import User
from base.paginations import ItemIndexPagination
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class GetListUsers(generics.ListAPIView):
    serializer_class = ListUsersSerializer
    permission_classes = [IsAdmin, ]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = [
        'first_name',
        'last_name',
        'email',
        'phone',
    ]
    filter_fields = {
        'is_verified_email': ['exact', 'in'],
        'is_superuser': ['exact', 'in'],
        'is_staff': ['exact', 'in'],
        'is_active': ['exact', 'in'],
    }

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


class GetDetailsUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ListUsersSerializer
    permission_classes = [IsAdmin, ]
    lookup_url_kwarg = "id"

    def get_queryset(self):
        return User.objects.filter(
            is_deleted=False,
            deleted_at=None
        )


class BlockUnBlockUserAPIView(generics.UpdateAPIView):
    model = User
    permission_classes = [IsAdmin, ]
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
