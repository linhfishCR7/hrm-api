from django.urls import path
from .views import (
    ListCreateDepartmentsAPIView,
    RetrieveUpdateDestroyDepartmentsAPIView
)


urlpatterns = [
    path('', ListCreateDepartmentsAPIView.as_view(), name='list-create-department'),
    path('<uuid:id>/', RetrieveUpdateDestroyDepartmentsAPIView.as_view(), name='retrieve-update-destroy-department'),
]
