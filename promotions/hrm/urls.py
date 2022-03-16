from django.urls import path
from .views import (
    ListCreatePromotionsAPIView,
    RetrieveUpdateDestroyPromotionsAPIView
)


urlpatterns = [
    path('', ListCreatePromotionsAPIView.as_view(), name='list-create-promotion'),
    path('<uuid:id>/', RetrieveUpdateDestroyPromotionsAPIView.as_view(), name='retrieve-update-destroy-promotion'),
]
