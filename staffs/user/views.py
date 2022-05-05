from django.utils import timezone
from base.permissions import IsUser
from base.paginations import ItemIndexPagination
from base.tasks import push_admin_notification_staff_deleted
from base.utils import print_value
from staffs.models import Staffs
from users.models import User
from .serializers import (
    RetrieveAndListStaffsSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class RetrieveStaffsAPIView(generics.RetrieveAPIView):

    model = Staffs
    permission_classes = [IsUser]
    lookup_url_kwarg = "id"
    serializer_class = RetrieveAndListStaffsSerializer

    def get_queryset(self):
        return Staffs.objects.filter(
            is_deleted=False,
            deleted_at=None,
        )
