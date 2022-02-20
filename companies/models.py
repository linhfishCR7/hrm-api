from django.db import models
from base.models import BaseModel
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Companies(BaseModel):
    # Companies
    company = models.CharField(max_length=255)
    name = models.CharField(max_length=255, default=None)
    tax_code = models.CharField(max_length=255, default=None)
    phone = PhoneNumberField(null=True)
    email = models.EmailField(max_length=255, default=None)
    website = models.CharField(max_length=255, default=None)
    fax = models.CharField(max_length=255, default=None)
    logo = models.CharField(max_length=255, default=None)
    
    addresses = models.ManyToManyField(
        'addresses.Address', 
        related_name='company_addresses',
        null=True, 
        default=None
    )

    