from django.urls import path
from .views import (
    GetListUsers, 
    GetDetailsUser,
    BlockUnBlockUserAPIView
)

urlpatterns = [
    path('list/', GetListUsers.as_view(), name='list-users'),
    path('<uuid:id>/', GetDetailsUser.as_view(), name='user-details'),
    path('block-unblock-user/<uuid:id>/', BlockUnBlockUserAPIView.as_view(), name='block-unblock-user'),
   
]
