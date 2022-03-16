from django.urls import path
from .views import (
    ListCreateStaffsAPIView,
    RetrieveUpdateDestroyStaffsAPIView
)


urlpatterns = [
    path('', ListCreateStaffsAPIView.as_view(), name='list-create-staff'),
    path('<uuid:id>/', RetrieveUpdateDestroyStaffsAPIView.as_view(), name='retrieve-update-destroy-staff'),
]
