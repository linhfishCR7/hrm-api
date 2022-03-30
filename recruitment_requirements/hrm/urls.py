from django.urls import path
from .views import (
    ListCreateRecruitmentRequirementAPIView,
    RetrieveUpdateDestroyRecruitmentRequirementAPIView
)


urlpatterns = [
    path('', ListCreateRecruitmentRequirementAPIView.as_view(), name='list-create-recruiment-requirement'),
    path('<uuid:id>/', RetrieveUpdateDestroyRecruitmentRequirementAPIView.as_view(), name='retrieve-update-destroy-recruiment-requirement'),
]
