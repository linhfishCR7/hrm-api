from django.urls import path
from .views import (
    ListCreateDayOffYearDetailsAPIView,
    RetrieveUpdateDestroyDayOffYearDetailsAPIView
)

urlpatterns = [
    path('', ListCreateDayOffYearDetailsAPIView.as_view(), name='list-create-day-off-year-detail'),
    path('<uuid:id>/', RetrieveUpdateDestroyDayOffYearDetailsAPIView.as_view(), name='retrieve-update-destroy-day-off-year-detail'),

]
