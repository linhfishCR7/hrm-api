from django.db import models
from base.constants.common import AddressType
from base.models import BaseModel

# Create your models here.
class Address(BaseModel): 
    """Address model"""
    address = models.CharField(max_length=255, null=True, default='') #Example: 154 Drainer Avenue
    city = models.CharField(max_length=255, null=True, default='')
    province = models.CharField(max_length=255, null=True, default='')
    state = models.CharField(max_length=255, null=True, default='')
    district = models.CharField(max_length=255, null=True, default='')
    commune = models.CharField(max_length=255, null=True, default='')
    country = models.CharField(max_length=255, null=True, default='')
    postcode = models.CharField(max_length=16, null = True, default='')
    lat = models.FloatField(null=True, default=0)
    lng = models.FloatField(null=True, default=0)
    type = models.CharField(max_length=255, blank=True, null=True, default=AddressType.PLACE_OF_BIRTH_ADDRESS)