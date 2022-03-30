from django.urls import path
from .views import (
    ListCreateTrainningRequirementDetailAPIView,
    RetrieveUpdateDestroyTrainningRequirementDetailAPIView
)


urlpatterns = [
    path('', ListCreateTrainningRequirementDetailAPIView.as_view(), name='list-create-trainning-requirement-detail'),
    path('<uuid:id>/', RetrieveUpdateDestroyTrainningRequirementDetailAPIView.as_view(), name='retrieve-update-destroy-trainning-requirement-detail'),
]
