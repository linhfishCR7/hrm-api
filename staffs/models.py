from django.db import models
from base.constants.common import GenderStatus, MaritalStatus
from base.models import BaseModel
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Staffs(BaseModel):
    # Staffs
    staff = models.SlugField(max_length=255, null=False,
                             default=None, unique=True)
    gender = models.CharField(max_length=255, default=GenderStatus.UNKNOWN)
    marital_status = models.CharField(
        max_length=255, default=MaritalStatus.SINGLE)
    number_of_children = models.IntegerField(null=True, blank=True, default=0)
    identity_card = models.CharField(max_length=255, default=None)
    issuance_date = models.DateField(null=True, blank=True, default=None)
    place_of_issuance = models.CharField(
        null=True, blank=True, max_length=255, default=None)  # Just need Province
    start_work_date = models.DateField(null=True, blank=True, default=None)
    probationary_end_date = models.DateField(
        null=True, blank=True, default=None)
    labor_contract_signing_date = models.DateField(
        null=True, blank=True, default=None)
    mobile_phone = PhoneNumberField(null=True, blank=True)
    personal_email = models.EmailField(max_length=255, null=True, blank=True, )
    facebook = models.CharField(
        max_length=255, null=True, blank=True, default=None)
    social_insurance_number = models.CharField(
        max_length=255, null=True, blank=True,  default=None)
    tax_code = models.CharField(
        max_length=255, null=True, blank=True,  default=None)
    bank_account = models.IntegerField(null=True, blank=True, default=None)
    elect_notifications = models.CharField(
        null=True, blank=True, max_length=255, default=None)
    elect_decision = models.CharField(
        null=True, blank=True, max_length=255, default=None)
    url = models.CharField(max_length=255, null=True,
                           blank=True,  default=None)
    password = models.CharField(
        max_length=255, null=True, blank=True,  default=None)
    note = models.TextField(null=True, blank=True, default=None)

    department = models.ForeignKey('departments.Departments', on_delete=models.CASCADE, related_name='staff_department', null=True,
                                   default=None, blank=True)

    nationality = models.ForeignKey('nationalities.Nationalities', on_delete=models.CASCADE, related_name='staff_nationalities', null=True,
                                    default=None, blank=True)

    ethnicity = models.ForeignKey('ethnicities.Ethnicities', on_delete=models.CASCADE, related_name='staff_ethnicities', null=True,
                                  default=None, blank=True)

    religion = models.ForeignKey('religions.Religions', on_delete=models.CASCADE, related_name='staff_religions', null=True,
                                 default=None, blank=True)

    literacy = models.ForeignKey('literacy.Literacy', on_delete=models.CASCADE, related_name='staff_literacy', null=True,
                                 default=None, blank=True)
    position = models.ForeignKey('positions.Positions', on_delete=models.CASCADE, related_name='staff_position', null=True,
                                 default=None, blank=True)
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='staff_user', default=None)

    addresses = models.ManyToManyField(
        'addresses.Address',
        related_name='staff_addresses',
        null=True,
        default=None,
        blank=True
    )
