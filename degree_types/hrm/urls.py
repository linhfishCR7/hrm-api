from django.urls import path
from .views import (
    ListCreateDegreeTypesAPIView,
    RetrieveUpdateDestroyDegreeTypesAPIView
)


urlpatterns = [
    path('', ListCreateDegreeTypesAPIView.as_view(), name='list-create-degree-types'),
    path('<uuid:id>/', RetrieveUpdateDestroyDegreeTypesAPIView.as_view(), name='retrieve-update-destroy-degree-types'),
]
