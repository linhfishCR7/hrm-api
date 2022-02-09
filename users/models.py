from django.db import models
from base.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(AbstractBaseUser):
    # Profile
    username = models.CharField(max_length=100, null=True, unique=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    is_notification_on = models.BooleanField(default=True)
    image = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(max_length=255)
    is_verified_email = models.BooleanField(default=False)
    verified_email_at = models.DateTimeField(null=True)
    phone = PhoneNumberField(null=True)
