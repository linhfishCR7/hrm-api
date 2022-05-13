from django.urls import path
from .views import (
    ListCreateDayOffYearsAPIView,
    RetrieveUpdateDestroyDayOffYearsAPIView,
    ListDayOffYearsAPIView
)


urlpatterns = [
    path('', ListCreateDayOffYearsAPIView.as_view(), name='list-create-day-off-year'),
    path('<uuid:id>/', RetrieveUpdateDestroyDayOffYearsAPIView.as_view(), name='retrieve-update-destroy-day-off-year'),
    path('list-day-off-year/', ListDayOffYearsAPIView.as_view(), name='list-day-off-year'),

]
