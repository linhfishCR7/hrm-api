from django.urls import path
from .views import (
    ListCreateBranchsAPIView,
    RetrieveUpdateDestroyBranchsAPIView,
    ListBranchsAPIView
)


urlpatterns = [
    path('', ListCreateBranchsAPIView.as_view(), name='list-create-branch'),
    path('list/', ListBranchsAPIView.as_view(), name='list-branch'),
    path('<uuid:id>/', RetrieveUpdateDestroyBranchsAPIView.as_view(), name='retrieve-update-destroy-branch'),
]
