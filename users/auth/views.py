
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import filters, generics, serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings 
from base.permissions import IsUser
from users.models import User
from .serializers import (
    RegistrationSerializer,
    ProfileUserSerializer,
    BESignUpSerializer,
    ConfirmCognitoSignUpSerializer,
    LoginWebSerializer
)



# @api_view(['POST',])
# def logout_view(request):
#     if request.method == 'POST':
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_200_OK)

@api_view(['POST',])
def  registration_view(request):
    
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Registration Successfully"
            data['username'] = account.username
            data['email'] = account.email

            # token = Token.objects.get(user=account).key
            # data['token'] = token
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }


        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)
    

class GetUpdateProfileAPIView(generics.RetrieveAPIView, generics.UpdateAPIView):
    
    model = User
    serializer_class = ProfileUserSerializer
    permission_classes = [IsAuthenticated,]
    
    def get(self, request, *args, **kwargs):
        return Response(self.serializer_class(self.request.user).data)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BESignUpView(generics.CreateAPIView):
    model = User
    serializer_class = BESignUpSerializer
    permission_classes = ()



class BEConfirmCognitoSignUpView(generics.CreateAPIView):
    model = User
    serializer_class = ConfirmCognitoSignUpSerializer
    permission_classes = ()        


class LoginWebView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = LoginWebSerializer