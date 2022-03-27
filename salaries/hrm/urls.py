from django.urls import path
from .views import (
    ListCreateSalaryAPIView,
    RetrieveUpdateDestroySalaryAPIView
)


urlpatterns = [
    path('', ListCreateSalaryAPIView.as_view(), name='list-create-salary'),
    path('<uuid:id>/', RetrieveUpdateDestroySalaryAPIView.as_view(), name='retrieve-update-destroy-salary'),
]
