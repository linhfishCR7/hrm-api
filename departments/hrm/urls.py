from django.urls import path
from .views import (
    ListCreateDepartmentsAPIView,
    RetrieveUpdateDestroyDepartmentsAPIView,
    ListDepartmentsAPIView
)


urlpatterns = [
    path('', ListCreateDepartmentsAPIView.as_view(), name='list-create-department'),
    path('list/', ListDepartmentsAPIView.as_view(), name='list-department'),
    path('<uuid:id>/', RetrieveUpdateDestroyDepartmentsAPIView.as_view(), name='retrieve-update-destroy-department'),
]
