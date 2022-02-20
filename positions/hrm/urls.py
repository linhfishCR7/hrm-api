from django.urls import path
from .views import (
    ListCreatePositionsAPIView,
    RetrieveUpdateDestroyPositionsAPIView
)


urlpatterns = [
    path('', ListCreatePositionsAPIView.as_view(), name='list-create-positions'),
    path('<uuid:id>/', RetrieveUpdateDestroyPositionsAPIView.as_view(), name='retrieve-update-destroy-positions'),
]
