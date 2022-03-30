from django.urls import path
from .views import (
    ListCreateRecruitmentTrackingAPIView,
    RetrieveUpdateDestroyRecruitmentTrackingAPIView
)


urlpatterns = [
    path('', ListCreateRecruitmentTrackingAPIView.as_view(), name='list-create-recruiment-tracking'),
    path('<uuid:id>/', RetrieveUpdateDestroyRecruitmentTrackingAPIView.as_view(), name='retrieve-update-destroy-recruiment-tracking'),
]
