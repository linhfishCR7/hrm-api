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

from django.template.loader import get_template
from base.services.s3_services import MediaUpLoad
import os
from django.conf import settings
from weasyprint import HTML, default_url_fetcher

# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
# import logging
# logger = logging.getLogger('weasyprint')
# logger.addHandler(logging.FileHandler('/tmp/weasyprint.log'))

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
            'mobile_phone',
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
            'is_print'
        ]
        read_only_fields = ['id']
        
    def to_representation(self, instance):
        """
        To show the data response to users
        """
        request = self.context.get('request')
        response = super().to_representation(instance)
        response['first_name'] = instance.user.first_name
        response['last_name'] = instance.user.last_name
        response['email'] = instance.user.email
        response['date_of_birth'] = instance.user.date_of_birth

        
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
        address = Staffs.objects.filter(id=instance.id).first().addresses.all().values()
        for item in address:
            if item['type']=='place_of_birth_address':
                response['place_of_birth'] = item['address']
                response['domicile'] = item['address']
            if item['type']=='permanent_address':
                response['permanent_address'] = item['address']
            if item['type']=='temporary_residence_address':
                response['temporary_residence_address'] = item['address']
            
        if instance.is_print==False:
            data = {
                "staff": instance.staff,
                "place_of_birth": response['place_of_birth'],
                "domicile": response['domicile'],
                "permanent_address": response['permanent_address'],
                "temporary_residence_address": response['temporary_residence_address'],
                "marital_status": instance.marital_status,
                "number_of_children": instance.number_of_children,
                "identity_card": instance.identity_card,
                "issuance_date": instance.issuance_date,
                "place_of_issuance": instance.place_of_issuance,
                "start_work_date": instance.start_work_date,
                "probationary_end_date": instance.probationary_end_date,
                "personal_email": instance.personal_email,
                "facebook": instance.tax_code,
                "social_insurance_number": instance.social_insurance_number,
                "tax_code": instance.tax_code,
                "bank_account": instance.bank_account,
                "nationality": response['nationality_data'],
                "ethnicity": response['ethnicity_data'],
                "religion": response['religion_data'],
                "literacy": response['literacy_data'],
                "position": response['position_data'],
                "user_fullname": response['last_name'] + response['first_name'],
                "email": instance.user.email,
                "gender": instance.gender,
                "phone": response['phone'],
                "logo_url": response['logo_url'],
                "day_of_birth": instance.user.date_of_birth,
                "mobile_phone": instance.mobile_phone,
            }
            template = get_template('profile_report_template.html')
            context = template.render(data).encode("UTF-8")
            filename = '{}_{}_profile_report.pdf'.format(response['last_name'] +  response['first_name'],instance.staff)
            f = open(filename, "w+b")
            HTML(string=context).write_pdf(f)
            f.close()
            key = MediaUpLoad().upload_pdf_to_s3(os.path.join(settings.BASE_DIR, filename), filename)
            response['key'] = MediaUpLoad().get_file_url(key)
            Staffs.objects.filter(id=instance.id).update(
                link_staff=response['key'],
                is_print=True
            )
        else:
            response['key'] = instance.link_staff

        return response
