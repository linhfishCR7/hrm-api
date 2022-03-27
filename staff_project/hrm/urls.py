from django.urls import path
from .views import (
    ListCreateStaffProjectAPIView,
    RetrieveUpdateDestroyStaffProjectAPIView
)


urlpatterns = [
    path('', ListCreateStaffProjectAPIView.as_view(), name='list-create-staff-project'),
    path('<uuid:id>/', RetrieveUpdateDestroyStaffProjectAPIView.as_view(), name='retrieve-update-destroy-staff-project'),
]
