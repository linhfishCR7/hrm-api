from django.urls import path
from .views import (
    ListCreateDayOffTypesAPIView,
    RetrieveUpdateDestroyDayOffTypesAPIView
)


urlpatterns = [
    path('', ListCreateDayOffTypesAPIView.as_view(), name='list-create-DayOff-types'),
    path('<uuid:id>/', RetrieveUpdateDestroyDayOffTypesAPIView.as_view(), name='retrieve-update-destroy-DayOff-types'),
]
