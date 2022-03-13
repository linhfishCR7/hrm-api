from django.db import models
from base.models import BaseModel

# Create your models here.
class Departments(BaseModel):
    # Departments
    department = models.CharField(max_length=255, default=None)
    name = models.CharField(max_length=255, default=None)
    branch = models.ForeignKey('branchs.Branchs', on_delete=models.CASCADE, related_name='departments_branch')