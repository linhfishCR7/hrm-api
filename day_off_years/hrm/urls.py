from django.urls import path
from .views import (
    ListDayOffYearsAPIView,
    RetrieveUpdateDestroyDayOffYearsAPIView
)


urlpatterns = [
    path('', ListDayOffYearsAPIView.as_view(), name='list-day-off-year'),
    path('<uuid:id>/', RetrieveUpdateDestroyDayOffYearsAPIView.as_view(), name='retrieve-update-destroy-day-off-year'),
]
