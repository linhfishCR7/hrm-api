from django.urls import path
from .views import (
    GeneratePdf,
    ListSalaryAPIView
)

urlpatterns = [
    path('<uuid:id>/', GeneratePdf.as_view(), name='retrieve-salary'),
    path('', ListSalaryAPIView.as_view(), name='list-salary'),
]
