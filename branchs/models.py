from django.db import models
from base.models import BaseModel

# Create your models here.
class Branchs(BaseModel):
    # Branchs
    branch = models.CharField(max_length=255, default=None)
    name = models.CharField(max_length=255, default=None)
    company = models.ForeignKey('companies.Companies', on_delete=models.CASCADE, related_name='branchs_company')