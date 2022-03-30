from django.db import models
from base.models import BaseModel

# Create your models here.
class RecruitmentRequirement(BaseModel):
    # Recruitment Requirement
    created_at_recruitment = models.DateField()
    approved_by = models.CharField(max_length=255, default=None) 
    asked_by = models.CharField(max_length=255, default=None)
    department = models.ForeignKey('departments.Departments', on_delete=models.CASCADE, related_name='recruitment_requirements_department')