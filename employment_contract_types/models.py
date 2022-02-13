from django.db import models
from base.models import BaseModel

# Create your models here.
class EmploymentContractTypes(BaseModel):
    # Employment Contract Types
    employment_contract_types = models.CharField(max_length=255)
    name = models.CharField(max_length=255, default=None)