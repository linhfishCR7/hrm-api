from django.urls import path
from .views import (
    ListCreateProjectsAPIView,
    RetrieveUpdateDestroyProjectsAPIView
)


urlpatterns = [
    path('', ListCreateProjectsAPIView.as_view(), name='list-create-project'),
    path('<uuid:id>/', RetrieveUpdateDestroyProjectsAPIView.as_view(), name='retrieve-update-destroy-project'),
]
