from django.urls import path
from .views import (
    ListCreateOnBusinessAPIView,
    RetrieveUpdateDestroyOnBusinessAPIView
)


urlpatterns = [
    path('', ListCreateOnBusinessAPIView.as_view(), name='list-create-on-business'),
    path('<uuid:id>/', RetrieveUpdateDestroyOnBusinessAPIView.as_view(), name='retrieve-update-destroy-on-business'),
]
