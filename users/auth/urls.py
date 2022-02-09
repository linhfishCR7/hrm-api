from django.urls import path
from rest_framework import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    registration_view, 
    # logout_view
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('register/', registration_view, name='register'),
    # path('logout/', logout_view, name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
