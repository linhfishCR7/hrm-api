from django.db import models
from base.constants.common import RelationshipType
from base.models import BaseModel
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class UrgentContacts(BaseModel):
    # UrgentContacts
    full_name = models.CharField(max_length=255, default=None)
    phone = PhoneNumberField()
    mobile_phone = PhoneNumberField(null=True, blank=True)
    address = models.CharField(max_length=255, default=None)
    type = models.CharField(max_length=255, default=RelationshipType.WIFE)
    staff = models.ForeignKey('staffs.Staffs', on_delete=models.CASCADE, related_name='urgent_contact_staff')