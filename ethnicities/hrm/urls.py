from django.urls import path
from .views import (
    ListCreateEthnicitiesAPIView,
    RetrieveUpdateDestroyEthnicitiesAPIView
)


urlpatterns = [
    path('', ListCreateEthnicitiesAPIView.as_view(), name='list-create-ethnicities'),
    path('<uuid:id>/', RetrieveUpdateDestroyEthnicitiesAPIView.as_view(), name='retrieve-update-destroy-ethnicities'),
]
