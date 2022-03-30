from django.urls import path
from .views import (
    ListCreateTrainningRequirementAPIView,
    RetrieveUpdateDestroyTrainningRequirementAPIView
)


urlpatterns = [
    path('', ListCreateTrainningRequirementAPIView.as_view(), name='list-create-trainning-requirement'),
    path('<uuid:id>/', RetrieveUpdateDestroyTrainningRequirementAPIView.as_view(), name='retrieve-update-destroy-trainning-requirement'),
]
