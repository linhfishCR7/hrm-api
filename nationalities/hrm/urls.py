from django.urls import path
from .views import (
    ListCreateNationalitiesAPIView,
    RetrieveUpdateDestroyNationalitiesAPIView
)


urlpatterns = [
    path('', ListCreateNationalitiesAPIView.as_view(), name='list-create-nationalities'),
    path('<uuid:id>/', RetrieveUpdateDestroyNationalitiesAPIView.as_view(), name='retrieve-update-destroy-nationalities'),
]
