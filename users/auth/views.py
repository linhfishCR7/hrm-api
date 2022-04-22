
from xml.dom import ValidationErr
from addresses.models import Address
from base.constants.common import Data, GenderStatus, MaritalStatus
from base.tasks import push_admin_notification_account_created, welcome_email
from base.templates.error_templates import ErrorTemplate
from base.utils import generate_staff, print_value
from departments.models import Departments
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import filters, generics, serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from base.permissions import IsUser
from staffs.models import Staffs
from users.models import User, UserFCMDevice
from .serializers import (
    CompleteSignupStartedSerializer,
    RegistrationSerializer,
    ProfileUserSerializer,
    BESignUpSerializer,
    ConfirmCognitoSignUpSerializer,
    LoginWebSerializer,
    UserFCMSerializer,
    AuthorizationSerializer
)


# @api_view(['POST',])
# def logout_view(request):
#     if request.method == 'POST':
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_200_OK)

@api_view(['POST', ])
def registration_view(request):

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
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        return Response(self.serializer_class(self.request.user).data)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user, data=request.data)
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


# FCM DEVICES FUNCTIONS
class UserFCMDeviceAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserFCMSerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            created_by=self.request.user.id
        )


class AuthorizationAPIView(generics.RetrieveAPIView):
    model = User
    serializer_class = AuthorizationSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        return Response(self.serializer_class(self.request.user).data)


class CompleteSignupAPIView(generics.CreateAPIView):
    model = User
    serializer_class = CompleteSignupStartedSerializer
    permission_classes = ()
    """
        Insert user in to the system
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = self.model.objects.get(
            email=serializer.validated_data['email'],
            is_deleted=False
        )

        department = Departments.objects.get(
            id=serializer.validated_data['department'],
            is_deleted=False
        )
        del serializer.validated_data['department']
        if user:
            self.model.objects.filter(
                email=serializer.validated_data['email'],
                is_deleted=False
            ).update(
                **serializer.validated_data
            )
            staff = Staffs.objects.create(
                gender=GenderStatus.UNKNOWN,
                marital_status=MaritalStatus.SINGLE,
                number_of_children=None,
                identity_card='',
                issuance_date=None,
                place_of_issuance='',
                start_work_date=None,
                probationary_end_date=None,
                labor_contract_signing_date=None,
                personal_email='',
                facebook='',
                social_insurance_number='',
                tax_code='',
                bank_account=None,
                elect_notifications='',
                elect_decision='',
                url='',
                note='',
                department=department,
                nationality=None,
                ethnicity=None,
                religion=None,
                literacy=None,
                position=None,
                user=user,
                is_active=False,
                staff=generate_staff(
                    department=department.department,
                    first_name=serializer.validated_data['first_name'],
                    last_name=serializer.validated_data['last_name']
                ),
            )
            addresses_body = Data.address
            address_data = []
            for address in addresses_body:
                address_data.append(
                    Address(
                        **address
                    )
                )
            addresses_data = Address.objects.bulk_create(address_data)

            staff.addresses.add(*addresses_data)

            welcome_email.delay(dict(email=user.email, name=user.first_name))
            push_admin_notification_account_created.delay(
                metadata=user.id, name=f'{user.first_name} {user.last_name}')
            return Response(dict(message='SUCCESS'))

        raise ValidationErr(ErrorTemplate.AuthorizedError.USER_NOT_EXISTED)

    # def perform_create(self, serializer):
    #     serializer.save(
    #         created_at=timezone.now(),
    #         created_by=self.request.user.id,
    #     )
