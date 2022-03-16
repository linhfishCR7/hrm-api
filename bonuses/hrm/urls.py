from django.urls import path
from .views import (
    ListCreateBonusesAPIView,
    RetrieveUpdateDestroyBonusesAPIView
)


urlpatterns = [
    path('', ListCreateBonusesAPIView.as_view(), name='list-create-bonus'),
    path('<uuid:id>/', RetrieveUpdateDestroyBonusesAPIView.as_view(), name='retrieve-update-destroy-bonus'),
]
