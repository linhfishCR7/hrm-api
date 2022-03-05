from django.urls import path
from .views import (
    ListCreateCustomersAPIView,
    RetrieveUpdateDestroyCustomersAPIView
)


urlpatterns = [
    path('', ListCreateCustomersAPIView.as_view(), name='list-create-customer'),
    path('<uuid:id>/', RetrieveUpdateDestroyCustomersAPIView.as_view(), name='retrieve-update-destroy-customer'),
]
