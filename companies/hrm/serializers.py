from base.utils import print_value, without_keys
from companies.models import Companies
from addresses.models import Address
from rest_framework import serializers
from rest_framework.validators import UniqueValidator,UniqueTogetherValidator
from base.serializers import ApplicationMethodFieldSerializer
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext_lazy as _


class AddressesSerializer(serializers.ModelSerializer):
    address = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    city = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    province = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    district = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    commune = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    country = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    postcode = serializers.CharField(allow_blank=True, allow_null=True, required=False)
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
    
    def to_representation(self, instance):
        """
        To show the data response to address
        """
        response = super().to_representation(instance)
        
        # if instance.logo:  
        #     response['logo'] = ApplicationMethodFieldSerializer.get_list_image(instance.logo)
            
        return response
    
        
class CompaniesSerializer(serializers.ModelSerializer):
    addresses = AddressesSerializer(many=True)
    company = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    name = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    tax_code = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    phone = PhoneNumberField()
    email = serializers.EmailField(allow_blank=True, allow_null=True, required=False)
    website = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    fax = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    logo = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    
    """Validate"""
    company = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(
            queryset=Companies.objects.filter(
                is_deleted=False,
                deleted_at=None
            ),
            # message=_("company field must be unique")
        )]
    )
   
    class Meta:
        model = Companies
        fields = [
            'id',
            'company',
            'name',
            'tax_code',
            'phone',
            'email',
            'website',
            'fax',
            'logo',
            'addresses',
        ]
        read_only_fields = ['id']
    
    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        if instance.logo:  
            response['logo'] = ApplicationMethodFieldSerializer.get_list_image(instance.logo)
        
        return response
    
    def create(self, validated_data):
    
        """ Add Company """
        company = Companies.objects.create(
            company=validated_data['company'],
            name=validated_data['name'],
            tax_code=validated_data['tax_code'],
            phone=validated_data['phone'],
            email=validated_data['email'],
            website=validated_data['website'],
            fax=validated_data['fax'],
            logo=validated_data['logo']
        )
                
        # """ add addresses """
        addresses_body = validated_data['addresses']
        address_data = []
        for address in addresses_body:
            address_data.append(
                Address(
                    **address
                )
            )   
        addresses_data = Address.objects.bulk_create(address_data)
        
        company.addresses.add(*addresses_data)
        
        return company

    def update(self, instance, validated_data):

        """ Add new address """
        addresses_body = validated_data['addresses']
        del validated_data['addresses']
        """ Delete old company address """
        Companies.objects.filter(id=instance.id).first().addresses.all().delete()
        """ Add new address """
        new_address_data = []
        for new_address in addresses_body:
            new_address_data.append(
                Address(**new_address)
            )
        
        new_address = Address.objects.bulk_create(new_address_data)
        Companies.objects.filter(id=instance.id).first().addresses.add(*new_address)
        updated_instance = super().update(instance, validated_data)
        return updated_instance
    
    
        