from django.db import models
from base.models import AbstractBaseUser, BaseModel
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractBaseUser):
    REQUIRED_VERIFY_FIELDS = ['is_verified_email']  # Add this to modify the which fields need to be verified for user authentication.
    REQUIRED_REGISTER_FIELDS = ['email', 'password']
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    # Profile
    username = models.CharField(max_length=100, null=True, unique=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    image = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, unique=True)
    is_verified_email = models.BooleanField(default=False)
    verified_email_at = models.DateTimeField(null=True)
    phone = PhoneNumberField(null=True, blank=True)


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