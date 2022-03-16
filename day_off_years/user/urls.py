from django.urls import path
from .views import (
    ListCreateDayOffYearsAPIView,
    RetrieveUpdateDestroyDayOffYearsAPIView
)


urlpatterns = [
    path('', ListCreateDayOffYearsAPIView.as_view(), name='list-create-day-off-year'),
    path('<uuid:id>/', RetrieveUpdateDestroyDayOffYearsAPIView.as_view(), name='retrieve-update-destroy-day-off-year'),
]
