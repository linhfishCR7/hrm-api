from django.urls import path
from .views import (
    ListCreateKindsOfWorkAPIView,
    RetrieveUpdateDestroyKindsOfWorkAPIView
)


urlpatterns = [
    path('', ListCreateKindsOfWorkAPIView.as_view(), name='list-create-kinds-of-work'),
    path('<uuid:id>/', RetrieveUpdateDestroyKindsOfWorkAPIView.as_view(), name='retrieve-update-destroy-kinds-of-work'),
]
