# Django imports
from django.urls import path

# Application imports
from .views import (
    ListNotificationAPIView,
    ReadOneNotificationAPIView,
    ReadAllNotificationAPIView
)
urlpatterns = [
    # Notification
    path('', ListNotificationAPIView.as_view(), name='list-admin-notification'),
    path('<uuid:id>/read-one/<uuid:user_id>/', ReadOneNotificationAPIView.as_view(), name='read-one-admin-notification'),
    path('read-all/<uuid:user_id>/', ReadAllNotificationAPIView.as_view(), name='read-all-admin-notification')    
]