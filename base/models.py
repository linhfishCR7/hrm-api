import uuid
from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
from django.db.models import Q

from rest_framework.exceptions import ValidationError
from base.templates.error_templates import ErrorTemplate
# Create your models here.


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_by = models.UUIDField(null=True)
    modified_at = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    modified_by = models.UUIDField(null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(default=None, null=True)
    deleted_by = models.UUIDField(null=True)

    class Meta:
        abstract = True
        
    def save(self, *args, **kwargs):
        """
        Base save method to extract update_fields for using in signals handlers: Notification & Activities Logging.
        """
        cls = self.__class__
        old = cls.objects.filter(pk=self.pk).first()
        if old:
            # If old is existed then it's an update.
            # This will get the current model state since super().save() isn't called yet.
            new = self  # This gets the newly instantiated Mode object with the new values.
            changed_fields = []
            for field in cls._meta.get_fields():
                field_name = field.name
                try:
                    if getattr(old, field_name) != getattr(new, field_name):
                        changed_fields.append(field_name)
                except Exception as ex:  # Catch field does not exist exception
                    pass
            kwargs['update_fields'] = changed_fields
            
        super().save(*args, **kwargs)

    
# User Base Config Model
class AbstractUserManager(UserManager):
    def get_or_create_for_cognito(self, payload):
        # In case Cognito user missed email
        user = self.filter(
            Q(username=payload['cognito:username']) |
            Q(email=payload['email'])
        ).first()
        if user:
            if not user.username:
                user.username = payload['cognito:username']
                user.save()
            return user
        else:
            raise ValidationError(ErrorTemplate.AuthorizedError.INCORRECT_AUTH_CRED)

class AbstractBaseUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)

    # Not used password field of Abstract User
    password = models.CharField(max_length=256, null=True)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_by = models.UUIDField(null=True)
    modified_at = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    modified_by = models.UUIDField(null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(default=None, null=True)
    deleted_by = models.UUIDField(null=True)

    REQUIRED_FIELDS = ('email',)
    USERNAME_FIELD = 'username'
    is_anonymous = False
    is_authenticated = True
    
    objects = AbstractUserManager()

    # def get_full_name(self):
    #        return "{fname} {lname}".format(fname=self.first_name, lname=self.last_name)

    # def get_short_name(self):
    #     return self.first_name

    # def get_role(self):
    #     return self.role

    # def __str__(self):
    #     return self.email
    
    class Meta:
        abstract = True
        