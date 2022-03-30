from django.urls import path
from .views import (
    ListCreateRecruitmentRequirementDetailAPIView,
    RetrieveUpdateDestroyRecruitmentRequirementDetailAPIView
)


urlpatterns = [
    path('', ListCreateRecruitmentRequirementDetailAPIView.as_view(), name='list-create-recruiment-requirement-detail'),
    path('<uuid:id>/', RetrieveUpdateDestroyRecruitmentRequirementDetailAPIView.as_view(), name='retrieve-update-destroy-recruiment-requirement-detail'),
]
