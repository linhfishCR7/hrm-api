from django.urls import path
from .views import (
    ListCreateTimekeepingAPIView,
    RetrieveUpdateDestroyTimekeepingAPIView
)


urlpatterns = [
    path('', ListCreateTimekeepingAPIView.as_view(), name='list-create-timekeeping'),
    path('<uuid:id>/', RetrieveUpdateDestroyTimekeepingAPIView.as_view(), name='retrieve-update-destroy-timekeeping'),
]
