from dataclasses import field
import uuid
from addresses.models import Address
from base.constants.common import Data, GenderStatus, MaritalStatus
from branchs.models import Branchs
from companies.models import Companies
from departments.models import Departments

from rest_framework.exceptions import ValidationError
from django.utils import timezone

from base.services.cognito import CognitoService
from base.tasks import push_admin_notification_account_created, welcome_email
from base.templates.error_templates import ErrorTemplate
from staffs.models import Staffs
from users.models import User, UserFCMDevice
from rest_framework import serializers
from base.serializers import ApplicationMethodFieldSerializer, CommonSerializer
from base.utils import generate_staff, print_value


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'error': 'P1 and P2 should be same'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError(
                {'error': 'Email already exists'})

        account = User(
            email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'image',
            'date_of_birth',
            'is_staff',
            'is_superuser',
            'is_active'

        ]
        read_only_fields = [
            'id',
            'username',
            'email',
            'is_staff',
            'is_superuser',
            'is_active'
        ]

    def to_representation(self, instance):
        """
        To show the data response to users
        """
        response = super().to_representation(instance)
        if instance.image:
            response['image'] = ApplicationMethodFieldSerializer.get_list_image(
                instance.image)

        return response

    def update(self, instance, validated_data):
        # Validate input data (if any)
        return super().update(instance, validated_data)


class BESignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = (
            'password',
            'email',
            'first_name',
            'last_name'
        )

    def create(self, validated_data):
        # Check phone, username already a unique field
        existed_user = User.objects.filter(
            email=validated_data['email'].lower(),
            is_deleted=False
        )
        if existed_user.exists():
            raise ValidationError(ErrorTemplate().UserError().EMAIL_IS_USED)

        username = str(uuid.uuid4())

        response = CognitoService().User().register(
            email=validated_data['email'],
            password=validated_data['password'],
            username=username,
            custom_attributes={
                "first_name": validated_data['first_name'],
                "last_name": validated_data['last_name']
            }

        )

        return dict(
            user=response,
            username=username
        )

    def to_representation(self, instance):
        return instance


class ConfirmCognitoSignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    verified_code = serializers.CharField(max_length=6)
    department = serializers.CharField(max_length=255)
    is_staff = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'verified_code',
            'is_staff',
            'is_superuser',
            'department'
            
        )

    def create(self, validated_data):
        user = User.objects.filter(email=validated_data['email']).first()
        department = Departments.objects.get(
            id=validated_data['department'],
            is_deleted=False
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
                first_name=user.first_name,
                last_name=user.last_name
            )

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

        if not user:
            raise ValidationError(ErrorTemplate.UserError.USER_NOT_EXIST)

        response = CognitoService().User().confirm_verified_email_code(
            verified_code=validated_data['verified_code'],
            username=str(user.username),
        )
        if validated_data['is_staff'] == True:
            user.is_staff = True
            user.is_superuser = False

        if validated_data['is_superuser'] == True:
            user.is_superuser = True
            user.is_staff = True

        user.is_verified_email = True
        user.is_active = True
        user.verified_email_at = timezone.now()
        user.save()
        welcome_email.delay(dict(email=user.email, name=user.first_name))
        push_admin_notification_account_created.delay(
            metadata=user.id, name=f'{user.first_name} {user.last_name}')

        return dict(response=response)

    def to_representation(self, instance):
        return instance


class LoginWebSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=200)

    def create(self, validated_data):
        result = CognitoService.User().authenticate(
            username=validated_data['email'],
            password=validated_data['password']
        )
        token = result['cognito_id_token']
        access_token = result['cognito_access_token']
        return dict(
            token=token,
            access_token=access_token
        )

    def to_representation(self, instance):
        return instance


# FMC DEVICE SERIALIZERS
class UserFCMSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        default='N', choices=UserFCMDevice.TYPES, required=False)
    device = serializers.ChoiceField(
        choices=UserFCMDevice.DEVICE_TYPES, allow_null=True, allow_blank=True, required=False)
    meid = serializers.CharField(
        max_length=100, allow_null=True, required=False, allow_blank=True)
    token = serializers.CharField(
        max_length=500, allow_blank=True, allow_null=True)

    class Meta:
        model = UserFCMDevice
        fields = (
            'user',
            'device',
            'meid',
            'token',
            'type',
        )

    def create(self, validated_data):
        fcm_register_token = UserFCMDevice.objects.filter(
            token=validated_data['token'],
            is_deleted=False,
            user=validated_data['user']
        ).first()
        print_value(fcm_register_token)
        if fcm_register_token:
            return fcm_register_token

        return super().create(validated_data)


class AuthorizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id']

    def to_representation(self, instance):

        response = super().to_representation(instance)

        staff = Staffs.objects.filter(user_id=instance.id).first()
        department = Departments.objects.filter(id=staff.department_id).first()
        branch = Branchs.objects.filter(id=department.branch_id).first()
        company = Companies.objects.filter(id=branch.company_id).first()

        response['branch'] = branch.id
        response['company'] = company.id

        return response


class CompleteSignupStartedSerializer(CommonSerializer):
    email = serializers.EmailField(
        default='', allow_blank=True, required=False, max_length=256)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    department = serializers.CharField(max_length=100)
