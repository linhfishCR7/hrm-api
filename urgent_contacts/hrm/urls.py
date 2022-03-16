from django.urls import path
from .views import (
    ListCreateUrgentContactsAPIView,
    RetrieveUpdateDestroyUrgentContactsAPIView
)


urlpatterns = [
    path('', ListCreateUrgentContactsAPIView.as_view(), name='list-create-urgent-contacts'),
    path('<uuid:id>/', RetrieveUpdateDestroyUrgentContactsAPIView.as_view(), name='retrieve-update-destroy-urgent-contacts'),
]
