from base.utils import generate_staff, print_value, without_keys
from branchs.models import Branchs
from companies.models import Companies
from addresses.models import Address
from departments.models import Departments
from ethnicities.models import Ethnicities
from literacy.models import Literacy
from nationalities.models import Nationalities
from positions.models import Positions
from religions.models import Religions
from staffs.models import Staffs
from users.models import User

from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from base.serializers import ApplicationMethodFieldSerializer
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext_lazy as _

from base.services.cognito import CognitoService
import uuid
from base.templates.error_templates import ErrorTemplate
from rest_framework.exceptions import ValidationError
from base.constants.common import Data, GenderStatus, MaritalStatus
from base.utils import generate_random_password
import pandas as pd
from pathlib import Path

class AddressesSerializer(serializers.ModelSerializer):
    address = serializers.CharField(
        allow_blank=True, allow_null=True, required=False)
    city = serializers.CharField(
        allow_blank=True, allow_null=True, required=False)
    province = serializers.CharField(
        allow_blank=True, allow_null=True, required=False)
    district = serializers.CharField(
        allow_blank=True, allow_null=True, required=False)
    commune = serializers.CharField(
        allow_blank=True, allow_null=True, required=False)
    country = serializers.CharField(
        allow_blank=True, allow_null=True, required=False)
    postcode = serializers.CharField(
        allow_blank=True, allow_null=True, required=False)
    lat = serializers.FloatField(required=False)
    lng = serializers.FloatField(required=False)

    class Meta:
        model = Address
        fields = [
            'id',
            'address',
            'city',
            'province',
            'district',
            'commune',
            'country',
            'postcode',
            'lat',
            'lng',
            'type'
        ]

        read_only_fields = ['id']


class UserSerializer(serializers.ModelSerializer):
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


class NationalitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nationalities
        fields = [
            'id',
            'nationality',
            'name'
        ]


class EthnicitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ethnicities
        fields = [
            'id',
            'ethnicity',
            'name'
        ]


class ReligionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Religions
        fields = [
            'id',
            'religion',
            'name'
        ]


class LiteracySerializer(serializers.ModelSerializer):

    class Meta:
        model = Literacy
        fields = [
            'id',
            'literacy',
            'name'
        ]


class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = [
            'id',
            'company',
            'name',
        ]


class BranchSerializer(serializers.ModelSerializer):
    company = CompaniesSerializer(read_only=True)

    class Meta:
        model = Branchs
        fields = [
            'id',
            'company',
            'name',
        ]


class DepartmentsSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)

    class Meta:
        model = Departments
        fields = [
            'id',
            'department',
            'name',
            'branch'
        ]


class PositionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Positions
        fields = [
            'id',
            'position',
            'name',
        ]


class StaffsSerializer(serializers.ModelSerializer):

    addresses = AddressesSerializer(many=True, required=False,)
    # staff = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    email = serializers.CharField(required=False)
    first_name = serializers.CharField(max_length=255,required=False)
    last_name = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Staffs
        fields = [
            'id',
            'staff',
            'gender',
            'marital_status',
            'number_of_children',
            'identity_card',
            'issuance_date',
            'place_of_issuance',
            'start_work_date',
            'probationary_end_date',
            'labor_contract_signing_date',
            'personal_email',
            'facebook',
            'social_insurance_number',
            'tax_code',
            'bank_account',
            'elect_notifications',
            'elect_decision',
            'url',
            'note',
            'department',
            'nationality',
            'ethnicity',
            'religion',
            'literacy',
            'position',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'addresses',
        ]

    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        password_data = generate_random_password()
        del validated_data['first_name']
        del validated_data['last_name']
        del validated_data['email']
        existed_user = User.objects.filter(
            email=email.lower(),
            is_deleted=False
        )
        if existed_user.exists():
            raise ValidationError(ErrorTemplate().UserError().EMAIL_IS_USED)

        username = str(uuid.uuid4())

        response = CognitoService().User().register(
            email=email,
            password=password_data,
            username=username,
            custom_attributes={
                "first_name": first_name,
                "last_name": last_name
            }

        )
        print_value(username)
        user = User.objects.filter(email=email).first()
        """ Add staff """
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
            department=validated_data['department'],
            nationality=None,
            ethnicity=None,
            religion=None,
            literacy=None,
            position=None,
            user=user,
            is_active=False,
            staff=generate_staff(
                first_name=first_name,
                last_name=last_name
            ),
        )
        # staff = Staffs.objects.create(
        #     gender=validated_data['gender'],
        #     marital_status=validated_data['marital_status'],
        #     number_of_children=validated_data['number_of_children'],
        #     identity_card=validated_data['identity_card'],
        #     issuance_date=validated_data['issuance_date'],
        #     place_of_issuance=validated_data['place_of_issuance'],
        #     start_work_date=validated_data['start_work_date'] if validated_data['start_work_date'] else None,
        #     probationary_end_date=validated_data['probationary_end_date'] if validated_data['probationary_end_date'] else None,
        #     labor_contract_signing_date=validated_data[
        #         'labor_contract_signing_date'] if validated_data['labor_contract_signing_date'] else None,
        #     personal_email=validated_data['personal_email'],
        #     facebook=validated_data['facebook'],
        #     social_insurance_number=validated_data['social_insurance_number'],
        #     tax_code=validated_data['tax_code'],
        #     bank_account=validated_data['bank_account'] if validated_data['bank_account'] else None,
        #     elect_notifications=validated_data['elect_notifications'],
        #     elect_decision=validated_data['elect_decision'],
        #     url=validated_data['url'],
        #     note=validated_data['note'],
        #     department=validated_data['department'],
        #     nationality=validated_data['nationality'],
        #     ethnicity=validated_data['ethnicity'],
        #     religion=validated_data['religion'],
        #     literacy=validated_data['literacy'],
        #     position=validated_data['position'],
        #     user=user,
        #     is_active=False,
        #     staff=generate_staff(
        #         first_name=first_name,
        #         last_name=last_name
        #     ),
        # )

        """ add addresses """
        
        # if validated_data['addresses']:
        #     addresses_body = validated_data['addresses']
        #     address_data = []
        #     for address in addresses_body:
        #         address_data.append(
        #             Address(
        #                 **address
        #             )
        #         )
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

        data_data = {
            'first_name': [first_name],
            'last_name': [last_name],
            'email': [email],
            'password': [password_data],
        }

        df = pd.DataFrame(data_data, columns = ['first_name', 'last_name', 'email', 'password'])
        downloads_path = str(Path.home() / "Downloads")
        file = df.to_excel(f'{downloads_path}/{first_name}-{last_name}-{email}.xlsx', index = False, header=True)

        return dict({
            "first_name":first_name,
            "last_name": last_name,
            "email":email,
            "password":password_data,
        })

    def update(self, instance, validated_data):
        """ Add new address """
        addresses_body = validated_data['addresses']
        del validated_data['addresses']
        """ Delete old company address """
        Staffs.objects.filter(id=instance.id).first().addresses.all().delete()

        """ Add new address """
        new_address_data = []
        for new_address in addresses_body:
            new_address_data.append(
                Address(**new_address)
            )

        new_address = Address.objects.bulk_create(new_address_data)
        Staffs.objects.filter(
            id=instance.id).first().addresses.add(*new_address)
        updated_instance = super().update(instance, validated_data)
        return updated_instance


class RetrieveAndListStaffsSerializer(serializers.ModelSerializer):
    department = DepartmentsSerializer()
    nationality = NationalitiesSerializer()
    ethnicity = EthnicitiesSerializer()
    religion = ReligionsSerializer()
    literacy = LiteracySerializer()
    user = UserSerializer()
    addresses = AddressesSerializer(many=True)
    position = PositionsSerializer()

    class Meta:
        model = Staffs
        fields = [
            'id',
            'staff',
            'gender',
            'marital_status',
            'number_of_children',
            'identity_card',
            'issuance_date',
            'place_of_issuance',
            'start_work_date',
            'probationary_end_date',
            'labor_contract_signing_date',
            'personal_email',
            'facebook',
            'social_insurance_number',
            'tax_code',
            'bank_account',
            'elect_notifications',
            'elect_decision',
            'url',
            'note',
            'department',
            'nationality',
            'ethnicity',
            'religion',
            'literacy',
            'position',
            'user',
            'is_active',
            'addresses',
        ]
        read_only_fields = ['id']

    def to_representation(self, instance):
        """
        To show the data response to users
        """
        response = super().to_representation(instance)
        response['first_name'] = instance.user.first_name
        response['last_name'] = instance.user.last_name
        response['email'] = instance.user.email
        if not instance.department == None:
            response['department_data'] = instance.department.name
        else:
            response['department_data'] = ''

        if not instance.position == None:
            response['position_data'] = instance.position.name
        else:
            response['position_data'] = ''

        if not instance.literacy == None:
            response['literacy_data'] = instance.literacy.name
        else:
            response['literacy_data'] = ''

        if not instance.religion == None:
            response['religion_data'] = instance.religion.name
        else:
            response['religion_data'] = ''

        if not instance.ethnicity == None:
            response['ethnicity_data'] = instance.ethnicity.name
        else:
            response['ethnicity_data'] = ''

        if not instance.nationality == None:
            response['nationality_data'] = instance.nationality.name
        else:
            response['nationality_data'] = ''

        if not instance.user.image == None:
            response['logo_url'] = 'https://hrm-s3.s3.amazonaws.com/' + \
                instance.user.image
        else:
            response['logo_url'] = ''

        # if not instance.user.first_name == None:
        #     response['first_name'] = instance.user.first_name
        # else:
        #     response['first_name'] = ''

        # if not instance.user.last_name == None:
        #     response['last_name'] = instance.user.last_name
        # else:
        #     response['last_name'] = ''

        if instance.is_active == False:
            response['is_active_data'] = 'Nghỉ Làm'
        else:
            response['is_active_data'] = 'Đang Làm'

        response['phone'] = str(instance.user.phone)

        return response
