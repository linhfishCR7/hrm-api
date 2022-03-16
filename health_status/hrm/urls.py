from django.urls import path
from .views import (
    ListCreateHealthStatusAPIView,
    RetrieveUpdateDestroyHealthStatusAPIView
)


urlpatterns = [
    path('', ListCreateHealthStatusAPIView.as_view(), name='list-create-heathy-status'),
    path('<uuid:id>/', RetrieveUpdateDestroyHealthStatusAPIView.as_view(), name='retrieve-update-destroy-heathy-status'),
]
