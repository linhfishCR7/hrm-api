from django.urls import path
from .views import (
    ListDayOffTypesAPIView
)


urlpatterns = [
    path('', ListDayOffTypesAPIView.as_view(), name='list-day-off-types'),
]
