from django.urls import path
from .views import (
    ListCreateDisciplineAPIView,
    RetrieveUpdateDestroyDisciplineAPIView
)


urlpatterns = [
    path('', ListCreateDisciplineAPIView.as_view(), name='list-create-discipline'),
    path('<uuid:id>/', RetrieveUpdateDestroyDisciplineAPIView.as_view(), name='retrieve-update-destroy-discipline'),
]
