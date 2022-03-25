from django.urls import path
from .views import (
    ListCreateDegreeAPIView,
    RetrieveUpdateDestroyDegreeAPIView
)


urlpatterns = [
    path('', ListCreateDegreeAPIView.as_view(), name='list-create-degree'),
    path('<uuid:id>/', RetrieveUpdateDestroyDegreeAPIView.as_view(), name='retrieve-update-destroy-degree'),
]
