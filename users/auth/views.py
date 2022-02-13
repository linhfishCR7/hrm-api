
from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.permissions import IsUser
from users.models import User
from .serializers import (
    RegistrationSerializer,
    ProfileUserSerializer
)
from rest_framework.authtoken.models import Token
from rest_framework import filters, generics, serializers, status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken


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
    

class GetProfileAPIView(generics.RetrieveAPIView):
    
    model = User
    serializer_class = ProfileUserSerializer
    permission_classes = [IsUser]
    
    # def get_queryset(self):
    #     return User.objects.filter(
    #         is_deleted=False,
    #         deleted_at=None,
    #         id=self.request.user.id
    #     )
    def get_object(self):
        return self.request.user
    