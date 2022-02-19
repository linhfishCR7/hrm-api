from django.urls import path
from .views import (
    ListCreateReligionsAPIView,
    RetrieveUpdateDestroyReligionsAPIView
)


urlpatterns = [
    path('', ListCreateReligionsAPIView.as_view(), name='list-create-religions'),
    path('<uuid:id>/', RetrieveUpdateDestroyReligionsAPIView.as_view(), name='retrieve-update-destroy-religions'),
]
