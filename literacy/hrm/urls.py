from django.urls import path
from .views import (
    ListCreateLiteracyAPIView,
    RetrieveUpdateDestroyLiteracyAPIView
)


urlpatterns = [
    path('', ListCreateLiteracyAPIView.as_view(), name='list-create-literacy'),
    path('<uuid:id>/', RetrieveUpdateDestroyLiteracyAPIView.as_view(), name='retrieve-update-destroy-literacy'),
]
