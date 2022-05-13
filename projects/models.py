from django.db import models
from base.constants.common import ProjectStatus
from base.models import BaseModel

# Create your models here.
class Projects(BaseModel):
    # Projects
    project = models.CharField(max_length=255, default=None)
    name = models.CharField(max_length=255, default=None)
    location = models.CharField(max_length=255, default=None)
    service = models.CharField(max_length=255, default=None)
    contract_number = models.CharField(max_length=255, default=None)
    signing_date = models.DateField(default=None)
    start_date = models.DateField(default=None)
    finish_date = models.DateField(default=None)
    status = models.CharField(max_length=255, default=ProjectStatus.PENDING_PROJECT)
    size = models.CharField(max_length=255, default=None)
    image = models.CharField(max_length=255, default=None)
    note = models.TextField(default=None, null=True, blank=True)
    file = models.CharField(max_length=255, default=None)
   
    customer = models.ForeignKey('customers.Customers', on_delete=models.CASCADE, related_name='project_customer', null=True, 
        default=None, blank=True)

    