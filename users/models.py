from django.db import models
from base.models import AbstractBaseUser, BaseModel
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(AbstractBaseUser):
    # Profile
    username = models.CharField(max_length=100, null=True, unique=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    image = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(max_length=255)
    is_verified_email = models.BooleanField(default=False)
    verified_email_at = models.DateTimeField(null=True)
    phone = PhoneNumberField(null=True)


class UserFCMDevice(BaseModel):
    TYPES = (
        ('P', 'PORTAL'),
        ('M', 'MOBILE')
    )
    DEVICE_TYPES = (
        ('A', 'ANDROID'),
        ('I', 'IOS'),
        ('B', 'BROWSER')
    )

    user = models.ForeignKey(
        'users.User', on_delete=models.Case, blank=True, null=True, default=0, related_name='UserFCMDevices'
    )
    type = models.CharField(max_length=50, choices=TYPES, null=True)
    device = models.CharField(max_length=200, choices=DEVICE_TYPES, null=True)
    user_type = models.CharField(max_length=200, null=True)
    meid = models.CharField(max_length=200, null=True)
    token = models.TextField()