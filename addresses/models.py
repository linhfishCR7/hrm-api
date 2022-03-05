from django.db import models
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
    is_place_of_birth_address = models.BooleanField(default=False) # Where You was born
    is_domicile = models.BooleanField(default=False) # Where you live with family line
    is_temporary_residence_address = models.BooleanField(default=False) # Where live for a short time just tem
    is_permanent_address = models.BooleanField(default=False) # Where lived for a long time
    is_head_office_address = models.BooleanField(default=False) # The main place that company is located
    is_working_office_address = models.BooleanField(default=False) # The office of company is located
    is_customer_address = models.BooleanField(default=False) # address of customer