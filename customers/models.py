from django.db import models
from base.models import BaseModel
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Customers(BaseModel):
    # Customers
    name = models.CharField(max_length=255, default=None)
    phone = PhoneNumberField(null=True)
    email = models.EmailField(max_length=255, default=None)
    website = models.CharField(max_length=255, null=True, default=None, blank=True)
    file = models.CharField(max_length=255, null=True, default=None, blank=True)
    company = models.CharField(max_length=255, null=True, default=None, blank=True)
    addresses = models.ManyToManyField(
        'addresses.Address', 
        related_name='customer_addresses',
        null=True, 
        default=None
    )

    # company = models.ForeignKey('companies.Companies', on_delete=models.CASCADE, related_name='customer_company', null=True, 
    #     default=None, blank=True)

    