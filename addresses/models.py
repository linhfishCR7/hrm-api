from django.db import models
from base.constants.common import AddressType
from base.models import BaseModel

# Create your models here.
class Address(BaseModel): 
    """Address model"""
    address = models.CharField(max_length=255, null=True, default=None) #Example: 154 Drainer Avenue
    city = models.CharField(max_length=255, null=True, default=None)
    province = models.CharField(max_length=255, null=True, default=None)
    state = models.CharField(max_length=255, null=True, default=None)
    district = models.CharField(max_length=255, null=True, default=None)
    commune = models.CharField(max_length=255, null=True, default=None)
    country = models.CharField(max_length=255, null=True, default=None)
    postcode = models.CharField(max_length=16, null = True, default=None)
    lat = models.FloatField(null=True, default=0)
    lng = models.FloatField(null=True, default=0)
    type = models.CharField(max_length=255, blank=True, null=True, default=AddressType.PLACE_OF_BIRTH_ADDRESS)