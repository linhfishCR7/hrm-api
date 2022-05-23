from addresses.models import Address
from companies.models import Companies
from customers.models import Customers
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


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
            'type',
        ]
        
        read_only_fields = ['id']   
    

class CompaniesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Companies
        fields = [
            'id',
            'company',
            'name'
        ]
        read_only_fields = ['id']
    


class CustomersSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(
            queryset=Customers.objects.filter(
                is_deleted=False,
                deleted_at=None
            )
        )]
    )
    addresses = AddressesSerializer(many=True)
    # company = CompaniesSerializer()
    website = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    file = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    
    class Meta:
        model = Customers
        fields = [
            'id',
            'name',
            'website',
            'phone',
            'email',
            'file',
            'addresses',
            'company'
        ]
        
    def create(self, validated_data):
        
        """ Add Customers """
        customer = Customers.objects.create(
            name=validated_data['name'],
            phone=validated_data['phone'],
            email=validated_data['email'],
            website=validated_data['website'],
            file=validated_data['file'],
            company=validated_data['company'],
            created_by=validated_data['created_by']
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
        
        customer.addresses.add(*addresses_data)
        
        return customer

    def update(self, instance, validated_data):

        """ Add new address """
        addresses_body = validated_data['addresses']
        del validated_data['addresses']
        """ Delete old company address """
        Customers.objects.filter(id=instance.id).first().addresses.all().delete()
        """ Add new address """
        new_address_data = []
        for new_address in addresses_body:
            new_address_data.append(
                Address(**new_address)
            )
        
        new_address = Address.objects.bulk_create(new_address_data)
        Customers.objects.filter(id=instance.id).first().addresses.add(*new_address)
        updated_instance = super().update(instance, validated_data)
        return updated_instance
    

class RetrieveAndListCustomersSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(
            queryset=Customers.objects.filter(
                is_deleted=False,
                deleted_at=None
            )
        )]
    )
    addresses = AddressesSerializer(many=True)
    website = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    file = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    
    class Meta:
        model = Customers
        fields = [
            'id',
            'name',
            'website',
            'phone',
            'email',
            'file',
            'addresses',
            'company'
        ]
