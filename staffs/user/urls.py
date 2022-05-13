from django.urls import path
from .views import (
    RetrieveStaffsAPIView
)


urlpatterns = [
    path('<uuid:id>/', RetrieveStaffsAPIView.as_view(), name='retrieve-staff'),
]
