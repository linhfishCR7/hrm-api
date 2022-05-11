from django.urls import path
from .views import (
    ListDayOffYearsAPIView,
    RetrieveUpdateDestroyDayOffYearsAPIView,
    ListDayOffYearsReportAPIView
)


urlpatterns = [
    path('', ListDayOffYearsAPIView.as_view(), name='list-day-off-year'),
    path('list-day-off-year-report/', ListDayOffYearsReportAPIView.as_view(), name='list-day-off-year-report'),
    path('<uuid:id>/', RetrieveUpdateDestroyDayOffYearsAPIView.as_view(), name='retrieve-update-destroy-day-off-year'),
]
