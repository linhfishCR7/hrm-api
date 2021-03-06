from django.utils import timezone
from base.permissions import IsHrm
from base.paginations import ItemIndexPagination
from base.utils import print_value
from trainning_requirement.models import TrainningRequirement
from .serializers import (
    TrainningRequirementSerializer,
    RetrieveAndListTrainningRequirementSerializer
)
from rest_framework import filters, generics, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class ListCreateTrainningRequirementAPIView(generics.ListCreateAPIView):
    
    model = TrainningRequirement
    permission_classes = [IsHrm]
    pagination_class = ItemIndexPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    ordering_fields = '__all__'
    search_fields = ['course_name']
    filter_fields = {
        'course_name': ['exact', 'in'],
        'branch__id': ['exact', 'in'],
    }
    
    def get_queryset(self):
        return TrainningRequirement.objects.filter(
            is_deleted=False,
            deleted_at=None,
        ).order_by("-created_at")
    
    @property
    def paginator(self):
        if self.request.query_params.get("no_pagination", "") == "true":
            return None
        return super().paginator
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RetrieveAndListTrainningRequirementSerializer
        if self.request.method == 'POST':
            return TrainningRequirementSerializer

class RetrieveUpdateDestroyTrainningRequirementAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    model = TrainningRequirement
    permission_classes = [IsHrm]
    lookup_url_kwarg = "id"
    
    def get_queryset(self):
        return TrainningRequirement.objects.filter(
            is_deleted=False,
            deleted_at=None,
        )
    
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.deleted_by = self.request.user.id
        instance.save()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return TrainningRequirementSerializer
        else: 
            return RetrieveAndListTrainningRequirementSerializer