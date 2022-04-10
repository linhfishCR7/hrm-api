from django.urls import path
from rest_framework import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    registration_view, 
    GetUpdateProfileAPIView,
    BEConfirmCognitoSignUpView,
    BESignUpView,
    LoginWebView,
    UserFCMDeviceAPIView,
    AuthorizationAPIView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('register/', registration_view, name='register'),
    # path('logout/', logout_view, name='logout'),
    #################################
    #  JWT SIMPLE                   #
    #################################
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    #################################
    path('profile/', GetUpdateProfileAPIView.as_view(), name='get-update-profile'),
    path('authorization/', AuthorizationAPIView.as_view(), name='get-update-profile'),
    
    # BE Test Cognito Authentication.
    path('be-confirm-sign-up/', BEConfirmCognitoSignUpView.as_view(), name='be-confirm-sign-up'),
    path('be-signup/', BESignUpView.as_view(), name='be-sign-up'),
    path('login/', LoginWebView.as_view(), name='login'),
    
    # FMC Devices.
    path('me/fcm-device/', UserFCMDeviceAPIView.as_view(), name='create-update-user-fcm-device'),
]
